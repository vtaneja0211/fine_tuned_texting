from bs4 import BeautifulSoup
from datetime import datetime

def extract_and_sort_chat_data(html_file, output_file):
    """
    Parses an HTML file containing chat data, removes all <span> content,
    sorts the remaining entries by timestamp, and writes it to a text file
    in the format: [MM/DD/YY, HH:MM:SS] Name: Text.

    Parameters:
        html_file (str): Path to the HTML file.
        output_file (str): Path to the output text file.
    """
    chat_data = []

    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Remove all <span> elements from the soup
    for span in soup.find_all('span'):
        span.decompose()

    # Find all the message containers
    messages = soup.find_all('div', class_='_a6-g')

    for message in messages:
        # Extract the name
        name = message.find('div', class_='_2ph_ _a6-h _a6-i')
        name_text = name.get_text(strip=True) if name else "Unknown"

        # Extract the main message text
        text_div = message.find('div', class_='_2ph_ _a6-p')
        text = text_div.get_text(strip=True) if text_div else "No message"

        # Extract the timestamp
        timestamp_div = message.find('div', class_='_a72d')
        timestamp_text = timestamp_div.get_text(strip=True) if timestamp_div else "Unknown time"

        # Convert timestamp to a sortable datetime object
        try:
            timestamp = datetime.strptime(timestamp_text, "%b %d, %Y %I:%M:%S %p")
        except ValueError:
            timestamp = None

        # Append data as a tuple
        chat_data.append((timestamp, timestamp_text, name_text, text))

    # Sort the chat data by timestamp
    chat_data.sort(key=lambda x: x[0] if x[0] else datetime.max)

    # Write to output file in desired format
    with open(output_file, 'w', encoding='utf-8') as out_file:
        for entry in chat_data:
            _, timestamp_text, name_text, text = entry
            # Format timestamp as [MM/DD/YY, HH:MM:SS]
            if entry[0]:
                formatted_timestamp = entry[0].strftime("[%m/%d/%y, %H:%M:%S]")
            else:
                formatted_timestamp = "[Unknown time]"
            # Write to the file
            out_file.write(f"{formatted_timestamp} {name_text}: {text}\n")

    print(f"Data extracted, filtered, sorted, and saved to {output_file}")

#usage
extract_and_sort_chat_data('./data/message_1.html', './data/chat.txt')
