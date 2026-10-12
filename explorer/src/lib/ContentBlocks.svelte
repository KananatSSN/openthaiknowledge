<script lang="ts">
	import katex from 'katex';
	import 'katex/dist/katex.min.css';
	import { assetUrl, type Block } from '$lib/data';

	let { blocks }: { blocks: Block[] } = $props();

	function renderMath(node: HTMLElement, tex: string) {
		const render = (value: string) => katex.render(value, node, { throwOnError: false });
		render(tex);
		return { update: render };
	}
</script>

<span class="blocks">
	{#each blocks as block, index (`${block.kind}-${index}`)}
		{#if block.kind === 'math'}
			<span class="math" role="img" aria-label={block.tex} use:renderMath={block.tex}></span>
		{:else if block.kind === 'image'}
			<img src={assetUrl(block.asset_id)} alt={block.alt || ''} loading="lazy" />
		{:else if block.kind === 'code'}
			<!-- A program keeps its line breaks and indentation: they are part of what it means. -->
			<pre data-language={block.language}><code>{block.code}</code></pre>
		{:else}
			<!-- Authored newlines matter (tables, food chains); source indentation does not. -->
			<span class="text">{block.text}</span>
		{/if}
	{/each}
</span>

<style>
	.blocks {
		display: inline-flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.4rem;
	}
	.text {
		white-space: pre-line;
	}
	img {
		max-width: 100%;
		max-height: 18rem;
		border-radius: 0.5rem;
		object-fit: contain;
		background: #fff;
	}
	pre {
		flex-basis: 100%;
		margin: 0;
		overflow-x: auto;
		padding: 0.5rem 0.75rem;
		border-radius: 0.5rem;
		background: var(--surface-sunk);
		font-size: 0.875rem;
		line-height: 1.5;
	}
</style>
