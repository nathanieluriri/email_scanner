from rich import print
from pathlib import Path
import json
from pydantic import BaseModel, Field,model_validator
from typing import List, Optional
from typing_extensions import Self
from finetuning.make_prediction import predict_reason
from location.searchLocationLogic import search_through_locations_provided
from tqdm import tqdm

def get_current_date_and_time():
    
    
    import datetime
    import pytz

    # Get the current date and time in Nigeria
    nigeria_tz = pytz.timezone('Africa/Lagos')
    now_nigeria = datetime.datetime.now(nigeria_tz)

    # Function to get the ordinal suffix for the day
    def get_ordinal_suffix(day):
        if 10 <= day <= 20:
            return 'th'
        suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
        return suffixes.get(day % 10, 'th')

    # Format the current date and time
    current_day_name = now_nigeria.strftime("%A").lower()
    current_day = now_nigeria.day
    current_day_with_suffix = f"{current_day}{get_ordinal_suffix(current_day)}"
    current_month_name = now_nigeria.strftime("%B").lower()
    current_year = now_nigeria.year
    current_hour_12 = now_nigeria.strftime("%I")
    current_minute = now_nigeria.strftime("%M")
    current_am_pm = now_nigeria.strftime("%p").lower()

    formatted_now = f"{current_day_name}.{current_day_with_suffix}.{current_month_name}.{current_year}.{current_hour_12}..{current_minute}{current_am_pm}"

    
    return formatted_now
    
with open("location/locations.json", 'r') as file:
    location_data = json.load(file)  

with open("emailll/email.json",'r') as file:
    email_data = json.load(file)

class PossibleLocation(BaseModel):
    primaryLocation:str
    PrimaryFallbackLocation:str
    SecondaryFallbackLocation:str
    TetiaryFallbackLocation:str
class NERSTORE(BaseModel):
    """
    A Pydantic model to hold text content and check for the presence of emails.
    """
    possible_location_texts: List[PossibleLocation] = Field(..., description="The text contents to be analyzed to find locations.")
    sent_date_texts:List = Field(..., description="The text contents for request date.")
    action_texts:List = Field(..., description="The text contents to be analyzed to find action, reason, maintenance, category, equipment.")
    extracted_data:Optional[List]=[]
    
    @model_validator(mode='before')
    def checkMatch(cls, values):
        failures=[]
        location_text_contents = values.get('possible_location_texts', [PossibleLocation(primaryLocation="",PrimaryFallbackLocation="",SecondaryFallbackLocation="",TetiaryFallbackLocation="")])
        action_text_contents = values.get('action_texts', [''])
        request_date = values.get('sent_date_texts', [''])
        max_length = max(len(location_text_contents), len(action_text_contents), len(request_date))
        location_text_contents += [PossibleLocation(primaryLocation="",PrimaryFallbackLocation="",SecondaryFallbackLocation="",TetiaryFallbackLocation="")] * (max_length - len(location_text_contents))
        action_text_contents += [''] * (max_length - len(action_text_contents))
        request_date += [''] * (max_length - len(request_date))
        
        
        for index, (location_text_extract, action_text_extract, request_date_extract) in tqdm(enumerate(zip(location_text_contents, action_text_contents, request_date)), desc="Running Named Entity Recognition System ", unit="field", total=max_length):
            locations_to_search = [
                location_text_extract.primaryLocation,
                location_text_extract.PrimaryFallbackLocation,
                location_text_extract.SecondaryFallbackLocation,
                location_text_extract.TetiaryFallbackLocation
            ]

            location_matches = next(
                (search_through_locations_provided(search_query=loc) 
                for loc in locations_to_search if search_through_locations_provided(search_query=loc) is not None),
                None
            )
            match_value =  values.get('extracted_data',[])
            try:
                action_matches = predict_reason(action_text=action_text_extract)
                
                match_value.append({"request_date":request_date_extract,"predicted_reason":action_matches,"location":location_matches})
                values['extracted_data']= match_value
            except Exception as e:
                for email in email_data:
                    if email['thread_group_name']==action_text_extract:
                        failures.append(email)
        print("✅ [bold green]Successfully extracted data with NER system[/bold green]")
        if len(failures)>=1:
            today = get_current_date_and_time()
            to= today.split(".")
            today = '_'.join(to)
            with open(f"emailll/Failures/{today}.json",'w') as file:
                json.dump(failures,file,indent=4)
                print("Saved The ones that failed to be extracted too")
            failures_path =  (f"emailll/Failures/{today}")
            print(f"❌ [bold red]NER system failed[/bold red] to extract {len(failures)} thread groups.")
            print(f"📂 [bold red]Check the groups that failed here[/bold red]: [bold yellow]{failures_path}[/bold yellow]")
        return values


    
    








# ["CR Yakubugowon <yakubugowon@chicken-republic.com>; Olaniyi Ojo <olaniyi@foodconceptsplc.com>; Inioluwa Okeowo <inioluwa@foodconceptsplc.com>","CR Yakubugowon\r","CR Akowonjo <akowonjo@chicken-republic.com>; CR. Abule Egba <abule-egba@chicken-republic.com>; CR Gbagada <gbagada@chicken-republic.com>; CR. Ireakari <ireakari@chicken-republic.com>; CR Okota <okota@chicken-republic.com>; CR okeafa <okeafa@chicken-republic.com>;\r"]


# system = NERSTORE(
#     sent_date_texts=["sas","saaa"],
#     action_texts=["FAULTY GENERATOR ONIRU PPU","QUOTATION FOR INSTALLATION OF DOUBLE MATT ENTERING SLAPS AT CR OKIGWE ROAD, OWERRI."],
#     possible_location_texts=[PossibleLocation(primaryLocation="CR Yakubugowon <yakubugowon@chicken-republic.com>; Olaniyi Ojo <olaniyi@foodconceptsplc.com>; Inioluwa Okeowo <inioluwa@foodconceptsplc.com>",PrimaryFallbackLocation="CR Yakubugowon\r",SecondaryFallbackLocation="",TetiaryFallbackLocation=""),
# PossibleLocation(primaryLocation="CR Akowonjo <akowonjo@chicken-republic.com>;",PrimaryFallbackLocation=" CR. Abule Egba <abule-egba@chicken-republic.com>;",SecondaryFallbackLocation="CR. Ireakari <ireakari@chicken-republic.com>;",TetiaryFallbackLocation="CR Okota <okota@chicken-republic.com>; ")                                           ])



# pprint.pprint(system.extracted_data)

# debug with python -m NER.ner_system