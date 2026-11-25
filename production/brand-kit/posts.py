#!/usr/bin/env python3
"""Social media posts (1080 x 1350) and certificates of publication.

Usage: BRANDKIT_OUT=/some/dir PLAYWRIGHT_MODULE=/path/to/playwright/index.mjs python3 posts.py
Run make.py once first: it prepares the logo and QR assets this script uses.
"""
import json, os, subprocess
import qrcode
import make
from make import A, HT, J, OUT, SECTIONS, write

POSTS = os.path.join(OUT, 'posts')
CERTS = os.path.join(OUT, 'certificates')
os.makedirs(POSTS, exist_ok=True)
os.makedirs(CERTS, exist_ok=True)

CSS = """
.post { width:1080px; height:1350px; position:relative; overflow:hidden; background:#fff; }
.top { position:absolute; left:0; right:0; top:0; background:linear-gradient(140deg,#0a1f44 0%,#0f2f63 65%,#164089 100%); color:#fff; overflow:hidden; }
.ring { position:absolute; border-radius:50%; border:70px solid rgba(61,142,240,.12); width:700px; height:700px; right:-300px; top:-320px; }
.logo { position:absolute; left:70px; top:56px; height:120px; }
.kicker { position:absolute; left:70px; font-size:22px; letter-spacing:.16em; color:#9fc3f5; font-weight:700; }
.title { position:absolute; left:70px; right:70px; font-family:'Caladea',serif; font-weight:700; line-height:1.08; }
.body { position:absolute; left:70px; right:70px; }
.foot { position:absolute; left:70px; right:70px; bottom:52px; display:flex; justify-content:space-between; align-items:center; font-size:21px; color:#5b6472; border-top:2px solid #c9d4e5; padding-top:20px; }
.foot b { color:#0a1f44; }
.tile { border:2px solid #c9d4e5; border-top:8px solid #0a1f44; padding:22px 24px; }
.tile b { display:block; font:700 30px Caladea; color:#0a1f44; }
.tile span { display:block; font-size:20px; color:#5b6472; margin-top:6px; line-height:1.4; }
.chip { padding:16px 22px; background:#eef3fa; border-left:10px solid #0050a4; font:700 27px Caladea; color:#0a1f44; }
.big { font:700 64px Caladea; color:#0050a4; line-height:1; }
table.fees { width:100%; border-collapse:collapse; font-size:24px; }
table.fees th { background:#0a1f44; color:#fff; text-align:left; padding:16px 18px; font-size:20px; letter-spacing:.05em; }
table.fees td { padding:18px; border-bottom:2px solid #c9d4e5; color:#1f2a3d; }
table.fees td.r { font:700 30px Caladea; color:#0a1f44; text-align:right; white-space:nowrap; }
.note { font-size:21px; color:#1f2a3d; line-height:1.5; }
.step { display:flex; gap:26px; align-items:flex-start; padding:20px 0; border-bottom:2px solid #e3e9f2; }
.step .n { width:64px; height:64px; border-radius:50%; background:#0050a4; color:#fff; font:700 30px Caladea; display:flex; align-items:center; justify-content:center; flex:none; }
.step b { display:block; font:700 30px Caladea; color:#0a1f44; } .step span { font-size:21px; color:#5b6472; }
.sub { display:flex; gap:30px; align-items:center; background:#0a1f44; color:#fff; padding:28px 32px; border-radius:14px; }
.sub img { width:140px; height:140px; border:8px solid #fff; border-radius:6px; }
"""


def head(kicker, title, height=470, title_size=70, title_top=240):
    return (f'<div class="top" style="height:{height}px"><div class="ring"></div><img class="logo" src="{A}/logo-white.png">'
            f'<div class="kicker" style="top:{title_top - 44}px">{kicker}</div>'
            f'<div class="title" style="top:{title_top}px;font-size:{title_size}px">{title}</div></div>')


def foot(right=J['issn']):
    return f'<div class="foot"><b>{J["web"]}</b><span>{right}</span></div>'


def submit_box(top):
    return (f'<div class="body" style="top:{top}px"><div class="sub"><img src="{A}/qr-submit.png"><div>'
            f'<div style="font-size:19px;letter-spacing:.14em;color:#9fc3f5;font-weight:700">SUBMIT YOUR MANUSCRIPT</div>'
            f'<div style="font:700 30px Caladea;margin-top:8px">{J["submit"]}</div>'
            f'<div style="font-size:20px;margin-top:8px;color:rgba(255,255,255,.85)">Guidelines: {J["web"]}/submission-guidelines</div>'
            f'</div></div></div>')


chips = ''.join(f'<div class="chip">{s}</div>' for s in SECTIONS)
POST_HTML = {
    '01-call-for-papers-vol2-issue1': head('CALL FOR PAPERS · SUBMISSIONS OPEN', 'Publish in Volume 2, Issue 1<br>(January–March 2027)', 520) + f"""
<div class="body" style="top:560px"><div class="note" style="margin-bottom:22px">Original research articles, review articles, case comments and short communications in English and Hindi, in seven research sections:</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px 18px">{chips}<div class="chip" style="background:#0050a4;color:#fff;border-left-color:#0a1f44">Interdisciplinary work welcome</div></div></div>
{submit_box(1010)}{foot('Processing charges only after acceptance')}""",
    '02-issn-assigned': head('ANNOUNCEMENT', 'Our journal now has an ISSN', 470) + f"""
<div class="body" style="top:560px;text-align:center"><div style="font-size:26px;color:#5b6472;letter-spacing:.12em">ISSN (ONLINE)</div>
<div style="font:700 150px Caladea;color:#0a1f44;letter-spacing:6px;margin-top:10px">2839-7134</div>
<div class="note" style="margin-top:30px">International Research Insights: Multidisciplinary e-Journal is now registered as a serial publication. The ISSN appears on our website and on every article.</div>
<div style="margin-top:40px;display:inline-block;background:#eef3fa;border-left:10px solid #0050a4;padding:20px 30px;font:700 28px Caladea;color:#0a1f44">Volume 1, Issue 1 is online: five peer-reviewed articles</div></div>{foot('Peer-reviewed · Open Access · Quarterly')}""",
    '03-why-publish-with-us': head('WHY PUBLISH WITH US', 'Six reasons authors choose<br>International Research Insights', 470, 60) + f"""
<div class="body" style="top:520px;display:grid;grid-template-columns:1fr 1fr;gap:20px">
<div class="tile"><b>Double anonymous review</b><span>Two reviewers assess every manuscript that passes screening</span></div>
<div class="tile"><b>A written reply</b><span>A first editorial response within seven working days</span></div>
<div class="tile"><b>ISSN 2839-7134</b><span>A registered online serial with stable article pages and PDFs</span></div>
<div class="tile"><b>International board</b><span>Members from India, Nepal, Sri Lanka, Bhutan and the UAE</span></div>
<div class="tile"><b>Open access</b><span>Every published article is free to read and share (CC BY 4.0)</span></div>
<div class="tile"><b>Hindi and English</b><span>Research in either language, in seven research sections</span></div></div>
{submit_box(1010)}{foot()}""",
    '04-how-publication-works': head('HOW IT WORKS', 'From submission to publication<br>in five clear steps', 470, 60) + """
<div class="body" style="top:510px">
<div class="step"><div class="n">1</div><div><b>Submit by e-mail</b><span>Manuscript, title page and author declaration to the submissions address</span></div></div>
<div class="step"><div class="n">2</div><div><b>Editorial screening</b><span>Scope, structure and similarity check, with a written reply within 7 working days</span></div></div>
<div class="step"><div class="n">3</div><div><b>Double anonymous peer review</b><span>Two reviewers, a published rubric, reports shared with the author</span></div></div>
<div class="step"><div class="n">4</div><div><b>Decision and revision</b><span>Accept, revise or decline, always with reasons</span></div></div>
<div class="step" style="border-bottom:0"><div class="n">5</div><div><b>Publication</b><span>Copy edited PDF, article page, citation details and an e-certificate for every author</span></div></div></div>
""" + submit_box(1010) + foot(),
    '05-research-sections': head('SCOPE', 'Seven research sections,<br>one standard of review', 470, 62) + f"""
<div class="body" style="top:520px;display:grid;grid-template-columns:1fr;gap:14px">{chips}</div>{foot()}""",
    '06-processing-charges': head('PROCESSING CHARGES', 'You pay only after your paper<br>is accepted', 470, 60) + f"""
<div class="body" style="top:510px"><table class="fees">
<tr><th>Category</th><th style="text-align:right">Per accepted paper</th></tr>
<tr><td>Single author</td><td class="r">₹1,500</td></tr>
<tr><td>2–3 authors</td><td class="r">₹2,000</td></tr>
<tr><td>Science, technology and health sciences papers</td><td class="r">₹5,000</td></tr>
<tr><td>Authors from outside India: humanities, law, social sciences</td><td class="r">USD 100</td></tr>
<tr><td>Authors from outside India: sciences</td><td class="r">USD 150</td></tr></table>
<div class="note" style="margin-top:30px"><b>No fee</b> at submission, during review or if a paper is not accepted. Every author of a published paper receives an e-certificate of publication.</div></div>{foot()}""",
    '07-international-editorial-board': head('EDITORIAL BOARD', 'An editorial board from<br>five countries', 470, 62) + """
<div class="body" style="top:520px;display:grid;grid-template-columns:repeat(3,1fr);gap:18px;text-align:center">
<div class="tile"><div class="big">11</div><span>board members</span></div>
<div class="tile"><div class="big">5</div><span>countries</span></div>
<div class="tile"><div class="big">6</div><span>members from outside India</span></div></div>
<div class="body note" style="top:760px;line-height:1.7">
<b>India</b> · Indraprastha Law College, J.S. University, ITM University Gwalior, KMGG PG College<br>
<b>Nepal</b> · Pokhara University<br><b>Sri Lanka</b> · University of Peradeniya<br>
<b>Bhutan</b> · Royal University of Bhutan<br><b>United Arab Emirates</b> · University of Dubai</div>
""" + submit_box(1030) + foot('internationalresearchinsights.com/editorial-board'),
}

# ------------------------------------------------------------------ certificates
CERT_CSS = """
.c { width:297mm; height:210mm; position:relative; background:#fff; overflow:hidden; }
.b1 { position:absolute; inset:8mm; border:2.2mm solid #0a1f44; }
.b2 { position:absolute; inset:12mm; border:.5mm solid #3d8ef0; }
.wm { position:absolute; left:50%; top:54%; width:105mm; transform:translate(-50%,-50%); opacity:.05; }
.in { position:absolute; left:24mm; right:24mm; top:18mm; bottom:20mm; text-align:center; }
.in .logo { height:26mm; }
.ct { font-family:'Caladea',serif; font-weight:700; font-size:30pt; color:#0a1f44; letter-spacing:3pt; margin-top:4mm; }
.cs { font-size:10pt; letter-spacing:3pt; color:#0050a4; font-weight:700; margin-top:1mm; }
.tx { font-size:12.5pt; color:#1f2a3d; margin-top:6mm; line-height:1.55; }
.nm { font-family:'Caladea',serif; font-size:24pt; font-weight:700; color:#0a1f44; margin:2mm 0 1mm; border-bottom:.4mm solid #c9d4e5; display:inline-block; padding:0 10mm 1mm; }
.pt { font-family:'Caladea',serif; font-size:15pt; font-style:italic; color:#0a1f44; margin:1mm 18mm 0; line-height:1.3; }
.sig { position:absolute; left:24mm; right:24mm; bottom:22mm; display:flex; justify-content:space-between; align-items:flex-end; }
.sig .s { width:62mm; border-top:.4mm solid #0a1f44; padding-top:1.5mm; font-size:10pt; text-align:center; color:#1f2a3d; }
.sig .s b { display:block; font-family:'Caladea',serif; font-size:11.5pt; color:#0a1f44; }
.sig .q { text-align:center; font-size:8pt; color:#5b6472; }
.sig .q img { width:22mm; height:22mm; display:block; margin:0 auto 1mm; }
.meta { position:absolute; left:0; right:0; bottom:13.5mm; text-align:center; font-size:8.5pt; color:#5b6472; }
"""
PAPERS = [
    ('case-pendency-indian-high-courts', 'Dr. Ravi Kumar',
     'A Quinquennial Empirical Analysis of Case Pendency in Indian High Courts and the Imperative for Expedited Adjudication', '1–17'),
    ('mn-roy-organised-democracy-popular-sovereignty', 'Puru Sharma',
     "Beyond the Ballot: M. N. Roy's Theory of Organised Democracy and the Problem of Popular Sovereignty in India", '18–24'),
    ('stress-among-bsc-nursing-students-guwahati', 'Jaiprakash Tyagi',
     'A Study to Assess the Level of Stress among B.Sc. Nursing Students in a Selected Nursing Institute of Guwahati, Assam', '25–35'),
    ('patient-safety-knowledge-skills-practice-nursing-students', 'Dr. Ramavatar Singh Tyagi',
     'A Study to Assess Knowledge, Skills and Practice Regarding Patient Safety among B.Sc. Nursing Students of Regional College of Nursing, Guwahati, Assam', '36–43'),
    ('neuropsychiatric-disorders-comprehensive-overview', 'Akhileshar Prasad Mishra',
     'Neuropsychiatric Disorders: A Comprehensive Overview', '44–53'),
]
ISSUED = '25 November 2026'


def certificate(no, name, title, pages, url):
    return f"""<div class="c"><div class="b1"></div><div class="b2"></div><img class="wm" src="{A}/emblem-transparent.png">
<div class="in"><img class="logo" src="{A}/logo-full-transparent.png"><div class="ct">CERTIFICATE OF PUBLICATION</div>
<div class="cs">PEER-REVIEWED · OPEN ACCESS · {J['issn'].upper()}</div>
<div class="tx">This is to certify that</div><div class="nm">{name}</div>
<div class="tx" style="margin-top:2mm">has authored the paper titled</div><div class="pt">“{title}”</div>
<div class="tx" style="margin-top:3mm">published in <b>{J['title']}</b>,<br>Volume 1, Issue 1, September 2026, pp. {pages}, after double anonymous peer review.</div></div>
<div class="sig"><div class="s"><b>Dr. Ravi Kumar</b>Editor-in-Chief</div>
<div class="q"><img src="{url}">Verify this publication</div>
<div class="s"><b>Dr. Ramavatar Singh Tyagi</b>Managing Editor</div></div>
<div class="meta">Certificate No. {no} · Issued on {ISSUED} · {J['web']}</div></div>"""


def main():
    make.prepare_assets()
    jobs = []
    for name, body in POST_HTML.items():
        html = write(f'post-{name}.html', f'<div class="post">{body}</div>', CSS, 'body{width:1080px;height:1350px}')
        jobs.append({'html': html, 'png': f'{POSTS}/{name}.png', 'w': 1080, 'h': 1350, 'scale': 1})
    for i, (slug, name, title, pages) in enumerate(PAPERS, 1):
        q = qrcode.QRCode(border=1, box_size=12)
        q.add_data(f'https://internationalresearchinsights.com/articles/{slug}')
        q.make(fit=True)
        qpath = os.path.join(A, f'qr-{slug}.png')
        q.make_image(fill_color='#0a1f44', back_color='white').convert('RGB').save(qpath)
        no = f'IRI/2026/V1I1/{i:02d}'
        html = write(f'cert-{i:02d}.html', certificate(no, name, title, pages, qpath), CERT_CSS,
                     '@page { size:297mm 210mm; margin:0; }')
        jobs.append({'html': html, 'pdf': f'{CERTS}/certificate-{i:02d}-{slug}.pdf'})
        if i == 1:
            jobs.append({'html': html, 'png': f'{CERTS}/certificate-preview.png', 'w': 1123, 'h': 794, 'scale': 1})
    blank = certificate('IRI/____/____/__', '______________________________',
                        '_____________________________________________________________', '____',
                        os.path.join(A, 'qr-website.png'))
    blank = blank.replace('Volume 1, Issue 1, September 2026', 'Volume ___, Issue ___, ____________ 20___').replace(
        f'Issued on {ISSUED}', 'Issued on ____________')
    jobs.append({'html': write('cert-blank.html', blank, CERT_CSS, '@page { size:297mm 210mm; margin:0; }'),
                 'pdf': f'{CERTS}/certificate-template-blank.pdf'})
    subprocess.run(['node', os.path.join(make.HERE, 'render.mjs'), json.dumps(jobs)], check=True)
    print('rendered', len(jobs))


if __name__ == '__main__':
    main()
