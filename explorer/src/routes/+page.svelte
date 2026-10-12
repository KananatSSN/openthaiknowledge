<script lang="ts">
	import { replaceState } from '$app/navigation';
	import { page } from '$app/state';
	import Board from '$lib/Board.svelte';

	let { data } = $props();
</script>

<Board
	items={data.catalog.sets}
	mistakes={data.catalog.mistakes}
	version={data.catalog.version}
	initialSet={page.url.searchParams.get('set') ?? ''}
	onselect={(key) => {
		const url = new URL(page.url);
		if (key) url.searchParams.set('set', key);
		else url.searchParams.delete('set');
		replaceState(url, {});
	}}
/>
