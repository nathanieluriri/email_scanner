from utils import save_sheet
from extraction import extract_email_data_into_object

from emailll.read_email import read_this_email

# read_this_email()

extracted_data= extract_email_data_into_object()

save_sheet(extracted_data)