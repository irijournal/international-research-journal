import settings from '../data/settings.json';

export const site = settings;

type MailKey = keyof typeof settings.emailLocalParts;

/** Builds an address from the single domain field in settings.json. */
export function mail(key: MailKey): string {
  return `${settings.emailLocalParts[key]}@${settings.domain}`;
}

export const fullJournalName = `${settings.journalTitle}: ${settings.journalSubtitle}`;

export function issnLine(): string {
  return settings.issnOnline ? `ISSN (Online): ${settings.issnOnline}` : 'ISSN: application in process';
}

/** Sorts by an "order" field first, then alphabetically by a given key. */
export function byOrder<T extends { data: { order?: number } }>(a: T, b: T): number {
  return (a.data.order ?? 50) - (b.data.order ?? 50);
}
