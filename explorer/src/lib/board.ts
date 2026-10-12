import type { SetRow } from './data';

// The curriculum board's grouping and layout, the same as TutorRank's /skills
// board: one column per subject, one row per level, a card per curriculum unit.

export type BoardTopic = {
	id: string;
	name: string;
	subject: string;
	level: string;
	course: string;
	strand: string;
	items: SetRow[];
};

export function levelOrder(level: string) {
	const number = Number(level.match(/\d+/)?.[0] || 0);
	if (/^ป\./.test(level)) return number;
	if (/^ม\./.test(level)) return 6 + number;
	return 100 + number;
}

export function boardTopics(items: SetRow[]): BoardTopic[] {
	const topics = new Map<string, BoardTopic>();
	for (const item of items) {
		const id = JSON.stringify([
			item.subject,
			item.level,
			item.course_type,
			item.strand_code,
			item.curriculum_node_id || item.topic
		]);
		let topic = topics.get(id);
		if (!topic) {
			topic = {
				id,
				name: item.unit || item.topic || item.subject,
				subject: item.subject,
				level: item.level,
				course: item.course_type || '',
				strand: item.strand || '',
				items: []
			};
			topics.set(id, topic);
		}
		topic.items.push(item);
	}
	for (const topic of topics.values()) {
		topic.items.sort(
			(a, b) =>
				a.learning_stage - b.learning_stage || a.display_name.localeCompare(b.display_name, 'th')
		);
	}
	return [...topics.values()];
}

export const COLUMN = 336;
export const TOP = 96;
export const LEFT = 100;
export const SET_HEIGHT = 62;

export function layoutBoard(
	topics: BoardTopic[],
	subjects: string[],
	levels: string[],
	expanded: ReadonlySet<string>
) {
	let y = TOP;
	const cards: Array<{ topic: BoardTopic; x: number; y: number; height: number }> = [];
	const rows = levels.map((level) => {
		const start = y;
		let height = 180;
		for (const [column, subject] of subjects.entries()) {
			let cursor = start + 40;
			for (const topic of topics.filter(
				(topic) => topic.level === level && topic.subject === subject
			)) {
				const cardHeight = 108 + (expanded.has(topic.id) ? topic.items.length * SET_HEIGHT + 12 : 0);
				cards.push({ topic, x: LEFT + column * COLUMN, y: cursor, height: cardHeight });
				cursor += cardHeight + 16;
			}
			height = Math.max(height, cursor - start + 24);
		}
		y += height;
		return { level, y: start, height };
	});
	return { cards, rows, width: LEFT + subjects.length * COLUMN + 24, height: y + 40 };
}
