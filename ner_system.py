import pprint
import re
import json
from pydantic import BaseModel, Field,model_validator
from typing import List, Optional
from typing_extensions import Self
from searchLocationLogic import search_through_locations_provided
from finetuning.make_prediction import predict_reason

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
    action_texts:List[str] = Field(..., description="The text contents to be analyzed to find action, reason, maintenance, category, equipment.")
    location_match:Optional[List]=[]
    action_match:Optional[List]=[]
    extracted_data:Optional[List]=[]
    
    @model_validator(mode='before')
    def checkMatch(cls, values):
        
        location_text_contents = values.get('possible_location_texts', [PossibleLocation(primaryLocation="",PrimaryFallbackLocation="",SecondaryFallbackLocation="",TetiaryFallbackLocation="")])
        action_text_contents = values.get('action_texts',[''])
        
        
        for index,(location_text_extract,action_text_extract) in enumerate(zip(location_text_contents,action_text_contents)):
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
            
            action_matches = predict_reason(action_text=action_text_extract)
            
            match_value.append({"predicted_reason":action_matches,"location":location_matches})
            values['extracted_data']= match_value
        
            
        
        
        # for text in location_text_contents:
        #     locations_to_search = [
        #         text.primaryLocation,
        #         text.PrimaryFallbackLocation,
        #         text.SecondaryFallbackLocation,
        #         text.TetiaryFallbackLocation
        #     ]

        #     location_matches = next(
        #         (search_through_locations_provided(search_query=loc) 
        #         for loc in locations_to_search if search_through_locations_provided(search_query=loc) is not None),
        #         None
        #     )
            
        #     if location_matches:    
        #         match_value =  values.get('location_match',[])
        #         match_value.append({"text":text,"location":location_matches})
        #         values['location_match']= match_value
        
        # for action in action_text_contents:
        #     action_matches = predict_reason(action_text=action)
        #     if action_matches:
        #         action_match_value = values.get('action_match',[])
        #         action_match_value.append({"text":action,"action_matches":action_matches})
        #         values['action_match']=action_match_value
        return values


    
    









# ["CR Yakubugowon <yakubugowon@chicken-republic.com>; Olaniyi Ojo <olaniyi@foodconceptsplc.com>; Inioluwa Okeowo <inioluwa@foodconceptsplc.com>","CR Yakubugowon\r","CR Akowonjo <akowonjo@chicken-republic.com>; CR. Abule Egba <abule-egba@chicken-republic.com>; CR Gbagada <gbagada@chicken-republic.com>; CR. Ireakari <ireakari@chicken-republic.com>; CR Okota <okota@chicken-republic.com>; CR okeafa <okeafa@chicken-republic.com>;\r"]


# system = NerStore(
#     action_texts=["FAULTY GENERATOR ONIRU PPU","QUOTATION FOR INSTALLATION OF DOUBLE MATT ENTERING SLAPS AT CR OKIGWE ROAD, OWERRI."],
#     possible_location_texts=[PossibleLocation(primaryLocation="CR Yakubugowon <yakubugowon@chicken-republic.com>; Olaniyi Ojo <olaniyi@foodconceptsplc.com>; Inioluwa Okeowo <inioluwa@foodconceptsplc.com>",PrimaryFallbackLocation="CR Yakubugowon\r",SecondaryFallbackLocation="",TetiaryFallbackLocation=""),
# PossibleLocation(primaryLocation="CR Akowonjo <akowonjo@chicken-republic.com>;",PrimaryFallbackLocation=" CR. Abule Egba <abule-egba@chicken-republic.com>;",SecondaryFallbackLocation="CR. Ireakari <ireakari@chicken-republic.com>;",TetiaryFallbackLocation="CR Okota <okota@chicken-republic.com>; ")                                           ])



# print(system.extracted_data)