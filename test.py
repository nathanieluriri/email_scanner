import re

# Sample locations (as per your example)
locations = [
    {"has_comma": False, "full_location_name": "PPU Ajah"},
    {"has_comma": True, "full_location_name": "LAG, ONIRU"},
    {"has_comma": True, "full_location_name": "LAG , ONIRU , Victoria Island"},
    {"has_comma": False, "full_location_name": "Victoria Island"}
]

# Function to create a dynamic regex pattern
def create_dynamic_pattern(locations):
    # Start with an empty list to store the dynamic parts for each location name
    location_parts = []
    pattern = rf"\b(?:{name_before_comma}[,\s]*\s*)?{name_after_space1}\s?{name_after_space2}\b"
    for location in locations:
        # Extract the location name and split into words
        location_name = location["full_location_name"]
        
        # Escape special regex characters in the location names (e.g., commas)
        location_name_escaped = re.escape(location_name)
        
        # Replace any commas with a pattern that allows for optional spaces after the comma
        location_name_pattern = location_name_escaped.replace(",", r"[,\s]*")
        
        # Add the pattern to the list of location parts
        location_parts.append(location_name_pattern)
    
    # Combine all the location patterns with an OR (`|`) operator
    dynamic_pattern = r"\b(" + r"|".join(location_parts) + r")\b"
    
    return dynamic_pattern

# Create the dynamic regex pattern
dynamic_pattern = create_dynamic_pattern(locations)

# Test the pattern on a sample text
sample_text = "I live in PPU Ajah, but I often visit LAG, ONIRU and Victoria Island."

# Use the pattern to search for matches in the sample text
matches = re.findall(dynamic_pattern, sample_text)

# Print out the matches
print("Matches found:", matches)
