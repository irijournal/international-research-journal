#!/usr/bin/env python3
"""Brand kit: business cards, the journal letterhead, the call-for-papers poster and social media images.

Usage: BRANDKIT_OUT=/some/dir PLAYWRIGHT_MODULE=/path/to/node_modules/playwright/index.mjs python3 make.py
Inputs come from ../vol1-issue1/brand (logo) and ../vol1-issue1/out (issue cover).
"""
import json, os, subprocess
import numpy as np
import qrcode
from docx import Document
from docx.enum.text import WD_TAB_ALIGNMENT
from docx.shared import Mm, Pt
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ISSUE = os.path.join(HERE, '..', 'vol1-issue1')
ROOT = os.environ['BRANDKIT_OUT']
A, OUT, HT = (os.path.join(ROOT, d) for d in ('assets', 'out', 'html'))
for d in (A, HT, *(os.path.join(OUT, x) for x in ('cards', 'letterheads', 'poster', 'social'))):
    os.makedirs(d, exist_ok=True)

J = {
    'title': 'International Research Insights: Multidisciplinary e-Journal',
    'web': 'www.internationalresearchinsights.com',
    'info': 'info@internationalresearchinsights.com',
    'submit': 'submissions@internationalresearchinsights.com',
    'issn': 'ISSN (Online): 2839-7134',
    'publisher': 'International Research Insights Editorial Board',
    'pub_addr': '85, Aath Visha, Kanasil, Tehsil Saipau, Dholpur, Rajasthan 328027, India',
    'office': 'B1 FS Plaza, Jagat Farm, Greater Noida, Uttar Pradesh, India',
}
PEOPLE = [
    {'key': 'ravi-kumar', 'name': 'Dr. Ravi Kumar', 'role': 'Editor-in-Chief', 'qual': 'Ph.D. (Law)',
     'aff': 'Head of Department, Indraprastha Law College, Greater Noida',
     'email': 'drravi.tyagi@internationalresearchinsights.com', 'orcid': '0000-0002-4288-7928'},
    {'key': 'ramavatar-singh-tyagi', 'name': 'Dr. Ramavatar Singh Tyagi', 'role': 'Managing Editor',
     'qual': 'Ph.D. (Nursing)', 'aff': 'Vice Principal, Department of Nursing, J.S. University, Shikohabad',
     'email': 'drram.tyagi@internationalresearchinsights.com', 'orcid': '0009-0006-5571-8345'},
]
SECTIONS = ['Law and Constitutional Studies', 'Health and Nursing Sciences', 'Hindi Language and Literature',
            'History, Heritage and Culture', 'Education and Pedagogy', 'Society, Economy and Public Policy',
            'Science, Technology and Environment']
ARTICLES = [('A Quinquennial Empirical Analysis of Case Pendency in Indian High Courts', 'Dr. Ravi Kumar'),
            ("Beyond the Ballot: M. N. Roy's Theory of Organised Democracy", 'Puru Sharma'),
            ('Level of Stress among B.Sc. Nursing Students, Guwahati', 'Jaiprakash Tyagi'),
            ('Patient Safety: Knowledge, Skills and Practice of Nursing Students', 'Dr. Ramavatar Singh Tyagi'),
            ('Neuropsychiatric Disorders: A Comprehensive Overview', 'Akhileshar Prasad Mishra')]


# ------------------------------------------------------------------ assets
def prepare_assets():
    brand = os.path.join(ISSUE, 'brand')
    for src, dst in (('emblem-transparent.png', 'emblem-white.png'), ('logo-full-transparent.png', 'logo-white.png')):
        a = np.array(Image.open(os.path.join(brand, src)).convert('RGBA'))
        a[:, :, 0:3] = 255
        Image.fromarray(a).save(os.path.join(A, dst))
    for f in ('emblem.png', 'logo-full.png', 'emblem-transparent.png', 'logo-full-transparent.png'):
        Image.open(os.path.join(brand, f)).save(os.path.join(A, f))
    Image.open(os.path.join(ISSUE, 'out', 'cover.png')).save(os.path.join(A, 'cover.png'))
    for url, name in (('https://internationalresearchinsights.com', 'qr-website.png'),
                      ('https://internationalresearchinsights.com/submission-guidelines', 'qr-submit.png')):
        q = qrcode.QRCode(border=1, box_size=20, error_correction=qrcode.constants.ERROR_CORRECT_M)
        q.add_data(url)
        q.make(fit=True)
        q.make_image(fill_color='#0a1f44', back_color='white').convert('RGB').save(os.path.join(A, name))


ICON = {
    'mail': '<path d="M3 6h18v12H3z"/><path d="M3 7l9 6 9-6"/>',
    'web': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/>',
    'pin': '<path d="M12 21s-7-6.5-7-12a7 7 0 0 1 14 0c0 5.5-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
    'id': '<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="11" r="2.2"/><path d="M6 16c.8-1.6 5.2-1.6 6 0M14 10h4M14 13h4"/>',
}


def icon(name):
    return ('<svg viewBox="0 0 24 24" width="3.2mm" height="3.2mm" fill="none" stroke="#0050a4" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</svg>')


BASE_CSS = """
* { box-sizing:border-box; margin:0; padding:0; }
html { -webkit-print-color-adjust:exact; print-color-adjust:exact; }
body { font-family:'Inter','Carlito',sans-serif; color:#1f2a3d; }
.serif { font-family:'Caladea','Liberation Serif',serif; }
"""


def write(name, body, css, page=''):
    path = os.path.join(HT, name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><style>{BASE_CSS}{page}{css}</style>'
                f'</head><body>{body}</body></html>')
    return path


jobs = []

# ------------------------------------------------------------------ business cards (85 x 55 mm + 3 mm bleed)
CARD_CSS = """
.card { width:91mm; height:61mm; position:relative; overflow:hidden; page-break-after:always; }
.front { background:linear-gradient(135deg,#0a1f44 0%,#0f2f63 70%,#123a7a 100%); color:#fff; }
.front .ring { position:absolute; border-radius:50%; border:6mm solid rgba(61,142,240,.10); }
.front .r1 { width:70mm; height:70mm; right:-28mm; top:-30mm; }
.front .r2 { width:46mm; height:46mm; left:-20mm; bottom:-22mm; border-width:4mm; border-color:rgba(255,255,255,.06); }
.front .frame { position:absolute; left:7mm; top:7mm; right:7mm; bottom:7mm; border:.35mm solid rgba(255,255,255,.35); border-radius:2mm; }
.front .inner { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; }
.front img { height:19mm; margin-bottom:2.2mm; }
.front .n1 { font-family:'Caladea',serif; font-size:3.2mm; letter-spacing:.55mm; text-transform:uppercase; }
.front .n2 { font-family:'Caladea',serif; font-size:5.6mm; font-weight:700; letter-spacing:.3mm; line-height:1.05; margin-top:.4mm; }
.front .n3 { font-size:2.3mm; color:#9fc3f5; letter-spacing:.45mm; margin-top:1.4mm; }
.front .n4 { font-size:1.9mm; color:rgba(255,255,255,.75); margin-top:1.2mm; letter-spacing:.2mm; }
.back { background:#fff; }
.back .bar { position:absolute; left:0; top:0; bottom:0; width:9mm; background:#0a1f44; }
.back .bar2 { position:absolute; left:9mm; top:0; bottom:0; width:1.2mm; background:#3d8ef0; }
.back .wm { position:absolute; right:-9mm; bottom:-10mm; width:42mm; opacity:.06; }
.back .body { position:absolute; left:15mm; top:9.5mm; right:7mm; bottom:7mm; }
.back .head { margin-right:18mm; }
.back .name { font-family:'Caladea',serif; font-size:4.3mm; font-weight:700; color:#0a1f44; line-height:1.1; }
.back .role { font-size:2.25mm; font-weight:700; color:#0050a4; letter-spacing:.45mm; text-transform:uppercase; margin-top:1.1mm; }
.back .aff { font-size:1.95mm; color:#5b6472; margin-top:.9mm; line-height:1.35; }
.back .rule { width:12mm; height:.45mm; background:#0050a4; margin:2.4mm 0 2.2mm; }
.back .row { display:flex; align-items:center; gap:1.6mm; font-size:1.95mm; color:#1f2a3d; margin-bottom:1.15mm; white-space:nowrap; }
.back .qr { position:absolute; right:7mm; top:9.5mm; width:15mm; text-align:center; }
.back .qr img { width:15mm; height:15mm; display:block; }
.back .qr span { display:block; font-size:1.45mm; color:#5b6472; margin-top:.6mm; letter-spacing:.1mm; }
.back .jn { position:absolute; right:7mm; bottom:6.2mm; font-family:'Caladea',serif; font-size:1.9mm; color:#0a1f44; text-align:right; line-height:1.3; }
"""
PREVIEW_CSS = """
body { background:#dfe5ee; width:1200px; height:860px; display:flex; flex-direction:column; align-items:center; justify-content:center; }
.trim { width:85mm; height:55mm; overflow:hidden; border-radius:3mm; box-shadow:0 18px 40px rgba(10,31,68,.28); transform:scale(1.55); transform-origin:center; }
.trim .card { margin:-3mm 0 0 -3mm; }
"""


def card_front():
    return (f'<div class="card front"><div class="ring r1"></div><div class="ring r2"></div><div class="frame"></div>'
            f'<div class="inner"><img src="{A}/emblem-white.png" alt=""><div class="n1">International</div>'
            f'<div class="n2">Research Insights</div><div class="n3">MULTIDISCIPLINARY e-JOURNAL</div>'
            f'<div class="n4">Peer-reviewed · Open Access · Online · ISSN 2839-7134</div></div></div>')


def card_back(p):
    return f"""<div class="card back"><div class="bar"></div><div class="bar2"></div>
<img class="wm" src="{A}/emblem-transparent.png" alt="">
<div class="body"><div class="head"><div class="name">{p['name']}</div><div class="role">{p['role']}</div>
<div class="aff">{p['qual']} · {p['aff']}</div></div><div class="rule"></div>
<div class="row">{icon('mail')}<span>{p['email']}</span></div>
<div class="row">{icon('web')}<span>{J['web']}</span></div>
<div class="row">{icon('pin')}<span>{J['office'].replace(', Uttar Pradesh, India', ', U.P.')}</span></div>
<div class="row">{icon('id')}<span>ORCID {p['orcid']}</span></div></div>
<div class="qr"><img src="{A}/qr-website.png" alt=""><span>Scan to visit</span></div>
<div class="jn">International Research Insights<br>Multidisciplinary e-Journal<br>{J['issn']}</div></div>"""


# ------------------------------------------------------------------ letterhead (A4, one for the journal)
LH_CSS = """
.page { width:210mm; height:297mm; position:relative; overflow:hidden; background:#fff; }
.topband { position:absolute; left:0; right:0; top:0; height:4mm; background:#0a1f44; }
.topband2 { position:absolute; left:0; right:0; top:4mm; height:1.2mm; background:#3d8ef0; }
.wm { position:absolute; left:50%; top:52%; width:120mm; transform:translate(-50%,-50%); opacity:.045; }
.head { position:absolute; left:18mm; right:18mm; top:11mm; }
.hrow { display:flex; align-items:center; gap:6mm; }
.hrow img { height:23mm; }
.hdiv { width:.4mm; align-self:stretch; background:#c9d4e5; }
.htext .t { font-family:'Caladea',serif; font-weight:700; font-size:14.5pt; color:#0a1f44; line-height:1.15; }
.htext .d { font-size:8.6pt; color:#5b6472; margin-top:1.2mm; letter-spacing:.02em; }
.htext .c { font-size:8.6pt; color:#0050a4; margin-top:.9mm; }
.rules { margin-top:4mm; border-top:1.6pt solid #0a1f44; border-bottom:.5pt solid #3d8ef0; height:1.4mm; }
.refline { position:absolute; left:18mm; right:18mm; top:52mm; display:flex; justify-content:space-between; font-size:10pt; }
.foot { position:absolute; left:18mm; right:18mm; bottom:11mm; border-top:.6pt solid #3d8ef0; padding-top:2.4mm;
  display:grid; grid-template-columns:1.25fr 1fr .9fr; gap:5mm; font-size:7.4pt; color:#5b6472; line-height:1.4; }
.foot b { color:#0a1f44; display:block; font-size:7.6pt; letter-spacing:.06em; text-transform:uppercase; }
.botband { position:absolute; left:0; right:0; bottom:0; height:5mm; background:#0a1f44; }
"""


def lh_head():
    return f"""<div class="head"><div class="hrow"><img src="{A}/logo-full-transparent.png" alt=""><div class="hdiv"></div>
<div class="htext"><div class="t">International Research Insights:<br>Multidisciplinary e-Journal</div>
<div class="d">Peer-reviewed · Open Access · Quarterly · Online</div>
<div class="d" style="margin-top:.4mm;color:#0a1f44;font-weight:600">{J['issn']}</div>
<div class="c">{J['web']}<br>{J['info']}</div></div></div><div class="rules"></div></div>"""


def lh_foot():
    return f"""<div class="foot"><div><b>Publisher</b>{J['publisher']}<br>{J['pub_addr']}</div>
<div><b>Editorial office</b>{J['office']}</div><div><b>Contact</b>{J['web']}<br>{J['info']}</div></div>"""


# ------------------------------------------------------------------ poster (A3)
POSTER_CSS = """
.p { width:297mm; height:420mm; position:relative; overflow:hidden; background:#fff; }
.hero { position:absolute; left:0; right:0; top:0; height:178mm; background:linear-gradient(150deg,#0a1f44 0%,#0f2f63 60%,#164089 100%); color:#fff; }
.c1 { position:absolute; width:230mm; height:230mm; right:-90mm; top:-110mm; border-radius:50%; border:22mm solid rgba(61,142,240,.12); }
.c2 { position:absolute; width:140mm; height:140mm; left:-60mm; top:95mm; border-radius:50%; border:14mm solid rgba(255,255,255,.05); }
.hero .logo { position:absolute; left:22mm; top:20mm; height:52mm; }
.hero .cfp { position:absolute; left:22mm; top:88mm; font-family:'Caladea',serif; font-weight:700; font-size:58pt; letter-spacing:4pt; line-height:1; }
.hero .iss { position:absolute; left:22mm; top:118mm; font-size:17pt; color:#9fc3f5; letter-spacing:1.5pt; }
.hero .inv { position:absolute; left:22mm; right:22mm; top:136mm; font-size:13pt; line-height:1.5; color:rgba(255,255,255,.88); }
.wave { position:absolute; left:0; right:0; top:170mm; height:16mm; background:#fff; border-radius:50% 50% 0 0 / 100% 100% 0 0; }
.sec { position:absolute; left:22mm; right:22mm; top:194mm; }
.h { font-size:10.5pt; font-weight:700; color:#0050a4; letter-spacing:2.4pt; text-transform:uppercase; margin-bottom:5mm; }
.grid { display:grid; grid-template-columns:1fr 1fr; gap:3.4mm 8mm; }
.chip { font-family:'Caladea',serif; font-size:14pt; color:#0a1f44; padding:3mm 4mm; background:#eef3fa; border-left:2mm solid #0050a4; }
.feat { position:absolute; left:22mm; right:22mm; top:276mm; display:grid; grid-template-columns:repeat(5,1fr); gap:4mm; }
.f { border:.5mm solid #c9d4e5; border-top:2mm solid #0a1f44; padding:4mm 3mm; text-align:center; }
.f b { display:block; font-family:'Caladea',serif; font-size:13pt; color:#0a1f44; }
.f span { display:block; font-size:9pt; color:#5b6472; margin-top:1mm; }
.sub { position:absolute; left:22mm; right:22mm; top:316mm; display:flex; gap:9mm; align-items:center; background:#0a1f44; color:#fff; padding:8mm 9mm; border-radius:3mm; }
.sub img { width:38mm; height:38mm; border:2mm solid #fff; border-radius:1.5mm; }
.sub .t1 { font-size:10pt; letter-spacing:2.4pt; text-transform:uppercase; color:#9fc3f5; font-weight:700; }
.sub .t2 { font-family:'Caladea',serif; font-size:20pt; font-weight:700; margin-top:2mm; }
.sub .t3 { font-size:11.5pt; margin-top:2.5mm; color:rgba(255,255,255,.85); line-height:1.5; }
.eds { position:absolute; left:22mm; right:22mm; top:375mm; display:flex; justify-content:space-between; font-size:10.5pt; }
.eds b { display:block; font-family:'Caladea',serif; font-size:13pt; color:#0a1f44; }
.eds span { font-size:8.5pt; color:#0050a4; letter-spacing:1.6pt; text-transform:uppercase; font-weight:700; }
.pf { position:absolute; left:0; right:0; bottom:0; height:16mm; background:#eef3fa; display:flex; align-items:center; justify-content:center; font-size:9pt; color:#5b6472; }
"""


def poster():
    chips = ''.join(f'<div class="chip">{s}</div>' for s in SECTIONS)
    return f"""<div class="p"><div class="hero"><div class="c1"></div><div class="c2"></div>
<img class="logo" src="{A}/logo-white.png" alt=""><div class="cfp">CALL FOR PAPERS</div>
<div class="iss">VOLUME 1 · ISSUE 2 · OCTOBER–DECEMBER 2026</div>
<div class="inv">{J['title']} invites original research articles, review articles, case comments, short communications
and book reviews in English and Hindi.</div></div><div class="wave"></div>
<div class="sec"><div class="h">Research sections</div><div class="grid">{chips}
<div class="chip" style="background:#0050a4;color:#fff;border-left-color:#0a1f44">Interdisciplinary work welcome</div></div></div>
<div class="feat"><div class="f"><b>Double anonymous</b><span>peer review</span></div><div class="f"><b>Quarterly</b><span>Mar · Jun · Sep · Dec</span></div>
<div class="f"><b>Online</b><span>open access</span></div><div class="f"><b>Bilingual</b><span>Hindi and English</span></div>
<div class="f"><b>Written reply</b><span>to every submission</span></div></div>
<div class="sub"><img src="{A}/qr-submit.png" alt=""><div><div class="t1">Submit your manuscript</div>
<div class="t2">{J['submit']}</div><div class="t3">Guidelines: {J['web']}/submission-guidelines<br>{J['issn']}</div></div></div>
<div class="eds"><div><span>Editor-in-Chief</span><b>{PEOPLE[0]['name']}</b>{PEOPLE[0]['qual']}</div>
<div style="text-align:right"><span>Managing Editor</span><b>{PEOPLE[1]['name']}</b>{PEOPLE[1]['qual']}</div></div>
<div class="pf"><span>Published by {J['publisher']}, {J['pub_addr']}</span></div></div>"""


# ------------------------------------------------------------------ social media images
SOC_CSS = """
.navy { background:linear-gradient(140deg,#0a1f44 0%,#0f2f63 65%,#164089 100%); color:#fff; position:relative; overflow:hidden; }
.ring { position:absolute; border-radius:50%; }
ol li { counter-increment:a; padding:16px 0 16px 64px; border-top:1px solid rgba(255,255,255,.18); position:relative; }
ol li:before { content:counter(a,decimal-leading-zero); position:absolute; left:0; top:16px; font:700 28px Caladea; color:#3d8ef0; }
ol li b { display:block; font:700 27px Caladea; line-height:1.25; } ol li span { display:block; font-size:20px; color:#9fc3f5; margin-top:4px; }
"""


def tile(title, sub):
    return (f'<div style="border:2px solid #c9d4e5;border-top:8px solid #0a1f44;padding:14px 8px">'
            f'<div style="font:700 26px Caladea;color:#0a1f44">{title}</div>'
            f'<div style="font-size:18px;color:#5b6472;margin-top:4px">{sub}</div></div>')


def social():
    items = ''.join(f'<li><b>{t}</b><span>{a}</span></li>' for t, a in ARTICLES)
    chips = ''.join(f'<div style="padding:16px 22px;background:#eef3fa;border-left:10px solid #0050a4;font:700 27px Caladea;'
                    f'color:#0a1f44">{s}</div>' for s in SECTIONS)
    return {
        'profile-picture-1080': (1080, 1080, f'<div style="width:1080px;height:1080px;background:#fff;display:flex;'
                                 f'align-items:center;justify-content:center"><img src="{A}/emblem.png" style="height:720px"></div>'),
        'facebook-cover-1640x624': (1640, 624, f"""<div class="navy" style="width:1640px;height:624px">
<div class="ring" style="width:760px;height:760px;right:-260px;top:-300px;border:70px solid rgba(61,142,240,.12)"></div>
<div class="ring" style="width:420px;height:420px;left:-170px;bottom:-230px;border:40px solid rgba(255,255,255,.05)"></div>
<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;gap:56px">
<img src="{A}/logo-white.png" style="height:300px"><div style="width:2px;height:240px;background:rgba(255,255,255,.3)"></div>
<div><div class="serif" style="font-size:44px;font-weight:700">Peer-reviewed research,<br>open to every reader.</div>
<div style="font-size:22px;color:#9fc3f5;margin-top:18px;letter-spacing:.08em">QUARTERLY · ONLINE · {J['issn'].upper()}</div>
<div style="font-size:22px;margin-top:14px">{J['web']}</div></div></div></div>"""),
        'linkedin-banner-1128x191': (1128, 191, f"""<div class="navy" style="width:1128px;height:191px">
<div class="ring" style="width:420px;height:420px;right:-120px;top:-170px;border:46px solid rgba(61,142,240,.13)"></div>
<div style="position:absolute;left:300px;right:40px;top:0;bottom:0;display:flex;align-items:center;justify-content:space-between">
<div><div class="serif" style="font-size:30px;font-weight:700">{J['title']}</div>
<div style="font-size:16px;color:#9fc3f5;margin-top:8px;letter-spacing:.08em">PEER-REVIEWED · OPEN ACCESS · ISSN 2839-7134</div></div>
<div style="font-size:15px;text-align:right">{J['web']}</div></div></div>"""),
        'instagram-post-issue1-1080x1350': (1080, 1350, f"""<div class="navy" style="width:1080px;height:1350px">
<div class="ring" style="width:900px;height:900px;right:-420px;top:-380px;border:80px solid rgba(61,142,240,.12)"></div>
<img src="{A}/logo-white.png" style="position:absolute;left:70px;top:70px;height:150px">
<div style="position:absolute;left:70px;top:270px;font-size:24px;letter-spacing:.16em;color:#9fc3f5;font-weight:700">NOW ONLINE</div>
<div class="serif" style="position:absolute;left:70px;top:310px;font-size:76px;font-weight:700;line-height:1.05">Volume 1<br>Issue 1</div>
<div style="position:absolute;left:70px;top:480px;font-size:26px;color:rgba(255,255,255,.85)">July–September 2026 · {J['issn']}</div>
<img src="{A}/cover.png" style="position:absolute;right:70px;top:270px;width:300px;border:6px solid #fff;box-shadow:0 20px 50px rgba(0,0,0,.35)">
<ol style="position:absolute;left:70px;right:70px;top:720px;list-style:none;counter-reset:a">{items}</ol>
<div style="position:absolute;left:70px;right:70px;bottom:60px;display:flex;justify-content:space-between;font-size:24px">
<span>Read: {J['web']}</span><span style="color:#9fc3f5">Open Access</span></div></div>"""),
        'instagram-post-call-for-papers-1080x1350': (1080, 1350, f"""<div style="width:1080px;height:1350px;background:#fff;position:relative;overflow:hidden">
<div class="navy" style="position:absolute;left:0;right:0;top:0;height:520px">
<div class="ring" style="width:700px;height:700px;right:-300px;top:-320px;border:70px solid rgba(61,142,240,.12)"></div>
<img src="{A}/logo-white.png" style="position:absolute;left:70px;top:60px;height:130px">
<div class="serif" style="position:absolute;left:70px;top:240px;font-size:84px;font-weight:700;letter-spacing:4px">CALL FOR PAPERS</div>
<div style="position:absolute;left:70px;top:350px;font-size:28px;color:#9fc3f5;letter-spacing:.1em">VOLUME 1 · ISSUE 2 · OCT–DEC 2026</div>
<div style="position:absolute;left:70px;right:70px;top:405px;font-size:24px;color:rgba(255,255,255,.85);line-height:1.45">Research articles, reviews, case comments and short communications in English and Hindi</div></div>
<div style="position:absolute;left:70px;right:70px;top:565px;display:grid;grid-template-columns:1fr 1fr;gap:14px 22px">{chips}
<div style="padding:16px 22px;background:#0050a4;border-left:10px solid #0a1f44;font:700 27px Caladea;color:#fff">Interdisciplinary work welcome</div></div>
<div style="position:absolute;left:70px;right:70px;top:965px;display:grid;grid-template-columns:repeat(3,1fr);gap:18px;text-align:center">
{tile('Quarterly', 'Mar · Jun · Sep · Dec')}{tile('Bilingual', 'Hindi and English')}{tile('ISSN 2839-7134', 'Online')}</div>
<div style="position:absolute;left:70px;right:70px;bottom:60px;display:flex;gap:34px;align-items:center;background:#0a1f44;color:#fff;padding:30px 34px;border-radius:14px">
<img src="{A}/qr-submit.png" style="width:150px;height:150px;border:8px solid #fff;border-radius:6px">
<div><div style="font-size:20px;letter-spacing:.14em;color:#9fc3f5;font-weight:700">SUBMIT YOUR MANUSCRIPT</div>
<div class="serif" style="font-size:31px;font-weight:700;margin-top:10px">{J['submit']}</div>
<div style="font-size:21px;margin-top:10px;color:rgba(255,255,255,.85)">Double anonymous peer review · {J['web']}</div></div></div></div>"""),
    }


def letterhead_docx():
    doc = Document()
    st = doc.styles['Normal']
    st.font.name, st.font.size = 'Calibri', Pt(11)
    s = doc.sections[0]
    s.page_width, s.page_height = Mm(210), Mm(297)
    s.left_margin = s.right_margin = Mm(18)
    s.header_distance, s.top_margin, s.footer_distance, s.bottom_margin = Mm(9), Mm(50), Mm(8), Mm(32)
    s.header.paragraphs[0].add_run().add_picture(os.path.join(HT, 'lh-head.png'), width=Mm(174))
    s.footer.paragraphs[0].add_run().add_picture(os.path.join(HT, 'lh-foot.png'), width=Mm(174))
    p = doc.add_paragraph()
    p.paragraph_format.tab_stops.add_tab_stop(Mm(174), WD_TAB_ALIGNMENT.RIGHT)
    p.add_run('Ref. No.: ____________________\tDate: ____________________')
    for t in ('', 'To,', '', 'Subject: ', '', 'Dear Sir/Madam,', ''):
        doc.add_paragraph(t)
    doc.save(os.path.join(OUT, 'letterheads', 'letterhead-journal.docx'))


def main():
    prepare_assets()
    for p in PEOPLE:
        html = write(f"card-{p['key']}.html", card_front() + card_back(p), CARD_CSS, '@page { size:91mm 61mm; margin:0; }')
        jobs.append({'html': html, 'pdf': f"{OUT}/cards/business-card-{p['key']}-print.pdf"})
        prev = write(f"card-{p['key']}-preview.html",
                     f'<div class="trim">{card_front()}</div><div class="trim" style="margin-top:120px">{card_back(p)}</div>',
                     CARD_CSS + PREVIEW_CSS)
        jobs.append({'html': prev, 'png': f"{OUT}/cards/business-card-{p['key']}-preview.png", 'w': 1200, 'h': 860, 'scale': 2})

    body = (f'<div class="page"><div class="topband"></div><div class="topband2"></div>'
            f'<img class="wm" src="{A}/emblem-transparent.png" alt="">{lh_head()}'
            f'<div class="refline"><span>Ref. No.: ____________________</span><span>Date: ____________________</span></div>'
            f'{lh_foot()}<div class="botband"></div></div>')
    html = write('letterhead.html', body, LH_CSS, '@page { size:A4; margin:0; }')
    jobs.append({'html': html, 'pdf': f'{OUT}/letterheads/letterhead-journal.pdf'})
    jobs.append({'html': html, 'png': f'{OUT}/letterheads/letterhead-journal-preview.png', 'w': 794, 'h': 1123, 'scale': 1.5})
    head = lh_head().replace('class="head"', 'class="head" style="left:0;right:0;top:0"')
    foot = lh_foot().replace('class="foot"', 'class="foot" style="left:0;right:0;bottom:auto;top:0"')
    parts = write('lhparts.html', f'<div id="h" style="position:relative;width:174mm;height:36mm">{head}</div>'
                  f'<div id="f" style="position:relative;width:174mm;height:17mm;margin-top:10mm">{foot}</div>',
                  LH_CSS, 'body{width:180mm;background:#fff}')
    jobs.append({'html': parts, 'sel': '#h', 'selpng': f'{HT}/lh-head.png', 'w': 700, 'h': 400, 'scale': 4})
    jobs.append({'html': parts, 'sel': '#f', 'selpng': f'{HT}/lh-foot.png', 'w': 700, 'h': 400, 'scale': 4})

    html = write('poster.html', poster(), POSTER_CSS, '@page { size:297mm 420mm; margin:0; }')
    jobs.append({'html': html, 'pdf': f'{OUT}/poster/poster-call-for-papers-A3.pdf'})
    jobs.append({'html': html, 'png': f'{OUT}/poster/poster-call-for-papers-preview.png', 'w': 1123, 'h': 1588, 'scale': 1.4})

    for name, (w, h, body) in social().items():
        html = write(f'social-{name}.html', body, SOC_CSS, f'@page {{ size:{w}px {h}px; margin:0; }} body{{width:{w}px;height:{h}px}}')
        jobs.append({'html': html, 'png': f'{OUT}/social/{name}.png', 'w': w, 'h': h, 'scale': 1 if w > 1000 else 2})

    subprocess.run(['node', os.path.join(HERE, 'render.mjs'), json.dumps(jobs)], check=True)
    letterhead_docx()
    print('rendered', len(jobs), 'into', OUT)


if __name__ == '__main__':
    main()
