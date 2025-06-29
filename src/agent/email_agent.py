import os
import time
import imaplib
from utils.email_utils import connect_to_email, fetch_emails, delete_email, is_unnecessary_email, fetch_all_email_ids, fetch_emails_by_ids
from email.header import decode_header

class EmailService:
    def __init__(self, username, password, imap_server='imap.gmail.com'):
        self.mail = connect_to_email(username, password, imap_server)

    def fetch_emails(self, mailbox="INBOX", limit=100):
        return fetch_emails(self.mail, mailbox, limit)

    def delete_email(self, email_tuple):
        eid, _ = email_tuple
        delete_email(self.mail, eid)

    def logout(self):
        self.mail.logout()

class EmailAgent:
    def __init__(self, email_service, batch_size=5, max_reconnects=3):
        self.email_service = email_service
        self.batch_size = batch_size
        self.max_reconnects = max_reconnects
        self.username = os.environ.get("EMAIL_USERNAME")
        self.password = os.environ.get("EMAIL_PASSWORD")
        self.imap_server = os.environ.get("IMAP_SERVER", "imap.gmail.com")

    def identify_unnecessary_emails_batch(self, email_tuples):
        unnecessary_emails = []
        for email_tuple in email_tuples:
            _, msg = email_tuple
            if is_unnecessary_email(msg):
                unnecessary_emails.append(email_tuple)
        return unnecessary_emails

    def clean_emails(self):
        all_ids = fetch_all_email_ids(self.email_service.mail)
        total = len(all_ids)
        print(f"Total emails found: {total}")
        deleted_count = 0
        i = 0
        reconnects = 0
        while i < total:
            batch_ids = all_ids[i:i+self.batch_size]
            try:
                email_tuples = fetch_emails_by_ids(self.email_service.mail, batch_ids)
            except imaplib.IMAP4.abort as e:
                reconnects += 1
                if reconnects > self.max_reconnects:
                    print("Too many reconnect attempts. Stopping.")
                    break
                print(f"Batch {i // self.batch_size + 1}: IMAP abort error: {e}. Reconnecting in 30 seconds...")
                time.sleep(30)
                print(f"Connecting to IMAP server: {self.imap_server}")
                self.email_service.mail = connect_to_email(
                    self.username,
                    self.password,
                    self.imap_server
                )
                self.email_service.mail.select("INBOX")  # Ensure mailbox is selected after reconnect
                continue  # Retry this batch
            except Exception as e:
                print(f"Batch fetch failed: {e}. Skipping batch {i // self.batch_size + 1}.")
                i += self.batch_size
                continue
            reconnects = 0  # Reset on success
            unnecessary_emails = self.identify_unnecessary_emails_batch(email_tuples)
            for email_tuple in unnecessary_emails:
                self.email_service.delete_email(email_tuple)
                _, msg = email_tuple
                print(f"Deleted email: {msg['subject']} from {msg['from']}")
                deleted_count += 1
            i += self.batch_size
            time.sleep(1)
        print(f"Total emails deleted: {deleted_count}")

def decode_header_value(header_value):
    if not header_value:
        return ""
    if isinstance(header_value, str):
        return header_value
    decoded_parts = decode_header(header_value)
    decoded_string = ''
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            try:
                # Try the provided encoding, fallback to utf-8, then latin1
                decoded_string += part.decode(encoding or 'utf-8', errors='ignore')
            except LookupError:
                decoded_string += part.decode('utf-8', errors='ignore')
        else:
            decoded_string += part
    return decoded_string