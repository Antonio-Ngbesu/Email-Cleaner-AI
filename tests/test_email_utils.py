import unittest
from utils.email_utils import is_unnecessary_email
from email.message import EmailMessage

class TestEmailUtils(unittest.TestCase):
    def test_is_unnecessary_email_spam_subject(self):
        msg = EmailMessage()
        msg['subject'] = 'Big SALE just for you!'
        msg['from'] = 'promo@shop.com'
        self.assertTrue(is_unnecessary_email(msg))

    def test_is_unnecessary_email_spam_sender(self):
        msg = EmailMessage()
        msg['subject'] = 'Hello'
        msg['from'] = 'newsletter@news.com'
        self.assertTrue(is_unnecessary_email(msg))

    def test_is_unnecessary_email_not_spam(self):
        msg = EmailMessage()
        msg['subject'] = 'Project Update'
        msg['from'] = 'colleague@company.com'
        self.assertFalse(is_unnecessary_email(msg))

if __name__ == '__main__':
    unittest.main()
