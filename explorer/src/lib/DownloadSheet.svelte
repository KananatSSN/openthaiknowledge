<script lang="ts">
	import { base } from '$app/paths';
	import { onMount } from 'svelte';
	import { t } from './locale.svelte';

	// One click, one PDF: a page of freshly drawn problems from this set and a
	// page of answers, made by the sheets server (otk.tools.explorer_pdf). The
	// server allows each visitor one sheet every 30 seconds, for every set, so the
	// wait is kept here across sets and reloads and the button counts it down.
	let { setKey }: { setKey: string } = $props();
	const COOLDOWN_MS = 30_000;
	const STORE = 'otk-explorer-sheet-wait-until';

	let waitUntil = $state(0);
	let now = $state(Date.now());
	let busy = $state(false);
	let failed = $state(false);
	let left = $derived(Math.max(0, Math.ceil((waitUntil - now) / 1000)));

	onMount(() => {
		try {
			waitUntil = Number(localStorage.getItem(STORE)) || 0;
		} catch {
			// Blocked storage: the wait just is not remembered across reloads.
		}
		const timer = setInterval(() => (now = Date.now()), 500);
		return () => clearInterval(timer);
	});

	function hold(ms: number) {
		waitUntil = Date.now() + ms;
		now = Date.now();
		try {
			localStorage.setItem(STORE, String(waitUntil));
		} catch {
			// As above.
		}
	}

	async function download() {
		if (busy || left > 0) return;
		busy = true;
		failed = false;
		try {
			const response = await fetch(`${base}/api/sheet?key=${encodeURIComponent(setKey)}`);
			if (response.status === 429) {
				hold((Number(response.headers.get('Retry-After')) || 30) * 1000);
				return;
			}
			if (!response.ok) throw new Error(`sheet ${response.status}`);
			const url = URL.createObjectURL(await response.blob());
			const link = document.createElement('a');
			link.href = url;
			link.download = `otk-${setKey}.pdf`;
			document.body.append(link);
			link.click();
			link.remove();
			setTimeout(() => URL.revokeObjectURL(url), 10_000);
			hold(COOLDOWN_MS);
		} catch {
			failed = true;
		} finally {
			busy = false;
		}
	}
</script>

<div class="download">
	<button onclick={download} disabled={busy || left > 0} aria-live="polite">
		<span class="icon" aria-hidden="true">⤓</span>
		<span class="label"
			>{#if busy}{t('กำลังสร้าง PDF…', 'Making the PDF…')}{:else if left > 0}{t(
					`ดาวน์โหลดได้อีกครั้งใน ${left} วินาที`,
					`Download again in ${left}s`
				)}{:else}{t('ดาวน์โหลดใบงาน PDF', 'Download worksheet PDF')}{/if}</span
		>
	</button>
	<p class="note">
		{#if failed}{t(
				'สร้าง PDF ไม่สำเร็จ ลองใหม่อีกครั้ง',
				'Could not make the PDF. Please try again.'
			)}{:else}{t(
				'โจทย์ชุดใหม่ 1 หน้า และเฉลย 1 หน้า ทุกครั้งที่กด',
				'A new page of problems and a page of answers each time'
			)}{/if}
	</p>
</div>

<style>
	.download {
		margin: 10px 0 14px;
	}
	button {
		display: flex;
		align-items: center;
		gap: 10px;
		width: 100%;
		padding: 11px 15px;
		background: #18766f;
		color: white;
		border: 0;
		border-radius: 10px;
		font: inherit;
		font-size: 13px;
		font-weight: 600;
		cursor: pointer;
	}
	button:hover:not(:disabled) {
		background: #136159;
	}
	button:disabled {
		background: #8aa9a6;
		cursor: default;
	}
	.icon {
		font-size: 16px;
		line-height: 1;
	}
	.note {
		margin: 6px 2px 0;
		font-size: 11px;
		color: #6b6b7b;
	}
</style>
