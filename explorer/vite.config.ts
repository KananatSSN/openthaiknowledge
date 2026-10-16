import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		// The contribute page renders the repository's README.md, one folder up.
		fs: { allow: ['..'] },
		// The PDF sheets, from `python -m otk.tools.explorer_pdf --serve` run beside `npm run dev`.
		proxy: { '/api': 'http://127.0.0.1:8000' }
	}
});
