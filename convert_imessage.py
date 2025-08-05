from datetime import datetime

def convert_chat_format(input_file, output_file, phone_number, name):
    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()
        
        output_lines = []
        current_sender = None
        formatted_time = None

        for line in lines:
            line = line.strip()
            
            # Check for date-time lines
            try:
                if "AM" in line or "PM" in line:
                    datetime_part = line.split(" (")[0].strip()
                    timestamp = datetime.strptime(datetime_part, "%b %d, %Y  %I:%M:%S %p")
                    formatted_time = timestamp.strftime("[%m/%d/%y, %H:%M:%S]")
                    continue  # Proceed to the next line after setting the timestamp
            except ValueError:
                pass  # Skip if it's not a valid datetime line

            # Check for sender lines
            if line.startswith("+") or line.startswith("Me"):
                if line.startswith("+"):
                    current_sender = name if phone_number in line else line
                elif line == "Me":
                    current_sender = "Varun Taneja"
                continue  # Proceed to the next line after setting the sender
            
            # Handle message lines
            if formatted_time and current_sender and line:
                output_lines.append(f"{formatted_time} {current_sender}: {line}")
            elif line:  # If the line doesn't fit, it's probably a system message or extra info
                output_lines.append(f"{formatted_time} System: {line}")
        
        # Write to the output file
        with open(output_file, 'w') as file:
            file.write("\n".join(output_lines))
        
        print(f"Conversion complete. Output saved to {output_file}")
    
    except Exception as e:
        print(f"An error occurred: {e}")


# Specify the input and output file paths, phone number, and name
input_file = "./data/input.txt"
output_file = "./data/chat.txt"
phone_number = #add phone number here
name = #add name here

# Convert the chat format
convert_chat_format(input_file, output_file, phone_number, name)
