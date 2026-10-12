import adapter from '@sveltejs/adapter-static';

/** @type {import('@sveltejs/kit').Config} */
export default {
	compilerOptions: { runes: true },
	kit: {
		// A static site with no server: every page renders in the browser from the
		// JSON that `npm run data` writes, and unknown paths fall back to the app.
		adapter: adapter({ fallback: '404.html' }),
		paths: { base: process.env.BASE_PATH ?? '' }
	}
};
