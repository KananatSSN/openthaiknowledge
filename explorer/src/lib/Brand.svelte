<script lang="ts">
	import { resolve } from '$app/paths';

	// The site's name at the top left: an open book on a tile, and the name.
	// Phones show the short form, OTK.
	let { subtitle = '' }: { subtitle?: string } = $props();
</script>

<a class="brand" href={resolve('/')} aria-label="OpenThaiKnowledge">
	<svg class="mark" viewBox="0 0 32 32" aria-hidden="true">
		<defs>
			<linearGradient id="otk-tile" x1="0" y1="0" x2="1" y2="1">
				<stop offset="0" stop-color="#7c5bd6" />
				<stop offset="1" stop-color="#2f8f87" />
			</linearGradient>
		</defs>
		<rect width="32" height="32" rx="9" fill="url(#otk-tile)" />
		<path
			d="M16 11.2C13.4 9.6 10.4 9.3 7 10v12c3.4-.7 6.4-.4 9 1.2 2.6-1.6 5.6-1.9 9-1.2V10c-3.4-.7-6.4-.4-9 1.2Z"
			fill="#fff"
			fill-opacity=".22"
			stroke="#fff"
			stroke-width="1.7"
			stroke-linejoin="round"
		/>
		<path d="M16 11.2v12" stroke="#fff" stroke-width="1.7" />
		<circle cx="16" cy="6" r="1.6" fill="#fff" />
	</svg>
	<span class="words">
		<span class="name"
			><span class="long">Open<em>Thai</em>Knowledge</span><span class="short">OTK</span></span
		>{#if subtitle}<span class="subtitle">{subtitle}</span>{/if}
	</span>
</a>

<style>
	.brand {
		display: flex;
		align-items: center;
		gap: 10px;
		min-width: 0;
		color: #2f2a3b;
		text-decoration: none;
	}
	.mark {
		width: 34px;
		height: 34px;
		flex-shrink: 0;
		filter: drop-shadow(0 3px 8px rgba(98, 74, 170, 0.28));
	}
	.words {
		display: flex;
		flex-direction: column;
		line-height: 1.15;
		min-width: 0;
	}
	.name {
		font-size: 16px;
		font-weight: 800;
		letter-spacing: -0.4px;
		white-space: nowrap;
	}
	.name em {
		font-style: normal;
		background: linear-gradient(90deg, #7c5bd6, #2f8f87);
		-webkit-background-clip: text;
		background-clip: text;
		color: transparent;
	}
	.short {
		display: none;
	}
	.subtitle {
		margin-top: 1px;
		color: #756b80;
		font-size: 10px;
		white-space: nowrap;
	}
	@media (max-width: 480px) {
		.long {
			display: none;
		}
		.short {
			display: inline;
		}
	}
</style>
