import os
from dotenv import load_dotenv
from agent.email_agent import EmailService, EmailAgent

def main():
    # Load environment variables from .env file
    load_dotenv()
    username = os.environ.get("EMAIL_USERNAME")
    password = os.environ.get("EMAIL_PASSWORD")
    imap_server = os.environ.get("IMAP_SERVER", "imap.gmail.com")

    if not username or not password:
        print("Please set EMAIL_USERNAME and EMAIL_PASSWORD in your .env file.")
        return

    service = EmailService(username, password, imap_server)
    agent = EmailAgent(service)

    try:
        print("Scanning for unnecessary emails...")
        agent.clean_emails()
    finally:
        try:
            service.logout()
        except Exception as e:
            print(f"Warning: logout failed ({e})")
        print("Logged out.")

if __name__ == "__main__":
    main()