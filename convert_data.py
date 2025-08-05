import json
import re
import sys

# Function to parse a single line of the chat
def parse_line(line):
    # Regex to match WhatsApp message pattern
    match = re.match(r"\[(.*?)\] (.*?): (.*)", line)
    if match:
        timestamp, sender, message = match.groups()
        return {"timestamp": timestamp, "sender": sender, "message": message}
    else:
        # Handle non-message lines (e.g., omitted content)
        omitted_match = re.match(r"\[(.*?)\] (.*?): (.*)", line)
        if omitted_match:
            timestamp, sender = omitted_match.groups()[:2]
            return {"timestamp": timestamp, "sender": sender, "message": "omitted content"}
    return None

# Function to process the chat data
def process_chat(chat_lines):
    chat_data = []
    for line in chat_lines:
        parsed_line = parse_line(line)
        if parsed_line:
            chat_data.append(parsed_line)
    return chat_data

# Check if a file name is provided as a command-line argument
if len(sys.argv) < 2:
    print("Usage: python script.py <file_path>")
    sys.exit(1)

file_path = sys.argv[1]

# Load chat data from the specified text file
try:
    with open(file_path, "r", encoding="utf-8") as file:
        chat_lines = file.readlines()
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
    sys.exit(1)

# Process the chat data
structured_chat = process_chat(chat_lines)

# Save to JSON file
output_file = "./data/chat_data.json"
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(structured_chat, json_file, indent=4, ensure_ascii=False)

print(f"Chat data has been successfully converted to JSON format and saved to '{output_file}'!")
