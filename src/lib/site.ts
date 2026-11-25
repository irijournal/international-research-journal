import settings from '../data/settings.json';

/** Fields the CMS removes from settings.json when they are saved empty. */
type OptionalSettings = {
  issnOnline?: string;
  phone?: string;
  web3formsKey?: string;
  googleFormUrl?: string;
  googleSiteVerification?: string;
  callForPapersDeadline?: string;
  bingSiteVerification?: string;
};

export const site: typeof settings & OptionalSettings = settings;

type MailKey = keyof typeof settings.emailLocalParts;

/** Builds an address from the single domain field in settings.json. */
export function mail(key: MailKey): string {
  return `${settings.emailLocalParts[key]}@${settings.domain}`;
}

export const fullJournalName = site.journalTitle.trim();

/** Where "Submit" buttons go: the online submission form when set, otherwise the guidelines page. */
export const submitUrl = site.googleFormUrl || '/submission-guidelines';
export const submitIsExternal = submitUrl.startsWith('http');

export function issnLine(): string {
  return site.issnOnline ? `ISSN (Online): ${site.issnOnline}` : 'ISSN (Online): Applied for';
}

/** The bibliographic line every issue and article carries: volume, issue, month and year. */
export function issueLabel(issue: { volume: number; number: number; month?: string; period: string; year: number }): string {
  return `Vol. ${issue.volume}, Issue ${issue.number}, ${issue.month ?? issue.period} ${issue.year}`;
}

/** Sorts by an "order" field first, then alphabetically by a given key. */
export function byOrder<T extends { data: { order?: number } }>(a: T, b: T): number {
  return (a.data.order ?? 50) - (b.data.order ?? 50);
}

/** Shortens text to a search-snippet length at a word boundary. */
export function snippet(text: string, max = 158): string {
  const clean = text.replace(/\s+/g, ' ').trim();
  if (clean.length <= max) return clean;
  return clean.slice(0, clean.lastIndexOf(' ', max - 1)).replace(/[,;:.]$/, '') + '…';
}
