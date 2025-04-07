import pprint
import re
import json
from pydantic import BaseModel, Field,model_validator
from typing import List, Optional
from typing_extensions import Self
from finetuning.make_prediction import predict_reason
from location.searchLocationLogic import search_through_locations_provided
from tqdm import tqdm
with open("location/locations.json", 'r') as file:
    location_data = json.load(file)  # Load JSON content into a Python dictionary



class PossibleLocation(BaseModel):
    primaryLocation:str
    PrimaryFallbackLocation:str
    SecondaryFallbackLocation:str
    TetiaryFallbackLocation:str
class NerStore(BaseModel):
    """
    A Pydantic model to hold text content and check for the presence of emails.
    """
    possible_location_texts: List[PossibleLocation] = Field(..., description="The text contents to be analyzed to find locations.")
    sent_date_texts:List = Field(..., description="The text contents for request date.")
    action_texts:List = Field(..., description="The text contents to be analyzed to find action, reason, maintenance, category, equipment.")
    extracted_data:Optional[List]=[]
    
    @model_validator(mode='before')
    def checkMatch(cls, values):
        
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
                print(f"Error occurced: {e} {action_text_extract}")
        print("✅ Done extracting data with NER system")
        return values


    
    









# ["CR Yakubugowon <yakubugowon@chicken-republic.com>; Olaniyi Ojo <olaniyi@foodconceptsplc.com>; Inioluwa Okeowo <inioluwa@foodconceptsplc.com>","CR Yakubugowon\r","CR Akowonjo <akowonjo@chicken-republic.com>; CR. Abule Egba <abule-egba@chicken-republic.com>; CR Gbagada <gbagada@chicken-republic.com>; CR. Ireakari <ireakari@chicken-republic.com>; CR Okota <okota@chicken-republic.com>; CR okeafa <okeafa@chicken-republic.com>;\r"]


# system = NerStore(
#     sent_date_texts=["sas","saaa"],
#     action_texts=["FAULTY GENERATOR ONIRU PPU","QUOTATION FOR INSTALLATION OF DOUBLE MATT ENTERING SLAPS AT CR OKIGWE ROAD, OWERRI."],
#     possible_location_texts=[PossibleLocation(primaryLocation="CR Yakubugowon <yakubugowon@chicken-republic.com>; Olaniyi Ojo <olaniyi@foodconceptsplc.com>; Inioluwa Okeowo <inioluwa@foodconceptsplc.com>",PrimaryFallbackLocation="CR Yakubugowon\r",SecondaryFallbackLocation="",TetiaryFallbackLocation=""),
# PossibleLocation(primaryLocation="CR Akowonjo <akowonjo@chicken-republic.com>;",PrimaryFallbackLocation=" CR. Abule Egba <abule-egba@chicken-republic.com>;",SecondaryFallbackLocation="CR. Ireakari <ireakari@chicken-republic.com>;",TetiaryFallbackLocation="CR Okota <okota@chicken-republic.com>; ")                                           ])



# pprint.pprint(system.extracted_data)

# debug with python -m NER.ner_system