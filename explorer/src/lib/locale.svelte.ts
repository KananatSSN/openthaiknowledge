// The interface language. Set names and questions are Thai either way; this
// switches the explorer's own labels. Remembered per browser when storage works.

const KEY = 'otk-explorer-locale';

function initial(): 'th' | 'en' {
	try {
		return localStorage.getItem(KEY) === 'en' ? 'en' : 'th';
	} catch {
		return 'th';
	}
}

export const locale = $state({ value: initial() });

export function setLocale(value: 'th' | 'en') {
	locale.value = value;
	try {
		localStorage.setItem(KEY, value);
	} catch {
		// Private windows and blocked storage: the choice just is not remembered.
	}
}

export const t = (th: string, en: string) => (locale.value === 'th' ? th : en);
