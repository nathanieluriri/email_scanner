import pprint
import re
import json
from pydantic import BaseModel, Field,model_validator
from typing import List, Optional
from typing_extensions import Self
from searchLocationLogic import search_through_locations_provided


with open("locations.json", 'r') as file:
    location_data = json.load(file)  # Load JSON content into a Python dictionary




class NerStore(BaseModel):
    """
    A Pydantic model to hold text content and check for the presence of emails.
    """
    text_contents: List[str] = Field(..., description="The text contents to be analyzed.")
    location_match:Optional[List]=[]
    
    @model_validator(mode='before')
    def checkMatch(cls, values):
        
        text_contents = values.get('text_contents', [''])
        for text in text_contents:
            matches = search_through_locations_provided(search_query=text)
            if matches:    
                match_value =  values.get('location_match',[])
                match_value.append({"text":text,"location":matches})
                values['location_match']= match_value
        return values


    
    












system = NerStore(text_contents=["CR Yakubugowon <yakubugowon@chicken-republic.com>; Olaniyi Ojo <olaniyi@foodconceptsplc.com>; Inioluwa Okeowo <inioluwa@foodconceptsplc.com>","CR Yakubugowon\r","CR Akowonjo <akowonjo@chicken-republic.com>; CR. Abule Egba <abule-egba@chicken-republic.com>; CR Gbagada <gbagada@chicken-republic.com>; CR. Ireakari <ireakari@chicken-republic.com>; CR Okota <okota@chicken-republic.com>; CR okeafa <okeafa@chicken-republic.com>;\r"])

pprint.pprint(system.location_match)
