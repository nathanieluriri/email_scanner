# Example dictionary structure
data = {
    "thread_group": [
        {"subject": "RE: FAULTY CABINET", "thread_index": 1},
        {"subject": "FW: FAULTY CABINET", "thread_index": 2},
        {"subject": "FAULTY CABINET", "thread_index": 3}
    ],
    "thread_Group_Name": "FAULTY CABINET"
}

# You could use frozenset to convert a mutable set (list or dictionary) into an immutable one
thread_group_frozen = frozenset(tuple(d.items()) for d in data["thread_group"])

# Create a set of these frozensets
my_set = {thread_group_frozen}

# Output the set
print(my_set)
