from utils import save_sheet, extract_email_data_into_object
from emailll.read_email import read_this_email
# step 1 the system will read and extract emails and then save those emails in a json file inside emailll/email.json to process later
read_this_email()
# step 2 after extracting those emails the system will then use said data by loading it in memory and running a custome NER system built with a finetuned version of t5 and some rulebased tokenizations
extracted_data= extract_email_data_into_object()
# after NER has done his thing I flatten the data in a format that can be saved in a new excel workbook a new excell file will be created everytime you run this and it ends with the current date and time incase you run multiple times and you only need the latest one 
save_sheet(extracted_data)

# bonus sometimes the NER system could fail to predict and when it does I save those email groups inside a folder called Failures and file with todays date the 
# N:B Failure folder is inside the emailll folder 