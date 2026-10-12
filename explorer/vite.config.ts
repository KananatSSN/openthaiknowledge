import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	// The contribute page renders the repository's README.md, one folder up.
	server: { fs: { allow: ['..'] } }
});
