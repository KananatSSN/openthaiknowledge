import { marked } from "marked";
import readmeEn from "../../../../README.md?raw";
import readmeTh from "../../../../README.th.md?raw";
import type { PageLoad } from "./$types";

// The repository's README.md and README.th.md are the contributor guide; this
// page shows them, so there is one copy of each to keep current.
const REPO = "https://github.com/KananatSSN/openthaiknowledge";

export const prerender = true;

/** A heading's anchor, the way GitHub makes it (Thai letters and marks kept). */
const slug = (html: string) =>
  html
    .replace(/<[^>]+>/g, "")
    .toLowerCase()
    .trim()
    .replace(/[^\p{L}\p{M}\p{N}\s_-]/gu, "")
    .replace(/\s/g, "-");

function render(markdown: string): string {
  // The page has its own language switch; drop the README's language links.
  const body = markdown.replace(/^.*\]\(README(\.th)?\.md\).*\n/m, "");
  return (marked.parse(body, { async: false, gfm: true }) as string)
    .replace(
      /<h([1-6])>([\s\S]*?)<\/h\1>/g,
      (_, level, inner) =>
        `<h${level} id="${slug(inner)}">${inner}</h${level}>`,
    )
    .replace(/href="(?!https?:|#|mailto:)([^"]+)"/g, (_, path: string) => {
      const kind = path.split("#")[0].endsWith("/") ? "tree" : "blob";
      return `href="${REPO}/${kind}/main/${path.replace(/^\.\//, "")}"`;
    });
}

export const load: PageLoad = () => ({
  html: { en: render(readmeEn), th: render(readmeTh) },
});
