import imaplib
import email
from email.header import decode_header

def connect_to_email(username, password, imap_server='imap.gmail.com'):
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(username, password)
    return mail

def fetch_emails(mail, mailbox="INBOX", limit=100):
    mail.select(mailbox)
    result, data = mail.search(None, "ALL")
    email_ids = data[0].split()[-limit:]
    emails = []
    for eid in email_ids:
        result, msg_data = mail.fetch(eid, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        emails.append((eid, msg))
    return emails

def delete_email(mail, email_id):
    mail.store(email_id, '+FLAGS', '\\Deleted')
    mail.expunge()

def decode_header_value(header_value):
    if not header_value:
        return ""
    if isinstance(header_value, str):
        return header_value
    decoded_parts = decode_header(header_value)
    decoded_string = ''
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            decoded_string += part.decode(encoding or 'utf-8', errors='ignore')
        else:
            decoded_string += part
    return decoded_string

def is_unnecessary_email(msg):
    """
    Simple rule-based classifier for unnecessary emails.
    You can expand this with more rules or ML later.
    """
    subject = decode_header_value(msg['subject'])
    sender = decode_header_value(msg['from'])
    # Example rules (customize as needed)
    spam_keywords = ['sale', 'discount', 'offer', 'unsubscribe', 'promotion']
    spam_senders = ['newsletter', 'noreply', 'promo']

    if any(keyword in subject.lower() for keyword in spam_keywords):
        return True
    if any(sender_keyword in sender.lower() for sender_keyword in spam_senders):
        return True
    return False

def fetch_all_email_ids(mail, mailbox="INBOX"):
    mail.select(mailbox)
    result, data = mail.search(None, "ALL")
    if result != 'OK':
        return []
    return data[0].split()

def fetch_emails_by_ids(mail, email_ids):
    emails = []
    for eid in email_ids:
        result, msg_data = mail.fetch(eid, "(RFC822)")
        if result != 'OK':
            continue
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        emails.append((eid, msg))
    return emails