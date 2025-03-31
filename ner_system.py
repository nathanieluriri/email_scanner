import re
import json
from pydantic import BaseModel, Field,model_validator
from typing import Optional
from typing_extensions import Self



with open("locations.json", 'r') as file:
    location_data = json.load(file)  # Load JSON content into a Python dictionary




class NerStore(BaseModel):
    """
    A Pydantic model to hold text content and check for the presence of emails.
    """
    text_content: str = Field(..., description="The text content to be analyzed.")
    match:Optional[str]=None
    
    @model_validator(mode='before')
    def checkMatch(cls, values):
        text_content = values.get('text_content', '')
        values['match']="sa"
        return values


    
    

































# The pattern explained above
# \b                    - Word boundary
# (?<!Kaduna[,\s]\s*) - Negative Lookbehind: Asserts that the preceding text is NOT:
#                         "Kaduna" followed by (a comma OR whitespace) followed by (zero or more whitespace)
# Yakubu                - Literal "Yakubu" (case-insensitive due to flag)
# \s?                   - Optional single whitespace character
# Gowon                 - Literal "Gowon" (case-insensitive due to flag)
# \b                    - Word boundary
pattern = r"\b(?:Kaduna[,\s]*\s*)?Yakubu\s?Gowon\b"

# Text examples
text1 = "The leader was yakubugowon during that time."
text2 = "Historical figure: Yakubu Gowon led the country."
text3 = "Avoid this one: Kaduna, yakubu gowon was mentioned."
text4 = "Also avoid: Kaduna yakubugowon connection."
text5 = "yakubugowon should be found here."
text6 = "General Yakubu Gowon is notable."
text7 = "Kaduna state and YakubuGowon Way are different contexts." # Lookbehind prevents match here too

texts_to_check = [text1, text2, text3, text4, text5, text6, text7]

print(f"Pattern: {pattern}\n")

for i, text in enumerate(texts_to_check, 1):
    # Use re.search to find the first match
    match = re.search(pattern, text, re.IGNORECASE) # Crucial: Use re.IGNORECASE
    print(f"Text {i}: '{text}'")
    if match:
        print(f"  -> Found: '{match.group(0)}'") # group(0) is the whole match
    else:
        print("  -> No match found.")
    print("-" * 20)

# If you want to find ALL non-overlapping occurrences:
print("\nUsing findall:")
text_multiple = "yakubugowon met with someone. Later, Yakubu Gowon spoke. Not Kaduna, yakubu gowon."
matches = re.findall(pattern, text_multiple, re.IGNORECASE)
print(f"Text: '{text_multiple}'")
print(f"  -> Found all: {matches}")