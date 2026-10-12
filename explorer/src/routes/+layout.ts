import { loadCatalog } from '$lib/data';
import type { LayoutLoad } from './$types';

// Everything renders in the browser from static JSON: there is no server.
export const ssr = false;
export const prerender = false;

export const load: LayoutLoad = async ({ fetch }) => ({ catalog: await loadCatalog(fetch) });
