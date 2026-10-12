<script lang="ts">
	import { resolve } from '$app/paths';
	import { page } from '$app/state';
	import { t } from '$lib/locale.svelte';
</script>

<h1>{page.status}</h1>
<p>{page.error?.message}</p>
<p><a href={resolve('/')}>{t('กลับไปหน้าแรก', 'Back to all problem sets')}</a></p>
