<script lang="ts">
	import { onMount, tick } from 'svelte';
	import { resolve } from '$app/paths';
	import { SvelteMap, SvelteSet } from 'svelte/reactivity';
	import type { SetDetail, SetRow } from './data';
	import Brand from './Brand.svelte';
	import ExampleQuestion from './ExampleQuestion.svelte';
	import GithubLink from './GithubLink.svelte';
	import Minimap from './Minimap.svelte';
	import { boardTopics, layoutBoard, levelOrder, COLUMN, LEFT, type BoardTopic } from './board';
	import { locale, setLocale, t as text } from './locale.svelte';

	// The curriculum board of TutorRank's /skills page, for exploring only: no
	// sign-in, progress or practice. The board fills the window and every panel
	// floats over it, so it reads as one wide surface.
	let {
		items,
		mistakes,
		version,
		initialSet = '',
		onselect
	}: {
		items: SetRow[];
		mistakes: Record<string, { th: string; en: string }>;
		version: string;
		initialSet?: string;
		onselect?: (key: string) => void;
	} = $props();
	const REPO = 'https://github.com/KananatSSN/openthaiknowledge';
	const PREFS = 'otk-explorer-panels';
	const GAP = 12;
	const NAV_WIDTH = 220;
	const INSPECTOR_WIDTH = 340;
	const colors = [
		'#7c5bd6',
		'#18766f',
		'#9b651a',
		'#366bb0',
		'#a54d74',
		'#657b35',
		'#b0553a',
		'#4f6f8f',
		'#7a6a2f'
	];
	let topics = $derived(boardTopics(items));
	let subjects = $derived([...new Set(items.map((item) => item.subject))]);
	let levels = $derived(
		[...new Set(items.map((item) => item.level))].sort(
			(a, b) => levelOrder(a) - levelOrder(b) || a.localeCompare(b, 'th')
		)
	);
	let query = $state('');
	let subjectFilter = $state('all');
	let expanded = new SvelteSet<string>();
	let selected = $state('');
	let detail = $state<SetDetail | null>(null);
	let current = $derived(items.find((item) => item.key === selected));
	let currentDetail = $derived(detail?.key === selected ? detail : null);
	let currentTopic = $derived(
		topics.find((topic) => topic.items.some((item) => item.key === selected))
	);
	let filtered = $derived.by(() => {
		const needle = query.trim().toLocaleLowerCase();
		return topics
			.map((topic) => ({
				...topic,
				items: topic.items.filter(
					(item) =>
						(!needle ||
							[
								item.display_name,
								item.topic,
								item.unit,
								item.subject,
								item.level,
								item.key,
								...(item.indicator_codes ?? [])
							]
								.join(' ')
								.toLocaleLowerCase()
								.includes(needle)) &&
						(subjectFilter === 'all' || item.subject === subjectFilter)
				)
			}))
			.filter((topic) => topic.items.length);
	});
	let shownSubjects = $derived(
		subjectFilter === 'all' ? subjects : subjects.filter((subject) => subject === subjectFilter)
	);
	let layout = $derived(layoutBoard(filtered, shownSubjects, levels, expanded));
	let resultCount = $derived(filtered.reduce((sum, topic) => sum + topic.items.length, 0));

	let viewport: HTMLDivElement;
	let searchInput: HTMLInputElement;
	let width = $state(1000);
	let height = $state(700);
	let headerHeight = $state(52);
	let levelBarHeight = $state(0);
	let view = $state({ x: 20, y: 20, k: 0.7 });
	let dragging = $state(false);
	let showHelp = $state(false);
	let activeLevel = $state('');
	// Panels the viewer can hide; remembered in this browser.
	let navOpen = $state(true);
	let inspectorHidden = $state(false);
	let showMinimap = $state(true);

	let mobile = $derived(width < 680);
	let chromeTop = $derived(GAP + headerHeight + GAP);
	// The part of the board no panel covers.
	let inset = $derived({
		top: chromeTop + (mobile ? levelBarHeight + 8 : 0),
		left: !mobile && navOpen ? GAP + NAV_WIDTH + GAP : 0,
		right: !mobile && current && !inspectorHidden ? GAP + INSPECTOR_WIDTH + GAP : 0
	});
	let open = $derived({ width: width - inset.left - inset.right, height: height - inset.top });

	let pointers = new SvelteMap<number, { x: number; y: number }>();
	let moved = false;
	let pinchDistance = 0;
	let last = { x: 0, y: 0 };
	const color = (subject: string) => colors[subjects.indexOf(subject) % colors.length];

	function remember() {
		try {
			localStorage.setItem(PREFS, JSON.stringify({ navOpen, showMinimap }));
		} catch {
			// Blocked storage: the choice just is not remembered.
		}
	}
	function toggleNav() {
		navOpen = !navOpen;
		remember();
	}
	function toggleMinimap() {
		showMinimap = !showMinimap;
		remember();
	}
	function zoomAt(factor: number, x = inset.left + open.width / 2, y = inset.top + open.height / 2) {
		const k = Math.max(0.04, Math.min(1.8, view.k * factor));
		view = { x: x - ((x - view.x) * k) / view.k, y: y - ((y - view.y) * k) / view.k, k };
	}
	function fit() {
		const k = Math.max(
			0.04,
			Math.min(1, (open.width - 48) / layout.width, (open.height - 130) / layout.height)
		);
		view = { x: inset.left + (open.width - layout.width * k) / 2, y: inset.top + 60, k };
		activeLevel = '';
	}
	function goLevel(level: string) {
		const row = layout.rows.find((row) => row.level === level);
		if (!row) return;
		const k = Math.max(0.25, Math.min(1, (open.width - 32) / layout.width));
		view = { x: inset.left + 16, y: inset.top + 67 - row.y * k, k };
		activeLevel = level;
	}
	function centreOn(x: number, y: number) {
		view = {
			...view,
			x: inset.left + open.width / 2 - x * view.k,
			y: inset.top + open.height / 2 - y * view.k
		};
	}
	async function search() {
		await tick();
		const first = filtered[0];
		if (first) goLevel(first.level);
	}
	function selectSet(key: string) {
		if (moved) return;
		selected = key;
		if (key) inspectorHidden = false;
		onselect?.(key);
	}
	async function toggleTopic(topic: BoardTopic) {
		if (expanded.has(topic.id)) {
			expanded.delete(topic.id);
		} else {
			expanded.add(topic.id);
			// Open at a readable scale, after the click has finished. Moving a card on
			// pointer focus can move it away before pointerup and swallow the click.
			if (view.k < 0.65) {
				await tick();
				reveal(topic);
			}
		}
	}
	function shortcuts(event: KeyboardEvent) {
		if ((event.target as HTMLElement).closest('input, textarea, select, [contenteditable="true"]'))
			return;
		if (event.key === '/') {
			event.preventDefault();
			searchInput.focus();
		}
		if (event.key === 'Escape') {
			selectSet('');
			showHelp = false;
		}
	}
	function down(event: PointerEvent) {
		if (event.button !== 0 && event.button !== 1) return;
		if ((event.target as HTMLElement).closest('button, a, input, select')) return;
		pointers.set(event.pointerId, { x: event.clientX, y: event.clientY });
		viewport.setPointerCapture(event.pointerId);
		dragging = true;
		moved = false;
		last = { x: event.clientX, y: event.clientY };
		if (pointers.size === 2) {
			const [a, b] = [...pointers.values()];
			pinchDistance = Math.hypot(a.x - b.x, a.y - b.y);
		}
	}
	function move(event: PointerEvent) {
		if (!pointers.has(event.pointerId)) return;
		pointers.set(event.pointerId, { x: event.clientX, y: event.clientY });
		moved = true;
		if (pointers.size === 2) {
			const [a, b] = [...pointers.values()];
			const distance = Math.hypot(a.x - b.x, a.y - b.y);
			const rect = viewport.getBoundingClientRect();
			if (pinchDistance > 0)
				zoomAt(distance / pinchDistance, (a.x + b.x) / 2 - rect.left, (a.y + b.y) / 2 - rect.top);
			pinchDistance = distance;
		} else {
			view.x += event.clientX - last.x;
			view.y += event.clientY - last.y;
		}
		last = { x: event.clientX, y: event.clientY };
	}
	function up(event: PointerEvent) {
		pointers.delete(event.pointerId);
		dragging = pointers.size > 0;
		const remaining = [...pointers.values()][0];
		if (remaining) last = remaining;
		// Set buttons are not drag handles; never leave a completed drag blocking them.
		moved = false;
	}
	function wheel(event: WheelEvent) {
		event.preventDefault();
		if (event.ctrlKey || event.metaKey) {
			const rect = viewport.getBoundingClientRect();
			zoomAt(Math.exp(-event.deltaY * 0.008), event.clientX - rect.left, event.clientY - rect.top);
		} else {
			view.x -= event.shiftKey ? event.deltaY : event.deltaX;
			view.y -= event.shiftKey ? 0 : event.deltaY;
		}
	}
	function keyboard(event: KeyboardEvent) {
		if (event.target !== viewport) return;
		const delta: Record<string, [number, number]> = {
			ArrowLeft: [80, 0],
			ArrowRight: [-80, 0],
			ArrowUp: [0, 80],
			ArrowDown: [0, -80]
		};
		if (delta[event.key]) {
			event.preventDefault();
			view.x += delta[event.key][0];
			view.y += delta[event.key][1];
		}
		if (event.key === '+' || event.key === '=') {
			event.preventDefault();
			zoomAt(1.2);
		}
		if (event.key === '-') {
			event.preventDefault();
			zoomAt(1 / 1.2);
		}
		if (event.key === '0') fit();
	}
	function reveal(topic: BoardTopic) {
		const card = layout.cards.find((card) => card.topic.id === topic.id);
		if (!card) return;
		view = {
			x: inset.left + open.width / 2 - (card.x + 160) * 0.9,
			y: inset.top + 70 - card.y * 0.9,
			k: 0.9
		};
	}
	onMount(() => {
		try {
			const saved = JSON.parse(localStorage.getItem(PREFS) || '{}');
			if (typeof saved.navOpen === 'boolean') navOpen = saved.navOpen;
			if (typeof saved.showMinimap === 'boolean') showMinimap = saved.showMinimap;
		} catch {
			// Nothing remembered, or storage blocked: keep the defaults.
		}
		const observer = new ResizeObserver(([entry]) => {
			width = entry.contentRect.width;
			height = entry.contentRect.height;
		});
		observer.observe(viewport);
		width = viewport.clientWidth;
		height = viewport.clientHeight;
		const item = items.find((item) => item.key === initialSet);
		const topic = topics.find((topic) => topic.items.some((row) => row.key === item?.key));
		if (topic) expanded.add(topic.id);
		if (item) selected = item.key;
		tick().then(() => {
			goLevel(item?.level || levels[0]);
			// A shared link opens on its set's card, at a readable scale.
			if (topic) reveal(topic);
		});
		return () => observer.disconnect();
	});
</script>

<svelte:window onkeydown={shortcuts} />

<section class="learning-map" class:mobile>
	<!-- svelte-ignore a11y_no_noninteractive_element_interactions, a11y_no_noninteractive_tabindex -->
	<div
		class="viewport"
		class:dragging
		bind:this={viewport}
		role="region"
		tabindex="0"
		aria-label={text(
			'แผนที่หลักสูตร ใช้ปุ่มลูกศรเพื่อเลื่อน และปุ่มบวกลบเพื่อซูม',
			'Curriculum board. Arrow keys to pan, plus and minus to zoom.'
		)}
		onpointerdown={down}
		onpointermove={move}
		onpointerup={up}
		onpointercancel={up}
		onlostpointercapture={up}
		onwheel={wheel}
		onkeydown={keyboard}
		style:background-position={`${view.x}px ${view.y}px, 0 0, 0 0, 0 0`}
		style:background-size={`${24 * view.k}px ${24 * view.k}px, 100% 100%, 100% 100%, 100% 100%`}
	>
		<div
			class="world"
			style:width={`${layout.width}px`}
			style:height={`${layout.height}px`}
			style:transform={`translate(${view.x}px, ${view.y}px) scale(${view.k})`}
		>
			{#each layout.rows as row (row.level)}<div
					class="grade-row"
					style:top={`${row.y}px`}
					style:height={`${row.height}px`}
					style:width={`${layout.width}px`}
				>
					<span class="grade-label">{row.level}</span><span class="row-caption"
						>{text('สำรวจ · ลองทำ · ร่วมพัฒนา', 'EXPLORE · TRY · CONTRIBUTE')}</span
					>
				</div>{/each}
			{#each layout.cards as card (card.topic.id)}
				{@const topic = card.topic}
				<article
					class="topic-card"
					style:left={`${card.x}px`}
					style:top={`${card.y}px`}
					style:height={`${card.height}px`}
					style:--subject-color={color(topic.subject)}
				>
					<button
						class="topic-heading"
						aria-expanded={expanded.has(topic.id)}
						title={topic.name}
						onclick={() => toggleTopic(topic)}
					>
						<span class="topic-meta"
							>{topic.course || topic.subject}{topic.strand ? ` · ${topic.strand}` : ''}</span
						><strong>{topic.name}</strong><span class="topic-summary"
							><span>{topic.items.length} {text('ชุดโจทย์', 'sets')}</span><span class="completion"
								>{text('สำรวจชุดโจทย์', 'Explore sets')}</span
							><span class="expand-icon">{expanded.has(topic.id) ? '−' : '+'}</span></span
						>
					</button>
					{#if expanded.has(topic.id)}<div class="set-list">
							{#each topic.items as item (item.key)}<button
									class="set-node"
									class:picked={selected === item.key}
									onclick={() => selectSet(item.key)}
									><span class="stage-dot stage-{item.learning_stage}">{item.learning_stage}</span
									><span class="set-copy"
										><strong>{item.display_name}</strong><small>{item.learning_stage_label}</small></span
									>{#if item.provenance === 'adapted'}<span
											class="set-badge"
											title={text('ดัดแปลงจากข้อสอบที่เผยแพร่แล้ว', 'Adapted from a published exam')}
											>{text('ดัดแปลง', 'adapted')}</span
										>{/if}</button
								>{/each}
						</div>{/if}
				</article>
			{/each}
		</div>
		<div
			class="subject-ruler"
			style:top={`${inset.top + 6}px`}
			style:transform={`translateX(${view.x}px)`}
		>
			{#each shownSubjects as subject, index (subject)}<div
					style:left={`${(LEFT + index * COLUMN) * view.k}px`}
					style:width={`${(COLUMN - 16) * view.k}px`}
					style:--subject-color={color(subject)}
				>
					<i></i><strong>{subject}</strong>
				</div>{/each}
		</div>
	</div>

	<header class="board-header glass" bind:clientHeight={headerHeight}>
		<div class="heading">
			<Brand subtitle={text('สำรวจชุดโจทย์', 'Problem set explorer')} />
			<h1 class="sr-only">{text('สำรวจชุดโจทย์', 'Problem set explorer')}</h1>
		</div>
		<label class="search"
			><span aria-hidden="true">⌕</span><input
				type="search"
				bind:this={searchInput}
				bind:value={query}
				oninput={search}
				aria-label={text('ค้นหาชุดโจทย์', 'Search problem sets')}
				placeholder={text('ค้นหาหัวข้อ ชุดโจทย์ หรือตัวชี้วัด…', 'Search topics, sets or indicators…')}
			/><kbd>/</kbd></label
		>
		<label class="subject-filter"
			><span class="sr-only">{text('กรองวิชา', 'Filter subject')}</span><select
				bind:value={subjectFilter}
				onchange={search}
				><option value="all">{text('ทุกวิชา', 'All subjects')}</option>{#each subjects as subject (subject)}<option
						value={subject}>{subject}</option
					>{/each}</select
			></label
		>
		<button class="pill collapse" onclick={() => expanded.clear()}
			>{text('ย่อหัวข้อ', 'Collapse')}</button
		>
		<span class="header-count"
			><strong>{items.length.toLocaleString()}</strong> {text('ชุดโจทย์', 'sets')}</span
		>
		<a class="pill contribute" href={resolve('/contribute')}>{text('ร่วมพัฒนา', 'Contribute')}</a>
		<GithubLink />
		<button
			class="pill locale"
			onclick={() => setLocale(locale.value === 'th' ? 'en' : 'th')}
			aria-label={text('Switch to English', 'เปลี่ยนเป็นภาษาไทย')}
			>{locale.value === 'th' ? 'EN' : 'ไทย'}</button
		>
	</header>

	{#if mobile}
		<nav
			class="level-bar glass"
			style:top={`${chromeTop}px`}
			bind:clientHeight={levelBarHeight}
			aria-label={text('ระดับชั้น', 'Grade levels')}
		>
			{#each levels as level (level)}<button
					class:active={activeLevel === level}
					onclick={() => goLevel(level)}>{level}</button
				>{/each}
		</nav>
	{:else if navOpen}
		<aside
			class="navigator glass"
			style:top={`${chromeTop}px`}
			aria-label={text('นำทางแผนที่', 'Map navigation')}
		>
			<div class="nav-title">
				<span>{text('ภาพรวมหลักสูตร', 'CURRICULUM')}</span><button
					class="icon-button"
					onclick={toggleNav}
					aria-label={text('ซ่อนแผงด้านซ้าย', 'Hide the side panel')}
					title={text('ซ่อนแผง', 'Hide panel')}>«</button
				>
			</div>
			<button class="overview" onclick={fit}
				><span aria-hidden="true">▦</span>
				{text('ดูทั้งแผนที่', 'Board overview')} <span>↗</span></button
			>
			<div class="nav-label">{text('ระดับชั้น', 'GRADE LEVELS')}</div>
			<nav class="levels" aria-label={text('ระดับชั้น', 'Grade levels')}>
				{#each levels as level (level)}<button
						class:active={activeLevel === level}
						onclick={() => goLevel(level)}
						><span class="level-dot"></span>{level}<span class="level-arrow" aria-hidden="true"
							>→</span
						></button
					>{/each}
			</nav>
			<div class="nav-label">{text('ทุกวิชาในบอร์ดเดียว', 'ALL SUBJECTS, ONE BOARD')}</div>
			<div class="subjects">
				{#each subjects as subject (subject)}<div>
						<i style:background={color(subject)}></i>{subject}
					</div>{/each}
			</div>
			<div class="about">
				<span class="eyebrow">OPENTHAIKNOWLEDGE {version}</span>
				<p>
					{text(
						'ชุดโจทย์ที่สร้างโจทย์ใหม่ได้ไม่จำกัด พร้อมเฉลยที่ตรวจแล้ว เปิดให้ทุกคนร่วมพัฒนา',
						'Problem sets that draw fresh, verified questions. Open for anyone to contribute.'
					)}
				</p>
				<a href={resolve('/contribute')}>{text('ร่วมพัฒนาด้วย AI agent', 'Contribute with your AI agent')} →</a>
				<a href={REPO}>{text('ซอร์สโค้ดบน GitHub', 'Source on GitHub')} →</a>
				<a href={`${REPO}/blob/main/SOURCES.md`}
					>{text('แหล่งที่มาและการขอให้นำออก', 'Sources and removal requests')} →</a
				>
			</div>
		</aside>
	{:else}
		<button
			class="nav-tab glass"
			style:top={`${chromeTop}px`}
			onclick={toggleNav}
			aria-label={text('แสดงแผงด้านซ้าย', 'Show the side panel')}
			><span aria-hidden="true">☰</span> {text('ระดับชั้น', 'Levels')}</button
		>
	{/if}

	{#if showMinimap && !mobile}
		<div
			class="minimap-panel glass"
			style:top={`${chromeTop + (current && inspectorHidden ? 48 : 0)}px`}
			style:right={`${inset.right + GAP}px`}
		>
			<div class="minimap-heading">
				<span>{text('แผนที่ย่อ', 'MINIMAP')}</span><button
					class="icon-button"
					onclick={toggleMinimap}
					aria-label={text('ซ่อนแผนที่ย่อ', 'Hide the minimap')}>×</button
				>
			</div>
			<Minimap
				cards={layout.cards.map((card) => ({
					x: card.x,
					y: card.y,
					height: card.height,
					subject: card.topic.subject,
					id: card.topic.id
				}))}
				rows={layout.rows}
				boardWidth={layout.width}
				boardHeight={layout.height}
				{view}
				viewWidth={width}
				viewHeight={height}
				{color}
				onnavigate={centreOn}
				label={text('แผนที่ย่อของบอร์ด คลิกเพื่อไปยังตำแหน่งนั้น', 'Board minimap. Click to go there.')}
			/>
		</div>
	{/if}

	{#if !resultCount}<div
			class="empty glass"
			role="status"
			style:left={`${inset.left + open.width / 2}px`}
		>
			<strong>{text('ไม่พบชุดโจทย์', 'No problem sets found')}</strong>
			<p>{text('ลองใช้คำค้นอื่น หรือเปลี่ยนตัวกรอง', 'Try another search or subject.')}</p>
			<button
				onclick={() => {
					query = '';
					subjectFilter = 'all';
					goLevel(levels[0]);
				}}>{text('ล้างตัวกรอง', 'Clear filters')}</button
			>
		</div>{/if}

	<div
		class="board-bottom"
		style:left={`${inset.left + GAP}px`}
		style:right={`${inset.right + GAP}px`}
	>
		<span class="board-hint glass"
			>{#if query || subjectFilter !== 'all'}<strong>{resultCount}</strong>
				{text('ชุดโจทย์ที่พบ', 'matching sets')} <span>·</span>{/if}{text(
				'ลากเพื่อเลื่อน',
				'Drag to pan'
			)} <span>·</span> Ctrl + {text('เลื่อนเพื่อซูม', 'scroll to zoom')}</span
		>
		<div class="zoom-controls glass">
			<button
				onclick={() => (showHelp = !showHelp)}
				aria-label={text('วิธีใช้แผนที่', 'Board help')}
				aria-expanded={showHelp}>?</button
			>{#if !mobile}<button
					class:on={showMinimap}
					onclick={toggleMinimap}
					aria-label={text('แผนที่ย่อ', 'Minimap')}
					aria-pressed={showMinimap}>▣</button
				>{/if}<span class="control-divider"></span><button
				onclick={() => zoomAt(1 / 1.2)}
				aria-label={text('ซูมออก', 'Zoom out')}>−</button
			><button
				class="zoom-number"
				onclick={() => zoomAt(1 / view.k)}
				aria-label={text('ซูม 100 เปอร์เซ็นต์', 'Zoom to 100 percent')}
				>{Math.round(view.k * 100)}%</button
			><button onclick={() => zoomAt(1.2)} aria-label={text('ซูมเข้า', 'Zoom in')}>+</button><span
				class="control-divider"
			></span><button onclick={fit} aria-label={text('ดูทั้งแผนที่', 'Fit board')}>⛶</button>
		</div>
	</div>

	{#if showHelp}<div class="help glass" style:right={`${inset.right + GAP}px`}>
			<strong>{text('วิธีสำรวจ', 'How to explore')}</strong>
			<p>
				{text(
					'เลือกชั้นเรียนทางซ้าย คลิกหัวข้อเพื่อเปิดชุดโจทย์ แล้วเลือกชุดเพื่อดูตัวอย่างโจทย์และเฉลย',
					'Choose a grade on the left. Expand a topic, then select a set to see example questions and answers.'
				)}
			</p>
			<p>
				{text(
					'ลากพื้นหลังหรือใช้ปุ่มลูกศรเพื่อเลื่อน ใช้ Ctrl + เลื่อน หรือจีบนิ้วเพื่อซูม กด 0 เพื่อดูทั้งแผนที่ คลิกแผนที่ย่อเพื่อไปยังตำแหน่งนั้น',
					'Drag the background or use arrow keys to pan. Ctrl + scroll or pinch to zoom. Press 0 to fit the board. Click the minimap to jump there.'
				)}
			</p>
			<button onclick={() => (showHelp = false)}>{text('เข้าใจแล้ว', 'Got it')}</button>
		</div>{/if}

	{#if current && inspectorHidden}<button
			class="inspector-tab glass"
			style:top={mobile ? null : `${chromeTop}px`}
			onclick={() => (inspectorHidden = false)}
			aria-label={text('แสดงรายละเอียดชุดโจทย์', 'Show the set details')}
			><span aria-hidden="true">‹</span><span class="tab-name">{current.display_name}</span></button
		>{:else if current}<aside
			class="inspector glass"
			style:top={mobile ? null : `${chromeTop}px`}
			aria-label={text('รายละเอียดชุดโจทย์', 'Problem set details')}
		>
			<div class="inspector-heading">
				<span class="eyebrow">{text('ชุดโจทย์', 'PROBLEM SET')}</span>
				<span class="heading-buttons"
					><button
						onclick={() => (inspectorHidden = true)}
						aria-label={text('ซ่อนแผงรายละเอียด', 'Hide the details panel')}
						title={text('ซ่อนแผง', 'Hide panel')}>{mobile ? '⌄' : '»'}</button
					><button
						onclick={() => selectSet('')}
						aria-label={text('ปิดรายละเอียด', 'Close details')}>×</button
					></span
				>
			</div>
			<div class="subject-tag" style:color={color(current.subject)}>
				<i style:background={color(current.subject)}></i>{current.subject} · {current.level}
			</div>
			<h2>{current.display_name}</h2>
			<p class="detail-topic">{current.unit || current.topic}</p>
			{#key current.key}<ExampleQuestion
					setKey={current.key}
					{mistakes}
					onload={(loaded) => (detail = loaded)}
				/>{/key}
			<dl>
				<dt>{text('ระดับการเรียนรู้', 'Learning stage')}</dt>
				<dd>{current.learning_stage_label}</dd>
				{#if current.course_type}<dt>{text('หลักสูตร', 'Course')}</dt>
					<dd>{current.course_type}</dd>{/if}{#if current.standard_code}<dt>
						{text('มาตรฐาน', 'Standard')}
					</dt>
					<dd>{current.standard_code}</dd>{/if}{#if current.indicator_codes?.length}<dt>
						{text('ตัวชี้วัด', 'Indicators')}
					</dt>
					<dd>{current.indicator_codes.join(', ')}</dd>{/if}
				<dt>{text('รหัสชุดโจทย์', 'Set key')}</dt>
				<dd><code>{current.key}</code></dd>
			</dl>
			<div class="origin">
				<span class="eyebrow">{text('ที่มา', 'ORIGIN')}</span>
				{#if current.provenance === 'original'}<p>
						{text('เขียนขึ้นใหม่สำหรับโครงการนี้', 'Written for this project.')}
					</p>{:else}<p>{text('ดัดแปลงจาก', 'Adapted from')}</p>
					{#if currentDetail}<ul>
							{#each currentDetail.provenance.sources as source (source)}<li>{source}</li>{/each}
						</ul>{/if}{/if}
				{#if currentDetail}<a
						class="source-button"
						href={`${REPO}/blob/main/${currentDetail.source_file}`}
						>{text('ดูโค้ดของชุดโจทย์นี้', "View this set's code")} <span>↗</span></a
					>{/if}
			</div>
			{#if currentTopic}<div class="related-heading">
					{text('ชุดโจทย์ในหัวข้อนี้', 'SETS IN THIS TOPIC')}
					<span>{currentTopic.items.length}</span>
				</div>
				<div class="related">
					{#each currentTopic.items as item (item.key)}<button
							class:active={current.key === item.key}
							onclick={() => selectSet(item.key)}
							><span>{item.display_name}</span><small>{item.learning_stage_label}</small></button
						>{/each}
				</div>{/if}
		</aside>{/if}
</section>

<style>
	.learning-map {
		--purple: #7560c9;
		--border: #e7e5eb;
		--glass: rgba(255, 255, 255, 0.62);
		--glass-edge: rgba(255, 255, 255, 0.8);
		--glass-shadow: 0 10px 34px rgba(52, 38, 92, 0.13), 0 1px 2px rgba(52, 38, 92, 0.06);
		position: relative;
		height: 100dvh;
		overflow: hidden;
		color: #35333f;
	}
	button,
	a,
	input,
	select {
		-webkit-tap-highlight-color: transparent;
	}
	button {
		cursor: pointer;
	}
	.glass {
		background: var(--glass);
		border: 1px solid var(--glass-edge);
		box-shadow: var(--glass-shadow);
		-webkit-backdrop-filter: blur(22px);
		/* Standard last: the minifier keeps only the last of the pair. */
		backdrop-filter: blur(22px);
	}
	@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
		.glass {
			background: rgba(255, 255, 255, 0.94);
		}
	}
	.sr-only {
		position: absolute;
		width: 1px;
		height: 1px;
		overflow: hidden;
		clip: rect(0 0 0 0);
		white-space: nowrap;
	}
	.eyebrow {
		color: #756b80;
		font-size: 9px;
		letter-spacing: 1.2px;
		font-weight: 650;
	}

	/* The board: the whole window, under every panel. */
	.viewport {
		position: absolute;
		inset: 0;
		overflow: hidden;
		background-color: #f1f0f7;
		background-image:
			radial-gradient(#cdc6dc 1px, transparent 1px),
			radial-gradient(circle at 10% 20%, #e3d9ff 0, transparent 36%),
			radial-gradient(circle at 92% 14%, #d3f0e8 0, transparent 32%),
			radial-gradient(circle at 68% 92%, #fde6d2 0, transparent 34%);
		background-repeat: repeat, no-repeat, no-repeat, no-repeat;
		cursor: grab;
		touch-action: none;
		user-select: none;
	}
	.viewport.dragging {
		cursor: grabbing;
	}
	.world {
		position: absolute;
		transform-origin: 0 0;
	}
	.grade-row {
		position: absolute;
		border-top: 1px dashed #d2cbdc;
		pointer-events: none;
	}
	.grade-label {
		position: absolute;
		top: 43px;
		left: 15px;
		font-size: 19px;
		font-weight: 700;
		color: #756b80;
	}
	.row-caption {
		position: absolute;
		left: 100px;
		top: 12px;
		color: #756b80;
		letter-spacing: 2px;
		font-size: 9px;
	}
	.topic-card {
		position: absolute;
		width: 320px;
		background: rgba(255, 255, 255, 0.86);
		border: 1px solid rgba(255, 255, 255, 0.95);
		border-radius: 12px;
		box-shadow: 0 4px 16px rgba(55, 48, 66, 0.07);
		overflow: hidden;
		cursor: default;
	}
	.topic-card::before {
		content: '';
		position: absolute;
		top: 18px;
		left: 0;
		height: 24px;
		width: 3px;
		background: var(--subject-color);
		border-radius: 0 3px 3px 0;
	}
	.topic-heading {
		width: 100%;
		height: 106px;
		padding: 14px 16px 10px;
		text-align: left;
		display: flex;
		flex-direction: column;
	}
	.topic-heading:hover {
		background: rgba(255, 255, 255, 0.7);
	}
	.topic-meta {
		color: #756b80;
		font-size: 9px;
		overflow: hidden;
		white-space: nowrap;
		text-overflow: ellipsis;
		max-width: 100%;
	}
	.topic-heading strong {
		color: #4c435c;
		font-size: 13px;
		font-weight: 650;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
		max-width: 100%;
		margin-top: 5px;
	}
	.topic-summary {
		display: flex;
		align-items: center;
		gap: 8px;
		width: 100%;
		font-size: 10px;
		color: #756b80;
		margin-top: auto;
	}
	.completion {
		margin-left: auto;
		font-size: 9px;
		color: #756b80;
	}
	.expand-icon {
		display: grid;
		place-items: center;
		width: 18px;
		height: 18px;
		background: #f4f1f8;
		border-radius: 4px;
		color: #756b80;
		font-size: 13px;
	}
	.set-list {
		padding: 5px 9px;
	}
	.set-node {
		display: flex;
		align-items: center;
		width: 100%;
		gap: 9px;
		height: 62px;
		padding: 8px;
		text-align: left;
		border-bottom: 1px solid #f0edf5;
		border-radius: 6px;
	}
	.set-node:hover,
	.set-node.picked {
		background: #f3effb;
	}
	.stage-dot {
		width: 17px;
		height: 17px;
		flex-shrink: 0;
		border: 1.5px solid #d2cbdc;
		border-radius: 50%;
		color: #756b80;
		display: grid;
		place-items: center;
		font-size: 9px;
		font-weight: 700;
	}
	.stage-dot.stage-2 {
		border-color: #dba147;
		background: #fcf1d8;
		color: #8a5a12;
	}
	.stage-dot.stage-3 {
		border-color: #64a78b;
		background: #e3f2eb;
		color: #2f6b52;
	}
	.set-copy {
		display: flex;
		flex-direction: column;
		gap: 3px;
		min-width: 0;
	}
	.set-copy strong {
		font-size: 11px;
		font-weight: 500;
		overflow: hidden;
		display: -webkit-box;
		-webkit-line-clamp: 2;
		line-clamp: 2;
		-webkit-box-orient: vertical;
	}
	.set-copy small {
		font-size: 8px;
		color: #756b80;
	}
	.set-badge {
		margin-left: auto;
		flex-shrink: 0;
		color: #756b80;
		background: #f4f1f8;
		border-radius: 4px;
		padding: 1px 6px;
		font-size: 9px;
	}
	.subject-ruler {
		position: absolute;
		left: 0;
		pointer-events: none;
		height: 38px;
	}
	.subject-ruler > div {
		display: flex;
		align-items: center;
		gap: 9px;
		position: absolute;
		padding: 10px 12px;
		background: rgba(255, 255, 255, 0.55);
		border: 1px solid rgba(255, 255, 255, 0.85);
		border-radius: 10px;
		box-shadow: 0 4px 14px rgba(53, 41, 67, 0.08);
		-webkit-backdrop-filter: blur(14px);
		/* Standard last: the minifier keeps only the last of the pair. */
		backdrop-filter: blur(14px);
		overflow: hidden;
	}
	.subject-ruler i {
		width: 7px;
		height: 7px;
		flex-shrink: 0;
		border-radius: 2px;
		background: var(--subject-color);
	}
	.subject-ruler strong {
		font-size: 11px;
		font-weight: 650;
		color: var(--subject-color);
		white-space: nowrap;
	}

	/* The header: one thin floating bar. */
	.board-header {
		--glass: rgba(255, 255, 255, 0.72);
		position: absolute;
		top: 12px;
		left: 12px;
		right: 12px;
		z-index: 4;
		min-height: 52px;
		display: flex;
		align-items: center;
		gap: 12px;
		padding: 8px 10px 8px 12px;
		border-radius: 16px;
	}
	.heading {
		display: flex;
		gap: 10px;
		align-items: center;
		min-width: 0;
		flex-shrink: 0;
	}
	.search {
		display: flex;
		align-items: center;
		gap: 8px;
		flex: 1;
		max-width: 440px;
		margin-left: 12px;
		padding: 6px 12px;
		border: 1px solid rgba(231, 229, 235, 0.9);
		border-radius: 10px;
		color: #756b80;
		background: rgba(255, 255, 255, 0.65);
	}
	.search > span {
		font-size: 20px;
		line-height: 1;
	}
	.search input {
		width: 100%;
		min-width: 0;
		outline: none;
		font-size: 12px;
		color: #35333f;
	}
	.search:focus-within {
		outline: 2px solid var(--purple);
	}
	kbd {
		font-size: 11px;
		border: 1px solid #e4e0e9;
		border-radius: 3px;
		padding: 0 5px;
	}
	.subject-filter select,
	.pill {
		height: 32px;
		padding: 0 12px;
		border: 1px solid rgba(231, 229, 235, 0.9);
		border-radius: 10px;
		background: rgba(255, 255, 255, 0.65);
		color: #645a72;
		font-size: 11px;
		white-space: nowrap;
	}
	.subject-filter select {
		max-width: 180px;
		cursor: pointer;
	}
	.contribute {
		display: grid;
		place-items: center;
		background: #8265bc;
		border-color: #8265bc;
		color: #fff;
		font-weight: 600;
	}
	.contribute:hover {
		background: #7256ab !important;
	}
	.pill:hover {
		background: rgba(255, 255, 255, 0.9);
	}
	.header-count {
		margin-left: auto;
		margin-right: 4px;
		color: #756b80;
		font-size: 11px;
		white-space: nowrap;
	}
	.header-count strong {
		color: #544d65;
	}

	/* The left panel. */
	.navigator {
		position: absolute;
		left: 12px;
		bottom: 12px;
		width: 220px;
		z-index: 3;
		border-radius: 16px;
		padding: 16px 14px;
		overflow-y: auto;
		display: flex;
		flex-direction: column;
	}
	.nav-title {
		display: flex;
		align-items: center;
		justify-content: space-between;
		font-size: 11px;
		font-weight: 700;
	}
	.icon-button {
		display: grid;
		place-items: center;
		width: 24px;
		height: 24px;
		border-radius: 7px;
		color: #756b80;
		font-size: 14px;
		background: rgba(255, 255, 255, 0.6);
	}
	.icon-button:hover {
		background: #fff;
		color: var(--purple);
	}
	.overview {
		display: flex;
		gap: 9px;
		align-items: center;
		border: 1px solid #e5ddf5;
		border-radius: 9px;
		background: rgba(247, 244, 253, 0.75);
		color: #7560b9;
		margin: 14px 0 18px;
		padding: 9px 10px;
		font-size: 12px;
		text-align: left;
	}
	.overview span:last-child {
		margin-left: auto;
	}
	.nav-label {
		font-size: 9px;
		letter-spacing: 1px;
		color: #756b80;
		font-weight: 700;
		margin-bottom: 8px;
	}
	.levels {
		display: flex;
		flex-direction: column;
		gap: 2px;
		margin-bottom: 20px;
	}
	.levels button {
		display: flex;
		align-items: center;
		padding: 6px 10px;
		gap: 10px;
		border-radius: 8px;
		font-size: 12px;
		color: #6f6879;
		text-align: left;
	}
	.levels button:hover,
	.levels button.active {
		color: #7356be;
		background: rgba(242, 237, 249, 0.85);
	}
	.level-dot {
		width: 5px;
		height: 5px;
		border-radius: 50%;
		background: #ccc6d4;
	}
	.active .level-dot {
		background: #8e70d2;
	}
	.level-arrow {
		margin-left: auto;
		opacity: 0;
	}
	.active .level-arrow {
		opacity: 1;
	}
	.subjects {
		display: grid;
		gap: 9px;
		font-size: 11px;
		color: #6f6879;
		padding: 2px 10px 20px;
	}
	.subjects div {
		display: flex;
		align-items: center;
		gap: 10px;
	}
	.subjects i,
	.subject-tag i {
		width: 7px;
		height: 7px;
		border-radius: 2px;
		display: inline-block;
	}
	.about {
		padding: 13px;
		background: rgba(255, 255, 255, 0.5);
		border: 1px solid rgba(255, 255, 255, 0.8);
		border-radius: 11px;
		margin-top: auto;
		display: flex;
		flex-direction: column;
		gap: 7px;
		font-size: 10px;
		color: #6f6879;
	}
	.about a {
		color: #765cb8;
		font-weight: 600;
	}
	.about p {
		margin: 0;
		line-height: 1.8;
	}
	.nav-tab {
		position: absolute;
		left: 12px;
		z-index: 3;
		display: flex;
		gap: 8px;
		align-items: center;
		height: 36px;
		padding: 0 14px;
		border-radius: 12px;
		font-size: 12px;
		color: #645a72;
	}
	.nav-tab:hover {
		color: var(--purple);
	}
	.level-bar {
		position: absolute;
		left: 12px;
		right: 12px;
		z-index: 3;
		display: flex;
		gap: 5px;
		overflow-x: auto;
		padding: 6px;
		border-radius: 14px;
	}
	.level-bar button {
		white-space: nowrap;
		padding: 5px 11px;
		border-radius: 9px;
		font-size: 12px;
		color: #6f6879;
	}
	.level-bar button.active {
		color: #7356be;
		background: rgba(242, 237, 249, 0.9);
	}

	/* The minimap. */
	.minimap-panel {
		--glass: rgba(255, 255, 255, 0.76);
		position: absolute;
		z-index: 3;
		padding: 8px 10px 10px;
		border-radius: 14px;
	}
	.minimap-heading {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-bottom: 6px;
		font-size: 9px;
		letter-spacing: 1px;
		font-weight: 700;
		color: #756b80;
	}
	.minimap-heading .icon-button {
		width: 20px;
		height: 20px;
	}

	/* Floating controls. */
	.board-bottom {
		position: absolute;
		bottom: 12px;
		z-index: 3;
		display: flex;
		align-items: center;
		justify-content: space-between;
		pointer-events: none;
		gap: 8px;
	}
	.board-hint {
		color: #6f6879;
		font-size: 10px;
		padding: 7px 10px;
		border-radius: 10px;
	}
	.board-hint span {
		padding: 0 5px;
	}
	.board-hint strong {
		color: #544d65;
	}
	.zoom-controls {
		display: flex;
		align-items: center;
		gap: 3px;
		border-radius: 12px;
		padding: 4px;
		margin-left: auto;
		pointer-events: auto;
	}
	.zoom-controls button {
		min-width: 29px;
		height: 29px;
		border-radius: 8px;
		font-size: 16px;
		color: #776c85;
	}
	.zoom-controls button:hover,
	.zoom-controls button.on {
		background: rgba(241, 237, 247, 0.9);
		color: var(--purple);
	}
	.zoom-controls .zoom-number {
		font-size: 10px;
		min-width: 40px;
	}
	.control-divider {
		height: 16px;
		width: 1px;
		background: #e8e4ed;
	}
	.help,
	.empty {
		position: absolute;
		z-index: 4;
		border-radius: 14px;
		padding: 18px;
		font-size: 12px;
	}
	.help {
		bottom: 64px;
		width: min(320px, calc(100% - 24px));
	}
	.help p,
	.empty p {
		color: #6f6879;
		margin: 10px 0;
		line-height: 1.8;
	}
	.help button,
	.empty button {
		color: var(--purple);
		font-weight: 600;
	}
	.empty {
		top: 45%;
		transform: translate(-50%, -50%);
		width: min(340px, 90%);
		text-align: center;
	}

	/* The details panel. */
	.inspector {
		position: absolute;
		right: 12px;
		bottom: 12px;
		width: 340px;
		z-index: 3;
		padding: 18px;
		border-radius: 16px;
		overflow-y: auto;
		/* Reading happens here: frosted, but nearly opaque. */
		--glass: rgba(255, 255, 255, 0.84);
	}
	.inspector-heading {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-bottom: 16px;
	}
	.heading-buttons {
		display: flex;
		gap: 6px;
	}
	.heading-buttons button {
		font-size: 18px;
		line-height: 1;
		color: #756b80;
		width: 28px;
		height: 28px;
		border-radius: 8px;
		background: rgba(247, 245, 250, 0.8);
	}
	.heading-buttons button:hover {
		color: var(--purple);
		background: #fff;
	}
	.inspector-tab {
		position: absolute;
		right: 12px;
		z-index: 3;
		display: flex;
		align-items: center;
		gap: 8px;
		max-width: 260px;
		height: 36px;
		padding: 0 14px;
		border-radius: 12px;
		font-size: 12px;
		color: #645a72;
	}
	.inspector-tab:hover {
		color: var(--purple);
	}
	.tab-name {
		overflow: hidden;
		white-space: nowrap;
		text-overflow: ellipsis;
	}
	.subject-tag {
		display: flex;
		gap: 7px;
		align-items: center;
		font-size: 10px;
	}
	h2 {
		font-size: 19px;
		font-weight: 650;
		line-height: 1.6;
		margin: 12px 0 5px;
		color: #4d425c;
	}
	.detail-topic {
		font-size: 11px;
		color: #756b80;
		margin: 0;
	}
	dl {
		display: grid;
		grid-template-columns: 1fr 1.2fr;
		gap: 10px;
		font-size: 10px;
		margin: 22px 0;
	}
	dt {
		color: #756b80;
	}
	dd {
		color: #72607f;
		text-align: right;
		margin: 0;
	}
	dd code {
		font-size: 9px;
		overflow-wrap: anywhere;
	}
	.origin {
		display: flex;
		flex-direction: column;
		gap: 6px;
		font-size: 11px;
		color: #756b80;
		margin-bottom: 22px;
	}
	.origin p {
		margin: 0;
		line-height: 1.7;
	}
	.origin ul {
		margin: 0;
		padding-left: 16px;
		line-height: 1.7;
		overflow-wrap: anywhere;
	}
	.source-button {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-top: 6px;
		padding: 11px 15px;
		background: #8265bc;
		color: white;
		border-radius: 10px;
		font-size: 12px;
		font-weight: 600;
	}
	.source-button:hover {
		background: #7256ab;
	}
	.related-heading {
		display: flex;
		justify-content: space-between;
		border-top: 1px solid rgba(231, 229, 235, 0.9);
		padding-top: 18px;
		font-size: 9px;
		color: #756b80;
		letter-spacing: 0.6px;
	}
	.related {
		display: grid;
		gap: 4px;
		margin-top: 10px;
	}
	.related button {
		display: flex;
		gap: 10px;
		justify-content: space-between;
		text-align: left;
		font-size: 11px;
		padding: 9px 10px;
		border-radius: 8px;
		color: #6f6879;
	}
	.related button.active,
	.related button:hover {
		background: rgba(243, 239, 249, 0.9);
		color: #7753a4;
	}
	.related small {
		flex-shrink: 0;
	}

	@media (max-width: 1100px) {
		.header-count {
			display: none;
		}
		.contribute {
			margin-left: auto;
		}
	}
	@media (max-width: 900px) {
		.collapse,
		.board-hint {
			display: none;
		}
	}

	/* Phones: the header wraps, levels become a chip row, details a bottom sheet. */
	.mobile .board-header {
		top: 8px;
		left: 8px;
		right: 8px;
		flex-wrap: wrap;
		gap: 8px;
	}
	.mobile .search {
		order: 3;
		flex-basis: 100%;
		max-width: none;
		margin-left: 0;
	}
	.mobile .contribute {
		margin-left: auto;
	}
	.mobile .subject-filter {
		order: 4;
		flex: 1;
	}
	.mobile .subject-filter select {
		width: 100%;
		max-width: none;
	}
	.mobile .level-bar {
		left: 8px;
		right: 8px;
	}
	.mobile .inspector {
		left: 8px;
		right: 8px;
		bottom: 8px;
		width: auto;
		max-height: 62dvh;
		border-radius: 18px;
	}
	.mobile .inspector-tab {
		top: auto;
		right: 8px;
		bottom: 60px;
	}
	.mobile .board-bottom {
		bottom: 8px;
	}
	.mobile .subject-ruler strong {
		font-size: 9px;
	}
</style>
