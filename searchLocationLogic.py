import re
import json
# Sample locations (as per your example)

with open("location/locations.json", 'r') as file:
    locations = json.load(file)  # Load JSON content into a Python dictionary




# Function to create a dynamic regex pattern
def create_dynamic_pattern(locations: str, has_comma: bool, number_of_commas: int = None):
    if has_comma == True:
        if number_of_commas == 1:
            name_before_comma, name_after_comma = locations.split(sep=",")
            
            # If there is only one word before the comma
            if len(name_before_comma.split(sep=" ")) <= 1:
                # If there are exactly 2 words after the comma
                if len(name_after_comma.split(sep=" ")) == 2:
                    name_after_space1, name_after_space2 = name_after_comma.split(sep=" ")
                    pattern = rf"\b(?:{name_before_comma}[,\s]*\s*)?{name_after_space1}\s?{name_after_space2}\b"
                    return pattern
                # If there are exactly 3 words after the comma
                elif len(name_after_comma.split(sep=" ")) == 3:
                    name_after_space1, name_after_space2, name_after_space3 = name_after_comma.split(sep=" ")
                    pattern = rf"\b(?:{name_before_comma}[,\s]*\s*)?{name_after_space1}\s?{name_after_space2}\s?{name_after_space3}\b"
                    return pattern

            # If there is more than one word before the comma (this case can be handled if needed)
            else:
                # If there are exactly 2 words before the comma
                if len(name_before_comma.split(sep=" ")) == 2:
                    name_before_comma_space1, name_before_comma_space2 = name_before_comma.split(sep=" ")
                    
                    # If there are exactly 2 words after the comma
                    if len(name_after_comma.split(sep=" ")) == 2:
                        name_after_space1, name_after_space2 = name_after_comma.split(sep=" ")
                        pattern = rf"\b(?:{name_before_comma_space1}\s?{name_before_comma_space2}[,\s]*\s*)?{name_after_space1}\s?{name_after_space2}\b"
                        return pattern
                    # If there are exactly 3 words after the comma
                    elif len(name_after_comma.split(sep=" ")) == 3:
                        name_after_space1, name_after_space2, name_after_space3 = name_after_comma.split(sep=" ")
                        pattern = rf"\b(?:{name_before_comma_space1}\s?{name_before_comma_space2}[,\s]*\s*)?{name_after_space1}\s?{name_after_space2}\s?{name_after_space3}\b"
                        return pattern

                # If there are exactly 3 words before the comma
                if len(name_before_comma.split(sep=" ")) == 3:
                    name_before_comma_space1, name_before_comma_space2, name_before_comma_space3 = name_before_comma.split(sep=" ")
                    
                    # If there are exactly 2 words after the comma
                    if len(name_after_comma.split(sep=" ")) == 2:
                        name_after_space1, name_after_space2 = name_after_comma.split(sep=" ")
                        pattern = rf"\b(?:{name_before_comma_space1}\s?{name_before_comma_space2}\s?{name_before_comma_space3}[,\s]*\s*)?{name_after_space1}\s?{name_after_space2}\b"
                        return pattern
                    # If there are exactly 3 words after the comma
                    elif len(name_after_comma.split(sep=" ")) == 3:
                        name_after_space1, name_after_space2, name_after_space3 = name_after_comma.split(sep=" ")
                        pattern = rf"\b(?:{name_before_comma_space1}\s?{name_before_comma_space2}\s?{name_before_comma_space3}[,\s]*\s*)?{name_after_space1}\s?{name_after_space2}\s?{name_after_space3}\b"
                        return pattern

        elif number_of_commas == 2:
            parts = locations.split(sep=",")
            
            # Check if there are exactly 3 parts (before, between, after)
            if len(parts) == 3:
                name_before_comma = parts[0].strip()  # First part before the first comma
                name_between_comma = parts[1].strip()  # Middle part between commas
                name_after_comma = parts[2].strip()  # Last part after the second comma
                
                # Check if there are two or three words in each part
                name_before_space1 = name_before_comma.split(sep=" ")[0]
                name_before_space2 = name_before_comma.split(sep=" ")[1] if len(name_before_comma.split(sep=" ")) > 1 else None
                
                name_between_space1 = name_between_comma.split(sep=" ")[0]
                name_between_space2 = name_between_comma.split(sep=" ")[1] if len(name_between_comma.split(sep=" ")) > 1 else None
                
                name_after_space1 = name_after_comma.split(sep=" ")[0]
                name_after_space2 = name_after_comma.split(sep=" ")[1] if len(name_after_comma.split(sep=" ")) > 1 else None
                name_after_space3 = name_after_comma.split(sep=" ")[2] if len(name_after_comma.split(sep=" ")) > 2 else None

                # Build the pattern conditionally
                pattern_parts = [rf"\b(?:{name_before_space1}"]
                if name_before_space2:
                    pattern_parts.append(rf"\s?{name_before_space2}")
                pattern_parts.append(rf"[,\s]*\s*)?")

                pattern_parts.append(f"{name_between_space1}")
                if name_between_space2:
                    pattern_parts.append(rf"\s?{name_between_space2}")
                
                pattern_parts.append(rf"\s?{name_after_space1}")
                if name_after_space2:
                    pattern_parts.append(rf"\s?{name_after_space2}")
                if name_after_space3:
                    pattern_parts.append(rf"\s?{name_after_space3}")

                pattern_parts.append(rf"\b")
                pattern = "".join(pattern_parts)
                return pattern
        
    # If there is no comma in the locations string
    elif has_comma == False:
        # If there are exactly 2 words in the locations
        if len(locations.split(sep=" ")) == 2:
            name_after_space1, name_after_space2 = locations.split(sep=" ")
            pattern = rf"\b{name_after_space1}\s?{name_after_space2}\b"
            return pattern
        # If there are exactly 3 words in the locations
        elif len(locations.split(sep=" ")) == 3:
            name_after_space1, name_after_space2, name_after_space3 = locations.split(sep=" ")
            pattern = rf"\b{name_after_space1}\s?{name_after_space2}\s?{name_after_space3}\b"
            return pattern

    # Default return if none of the conditions matched
    return None


stuff ={}
listOfStuff=[]

for locationDict in locations:
    pattern = create_dynamic_pattern(locations=locationDict['full_location_name'],has_comma=locationDict['has_comma'],number_of_commas=locationDict.get('number_of_commas',None))
    if pattern:
        compiled_pattern = re.compile(pattern, re.IGNORECASE)
        # print(pattern)
        stuff['compiled_pattern']=compiled_pattern
        stuff['full_location_name']=locationDict['full_location_name']
        listOfStuff.append(stuff)
        stuff={}
    else:
        pass
        # print(locationDict['full_location_name'])




    
def search_through_locations_provided(search_query:str)->str|None:    

    import os
    for sd in listOfStuff:
        match = sd['compiled_pattern'].search(search_query)
        if match:
            print("match",sd['full_location_name'])
            return sd['full_location_name']
            
        
        
    from itertools import product    
    words = search_query.split(sep=" ")
    locations = [listOflocations['full_location_name'] for listOflocations  in listOfStuff ]
    cartesian_product_of_locations_and_words = list(product(words,locations))

    for word,location  in cartesian_product_of_locations_and_words:
        if word in location:
            print("match found ",word,"---",location)
            return location
        elif word.upper() in location:
            print("match found word.in upper:",word,"---",location)
            return location
        else: 
            print("no match found for search query:",search_query)
            return None
            
        
        
        
        
        
        
        
        

