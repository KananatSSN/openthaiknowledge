import { base } from '$app/paths';

// The shapes `python -m otk.tools.explorer_data` writes into static/data.

export type Block =
	| { kind: 'text'; text: string }
	| { kind: 'math'; tex: string }
	| { kind: 'image'; asset_id: string; alt?: string }
	| { kind: 'code'; code: string; language?: string };

export type Names = { th: string; en: string };

export type SetRow = {
	key: string;
	display_name: string;
	subject: string;
	level: string;
	topic: string;
	unit: string | null;
	learning_stage: number;
	learning_stage_label: string;
	course_type: string | null;
	strand_code: string | null;
	strand: string | null;
	standard_code: string | null;
	indicator_codes: string[] | null;
	curriculum_node_id: string | null;
	provenance: 'original' | 'adapted';
};

export type Example = {
	stem: Block[];
	choices: { content: Block[] }[];
	answer: number;
	hint: Block[];
	mistakes: (string | null)[];
};

export type SetDetail = Omit<SetRow, 'provenance'> & {
	provenance: { kind: 'original' | 'adapted'; sources: string[]; derived: boolean };
	source_file: string;
	examples: Example[];
};

export type Catalog = { version: string; sets: SetRow[]; mistakes: Record<string, Names> };

async function json<T>(fetcher: typeof fetch, path: string): Promise<T> {
	const response = await fetcher(`${base}/data/${path}`);
	if (!response.ok) throw new Error(`${path}: ${response.status}`);
	return (await response.json()) as T;
}

export const loadCatalog = (fetcher: typeof fetch) => json<Catalog>(fetcher, 'catalog.json');

export const loadSet = (fetcher: typeof fetch, key: string) =>
	json<SetDetail>(fetcher, `sets/${encodeURIComponent(key)}.json`);

export const assetUrl = (id: string) => `${base}/data/assets/${encodeURIComponent(id)}.png`;
