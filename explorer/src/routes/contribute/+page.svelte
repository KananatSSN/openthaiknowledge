<script lang="ts">
	import { resolve } from '$app/paths';
	import Brand from '$lib/Brand.svelte';
	import GithubLink from '$lib/GithubLink.svelte';
	import { locale, setLocale, t } from '$lib/locale.svelte';

	let { data } = $props();

	// Every code block gets a copy button; the set-up prompt is the one people
	// copy into their agent, so it is the first thing the page offers.
	// Re-run when the language switches: the article's content is replaced.
	function copyButtons(node: HTMLElement, _html: string) {
		const label = () => (locale.value === 'th' ? 'คัดลอก' : 'Copy');
		const add = () => {
			for (const pre of node.querySelectorAll('pre')) {
				if (pre.querySelector('.copy')) continue;
				const button = document.createElement('button');
				button.type = 'button';
				button.className = 'copy';
				button.textContent = label();
				button.addEventListener('click', async () => {
					try {
						await navigator.clipboard.writeText(pre.querySelector('code')?.textContent ?? '');
						button.textContent = locale.value === 'th' ? 'คัดลอกแล้ว ✓' : 'Copied ✓';
					} catch {
						button.textContent = locale.value === 'th' ? 'คัดลอกไม่ได้' : 'Could not copy';
					}
					setTimeout(() => (button.textContent = label()), 1800);
				});
				pre.append(button);
			}
		};
		add();
		return { update: add };
	}
</script>

<svelte:head>
	<title>{t('ร่วมพัฒนา', 'Contribute')} · OpenThaiKnowledge</title>
</svelte:head>

<div class="page">
	<header class="bar glass">
		<Brand subtitle={t('ร่วมพัฒนา', 'Contribute')} />
		<a class="board-link" href={resolve('/')}>{t('สำรวจชุดโจทย์', 'Explore sets')} →</a>
		<GithubLink />
		<button
			class="pill"
			onclick={() => setLocale(locale.value === 'th' ? 'en' : 'th')}
			aria-label={t('Switch to English', 'เปลี่ยนเป็นภาษาไทย')}
			>{locale.value === 'th' ? 'EN' : 'ไทย'}</button
		>
	</header>
	<main class="sheet glass">
		<p class="lead">
			{t(
				'ร่วมพัฒนาด้วย AI agent ของคุณ: คัดลอกข้อความในหัวข้อ "ร่วมพัฒนาด้วย AI agent ของคุณ" ไปวางใน agent แล้ว agent จะ fork, clone, ติดตั้ง และตรวจโปรเจกต์ให้พร้อมทำงาน',
				'Contribute with your own AI agent: copy the prompt under "Contribute with your AI agent" into it, and it forks, clones, installs and checks the project, ready to work.'
			)}
		</p>
		<article class="readme" lang={locale.value} use:copyButtons={data.html[locale.value]}>
			<!-- The repository's own README, rendered at build time. -->
			<!-- eslint-disable-next-line svelte/no-at-html-tags -->
			{@html data.html[locale.value]}
		</article>
	</main>
</div>

<style>
	.page {
		min-height: 100dvh;
		padding: 12px 12px 48px;
		color: #35333f;
		background-color: #f1f0f7;
		background-image:
			radial-gradient(circle at 10% 12%, #e3d9ff 0, transparent 34%),
			radial-gradient(circle at 92% 8%, #d3f0e8 0, transparent 30%),
			radial-gradient(circle at 70% 70%, #fde6d2 0, transparent 34%);
		background-attachment: fixed;
	}
	.glass {
		background: rgba(255, 255, 255, 0.66);
		border: 1px solid rgba(255, 255, 255, 0.8);
		box-shadow: 0 10px 34px rgba(52, 38, 92, 0.12), 0 1px 2px rgba(52, 38, 92, 0.06);
		-webkit-backdrop-filter: blur(22px);
		/* Standard last: the minifier keeps only the last of the pair. */
		backdrop-filter: blur(22px);
	}
	.bar {
		position: sticky;
		top: 12px;
		z-index: 2;
		display: flex;
		align-items: center;
		gap: 12px;
		max-width: 920px;
		margin: 0 auto;
		min-height: 52px;
		padding: 8px 10px 8px 12px;
		border-radius: 16px;
	}
	.board-link {
		margin-left: auto;
		color: #6a4fc0;
		font-size: 12px;
		font-weight: 600;
		white-space: nowrap;
	}
	.pill {
		height: 32px;
		padding: 0 12px;
		border: 1px solid rgba(231, 229, 235, 0.9);
		border-radius: 10px;
		background: rgba(255, 255, 255, 0.65);
		color: #645a72;
		font-size: 11px;
		cursor: pointer;
	}
	.sheet {
		max-width: 920px;
		margin: 16px auto 0;
		padding: 28px clamp(16px, 4vw, 44px) 36px;
		border-radius: 20px;
		background: rgba(255, 255, 255, 0.84);
	}
	.lead {
		margin: 0 0 8px;
		padding: 14px 16px;
		border-radius: 12px;
		background: rgba(244, 240, 252, 0.85);
		border: 1px solid #e6e0f3;
		color: #5b4e78;
		font-size: 14px;
		line-height: 1.8;
	}
	.readme {
		font-size: 15px;
		line-height: 1.75;
		overflow-wrap: anywhere;
	}
	/* Clear the sticky bar when a link jumps to a heading. */
	.readme :global(:is(h1, h2, h3)) {
		scroll-margin-top: 84px;
	}
	.readme :global(h1) {
		font-size: 28px;
		letter-spacing: -0.5px;
		margin: 24px 0 8px;
	}
	.readme :global(h2) {
		font-size: 20px;
		margin: 36px 0 8px;
		padding-top: 20px;
		border-top: 1px solid rgba(231, 229, 235, 0.9);
	}
	.readme :global(h3) {
		font-size: 16px;
		margin: 24px 0 6px;
	}
	.readme :global(a) {
		color: #6a4fc0;
		text-decoration: underline;
		text-underline-offset: 3px;
	}
	.readme :global(code) {
		font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
		font-size: 0.88em;
		background: rgba(238, 235, 245, 0.9);
		padding: 1px 5px;
		border-radius: 5px;
	}
	.readme :global(pre) {
		position: relative;
		margin: 14px 0;
		padding: 16px 18px;
		padding-top: 40px;
		border-radius: 12px;
		background: #1f1c2b;
		color: #ece9f5;
		overflow-x: auto;
		font-size: 13px;
		line-height: 1.6;
	}
	.readme :global(pre code) {
		background: none;
		padding: 0;
		color: inherit;
		white-space: pre;
		overflow-wrap: normal;
	}
	.readme :global(.copy) {
		position: absolute;
		top: 8px;
		right: 8px;
		padding: 4px 12px;
		border-radius: 8px;
		background: #8265bc;
		color: #fff;
		font-size: 12px;
		font-weight: 600;
		cursor: pointer;
	}
	.readme :global(.copy:hover) {
		background: #7256ab;
	}
	.readme :global(table) {
		display: block;
		overflow-x: auto;
		border-collapse: collapse;
		font-size: 13px;
		margin: 14px 0;
	}
	.readme :global(th),
	.readme :global(td) {
		border: 1px solid rgba(225, 221, 233, 0.95);
		padding: 7px 10px;
		text-align: left;
		vertical-align: top;
	}
	.readme :global(th) {
		background: rgba(244, 240, 252, 0.8);
	}
	.readme :global(ul) {
		padding-left: 22px;
	}
</style>
