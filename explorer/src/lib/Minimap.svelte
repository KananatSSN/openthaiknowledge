<script lang="ts">
	// A small overview of the board. It is drawn at the board's width, so on a
	// tall board it shows a window that follows the view, like an editor's
	// minimap. Click or drag on it to move the view there.
	type Card = { x: number; y: number; height: number; subject: string; id: string };
	type Row = { level: string; y: number; height: number };
	let {
		cards,
		rows,
		boardWidth,
		boardHeight,
		view,
		viewWidth,
		viewHeight,
		color,
		onnavigate,
		label
	}: {
		cards: Card[];
		rows: Row[];
		boardWidth: number;
		boardHeight: number;
		view: { x: number; y: number; k: number };
		viewWidth: number;
		viewHeight: number;
		color: (subject: string) => string;
		onnavigate: (x: number, y: number) => void;
		label: string;
	} = $props();
	const WIDTH = 176;
	const MAX_HEIGHT = 220;
	const CARD_WIDTH = 320;

	let scale = $derived(WIDTH / Math.max(boardWidth, 1));
	let fullHeight = $derived(boardHeight * scale);
	let height = $derived(Math.min(MAX_HEIGHT, Math.max(fullHeight, 60)));
	// What the main view shows, in board coordinates.
	let shown = $derived({
		x: -view.x / view.k,
		y: -view.y / view.k,
		width: viewWidth / view.k,
		height: viewHeight / view.k
	});
	// The window keeps the view's centre in the middle where it can.
	let offset = $derived(
		Math.max(
			0,
			Math.min(fullHeight - height, (shown.y + shown.height / 2) * scale - height / 2)
		)
	);
	let dragging = false;

	function go(event: PointerEvent) {
		const rect = (event.currentTarget as SVGElement).getBoundingClientRect();
		onnavigate((event.clientX - rect.left) / scale, (event.clientY - rect.top + offset) / scale);
	}
	function down(event: PointerEvent) {
		dragging = true;
		(event.currentTarget as SVGElement).setPointerCapture(event.pointerId);
		go(event);
	}
	function move(event: PointerEvent) {
		if (dragging) go(event);
	}
	function up() {
		dragging = false;
	}
</script>

<svg
	class="minimap"
	width={WIDTH}
	{height}
	viewBox={`0 ${offset / scale} ${boardWidth} ${height / scale}`}
	preserveAspectRatio="xMinYMin slice"
	role="img"
	aria-label={label}
	onpointerdown={down}
	onpointermove={move}
	onpointerup={up}
	onpointercancel={up}
>
	{#each rows as row (row.level)}<line
			x1="0"
			x2={boardWidth}
			y1={row.y}
			y2={row.y}
			class="row-line"
			vector-effect="non-scaling-stroke"
		/>{/each}
	{#each cards as card (card.id)}<rect
			x={card.x}
			y={card.y}
			width={CARD_WIDTH}
			height={card.height}
			rx="16"
			fill={color(card.subject)}
			class="card"
		/>{/each}
	<rect
		class="window"
		x={shown.x}
		y={shown.y}
		width={shown.width}
		height={shown.height}
		rx="12"
		vector-effect="non-scaling-stroke"
	/>
</svg>

<style>
	.minimap {
		display: block;
		cursor: crosshair;
		touch-action: none;
		border-radius: 10px;
	}
	.row-line {
		stroke: #b9b2c7;
		stroke-width: 1;
		stroke-dasharray: 3 3;
	}
	.card {
		opacity: 0.55;
	}
	.window {
		fill: #7560c91f;
		stroke: #7560c9;
		stroke-width: 1.5;
	}
</style>
