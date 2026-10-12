import { redirect } from '@sveltejs/kit';
import { base } from '$app/paths';
import type { PageLoad } from './$types';

// Sets used to have pages of their own; the board opens them now.
export const load: PageLoad = ({ params }) => {
	redirect(308, `${base}/?set=${encodeURIComponent(params.key)}`);
};
