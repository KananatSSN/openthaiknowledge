<script lang="ts">
	let { children } = $props();
</script>

<svelte:head>
	<title>OpenThaiKnowledge · สำรวจชุดโจทย์</title>
</svelte:head>

{@render children()}

<style>
	:global(:root) {
		--surface-sunk: #eef0f3;
		color-scheme: light;
	}
	:global(*, *::before, *::after) {
		box-sizing: border-box;
	}
	:global(body) {
		margin: 0;
		background: #fff;
		color: #0f172a;
		font-family: Inter, 'Noto Sans Thai', ui-sans-serif, system-ui, sans-serif;
		-webkit-font-smoothing: antialiased;
		line-height: 1.5;
	}
	/* The board was designed on a reset stylesheet: controls inherit the page's type. */
	:global(button, input, select) {
		font: inherit;
		color: inherit;
		margin: 0;
		padding: 0;
		border: 0;
		background: none;
	}
	:global(a) {
		text-decoration: none;
	}
	:global(:focus-visible) {
		outline: 3px solid #f59e0b;
		outline-offset: 3px;
	}
</style>
