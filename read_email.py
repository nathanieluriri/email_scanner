import email
import imaplib
from bs4 import BeautifulSoup
import re
import json
from_pattern = r"From:\s*(.*)"
to_pattern = r"To:\s*(.*)"
sent_pattern = r"Sent:\s*(.*)"
subject_pattern = r"Subject:\s*(.*)"
Cc_pattern = r"Cc:\s*(.*)"
password = "Nathanie101!"  
username = "nat@uriri.com.ng"
host = "imap.hostinger.com"

# Set up IMAP connection
mail = imaplib.IMAP4_SSL(host)

# Login
mail.login(username, password)

# Select the inbox
mail.select("INBOX")

# Search for all emails from a specific sender
status, selected_mails = mail.search(None, 'FROM', '"inioluwa@foodconceptsplc.com"')

# Convert to a list of email IDs
email_ids = selected_mails[0].split()
print(f"Total Emails: {len(email_ids)}")
thread_pattern = r"From:.*?Sent:.*?Subject:.*?[\r\n]+"

# Extract all the threads
email_content = []
# Fetch and display subject of each email
for email_id in email_ids:
    status, data = mail.fetch(email_id, "(RFC822)")
    raw_email = data[0][1] 
    email_msg = email.message_from_bytes(raw_email)
    for part in email_msg.walk():
        if part.get_content_type()=='text/plain' or part.get_content_type() =='text/html':
            message= part.get_payload(decode=True)
            decoded_message=message.decode('windows-1252')
            soup = BeautifulSoup(decoded_message, 'html.parser')
            cleaned_text = soup.get_text()
            
            threads = re.findall(thread_pattern, cleaned_text, re.DOTALL)
           
            thread_groups = {}
            thread_group_list=[]
            
            for i, thread in enumerate(threads, start=1):
                threadss={}
                print(f"Thread {i}: ")
  
                from_match = re.search(from_pattern, thread)
                to_match = re.search(to_pattern, thread)
                sent_match = re.search(sent_pattern, thread)
                subject_match = re.search(subject_pattern, thread)
                cc_match = re.search(Cc_pattern,thread)
                threadss["thread_index"]= i
                threadss["subject"]=subject_match.group(1)
                threadss['sent_date']=sent_match.group(1)
                threadss['to']=to_match.group(1)
                threadss['from']=from_match.group(1)
                try:
                    threadss["cc"] =cc_match.group(1)
                except:
                    pass
                threadss["thread_index"]= i

                thread_group_list.append(threadss)
                
                
            thread_groups["thread_group_name"]=subject_match.group(1)
            thread_groups["thread_group"]=thread_group_list
            
    if len(email_content)>=1:
        if email_content[-1]!= thread_groups:
            email_content.append(thread_groups)
    else:
        email_content.append(thread_groups)

# Logout
mail.logout()

with open('email/email.json', 'w') as json_file:
    json.dump(email_content,json_file)