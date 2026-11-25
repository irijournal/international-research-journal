"""LinkedIn kit: call-for-papers posters, page cover, profile banner and five posts.

Writes HTML files plus manifest.json into $LINKEDIN_OUT; render.mjs turns them into PNGs.
Style follows the website: navy, EB Garamond, uppercase letterspaced labels.
"""
import json
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.environ.get('LINKEDIN_OUT', os.path.join(REPO, 'production', 'brand-kit', 'out-linkedin'))
IMG = os.path.join(REPO, 'public', 'images')
UP = os.path.join(REPO, 'public', 'uploads', 'vol1-issue1')
os.makedirs(OUT, exist_ok=True)

SITE = 'internationalresearchinsights.com'
EMAIL = 'submissions@internationalresearchinsights.com'
FORM = 'forms.gle/3C8Ksvb4vjYAdRey5'
FORM_URL = 'https://' + FORM
ISSN = '2839-7134'
SECTIONS = [
    'Law and Constitutional Studies',
    'Health and Nursing Sciences',
    'Hindi Language and Literature',
    'History, Heritage and Culture',
    'Education and Pedagogy',
    'Society, Economy and Public Policy',
    'Science, Technology and Environment',
]
SECTIONS_HI = [
    'विधि एवं संवैधानिक अध्ययन',
    'स्वास्थ्य एवं नर्सिंग विज्ञान',
    'हिंदी भाषा एवं साहित्य',
    'इतिहास, विरासत एवं संस्कृति',
    'शिक्षा एवं शिक्षाशास्त्र',
    'समाज, अर्थव्यवस्था एवं लोक नीति',
    'विज्ञान, प्रौद्योगिकी एवं पर्यावरण',
]

WAVES = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='1200' height='1350' viewBox='0 0 1200 1350' preserveAspectRatio='none'%3E"
         "%3Cg fill='none' stroke='%23ffffff' stroke-opacity='0.06' stroke-width='1.5'%3E"
         "%3Cpath d='M-100 1050C250 880 520 1180 840 960S1150 760 1300 860'/%3E"
         "%3Cpath d='M-100 1100C250 930 520 1230 840 1010S1150 810 1300 910'/%3E"
         "%3Cpath d='M-100 1150C250 980 520 1280 840 1060S1150 860 1300 960'/%3E"
         "%3Cpath d='M-100 260C320 420 600 120 900 300S1150 520 1300 400'/%3E"
         "%3Cpath d='M-100 310C320 470 600 170 900 350S1150 570 1300 450'/%3E"
         "%3C/g%3E%3C/svg%3E\")")

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'EB Garamond',Georgia,serif;color:#0e2547;-webkit-font-smoothing:antialiased}
.c{position:relative;overflow:hidden;display:flex;flex-direction:column}
.navy{background:#0e2547;color:#fff}
.paper{background:#f6f8fb}
.waves{background-image:WAVES;background-size:100% 100%}
.hi{font-family:'Noto Serif Devanagari','EB Garamond',serif}
.brand{display:flex;align-items:center;gap:20px;padding:46px 64px 0}
.brand img{height:78px}
.bt{border-left:1.5px solid rgba(255,255,255,.35);padding-left:20px}
.paper .bt{border-color:#c8d3e2}
.bn{font-weight:700;font-size:25px;letter-spacing:.06em;text-transform:uppercase;line-height:1.1}
.bs{font-size:16px;font-weight:600;letter-spacing:.26em;text-transform:uppercase;opacity:.75;margin-top:5px}
.pill{margin-left:auto;border:1.5px solid rgba(255,255,255,.5);border-radius:999px;padding:9px 20px;font-size:17px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;white-space:nowrap}
.paper .pill{border-color:#9fb2cb;color:#34506f}
.body{padding:0 64px;flex:1;display:flex;flex-direction:column}
.eb{display:flex;align-items:center;gap:18px;font-size:21px;font-weight:700;letter-spacing:.26em;text-transform:uppercase;color:#a9c0e0}
.paper .eb{color:#4b6584}
.eb::before{content:'';width:56px;height:1.5px;background:currentColor;flex:none}
h1{font-weight:500;line-height:1.02;letter-spacing:-.005em}
.it{font-style:italic}
.muted{color:#b9c8dd}
.paper .muted{color:#4b6584}
.panel{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.14);border-radius:10px}
.k{font-size:18px;font-weight:700;letter-spacing:.22em;text-transform:uppercase}
ol.num{list-style:none;counter-reset:n}
ol.num li{counter-increment:n;display:flex;gap:16px;align-items:baseline}
ol.num li::before{content:counter(n,decimal-leading-zero);font-size:.8em;opacity:.6;min-width:1.6em}
.facts{display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid rgba(255,255,255,.25)}
.facts div{padding:22px 22px 0 0}
.facts b{display:block;font-size:44px;font-weight:600;line-height:1}
.facts span{display:block;font-size:21px;line-height:1.3;margin-top:8px;color:#c9d6ea}
.foot{background:#fff;color:#0e2547;padding:30px 64px 36px;display:flex;justify-content:space-between;align-items:flex-end;gap:24px}
.foot .k{color:#4b6584;font-size:16px}
.foot p{font-size:27px;margin-top:6px}
.foot .r{text-align:right}
.navyfoot{background:#16335a;color:#fff}
.navyfoot .k{color:#a9c0e0}
.paper .navy .eb{color:#a9c0e0}
.paper .navy .pill{border-color:rgba(255,255,255,.5);color:#fff}
.paper .navy .bt{border-color:rgba(255,255,255,.35)}
.qr{width:150px;height:150px;flex:none;margin-left:22px}
.foot .r.withqr{display:flex;align-items:flex-end;gap:0}
"""

FONTS = ('<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500'
         '&family=Noto+Serif+Devanagari:wght@400;500;600;700&display=swap" rel="stylesheet">')


def page(name, w, h, body, extra=''):
    html = (f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{CSS.replace("WAVES", WAVES)}'
            f'body{{width:{w}px;height:{h}px}} .c{{width:{w}px;height:{h}px}} {extra}</style></head>'
            f'<body>{body}</body></html>')
    path = os.path.join(OUT, f'{name}.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return {'html': path, 'png': os.path.join(OUT, f'{name}.png'), 'w': w, 'h': h}


def brand(dark=True):
    img = 'emblem-white.png' if dark else 'emblem.png'
    return (f'<div class="brand"><img src="file://{IMG}/{img}" alt="">'
            '<div class="bt"><div class="bn">International Research Insights</div>'
            '<div class="bs">Multidisciplinary e-Journal</div></div>'
            f'<div class="pill">ISSN {ISSN}</div></div>')


def foot(left_k, left, right_k, right, navy=False):
    cls = 'foot navyfoot' if navy else 'foot'
    return (f'<div class="{cls}"><div><div class="k">{left_k}</div><p>{left}</p></div>'
            f'<div class="r"><div class="k">{right_k}</div><p>{right}</p></div></div>')


def qrfoot(k, link, sub):
    return (f'<div class="foot"><div><div class="k">{k}</div><p style="font-size:34px">{link}</p>'
            f'<p style="font-size:21px;color:#4b6584;margin-top:8px">{sub}</p></div>'
            f'<img class="qr" src="file://{OUT}/form-qr.png" alt=""></div>')


import qrcode  # noqa: E402
qrcode.make(FORM_URL, border=1, box_size=10, error_correction=qrcode.constants.ERROR_CORRECT_M).save(os.path.join(OUT, 'form-qr.png'))

jobs = []

# 1. Call for papers, portrait (detailed)
sections = ''.join(f'<li>{s}</li>' for s in SECTIONS)
jobs.append(page('01-cfp-vol2-issue1-portrait', 1080, 1350, f"""
<div class="c navy waves">
  {brand()}
  <div class="body" style="padding-top:64px">
    <div class="eb">Call for papers · Submissions open</div>
    <h1 style="font-size:104px;margin-top:22px">Volume 2, Issue 1</h1>
    <p class="it" style="font-size:40px;margin-top:10px">January–March 2027 <span class="muted" style="font-style:normal">· published March 2027</span></p>
    <div class="panel" style="margin-top:40px;padding:30px 34px">
      <div class="k" style="color:#a9c0e0">Seven research sections</div>
      <ol class="num" style="columns:2;column-gap:36px;font-size:29px;line-height:1.25;margin-top:18px">{sections.replace('<li>', '<li style="break-inside:avoid;margin-bottom:12px">')}</ol>
      <p style="font-size:22px;margin-top:6px" class="muted">Research articles · Review articles · Case comments · Short communications · Book reviews</p>
    </div>
    <div class="facts" style="margin-top:38px">
      <div><b>2</b><span>reviewers, double anonymous peer review</span></div>
      <div><b>7</b><span>working days to a written first response</span></div>
      <div><b>2</b><span>languages: English and Hindi</span></div>
    </div>
    <p style="font-size:23px;margin-top:30px;color:#dbe5f3">Processing charges apply <b>only after acceptance</b>. Nothing at submission, nothing on rejection.</p>
  </div>
  {qrfoot('Submit your manuscript online', FORM, 'Guidelines: ' + SITE)}
</div>"""))

# 2. Call for papers, square (short)
jobs.append(page('02-cfp-vol2-issue1-square', 1080, 1080, f"""
<div class="c navy waves">
  {brand()}
  <div class="body" style="justify-content:center">
    <div class="eb">Volume 2 · Issue 1 · January–March 2027</div>
    <h1 style="font-size:150px;margin-top:22px;font-weight:500">Call for<br>Papers</h1>
    <p class="it" style="font-size:38px;margin-top:22px">Rigorous Research. Fair Review. Open to Every Reader.</p>
    <p style="font-size:26px;margin-top:26px;color:#c9d6ea;letter-spacing:.02em">All seven sections · English and Hindi · Double anonymous peer review</p>
  </div>
  {foot('Submit online', FORM, 'Read the guidelines', SITE)}
</div>"""))

# 3. Call for papers, Hindi
sections_hi = ''.join(f'<li style="break-inside:avoid;margin-bottom:12px">{s}</li>' for s in SECTIONS_HI)
jobs.append(page('03-cfp-vol2-issue1-hindi', 1080, 1350, f"""
<div class="c navy waves">
  {brand()}
  <div class="body hi" style="padding-top:60px">
    <div class="eb hi" style="letter-spacing:.06em;font-size:26px">शोध-पत्र आमंत्रण · प्रविष्टियाँ खुली हैं</div>
    <h1 class="hi" style="font-size:92px;margin-top:22px;line-height:1.2">खंड 2, अंक 1</h1>
    <p style="font-size:36px;margin-top:6px">जनवरी–मार्च 2027 <span class="muted">· प्रकाशन मार्च 2027</span></p>
    <div class="panel" style="margin-top:36px;padding:28px 34px">
      <div style="font-size:24px;font-weight:600;color:#a9c0e0">सात शोध खंड</div>
      <ol class="num" style="columns:2;column-gap:36px;font-size:26px;line-height:1.45;margin-top:14px">{sections_hi}</ol>
    </div>
    <div class="facts" style="margin-top:34px">
      <div><b>2</b><span class="hi" style="font-size:21px">समीक्षक, दोहरी अनाम सहकर्मी समीक्षा</span></div>
      <div><b>7</b><span class="hi" style="font-size:21px">कार्यदिवसों में लिखित उत्तर</span></div>
      <div><b>2</b><span class="hi" style="font-size:21px">भाषाएँ: हिंदी और अंग्रेज़ी</span></div>
    </div>
    <p style="font-size:24px;margin-top:28px;color:#dbe5f3">प्रकाशन शुल्क <b>केवल स्वीकृति के बाद</b>। जमा करते समय या अस्वीकृति पर कोई शुल्क नहीं।</p>
  </div>
  <div class="foot hi"><div><div class="k" style="letter-spacing:.04em;font-size:22px">ऑनलाइन शोध-पत्र जमा करें</div><p style="font-family:'EB Garamond',serif;font-size:32px">{FORM}</p>
  <p style="font-size:20px;color:#4b6584;margin-top:8px">दिशानिर्देश: <span style="font-family:'EB Garamond',serif">{SITE}</span></p></div>
  <img class="qr" src="file://{OUT}/form-qr.png" alt=""></div>
</div>"""))

# 4. LinkedIn company page cover (1128 x 191). Left part stays clear for the logo overlay.
jobs.append(page('04-linkedin-page-cover-1128x191', 1128, 191, f"""
<div class="c navy waves" style="flex-direction:row;align-items:center;justify-content:flex-end;padding:0 46px 0 330px">
  <div style="text-align:right">
    <div style="font-size:12.5px;font-weight:700;letter-spacing:.3em;text-transform:uppercase;color:#a9c0e0">International Research Insights · Multidisciplinary e-Journal</div>
    <div class="it" style="font-size:33px;margin-top:8px;line-height:1.1">Rigorous Research. Fair Review. Open to Every Reader.</div>
    <div style="font-size:14.5px;letter-spacing:.14em;text-transform:uppercase;margin-top:12px;color:#dbe5f3">ISSN (Online) {ISSN} · Peer reviewed · Open access · English &amp; Hindi</div>
  </div>
</div>"""))

# 5. Personal profile banner for editors (1584 x 396). Left part stays clear for the profile photo.
jobs.append(page('05-linkedin-profile-banner-1584x396', 1584, 396, f"""
<div class="c navy waves" style="flex-direction:row;align-items:center;justify-content:flex-end;padding:0 70px 0 440px;gap:44px">
  <div style="text-align:right">
    <div style="font-size:17px;font-weight:700;letter-spacing:.3em;text-transform:uppercase;color:#a9c0e0">Multidisciplinary e-Journal · ISSN (Online) {ISSN}</div>
    <div style="font-size:40px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;margin-top:12px;white-space:nowrap">International Research Insights</div>
    <div class="it" style="font-size:32px;margin-top:8px;white-space:nowrap">Rigorous Research. Fair Review. Open to Every Reader.</div>
    <div style="font-size:18px;letter-spacing:.16em;text-transform:uppercase;margin-top:16px;color:#dbe5f3">Call for papers open · {SITE}</div>
  </div>
  <img src="file://{IMG}/emblem-white.png" style="height:190px;flex:none" alt="">
</div>"""))

# 6. Post: Volume 1, Issue 1 is out
articles = [
    ('A Quinquennial Empirical Analysis of Case Pendency in Indian High Courts', 'Dr. Ravi Kumar', 'Law'),
    ("Beyond the Ballot: M. N. Roy's Theory of Organised Democracy", 'Puru Sharma', 'Political theory'),
    ('Level of Stress among B.Sc. Nursing Students, Guwahati', 'Jaiprakash Tyagi', 'Nursing'),
    ('Knowledge, Skills and Practice of Patient Safety among Nursing Students', 'Dr. Ramavatar Singh Tyagi', 'Nursing'),
    ('Neuropsychiatric Disorders: A Comprehensive Overview', 'Akhileshar Prasad Mishra', 'Health sciences'),
]
rows = ''.join(
    f'<li style="padding:20px 0;border-bottom:1px solid #d6dee9"><div><div style="font-size:30px;line-height:1.2">{t}</div>'
    f'<div style="font-size:22px;color:#4b6584;margin-top:5px">{a} · {s}</div></div></li>'
    for t, a, s in articles)
jobs.append(page('06-post-issue1-published', 1080, 1350, f"""
<div class="c paper">
  <div class="navy waves" style="padding-bottom:40px;position:relative">
    {brand()}
    <div style="display:flex;gap:44px;padding:44px 64px 0;align-items:flex-end">
      <div style="flex:1">
        <div class="eb">Now published · free to read</div>
        <h1 style="font-size:84px;margin-top:20px">Volume 1,<br>Issue 1</h1>
        <p class="it" style="font-size:36px;margin-top:10px">September 2026 · five peer-reviewed articles</p>
      </div>
      <img src="file://{UP}/cover.png" style="width:250px;border:6px solid #fff;box-shadow:0 18px 40px rgba(0,0,0,.35);margin-bottom:-90px" alt="">
    </div>
  </div>
  <div class="body" style="padding-top:54px">
    <div class="k" style="color:#4b6584;font-size:16px">In this issue</div>
    <ol class="num" style="margin-top:4px">{rows}</ol>
  </div>
  {foot('Read every article free', SITE + '/current', 'ISSN (Online)', ISSN, navy=True)}
</div>"""))


def spotlight(name, section, hook, title, author, pages, points):
    items = ''.join(
        f'<li style="padding:26px 0;border-top:1px solid #d6dee9;font-size:32px;line-height:1.32"><div><b style="font-weight:600">{h}</b> {t}</div></li>'
        for h, t in points)
    return page(name, 1080, 1350, f"""
<div class="c paper">
  <div class="navy waves" style="padding-bottom:46px">
    {brand()}
    <div style="padding:46px 64px 0">
      <div class="eb">Research spotlight · {section}</div>
      <h1 style="font-size:76px;margin-top:20px">{hook}</h1>
    </div>
  </div>
  <div class="body" style="padding-top:34px">
    <p class="it" style="font-size:29px;line-height:1.3;color:#34506f">“{title}”</p>
    <p style="font-size:22px;margin-top:10px;color:#4b6584">{author} · Vol. 1, Issue 1, September 2026 · pp. {pages}</p>
    <div class="k" style="color:#4b6584;font-size:16px;margin-top:30px">What the paper argues</div>
    <ol class="num" style="margin-top:10px">{items}</ol>
  </div>
  {foot('Read the full article free', SITE, 'ISSN (Online)', ISSN, navy=True)}
</div>""")


# 7. Spotlight: case pendency
jobs.append(spotlight(
    '07-post-spotlight-case-pendency', 'Law',
    'Why do cases wait so long in India’s High Courts?',
    'A Quinquennial Empirical Analysis of Case Pendency in Indian High Courts and the Imperative for Expedited Adjudication',
    'Dr. Ravi Kumar', '1–17',
    [('The causes:', 'a rising caseload, unfilled judicial vacancies and too few staff in the higher judiciary.'),
     ('The cost:', 'higher expense and delay for litigants, rights realised late, and in criminal cases, prolonged trials that affect the rights of the accused and victims.'),
     ('The way forward:', 'fill vacancies, case-flow management, fewer adjournments, e-courts and virtual courts, mediation and regular review of pending lists.')]))

# 8. Spotlight: M. N. Roy
jobs.append(spotlight(
    '08-post-spotlight-mn-roy', 'Political Theory',
    'Are elections alone enough for democracy?',
    "Beyond the Ballot: M. N. Roy's Theory of Organised Democracy and the Problem of Popular Sovereignty in India",
    'Puru Sharma', '18–24',
    [('Roy’s answer:', 'no. Power must stay with the people between elections, through citizens taking part in People’s Committees.'),
     ('The test:', 'Roy’s draft Constitution of Free India is read against Carole Pateman’s theory of participatory democracy.'),
     ('The verdict:', 'organised democracy works best as an addition to representative democracy, not a replacement, with open questions on administration, inequality and minority protection.')]))

# 9. Post: write in Hindi (bilingual)
jobs.append(page('09-post-write-in-hindi', 1080, 1350, f"""
<div class="c navy waves">
  {brand()}
  <div class="body" style="padding-top:70px">
    <div class="eb">English and Hindi · every section</div>
    <h1 class="hi" style="font-size:96px;margin-top:26px;line-height:1.25;font-weight:600">हिंदी में लिखिए,<br>दुनिया तक पहुँचिए।</h1>
    <p class="it" style="font-size:44px;margin-top:14px;color:#dbe5f3">Write in Hindi. Be read worldwide.</p>
    <div class="panel" style="margin-top:50px;padding:10px 34px">
      <ol class="num" style="font-size:28px;line-height:1.32">
        <li style="padding:20px 0;border-bottom:1px solid rgba(255,255,255,.14)"><div>Hindi manuscripts are reviewed by <b style="font-weight:600">Hindi-speaking referees</b>.</div></li>
        <li style="padding:20px 0;border-bottom:1px solid rgba(255,255,255,.14)"><div>Published in Hindi, with an <b style="font-weight:600">English title, abstract and keywords</b> so the work can be found and cited internationally.</div></li>
        <li style="padding:20px 0"><div>The editorial office <b style="font-weight:600">helps prepare the English abstract</b> if you ask.</div></li>
      </ol>
    </div>
  </div>
  {foot('Submit for Volume 2, Issue 1', FORM, 'Guidelines', SITE)}
</div>"""))

# 10. Post: five checks before you submit
checks = [
    ('Anonymise the manuscript.', 'No names, no affiliations, no acknowledgements, and clear your name from the file properties.'),
    ('Write an abstract that reports.', 'State the question, the method, the findings and the conclusion, in 150 to 250 words.'),
    ('Match every citation to the reference list.', 'One referencing style, used completely and consistently.'),
    ('Stay within the word limit.', 'Research articles: 4,000 to 8,000 words, excluding references.'),
    ('Sign the declaration.', 'Originality, authorship, permissions and ethics approval, confirmed in writing.'),
]
check_rows = ''.join(
    f'<li style="padding:24px 0;border-top:1px solid #d6dee9;font-size:31px;line-height:1.32"><div><b style="font-weight:600">{h}</b> {t}</div></li>'
    for h, t in checks)
jobs.append(page('10-post-five-checks-before-you-submit', 1080, 1350, f"""
<div class="c paper">
  <div class="navy waves" style="padding-bottom:46px">
    {brand()}
    <div style="padding:46px 64px 0">
      <div class="eb">For authors</div>
      <h1 style="font-size:80px;margin-top:20px">Five checks before you submit</h1>
      <p class="it" style="font-size:31px;margin-top:12px;color:#dbe5f3">Most papers returned without review miss one of these.</p>
    </div>
  </div>
  <div class="body" style="padding-top:24px">
    <ol class="num">{check_rows}</ol>
  </div>
  {foot('Full submission guidelines', SITE + '/submission-guidelines', 'ISSN (Online)', ISSN, navy=True)}
</div>"""))

with open(os.path.join(OUT, 'manifest.json'), 'w') as f:
    json.dump(jobs, f, indent=1)
print(len(jobs), 'pages written to', OUT)
