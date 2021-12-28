import os


# Run iterator across all directories with "_" in name

current_directory = os.listdir('.')

for item in current_directory:
    
    if os.path.isdir(item) and item.find("_") != -1:
        print(item)
