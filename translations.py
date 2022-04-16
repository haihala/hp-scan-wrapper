from __future__ import annotations


EN = {
    'scan_page': 'Scanning a page',
    'another_page_prompt': 'Scan more pages (y/n): ',
    'yes': 'y',
    'no': 'n',
    'retry_input': 'Couldn\'t parse input, please retry',
    'presentation_prompt': '''Scanning done. How to present?
1. Open folder
2. Send email
3. Open folder and send email
4. Quit''',
    'presentation_input': 'Please enter a number: ',
    'quitting': 'Quitting',
    'email_prompt_header': 'Where do you want to email the scanned images?',
    'email_prompt_row': '{}. {}',
    'email_input': 'Enter a number from the list above or an email address: ',
    'email_subject': 'Scanned files',
    'setup_smtp_sender': 'Enter the gmail address used to send scanned images: ',
    'setup_smtp_password': 'Enter the password for the gmail address: ',
}

FI = {
    'scan_page': 'Skannataan sivu',
    'another_page_prompt': 'Lisää sivuja (k/e): ',
    'yes': 'k',
    'no': 'e',
    'retry_input': 'Ei ymmmärretty, yritä uudestaan',
    'presentation_prompt': '''Kuvat on skannattu. Mitäs sitten.
1. Avaa kansio
2. Lähetä sähköpostia
3. Tee molemmat
4. Lopeta''',
    'presentation_input': 'Anna numero: ',
    'quitting': 'Lopetetaan',
    'email_prompt_header': 'Mihin haluat lähettää sähköpostia?',
    'email_prompt_row': '{}. {}',
    'email_input': 'Anna joko numero tai sähköpostiosoite: ',
    'email_subject': 'Skannatut tiedostot',
    'setup_smtp_sender': 'Anna lähettäjän gmail osoite: ',
    'setup_smtp_password': 'Anna lähettäjän gmail osoitteen salasana: ',
}


TRANSLATIONS = {
    'en': EN,
    'fi': FI,
}
