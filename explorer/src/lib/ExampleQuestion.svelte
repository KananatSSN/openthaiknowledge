<script lang="ts">
	import ContentBlocks from './ContentBlocks.svelte';
	import { loadSet, type SetDetail } from './data';
	import { locale, t } from './locale.svelte';

	// The set's pre-drawn examples (fixed seeds, built by `npm run data`). "Another"
	// steps through them; the answer shows the named mistake behind each wrong choice.
	let {
		setKey,
		mistakes,
		onload
	}: {
		setKey: string;
		mistakes: Record<string, { th: string; en: string }>;
		onload?: (detail: SetDetail) => void;
	} = $props();
	const LABELS = 'กขคงจฉชซ';

	let detail = $state<SetDetail | null>(null);
	let failed = $state(false);
	let index = $state(0);
	let revealed = $state(false);
	const question = $derived(detail?.examples[index] ?? null);
	const mistakeName = (key: string | null) =>
		key ? (mistakes[key]?.[locale.value] ?? key) : null;

	$effect(() => {
		const key = setKey;
		detail = null;
		failed = false;
		index = 0;
		revealed = false;
		loadSet(fetch, key)
			.then((loaded) => {
				if (key !== setKey) return;
				detail = loaded;
				onload?.(loaded);
			})
			.catch(() => {
				if (key === setKey) failed = true;
			});
	});

	function another() {
		if (!detail) return;
		index = (index + 1) % detail.examples.length;
		revealed = false;
	}
</script>

<section class="example" aria-label={t('ตัวอย่างโจทย์', 'Example question')}>
	<div class="example-heading">
		<span
			>{t('ตัวอย่างโจทย์', 'EXAMPLE QUESTION')}{detail && detail.examples.length > 1
				? ` ${index + 1}/${detail.examples.length}`
				: ''}</span
		>
		{#if detail && detail.examples.length > 1}<button type="button" onclick={another}
				>🎲 {t('ข้ออื่น', 'Another')}</button
			>{/if}
	</div>
	{#if failed}
		<p class="example-note">{t('โหลดตัวอย่างไม่สำเร็จ', 'Could not load the examples.')}</p>
	{:else if !question}
		<p class="example-note">{t('กำลังโหลดตัวอย่าง…', 'Loading an example…')}</p>
	{:else}
		<div class="example-stem"><ContentBlocks blocks={question.stem} /></div>
		<ol class="example-choices">
			{#each question.choices as choice, i (i)}
				<li class:correct={revealed && i === question.answer}>
					<span class="letter">{LABELS[i] ?? i + 1}</span>
					<span class="choice"
						><ContentBlocks blocks={choice.content} />{#if revealed && i !== question.answer && mistakeName(question.mistakes[i])}<small
								class="mistake">{mistakeName(question.mistakes[i])}</small
							>{/if}</span
					>
				</li>
			{/each}
		</ol>
		{#if revealed}
			{#if question.hint?.length}<div class="example-hint">
					<ContentBlocks blocks={question.hint} />
				</div>{/if}
		{:else}
			<button type="button" class="reveal" onclick={() => (revealed = true)}
				>{t('ดูเฉลย', 'Show answer')}</button
			>
		{/if}
	{/if}
</section>

<style>
	.example {
		margin-top: 1rem;
		border: 1px solid #e2e8f0;
		border-radius: 0.9rem;
		padding: 0.85rem;
		background: #fbfcfe;
	}
	.example-heading {
		display: flex;
		align-items: center;
		justify-content: space-between;
		font-size: 0.72rem;
		font-weight: 800;
		letter-spacing: 0.06em;
		color: #64748b;
	}
	.example-heading button,
	.reveal {
		border: 1px solid #cbd5e1;
		border-radius: 999px;
		background: white;
		padding: 0.2rem 0.7rem;
		font-size: 0.78rem;
		font-weight: 700;
		color: #334155;
		letter-spacing: 0;
	}
	.example-stem {
		margin-top: 0.7rem;
		line-height: 1.6;
	}
	.example-choices {
		margin: 0.7rem 0 0;
		padding: 0;
		list-style: none;
		display: grid;
		gap: 0.4rem;
	}
	.example-choices li {
		display: flex;
		align-items: flex-start;
		gap: 0.5rem;
		border: 1px solid #e2e8f0;
		border-radius: 0.6rem;
		background: white;
		padding: 0.4rem 0.6rem;
	}
	.example-choices li.correct {
		border-color: #16a34a;
		background: #f0fdf4;
	}
	.choice {
		display: flex;
		flex-direction: column;
		gap: 0.15rem;
		min-width: 0;
	}
	.mistake {
		font-size: 0.72rem;
		color: #b42318;
	}
	.letter {
		font-weight: 800;
		color: #64748b;
		min-width: 1.1rem;
	}
	.reveal {
		margin-top: 0.7rem;
	}
	.example-hint {
		margin-top: 0.7rem;
		border-left: 3px solid #16a34a;
		padding-left: 0.6rem;
		color: #334155;
		font-size: 0.9rem;
	}
	.example-note {
		margin-top: 0.7rem;
		color: #64748b;
		font-size: 0.9rem;
	}
</style>
