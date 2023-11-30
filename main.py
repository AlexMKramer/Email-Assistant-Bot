import imapclient
import email
from email.mime.text import MIMEText
from email.header import decode_header
from smtplib import SMTP

import requests
import json
import re

from dotenv import load_dotenv
import os

load_dotenv()
username = os.getenv('USERNAME')
username_email_address = os.getenv('USERNAME_EMAIL_ADDRESS')
password = os.getenv('PASSWORD')
email_address = os.getenv('EMAIL_ADDRESS')

imap_server_address = 'imap.mail.me.com'
smtp_server_address = 'smtp.mail.me.com'


def extract_content_within_curly_brackets(prompt):
    # Use regular expression to find content within curly brackets
    match = re.search(r'\{(.+?)\}', prompt)

    if match:
        return match.group(1)
    else:
        return None


# Function to decode email subject
def decode_subject(encoded_subject):
    decoded_parts = decode_header(encoded_subject)
    decoded_subject = ""
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            decoded_subject += part.decode(encoding or 'utf-8', errors='replace')
        elif isinstance(part, str):
            decoded_subject += part
    return decoded_subject


# Function to connect to IMAP server
def connect_to_imap_server():
    server = imapclient.IMAPClient(imap_server_address, ssl=True)
    server.login(username, password)
    return server


# Function to read unread emails
def read_unread_emails(server):
    server.select_folder('INBOX', readonly=True)
    messages = server.search(['UNSEEN'])
    for msg_id, data in server.fetch(messages, ['ENVELOPE']).items():
        envelope = data[b'ENVELOPE']
        subject = decode_subject(envelope.subject.decode('utf-8'))
        sender = envelope.sender[0].mailbox.decode('utf-8') + "@" + envelope.sender[0].host.decode('utf-8')
        print(f"Subject: {subject}")
        print(f"From: {sender}")
        print("Body:")

        # Fetch the full email message
        response = server.fetch([msg_id], ['BODY[]'])
        raw_email = response[msg_id][b'BODY[]']

        # Parse the email
        msg = email.message_from_bytes(raw_email)

        email_body = None
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                email_body = part.get_payload(decode=True).decode('utf-8')
                print(email_body)

        # Respond to the email
        email_response = generate(email_body, context=None)
        respond_to_email(server, msg_id, sender, subject, email_response)


# Function to respond to an email
def respond_to_email(server, msg_id, recipient, subject, email_response):
    subject = "Re: " + subject  # Change this to your desired subject
    # body = "Thank you for your email. This is an automated response."  # Change this to your desired response

    # Create MIMEText message
    response_msg = MIMEText(email_response)
    response_msg['Subject'] = subject
    response_msg['From'] = email_address
    response_msg['To'] = recipient

    # Connect to SMTP server using TLS
    smtp_server = SMTP(smtp_server_address, port=587)
    smtp_server.starttls()  # Use starttls() to upgrade the connection to TLS
    smtp_server.login('alexmkramer.9494@gmail.com', password)

    # Send the response
    smtp_server.sendmail(email_address, recipient, response_msg.as_string())

    # Mark the original email as read
    server.add_flags(msg_id, [b'\\Seen'])

    # Close the connections
    server.logout()
    smtp_server.quit()


def generate(prompt, context):
    prompt = "I received this email, can you help me respond to it?  Here it is:\n\n" + prompt
    r = requests.post('http://localhost:11434/api/generate',
                      json={
                          'model': 'emailAssistant',
                          'prompt': prompt,
                          'context': context,
                      },
                      stream=True)
    r.raise_for_status()

    full_response = ""  # Initialize an empty string to accumulate the response parts

    for line in r.iter_lines():
        body = json.loads(line)
        response_part = body.get('response', '')
        full_response += response_part  # Accumulate the response parts

        if 'error' in body:
            raise Exception(body['error'])

        if body.get('done', False):
            print(full_response)  # Print the full response when it's completed
            extracted_response = extract_content_within_curly_brackets(full_response)
            if extracted_response:
                return extracted_response
            else:
                return full_response


def main():
    server = connect_to_imap_server()
    read_unread_emails(server)


if __name__ == "__main__":
    main()
