import json

# Input and output file names
input_file = './data/merged_chat_data.json'
output_file = './data/final_output.jsonl'

# Define the system message
system_message = {"role": "system", "content": "You are a chatbot who replies to texts"}

# Load the input JSON
with open(input_file, 'r') as infile:
    data = json.load(infile)

# Skip the first message if it's from "Varun Taneja"
start_index = 0
if data[0]["sender"] == "Varun Taneja":
    start_index = 1

# Open the output file in append mode
with open(output_file, 'a') as outfile:
    for i in range(start_index, len(data) - 1, 2):  # Iterate in pairs
        user_message = {"role": "user", "content": data[i]["message"]}
        assistant_message = {"role": "assistant", "content": data[i + 1]["message"]}

        # Include only complete sets (system, user, assistant)
        if user_message["content"] and assistant_message["content"]:
            messages = [system_message, user_message, assistant_message]
            jsonl_entry = {"messages": messages}
            json.dump(jsonl_entry, outfile)
            outfile.write('\n')

print(f"Data appended to {output_file}")
