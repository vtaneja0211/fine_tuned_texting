import os
import subprocess

# Folder containing the files to process
input_folder = "./data/chats"

# List all files in the folder
files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

# Paths to the Python scripts
script1 = "convert_data.py"
script2 = "merge_data.py"
script3 = "to_jsonl.py"

# Iterate through each file
for file in files:
    file_path = os.path.join(input_folder, file)
    
    print(f"Processing {file_path}...")
    
    
    # Run the first script
    subprocess.run(["python3", script1, file_path], check=True)
 
    # Run the second script
    subprocess.run(["python3", script2], check=True)
    
    # Run the third script
    subprocess.run(["python3", script3], check=True)
    
    print(f"Finished processing {file_path}\n")

