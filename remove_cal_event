#!/bin/python3

import json
import getopt
import sys

filename = "calendar.json"
base_path = sys.path[0]
data_path = base_path + "/" + filename

def remove_event(event_id):
    data = []

    with open(data_path) as fileptr:
        data = json.load(fileptr)
        fileptr.close()

    new_data = []
    for event in data:
        if event["id"] != event_id:
            new_data.append(event)

    with open(data_path, 'w') as fileptr:
        fileptr.write(json.dumps(new_data))
        print("Delete successful!")
        fileptr.close()

def main():
    # Get arguments
    argv = sys.argv[1:]
    args = getopt.getopt(argv, "i:")
    args = args[0]

    selected_id = None

    # Parse arguments
    for key, val in args:
        if key == "-i":
            selected_id = int(val)

    if selected_id == None:
        print("ID (-i) is required")
        return

    remove_event(selected_id)
    
if __name__ == "__main__":
    main()
