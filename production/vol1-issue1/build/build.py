#!/usr/bin/env python3
"""Typesets Volume 1, Issue 1: article PDFs, front matter and the full issue PDF.

HTML is printed by Chromium (print.mjs); running heads, footers and page numbers are
stamped afterwards with reportlab so numbering runs continuously through the issue.
"""
import glob, html, io, json, os, re, subprocess, sys
import yaml
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

ISSUE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ISSUE, 'build')
OUT = os.path.join(ISSUE, 'out')
TMP = os.path.join(BUILD, 'tmp')
REPO = '/home/user/international-research-journal'
os.makedirs(os.path.join(OUT, 'articles'), exist_ok=True)
os.makedirs(TMP, exist_ok=True)

CFG = yaml.safe_load(open(os.path.join(ISSUE, 'issue.yaml')))
J, I, NX, B = CFG['journal'], CFG['issue'], CFG['next_issue'], CFG['brand']
ISSN = J.get('issn_online') and f"ISSN (Online): {J['issn_online']}" or J.get('issn_display_when_empty', '')
E = html.escape


def font_path(name):
    out = subprocess.run(['fc-match', '-f', '%{file}', name], capture_output=True, text=True).stdout
    return out


for alias, name in [('Serif', 'Liberation Serif'), ('Serif-Bold', 'Liberation Serif:bold'),
                    ('Serif-Italic', 'Liberation Serif:italic'), ('Serif-BoldItalic', 'Liberation Serif:bold:italic')]:
    pdfmetrics.registerFont(TTFont(alias, font_path(name)))

NAVY, BLUE, GREY = HexColor(B['navy']), HexColor(B['blue']), HexColor(B['grey'])


# ----------------------------------------------------------------------------- helpers

def read_front_matter(path):
    text = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', text, re.S)
    return yaml.safe_load(m.group(1)), m.group(2)


def md_to_html(md, cwd=None):
    r = subprocess.run(['pandoc', '--from', 'markdown+implicit_figures+pipe_tables+grid_tables+superscript-yaml_metadata_block',
                        '--to', 'html5', '--section-divs', '--wrap=none'],
                       input=md, capture_output=True, text=True, cwd=cwd)
    if r.returncode:
        sys.exit(r.stderr)
    return r.stdout


def inline_md(text):
    return md_to_html(text).strip()


def print_pdfs(jobs):
    subprocess.run(['node', os.path.join(BUILD, 'print.mjs'), json.dumps(jobs)], check=True)


def page_count(pdf):
    return len(PdfReader(pdf).pages)


def roman(n):
    vals = [(10, 'x'), (9, 'ix'), (5, 'v'), (4, 'iv'), (1, 'i')]
    s = ''
    for v, r in vals:
        while n >= v:
            s += r
            n -= v
    return s


def join_authors(names):
    return names[0] if len(names) == 1 else ', '.join(names[:-1]) + ' & ' + names[-1]


def plain_name(name):
    return re.sub(r'^(Dr\.|Prof\.|Professor \(Dr\.\)|Professor)\s+', '', name)


def citation(meta, first, last):
    names = join_authors([a['name'] for a in meta['authors']])
    return (f"{names} ({I['year']}). {meta['title']}. <i>{J['title']}</i>, {I['label']}, pp. {first}–{last}. "
            f"{J['website']}/articles/{meta['slug']}")


def write(path, text):
    open(path, 'w', encoding='utf-8').write(text)
    return path


CSS = open(os.path.join(BUILD, 'style.css'), encoding='utf-8').read()


def page_html(body, cls=''):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>x</title>
<style>{CSS}</style></head><body class="{cls}">{body}</body></html>"""


# ----------------------------------------------------------------------------- papers

papers = []
for a in CFG['articles']:
    path = os.path.join(ISSUE, 'papers', a['slug'], 'paper.md')
    if not os.path.exists(path):
        print('missing paper', a['slug'])
        continue
    meta, body = read_front_matter(path)
    meta['slug'] = a['slug']
    meta['article_type'] = a['article_type']
    meta['section'] = a['section']
    papers.append({'meta': meta, 'body': body, 'dir': os.path.dirname(path)})


# ----------------------------------------------------------------------------- cover

def cover_html():
    items = ''.join(
        f"<li><span class='ct'>{E(p['meta']['title'])}</span><span class='ca'>{E(join_authors([x['name'] for x in p['meta']['authors']]))}</span></li>"
        for p in papers)
    return page_html(f"""
<div class="cover">
  <div class="cover-issn">{E(ISSN)}</div>
  <img class="cover-logo" src="{ISSUE}/{B['logo_full']}" alt="">
  <div class="cover-title">{E(J['title'])}</div>
  <div class="cover-desc">{E(J['descriptor'])} · Quarterly</div>
  <div class="cover-band">
    <div class="cover-issue">Volume {I['volume']} · Issue {I['number']} · {E(I['period'].replace(' to ', '–'))} {I['year']}</div>
  </div>
  <div class="cover-inside">
    <div class="cover-h">In this issue</div>
    <ol>{items}</ol>
  </div>
  <div class="cover-foot">
    <div><b>Published by</b> {E(J['publisher'])}</div>
    <div>{E(J['publisher_address'])}</div>
    <div class="cover-web">{E(J['website_display'])} · {E(J['email_general'])}</div>
  </div>
</div>""", 'cover-page')


# ----------------------------------------------------------------------------- front matter

def board_members():
    out = []
    for f in glob.glob(os.path.join(REPO, 'src/content/board/*.md')):
        m, _ = read_front_matter(f)
        out.append(m)
    return sorted(out, key=lambda m: m.get('order', 50))


def front_html(page_ranges, starts=('i', 'ii', 'iii', 'iv')):
    rows = [('Title', J['title']), ('Type of publication', 'Journal (peer-reviewed, academic)'),
            ('Subject', J['subject']), ('Frequency', J['frequency']), ('Language', J['languages']),
            ('Format of publication', J['format']), ('Starting year', str(J['starting_year'])),
            ('ISSN', ISSN or '—'), ('Publisher', J['publisher']), ("Publisher's address", J['publisher_address']),
            ('Place of publication', J['place_of_publication'])]
    board = board_members()
    eic = next((m for m in board if m['role'] == 'Editor in Chief'), None)
    if eic:
        rows.append(('Editor in Chief', f"{eic['name']}, {eic['designation']}, {eic.get('institution', '')}"))
    rows += [('Website', J['website']), ('General enquiries', J['email_general']),
             ('Manuscript submissions', J['email_submissions']), ('Review model', J['review_model']),
             ('Access', J['access_model']), ('Licence', J['licence']), ('This issue', f"{I['label_long']}"),
             ('Published online', I['published_online'])]
    info = ''.join(f"<tr><th>{E(k)}</th><td>{E(v)}</td></tr>" for k, v in rows)
    imprint = f"""
<section class="fm">
  <h1 class="fm-h">Journal Information</h1>
  <table class="info">{info}</table>
  <p class="small"><b>Disclaimer.</b> The views and opinions expressed in the articles are those of the authors and do not
  necessarily reflect those of the editorial board or the publisher. The authors are responsible for the accuracy of the
  facts, data and references in their articles.</p>
  <p class="small"><b>Copyright and licence.</b> © {I['year']} The Author(s). All articles in this issue are published open
  access under the {E(J['licence'])}, which permits use, sharing and adaptation in any medium provided the original work
  is properly cited. The journal charges no submission, processing or publication fee.</p>
</section>"""

    def member(m):
        lines = [f"<div class='bm-role'>{E(m['role'])}</div>", f"<div class='bm-name'>{E(m['name'])}</div>"]
        for key in ('qualification', 'designation', 'department', 'institution', 'address', 'country'):
            if m.get(key):
                lines.append(f"<div>{E(str(m[key]))}</div>")
        if m.get('email'):
            lines.append(f"<div>E-mail: {E(m['email'])}</div>")
        if m.get('profileUrl'):
            lines.append(f"<div>Profile: {E(m['profileUrl'])}</div>")
        if m.get('orcid'):
            lines.append(f"<div>ORCID: {E(m['orcid'])}</div>")
        return f"<div class='bm'>{''.join(lines)}</div>"

    groups = ''
    for g in ['Editorial Leadership', 'Editorial Board Members', 'Advisory Board']:
        ms = [m for m in board if m.get('roleGroup') == g]
        if ms:
            groups += f"<h2 class='fm-h2'>{E(g)}</h2><div class='bgrid'>{''.join(member(m) for m in ms)}</div>"
    board_page = f"<section class='fm'><h1 class='fm-h'>Editorial Board</h1>{groups}</section>"

    trs = ''.join(
        f"<tr><td class='c'>{i:02d}</td><td><b>{E(p['meta']['title'])}</b></td>"
        f"<td>{E(join_authors([x['name'] for x in p['meta']['authors']]))}</td>"
        f"<td>{E(p['meta']['section'])}<br><i>{E(p['meta']['article_type'])}</i></td>"
        f"<td class='c'>{page_ranges[p['meta']['slug']][0]}–{page_ranges[p['meta']['slug']][1]}</td></tr>"
        for i, p in enumerate(papers, 1))
    contents = f"""
<section class="fm">
  <h1 class="fm-h">Contents</h1>
  <p class="fm-sub">{E(J['title'])} · {E(I['label_long'])}</p>
  <table class="toc"><thead><tr><th>S.No.</th><th>Title</th><th>Author(s)</th><th>Section / Type</th><th>Page No.</th></tr></thead>
  <tbody>
  <tr><td class='c'>—</td><td>Journal Information</td><td>Journal</td><td>Front matter</td><td class='c'>{starts[0]}</td></tr>
  <tr><td class='c'>—</td><td>Editorial Board</td><td>Journal</td><td>Front matter</td><td class='c'>{starts[1]}</td></tr>
  <tr><td class='c'>—</td><td>Contents</td><td>Journal</td><td>Front matter</td><td class='c'>{starts[2]}</td></tr>
  <tr><td class='c'>—</td><td>Editorial: {{EDTITLE}}</td><td>{{EDAUTHOR}}</td><td>Editorial</td><td class='c'>{{EDPAGE}}</td></tr>
  {trs}
  </tbody></table>
</section>"""

    em, ebody = read_front_matter(os.path.join(REPO, 'src/content/issues/volume-1-issue-1.md'))
    ebody = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', ebody)
    editorial = f"""
<section class="fm editorial">
  <h1 class="fm-h">Editorial</h1>
  <h2 class="ed-title">{E(em['editorialTitle'])}</h2>
  <p class="ed-author">{E(em['editorialAuthor'])}</p>
  <div class="ed-body">{md_to_html(ebody)}</div>
</section>"""
    contents = (contents.replace('{EDTITLE}', E(em['editorialTitle']))
                .replace('{EDAUTHOR}', E(em['editorialAuthor'].split(',')[0])).replace('{EDPAGE}', starts[3]))
    return [imprint, board_page, contents, editorial]


# ----------------------------------------------------------------------------- articles

def article_html(p, first=None, last=None):
    m = p['meta']
    aff_ids = [a['id'] for a in m.get('affiliations', [])]
    multi = len(aff_ids) > 1
    authors = []
    for a in m['authors']:
        sup = ','.join(a.get('affiliations', [])) if multi or True else ''
        star = '*' if a.get('corresponding') else ''
        authors.append(f"{E(a['name'])}<sup>{E(sup)}{star}</sup>")
    affs = ''.join(f"<div><sup>{E(x['id'])}</sup>{E(x['text'])}</div>" for x in m.get('affiliations', []))
    kws = ', '.join(E(k) for k in m.get('keywords', []))
    abstract = md_to_html(m.get('abstract', ''))
    corr = next((a for a in m['authors'] if a.get('corresponding')), m['authors'][0])
    if corr.get('email'):
        contact = f"<b>*Corresponding author:</b> {E(corr['name'])}, e-mail: {E(corr['email'])}"
        if corr.get('orcid'):
            contact += f" · ORCID: {E(corr['orcid'])}"
    else:
        contact = (f"<b>*Corresponding author:</b> {E(corr['name'])}. Correspondence through the editorial office: "
                   f"{E(J['email_editor'])}")
    dates = []
    if m.get('received'):
        dates.append(f"Received: {E(m['received'])}")
    if m.get('accepted'):
        dates.append(f"Accepted: {E(m['accepted'])}")
    dates.append(f"Published online: {E(I['published_online'])}")
    body = md_to_html(p['body'], cwd=p['dir'])
    body = re.sub(r'src="(fig/[^"]+)"', lambda mm: f'src="{p["dir"]}/{mm.group(1)}"', body)
    # wide tables span both columns
    def widen(mm):
        t = mm.group(0)
        head = re.search(r'<tr[^>]*>(.*?)</tr>', t, re.S)
        cols = len(re.findall(r'<t[hd]', head.group(1))) if head else 0
        return f'<div class="tbl{" wide" if cols >= 5 else ""}">{t}</div>'
    body = re.sub(r'<table.*?</table>', widen, body, flags=re.S)
    cite = citation(m, first or '?', last or '?')
    cite_box = f'<div class="cite"><b>How to cite this article:</b> {cite}</div>'
    if '<section id="references"' in body:
        body = body.replace('<section id="references"', cite_box + '<section id="references"', 1)
    else:
        body += cite_box
    return page_html(f"""
<header class="jhead">
  <img class="emblem" src="{ISSUE}/{B['emblem']}" alt="">
  <div class="jbox">
    <div class="jname">{E(J['title_main'])}</div>
    <div class="jsub">{E(J['subtitle'])}</div>
    <div class="jmeta">(Peer-reviewed · Open Access · Online)</div>
    <div class="jmeta">Journal home page: <b>{E(J['website_display'])}</b></div>
    <div class="jmeta">{E(ISSN)}{' · ' if ISSN else ''}<span class="jissue">{E(I['label'])}</span></div>
  </div>
  <img class="thumb" src="{OUT}/cover-thumb.png" alt="">
</header>
<div class="rule"></div>
<div class="atype">{E(m['article_type'])} · {E(m['section'])}</div>
<h1 class="title">{E(m['title'])}</h1>
<div class="authors">{', '.join(authors)}</div>
<div class="affs">{affs}</div>
<table class="kwabs"><thead><tr><th class="kw">KEYWORDS</th><th>ABSTRACT</th></tr></thead>
<tbody><tr><td class="kw">{kws}</td><td class="abs">{abstract}</td></tr></tbody></table>
<div class="ainfo">{contact}<br>{' · '.join(dates)} · © {I['year']} The Author(s). Published by {E(J['publisher'])}.
Open access under the CC BY 4.0 licence. {E(J['website'])}/articles/{E(m['slug'])}</div>
<div class="body">{body}<div class="end">* * * * *</div></div>
""", 'article')


# ----------------------------------------------------------------------------- stamping

def stamp(src_pdf, dst_pdf, numbers, header=None, skip_header_first=True):
    """numbers: list of page labels (str or None) for each page; header: (left, right) running head."""
    reader = PdfReader(src_pdf)
    writer = PdfWriter()
    for i, pg in enumerate(reader.pages):
        w, h = float(pg.mediabox.width), float(pg.mediabox.height)
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=(w, h))
        mx = 16 * 72 / 25.4
        if header and not (skip_header_first and i == 0):
            c.setFont('Serif-Italic', 8.5)
            c.setFillColor(BLUE)
            c.drawString(mx, h - 34, header[0])
            c.drawRightString(w - mx, h - 34, header[1])
            c.setStrokeColor(HexColor(B['line']))
            c.setLineWidth(0.6)
            c.line(mx, h - 39, w - mx, h - 39)
        if numbers[i] is not None:
            c.setStrokeColor(HexColor(B['line']))
            c.setLineWidth(0.6)
            c.line(mx, 40, w - mx, 40)
            c.setFillColor(NAVY)
            c.setFont('Serif-BoldItalic', 8)
            c.drawString(mx, 28, J['title'])
            c.drawRightString(w - mx, 28, I['label'])
            c.setFont('Serif-Bold', 9)
            c.drawCentredString(w / 2, 14, str(numbers[i]))
        c.save()
        buf.seek(0)
        pg.merge_page(PdfReader(buf).pages[0])
        writer.add_page(pg)
    return writer


def finish(writer, path, title, author, keywords=''):
    writer.add_metadata({'/Title': title, '/Author': author, '/Keywords': keywords,
                         '/Subject': f"{J['title']}, {I['label']}", '/Creator': J['title']})
    with open(path, 'wb') as f:
        writer.write(f)


# ----------------------------------------------------------------------------- build

def main():
    # 1. cover (needs only titles), then cover images used inside the articles
    cover_pdf = os.path.join(TMP, 'cover.pdf')
    print_pdfs([[write(os.path.join(TMP, 'cover.html'), cover_html()), cover_pdf]])
    subprocess.run(['pdftoppm', '-png', '-r', '150', '-singlefile', cover_pdf, os.path.join(OUT, 'cover')], check=True)
    subprocess.run(['pdftoppm', '-png', '-r', '40', '-singlefile', cover_pdf, os.path.join(OUT, 'cover-thumb')], check=True)

    # 2. articles (first pass to count pages, second with page numbers in the citation)
    raw = {}
    jobs = []
    for p in papers:
        s = p['meta']['slug']
        raw[s] = os.path.join(TMP, f'{s}.pdf')
        jobs.append([write(os.path.join(TMP, f'{s}.html'), article_html(p)), raw[s]])
    print_pdfs(jobs)
    ranges, n = {}, 1
    for p in papers:
        s = p['meta']['slug']
        k = page_count(raw[s])
        ranges[s] = (n, n + k - 1)
        n += k
    jobs = [[write(os.path.join(TMP, f"{p['meta']['slug']}.html"), article_html(p, *ranges[p['meta']['slug']])),
             raw[p['meta']['slug']]] for p in papers]
    print_pdfs(jobs)
    for p in papers:  # citation text could change the page count; it must not
        s = p['meta']['slug']
        assert page_count(raw[s]) == ranges[s][1] - ranges[s][0] + 1, f'page count changed for {s}'

    # 3. front matter (one PDF per section so each starts on a new page)
    fm_parts = front_html(ranges)
    print_pdfs([[write(os.path.join(TMP, f'fm{i}.html'), page_html(part, 'front')), os.path.join(TMP, f'fm{i}.pdf')]
                for i, part in enumerate(fm_parts)])
    starts, r = [], 1
    for i in range(len(fm_parts)):
        starts.append(roman(r))
        r += page_count(os.path.join(TMP, f'fm{i}.pdf'))
    fm_parts = front_html(ranges, starts)
    fm_pdfs = []
    jobs = []
    for i, part in enumerate(fm_parts):
        pdf = os.path.join(TMP, f'fm{i}.pdf')
        jobs.append([write(os.path.join(TMP, f'fm{i}.html'), page_html(part, 'front')), pdf])
        fm_pdfs.append(pdf)
    cfp = f"""
<section class="fm cfp">
  <h1 class="fm-h">Call for Papers</h1>
  <p class="fm-sub">Volume {NX['volume']}, Issue {NX['number']} · {E(NX['period'])} {NX['year']}</p>
  <p>{E(J['title'])} invites original research articles, review articles, case comments, short communications and
  book reviews in English and Hindi across law, health and nursing sciences, Hindi language and literature, history,
  education, society, economy, public policy, science, technology and environment.</p>
  <table class="info">
   <tr><th>Last date for submission</th><td>{E(NX['submission_deadline'])}</td></tr>
   <tr><th>Publication</th><td>{E(NX['publication_date'])}</td></tr>
   <tr><th>Send manuscripts to</th><td>{E(J['email_submissions'])}</td></tr>
   <tr><th>Guidelines</th><td>{E(J['website'])}/submission-guidelines</td></tr>
   <tr><th>Charges</th><td>None. No submission, processing or publication fee.</td></tr>
   <tr><th>Review</th><td>{E(J['review_model'])}</td></tr>
  </table>
</section>"""
    back = f"""
<div class="back">
  <img class="back-logo" src="{ISSUE}/{B['logo_full']}" alt="">
  <div class="back-title">{E(J['title'])}</div>
  <div class="back-line">{E(J['descriptor'])} · Quarterly · {E(J['languages'])}</div>
  <div class="back-addr"><b>{E(J['publisher'])}</b><br>{E(J['publisher_address'])}<br>{E(J['website_display'])} · {E(J['email_general'])}</div>
</div>"""
    cfp_pdf, back_pdf = os.path.join(TMP, 'cfp.pdf'), os.path.join(TMP, 'back.pdf')
    jobs += [[write(os.path.join(TMP, 'cfp.html'), page_html(cfp, 'front')), cfp_pdf],
             [write(os.path.join(TMP, 'back.html'), page_html(back, 'cover-page')), back_pdf]]
    print_pdfs(jobs)

    # 4. stamp and assemble
    full = PdfWriter()
    full.append(PdfReader(cover_pdf))
    r = 1
    for pdf in fm_pdfs:
        k = page_count(pdf)
        wtr = stamp(pdf, None, [roman(r + j) for j in range(k)])
        for pg in wtr.pages:
            full.add_page(pg)
        r += k
    pages = {'full_issue': I['full_issue_pdf_name'], 'front_matter_pages': r - 1}
    for p in papers:
        m, s = p['meta'], p['meta']['slug']
        a, z = ranges[s]
        names = join_authors([plain_name(x['name']) for x in m['authors']])
        wtr = stamp(raw[s], None, list(range(a, z + 1)), header=(names, m.get('short_title', m['title'])))
        finish(wtr, os.path.join(OUT, 'articles', f'{s}.pdf'), m['title'],
               ', '.join(x['name'] for x in m['authors']), ', '.join(m.get('keywords', [])))
        for pg in PdfReader(os.path.join(OUT, 'articles', f'{s}.pdf')).pages:
            full.add_page(pg)
        pages[s] = {'first': a, 'last': z, 'pdf': f'articles/{s}.pdf'}
    last = ranges[papers[-1]['meta']['slug']][1]
    wtr = stamp(cfp_pdf, None, [last + 1 + j for j in range(page_count(cfp_pdf))])
    for pg in wtr.pages:
        full.add_page(pg)
    full.append(PdfReader(back_pdf))
    finish(full, os.path.join(OUT, I['full_issue_pdf_name']), f"{J['title']}, {I['label']}", J['publisher'])
    json.dump(pages, open(os.path.join(OUT, 'pages.json'), 'w'), indent=2)
    print(json.dumps(pages, indent=2))


if __name__ == '__main__':
    main()
