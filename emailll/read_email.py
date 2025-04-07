import os
from dotenv import load_dotenv
import email
import imaplib
from bs4 import BeautifulSoup
import re
import json
from tqdm import tqdm
load_dotenv()


def read_this_email():
    password = os.getenv("PASSWORD")
    username = os.getenv("USERNAME")
    host = os.getenv("HOST")

    from_pattern = r"From:\s*(.*)"
    to_pattern = r"To:\s*(.*)"
    sent_pattern = r"Sent:\s*(.*)"
    subject_pattern = r"Subject:\s*(.*)"
    Cc_pattern = r"Cc:\s*(.*)"

    mail = imaplib.IMAP4_SSL(host)
    mail.login(username, password)
    mail.select("INBOX")

    status, selected_mails = mail.search(None, 'FROM', '"inioluwa@foodconceptsplc.com"')
    email_ids = selected_mails[0].split()
    print(f"Total Emails: {len(email_ids)}")
    thread_pattern = r"From:.*?Sent:.*?Subject:.*?[\r\n]+"

    email_content = []

    
    for email_id in tqdm(email_ids, desc="Reading Emails", unit="email"):
        status, data = mail.fetch(email_id, "(RFC822)")
        raw_email = data[0][1]
        email_msg = email.message_from_bytes(raw_email)

        for part in email_msg.walk():
            if part.get_content_type() == 'text/plain' or part.get_content_type() == 'text/html':
                message = part.get_payload(decode=True)
                decoded_message = message.decode('windows-1252')
                soup = BeautifulSoup(decoded_message, 'html.parser')
                cleaned_text = soup.get_text()
                threads = re.findall(thread_pattern, cleaned_text, re.DOTALL)

                thread_groups = {}
                thread_group_list = []

                for i, thread in enumerate(threads, start=1):
                    threadss = {}
                    from_match = re.search(from_pattern, thread)
                    to_match = re.search(to_pattern, thread)
                    sent_match = re.search(sent_pattern, thread)
                    subject_match = re.search(subject_pattern, thread)
                    cc_match = re.search(Cc_pattern, thread)

                    threadss["thread_index"] = i
                    threadss["subject"] = subject_match.group(1) if subject_match else ""
                    threadss["sent_date"] = sent_match.group(1) if sent_match else ""
                    threadss["to"] = to_match.group(1) if to_match else ""
                    threadss["from"] = from_match.group(1) if from_match else ""
                    if cc_match:
                        threadss["cc"] = cc_match.group(1)

                    thread_group_list.append(threadss)

                thread_groups["thread_group_name"] = subject_match.group(1) if subject_match else "UNKNOWN"
                thread_groups["thread_group"] = thread_group_list

        if len(email_content) >= 1:
            if email_content[-1] != thread_groups:
                email_content.append(thread_groups)
        else:
            email_content.append(thread_groups)

    mail.logout()

    with open('emailll/email.json', 'w') as json_file:
        json.dump(email_content, json_file, indent=4)
        print("✅ Done extracting and saving emails")

        
        
# read_this_email()

# debug with python -m emailll.read_email