from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from config import *
from string import Template


def send_email(log, summary_list):
    log.info('In the send email listing method')

    #load in the template from the file
    with open('emailTemplate.html') as file:
        template_content = file.read()

    log.info('Template file loaded')

    template = Template(template_content)

    table_rows = ''

    #for every row in the summary_list, we want to create a table row to be added to our email template
    for summary in summary_list:
        ticker = summary['ticker']
        gpt_summary = summary['gpt_summary']
        current_price = summary['current_price']

        table_rows += f'''
                <tr>
                    <td><b>{ticker}</b> <br> {current_price}</td>
                    <td>{gpt_summary}</td>
                <tr>
        '''

    context = {
        'table_body':table_rows,
        'subreddits': ", ".join(SUBREDDITS_TO_QUERY)
    }

    email_body = template.substitute(context)

    message = MIMEMultipart()
    message['From'] = f"{MAIL_DISPLAY_NAME} <{MAIL_SMTP_USERNAME}>"
    message['To'] = 'ghanimohamed73@gmail.com'
    message['Subject'] = 'SENTIMENTAL_NEWSLETTER_From_Reddit'

    log.info('email header set')

    message.attach(MIMEText(email_body, 'html'))

    log.info('email body set')

    with smtplib.SMTP(MAIL_SMTP_SERVER, MAIL_SMTP_PORT) as server: 
        server.starttls()
        server.login(MAIL_SMTP_USERNAME, MAIL_SMTP_PASSWORD)
        server.sendmail(MAIL_SMTP_USERNAME, [message['To']], message.as_string())

    log.info('email sent')
