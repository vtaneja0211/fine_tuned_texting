import json
import re

# Function to remove emojis from a string
def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F700-\U0001F77F"  # alchemical symbols
        u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        u"\U0001FA00-\U0001FA6F"  # Chess symbols
        u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        u"\U00002702-\U000027B0"  # Dingbats
        u"\U000024C2-\U0001F251"  # Enclosed characters
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub(r'', text)

# Function to check if a message matches specific unwanted phrases
def contains_unwanted_phrases(message):
    unwanted_phrases = [
        r"Reacted .* to your message",  # Matches "Reacted <emoji> to your message"
        r"missed your call",
        r"called you",
        r"missed your video call",
        r"missed a video call",
        r"The video call ended",
        r"Click for video:",
        r"IP Address:",
        r"Tapbacks:",
        r"GamePigeon message:",
        r"Your move",
        r"This message responded to an earlier message.",
        r"unsent a message!",
        r"This message was deleted from the conversation!",
        r"I won!",
        r"Lets play"
    ]
    for phrase in unwanted_phrases:
        if re.search(phrase, message, re.IGNORECASE):
            return True
    return False

# Function to check if a message contains a name with timestamp
def contains_name_with_timestamp(message):
    pattern = r"[A-Z][a-z]+\s[A-Z][a-z]+\s\(\w{3}\s\d{1,2},\s\d{4}\s\d{1,2}:\d{2}:\d{2}\s(?:am|pm)\)"
    return bool(re.search(pattern, message))

# Function to check if a message looks like a password
def is_password_like(message):
    password_patterns = [
        r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}',  # Strong password pattern
        r'\b(?:[A-Za-z\d@$!%*?&#]{10,})\b',  # Any string of 10+ characters with special characters
    ]
    for pattern in password_patterns:
        if re.search(pattern, message):
            return True
    return False

# Function to check if a message contains a link
def contains_link(message):
    url_pattern = r'(https?://\S+|www\.\S+)'
    return bool(re.search(url_pattern, message))


# Function to process JSON file
def merge_messages_from_file(file_path):
    try:
        # Load the JSON data from the file
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Remove messages containing unwanted patterns
        filtered_data = [
            chat for chat in data
            if '\u200e' not in chat['message']  # Remove messages containing \u200e
            and not is_password_like(chat['message'])  # Remove password-like messages
            and not contains_link(chat['message'])  # Remove messages with links
            and not contains_name_with_timestamp(chat['message'])  # Remove messages containing names with timestamps
            and not contains_unwanted_phrases(chat['message'])  # Remove messages with unwanted phrases
        ]

        # Process and merge messages
        merged_data = []
        for chat in filtered_data:
            # Replace problematic characters
            chat['message'] = (
                chat['message']
                .replace("\u2019", "'")  # Replace curly apostrophe
                .replace("\u2026", "...")  # Replace ellipsis
                .replace("\u201c", "\"")  # Replace opening quote
                .replace("\u201d", "\"")  # Replace closing quote
                .replace("\n",".")
            )
            
            # Remove emojis
            chat['message'] = remove_emojis(chat['message'])
            
            if not merged_data or merged_data[-1]['sender'] != chat['sender']:
                # Start a new entry if the sender is different or the list is empty
                merged_data.append(chat)
            else:
                # Merge messages from the same sender
                merged_data[-1]['message'] += f". {chat['message']}"
        
        return merged_data
    
    except Exception as e:
        print(f"Error processing file: {e}")
        return []

# Specify the input JSON file path
input_file = './data/chat_data.json'  # Replace with your actual JSON file path

# Process the file and merge messages
merged_output = merge_messages_from_file(input_file)

# Save the output to a new file or print it
output_file = './data/merged_chat_data.json'
with open(output_file, 'w') as file:
    json.dump(merged_output, file, indent=4)

print(f"Merged data has been saved to {output_file}")
