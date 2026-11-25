/**
 * Manuscript Submission form for International Research Insights.
 *
 * HOW TO USE (2 minutes):
 *   1. Open https://script.google.com while signed in to the journal's Google account.
 *   2. Click "New project", delete the sample code, paste this whole file.
 *   3. Click Save, choose createSubmissionForm in the function menu, then click Run.
 *   4. Allow the permissions Google asks for (it needs to create a Form and a Sheet in your Drive).
 *   5. Open "Execution log": it prints the form link to share, the edit link and the responses sheet.
 *
 * Run it only once; every run creates a new form.
 */

// Address where authors email their three Word files. Change it if needed.
const SUBMISSIONS_EMAIL = 'submissions@internationalresearchinsights.com';

const JOURNAL = 'International Research Insights: Multidisciplinary e-Journal';
const ISSN = 'ISSN (Online): 2839-7134';

const SECTIONS = [
  'Law and Constitutional Studies',
  'Health and Nursing Sciences',
  'Hindi Language and Literature',
  'History, Heritage and Culture',
  'Education and Pedagogy',
  'Society, Economy and Public Policy',
  'Science, Technology and Environment',
];

const ARTICLE_TYPES = [
  'Research article',
  'Review article',
  'Case comment',
  'Short communication',
  'Book review',
];

const SUBJECT_LINE = 'SUBMISSION | Section | Article type | First author surname | Short title';

function createSubmissionForm() {
  const form = FormApp.create('Manuscript Submission | International Research Insights');

  form
    .setTitle('Manuscript Submission')
    .setDescription(
      JOURNAL + '\n' + ISSN + '\n\n' +
      'Use this form to submit a manuscript for peer review. It takes about 10 minutes.\n\n' +
      'Before you start, keep these ready: the title, abstract and keywords, the details of every author, ' +
      'and the three Word files described in the Submission Guidelines ' +
      '(internationalresearchinsights.com/submission-guidelines).\n\n' +
      'There is no charge at submission or if a paper is not accepted.'
    )
    .setConfirmationMessage(
      'Thank you. Your submission details have been received.\n\n' +
      'Final step: email the three Word files (manuscript-anonymous.docx, title-page.docx, declaration.docx) to ' +
      SUBMISSIONS_EMAIL + ' with the subject line:\n' + SUBJECT_LINE + '\n\n' +
      'You will receive an acknowledgement with a manuscript number within two working days.'
    )
    .setCollectEmail(true)
    .setProgressBar(true)
    .setAllowResponseEdits(false)
    .setShowLinkToRespondAgain(false);

  const email = FormApp.createTextValidation()
    .setHelpText('Enter a valid email address.')
    .requireTextIsEmail()
    .build();
  const phone = FormApp.createTextValidation()
    .setHelpText('Enter a phone number with country code, e.g. +91 98765 43210.')
    .requireTextMatchesPattern('^[+0-9 ()-]{8,20}$')
    .build();
  const orcid = FormApp.createTextValidation()
    .setHelpText('Format: 0000-0000-0000-0000')
    .requireTextMatchesPattern('^\\d{4}-\\d{4}-\\d{4}-\\d{3}[\\dX]$')
    .build();

  // ---- Page 1: Corresponding author ----
  form.addSectionHeaderItem()
    .setTitle('1. Corresponding author')
    .setHelpText('The person the editorial office will write to about this manuscript.');
  form.addTextItem().setTitle('Full name').setHelpText('With title, e.g. Dr. Anita Sharma').setRequired(true);
  form.addTextItem().setTitle('Mobile / WhatsApp number').setValidation(phone).setRequired(true);
  form.addTextItem().setTitle('Designation').setHelpText('e.g. Assistant Professor, Research Scholar, Advocate').setRequired(true);
  form.addTextItem().setTitle('Department and institution').setRequired(true);
  form.addTextItem().setTitle('City, State, Country').setRequired(true);
  form.addTextItem().setTitle('ORCID iD (if you have one)').setValidation(orcid);

  // ---- Page 2: Authors ----
  form.addPageBreakItem().setTitle('2. Authors');
  form.addListItem()
    .setTitle('Total number of authors, including you')
    .setChoiceValues(['1', '2', '3', '4', '5', '6', '7', '8 or more'])
    .setRequired(true);
  form.addParagraphTextItem()
    .setTitle('Co-author details')
    .setHelpText('One co-author per line, in the order they should appear: Name, Designation, Institution, Email. Leave blank if you are the only author.');
  form.addMultipleChoiceItem()
    .setTitle('Is any author based outside India?')
    .setChoiceValues(['No, all authors are in India', 'Yes'])
    .setRequired(true);

  // ---- Page 3: Manuscript ----
  form.addPageBreakItem().setTitle('3. Manuscript');
  form.addTextItem().setTitle('Title of the manuscript').setRequired(true);
  form.addMultipleChoiceItem()
    .setTitle('Research section')
    .setHelpText('Choose the section closest to your work. The editors may move it if another section fits better.')
    .setChoiceValues(SECTIONS)
    .setRequired(true);
  form.addMultipleChoiceItem().setTitle('Article type').setChoiceValues(ARTICLE_TYPES).setRequired(true);
  form.addMultipleChoiceItem().setTitle('Language of the manuscript').setChoiceValues(['English', 'Hindi']).setRequired(true);
  form.addParagraphTextItem()
    .setTitle('Abstract')
    .setHelpText('150 to 250 words for research and review articles. State the question, method, findings and conclusion.')
    .setValidation(
      FormApp.createParagraphTextValidation()
        .setHelpText('The abstract is too long. Keep it under about 300 words.')
        .requireTextLengthLessThanOrEqualTo(2200)
        .build()
    )
    .setRequired(true);
  form.addTextItem().setTitle('Keywords').setHelpText('4 to 6 keywords, separated by commas').setRequired(true);
  form.addTextItem()
    .setTitle('Word count, excluding references')
    .setValidation(
      FormApp.createTextValidation()
        .setHelpText('Enter a number, e.g. 5200')
        .requireNumberBetween(300, 20000)
        .build()
    )
    .setRequired(true);
  form.addMultipleChoiceItem()
    .setTitle('Referencing style')
    .setChoiceValues(['APA 7th edition', 'Bluebook 20th edition', 'Indian Law Institute (ILI)', 'MLA 9th edition'])
    .showOtherOption(true)
    .setRequired(true);
  form.addMultipleChoiceItem()
    .setTitle('Did the research involve human participants, patients or patient records?')
    .setChoiceValues([
      'No',
      'Yes, and ethics approval was obtained (approving body named in the title page)',
    ])
    .setRequired(true);
  form.addMultipleChoiceItem()
    .setTitle('Did you use any AI tool while preparing the manuscript?')
    .setHelpText('AI tools may be used only for language editing, never to generate data, results, references or analysis.')
    .setChoiceValues(['No', 'Yes, for language editing only'])
    .setRequired(true);
  form.addParagraphTextItem()
    .setTitle('Note to the editors (optional)')
    .setHelpText('Anything the editors should know: the AI tool used, a reason for extra length, a related earlier publication, etc.');

  // ---- Page 4: Declarations ----
  form.addPageBreakItem()
    .setTitle('4. Declarations')
    .setHelpText('Every statement must be true for the manuscript to be considered.');
  const declarations = [
    'The work is original, is not published elsewhere, and is not under consideration by another journal.',
    'Every author listed has contributed to the work and has approved this version.',
    'Every source used is cited, and every citation appears in the reference list.',
    'Any data, images or instruments belonging to others are used with permission.',
    'I can produce the underlying data, transcripts, case files or field notes if the editors ask for them.',
    'The manuscript file is anonymous: no author names, affiliations or acknowledgements.',
    'If accepted, the article will be published open access under the Creative Commons Attribution 4.0 (CC BY 4.0) licence.',
    'I understand that a processing charge is payable only after acceptance, as listed on the Processing Charges page, and that nothing is charged at submission or if the paper is not accepted.',
  ];
  form.addCheckboxItem()
    .setTitle('I confirm that')
    .setChoiceValues(declarations)
    .setValidation(
      FormApp.createCheckboxValidation()
        .setHelpText('Please confirm every statement.')
        .requireSelectAtLeast(declarations.length)
        .build()
    )
    .setRequired(true);

  // ---- Page 5: Send the files ----
  form.addPageBreakItem().setTitle('5. Send your files');
  form.addSectionHeaderItem()
    .setTitle('Email the three Word files after you press Submit')
    .setHelpText(
      'To: ' + SUBMISSIONS_EMAIL + '\n' +
      'Subject: ' + SUBJECT_LINE + '\n\n' +
      '1. manuscript-anonymous.docx: the full text with no author details\n' +
      '2. title-page.docx: title, all authors with designation, institution and email, ORCID, funding and conflict of interest statement\n' +
      '3. declaration.docx: the signed author declaration (internationalresearchinsights.com/author-declaration)\n\n' +
      'Send Word files, not PDF only.'
    );
  form.addCheckboxItem()
    .setTitle('Files')
    .setChoiceValues(['I will email the three Word files to ' + SUBMISSIONS_EMAIL + ' now.'])
    .setRequired(true);

  // ---- Responses go to a Google Sheet ----
  const sheet = SpreadsheetApp.create('Manuscript Submissions | International Research Insights (responses)');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, sheet.getId());

  // Newer Google Forms have a Publish switch; publish if this account has it.
  if (typeof form.setPublished === 'function') form.setPublished(true);
  form.setAcceptingResponses(true);

  const link = form.getPublishedUrl();
  Logger.log('FORM LINK (share this):  ' + link);
  Logger.log('SHORT LINK:              ' + form.shortenFormUrl(link));
  Logger.log('EDIT THE FORM:           ' + form.getEditUrl());
  Logger.log('RESPONSES SHEET:         ' + sheet.getUrl());
}
