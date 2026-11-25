import sys
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

F = 'https://forms.gle/3C8Ksvb4vjYAdRey5'
S = 'internationalresearchinsights.com'
doc = Document()
st = doc.styles['Normal']; st.font.name = 'Georgia'; st.font.size = Pt(11)
NAVY = RGBColor(0x0e, 0x25, 0x47)

def h(text, lvl=1):
    p = doc.add_heading(text, lvl)
    for r in p.runs: r.font.color.rgb = NAVY
def para(text, bold=False, italic=False, size=None):
    p = doc.add_paragraph(); r = p.add_run(text); r.bold = bold; r.italic = italic
    if size: r.font.size = Pt(size)
    return p
def caption(text):
    t = doc.add_table(rows=1, cols=1); t.style = 'Table Grid'
    c = t.rows[0].cells[0]; c.text = ''
    for i, line in enumerate(text.strip('\n').split('\n')):
        p = c.paragraphs[0] if i == 0 else c.add_paragraph()
        p.add_run(line)
    doc.add_paragraph()

h('LinkedIn Kit: International Research Insights', 0)
para('Posters, page cover and ready-to-paste captions. ISSN (Online) 2839-7134.', italic=True)

h('1. Set up the page')
para('Company page cover: upload 04-linkedin-page-cover-1128x191.png (Edit page → Header image). The left side is kept clear because LinkedIn places the logo there.')
para('Editors’ personal profiles: upload 05-linkedin-profile-banner-1584x396.png as the background photo (Edit intro → camera icon on the banner). The left side is kept clear for the profile photo.')
para('Logo for the page: use the emblem from the brand kit (emblem.png).')

h('2. Two-week posting plan')
plan = [
    ('Day 1', '01 Call for papers (portrait)'),
    ('Day 3', '06 Volume 1, Issue 1 is published'),
    ('Day 5', '07 Spotlight: case pendency in High Courts'),
    ('Day 7', '09 Write in Hindi, plus 03 Hindi call for papers in Hindi groups and WhatsApp'),
    ('Day 9', '08 Spotlight: M. N. Roy and organised democracy'),
    ('Day 11', '10 Five checks before you submit'),
    ('Day 14', '02 Call for papers reminder (square)'),
]
t = doc.add_table(rows=1, cols=2); t.style = 'Light Grid Accent 1'
t.rows[0].cells[0].text = 'When'; t.rows[0].cells[1].text = 'Post'
for a, b in plan:
    r = t.add_row().cells; r[0].text = a; r[1].text = b
doc.add_paragraph()

h('3. Tips that raise reach')
for tip in [
    'Post on weekday mornings and reply to every comment in the first hour.',
    'Ask each editor to reshare from their personal profile with one line of their own; personal profiles reach far more people than a page.',
    'Tag the authors in article posts and the board members in board posts.',
    'Many pages put the link in the first comment instead of the post text, because LinkedIn tends to show posts with outside links to fewer people. Try both and compare.',
    'Use three to five hashtags, not more.',
    'Share the call-for-papers posters in research scholar WhatsApp and Telegram groups too, but do not post the same poster in many groups at once.',
]:
    doc.add_paragraph(tip, style='List Bullet')

h('4. Captions (copy and paste)')

posts = [
('01 · Call for papers (portrait)', f'''
Call for Papers: submissions open all year

International Research Insights: Multidisciplinary e-Journal (ISSN 2839-7134) invites original research at any time. There is no deadline: accepted papers are published as soon as they are ready.

What we publish
• Research articles, review articles, case comments, short communications and book reviews
• In English or Hindi
• Across seven sections: Law and Constitutional Studies · Health and Nursing Sciences · Hindi Language and Literature · History, Heritage and Culture · Education and Pedagogy · Society, Economy and Public Policy · Science, Technology and Environment

How we work
✔ Double anonymous peer review by two reviewers
✔ A written first response within 7 working days
✔ Processing charges only after acceptance; nothing at submission or on rejection

Submit online: {F}
Guidelines: {S}/submission-guidelines

Please share this with colleagues and research scholars who are working on a paper.

#CallForPapers #ResearchPaper #AcademicPublishing #ResearchScholar #OpenAccess
'''),
('02 · Call for papers (square)', f'''
Our call for papers is open all year. Send your paper whenever it is ready.

All seven research sections · English and Hindi · Double anonymous peer review · Processing charges only after acceptance.

Submit online: {F}

#CallForPapers #Research #AcademicJournal
'''),
('03 · शोध-पत्र आमंत्रण (Hindi)', f'''
शोध-पत्र आमंत्रण: पूरे वर्ष प्रविष्टियाँ खुली हैं

International Research Insights: Multidisciplinary e-Journal (ISSN 2839-7134) पूरे वर्ष हिंदी और अंग्रेज़ी में मौलिक शोध-पत्र आमंत्रित करता है। कोई अंतिम तिथि नहीं: स्वीकृत शोध-पत्र तैयार होते ही प्रकाशित किए जाते हैं।

• सात शोध खंड: विधि, स्वास्थ्य एवं नर्सिंग, हिंदी भाषा एवं साहित्य, इतिहास, शिक्षा, समाज एवं लोक नीति, विज्ञान एवं पर्यावरण
• दोहरी अनाम सहकर्मी समीक्षा (दो समीक्षक)
• 7 कार्यदिवसों में लिखित उत्तर
• प्रकाशन शुल्क केवल स्वीकृति के बाद; जमा करते समय या अस्वीकृति पर कोई शुल्क नहीं

ऑनलाइन जमा करें: {F}
दिशानिर्देश: {S}/submission-guidelines

#शोध #हिंदी #CallForPapers #HindiResearch
'''),
('06 · Volume 1, Issue 1 published', f'''
Volume 1, Issue 1 (September 2026) of International Research Insights is online, and every article is free to read.

Five peer-reviewed articles:
1. A Quinquennial Empirical Analysis of Case Pendency in Indian High Courts (Dr. Ravi Kumar)
2. Beyond the Ballot: M. N. Roy's Theory of Organised Democracy (Puru Sharma)
3. Level of Stress among B.Sc. Nursing Students in Guwahati (Jaiprakash Tyagi)
4. Knowledge, Skills and Practice of Patient Safety among B.Sc. Nursing Students (Dr. Ramavatar Singh Tyagi)
5. Neuropsychiatric Disorders: A Comprehensive Overview (Akhileshar Prasad Mishra)

Read the full issue: {S}/current

Thank you to our authors, reviewers and editorial board.

#OpenAccess #AcademicJournal #LegalResearch #NursingResearch #Research
'''),
('07 · Spotlight: case pendency', f'''
Why do cases wait so long in India's High Courts?

In our first issue, Dr. Ravi Kumar analyses five years of case-pendency data from India's High Courts.

What the paper argues:
→ The causes: a rising caseload, unfilled judicial vacancies and too few staff in the higher judiciary.
→ The cost: higher expense and delay for litigants, rights realised late, and in criminal cases, prolonged trials that affect the rights of the accused and victims.
→ The way forward: filling vacancies, case-flow management, fewer adjournments, e-courts and virtual courts, mediation and regular review of pending lists.

Read it free: {S}/articles/case-pendency-indian-high-courts

Which of these would make the biggest difference? Tell us in the comments.

#JudicialReforms #HighCourts #AccessToJustice #IndianLaw #LegalResearch
'''),
('08 · Spotlight: M. N. Roy', f'''
Are elections alone enough for democracy?

M. N. Roy said no. In "Beyond the Ballot", Puru Sharma revisits Roy's idea of organised democracy, in which power stays with the people between elections through People's Committees.

→ Roy's draft Constitution of Free India is read alongside Carole Pateman's theory of participatory democracy.
→ The conclusion: organised democracy works best as an addition to representative democracy, not a replacement, and it leaves open questions about administration, social inequality and the protection of minorities.

Read it free: {S}/articles/mn-roy-organised-democracy-popular-sovereignty

#PoliticalTheory #Democracy #MNRoy #PoliticalScience #IndianPolitics
'''),
('09 · Write in Hindi', f'''
हिंदी में लिखिए, दुनिया तक पहुँचिए। Write in Hindi. Be read worldwide.

International Research Insights publishes research in Hindi as well as English, in every section.
• Hindi manuscripts are reviewed by Hindi-speaking referees.
• They are published in Hindi with an English title, abstract and keywords, so the work can be found and cited internationally.
• Our editorial office helps prepare the English abstract if you ask.

Submissions are open all year: {F}

#हिंदी #HindiSahitya #HindiResearch #CallForPapers
'''),
('10 · Five checks before you submit', f'''
Most manuscripts returned without review miss one of these five checks:

1. Anonymise the manuscript: no names, affiliations or acknowledgements, and clear your name from the file properties.
2. Write an abstract that reports the question, the method, the findings and the conclusion, in 150 to 250 words.
3. Match every citation to the reference list, in one style used consistently.
4. Stay within the word limit: research articles 4,000 to 8,000 words, excluding references.
5. Sign the declaration: originality, authorship, permissions and ethics approval.

Save this post for your next submission. Full guidelines: {S}/submission-guidelines

#ResearchTips #AcademicWriting #ResearchScholar #PhD
'''),
]
for title, text in posts:
    h(title, 2)
    caption(text)
doc.save(sys.argv[1])
