import pprint
import json
from NER.ner_system import NerStore, PossibleLocation
from emailll.read_email import read_this_email

read_this_email()

with open("emailll/email.json", "r") as file:
    data = json.load(file)

extracted_sent_date=[]
extracted_action_text=[]
extracted_possible_location=[]

for email_thread_group in data:
    thread_group_name = email_thread_group['thread_group_name']
    extracted_action_text.append(thread_group_name)
    
    thread_group = email_thread_group['thread_group']
    extracted_sent_date.append(thread_group[-1]['sent_date'])
    extracted_possible_location.append(PossibleLocation(primaryLocation=thread_group[-1]['from'],PrimaryFallbackLocation=thread_group[0]['to'],SecondaryFallbackLocation=thread_group[0].get('cc',""),TetiaryFallbackLocation=thread_group[0]['subject']))
    
        
        
        

extracted_data=NerStore( sent_date_texts=extracted_sent_date,action_texts=extracted_action_text,possible_location_texts=extracted_possible_location)


pprint.pprint(extracted_data.extracted_data)