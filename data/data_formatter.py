import json

# Load the JSON file
with open("actionAUGUST.json", "r") as file:
    data = json.load(file)

# Convert data to JSONL format
with open("output.jsonl", "w") as jsonl_file:
    for entry in data:
        if entry.get('reason') !=None and entry.get('maintenenance')!=None and entry.get('category') !=None and entry.get('equipment') !=None and entry.get('action')!=None:
            jsonl_entry = {
                "input": f"'action': '{entry['action']}'",
                "target": (
                    f"'reason': '{entry['reason']}', "
                    f"'maintenance': '{entry['maintenenance']}', "
                    f"'category': '{entry['category']}', "
                    f"'equipment': '{entry['equipment']}'"
                )
            }
            jsonl_file.write(json.dumps(jsonl_entry) + "\n")

print("JSONL file created: output.jsonl")
