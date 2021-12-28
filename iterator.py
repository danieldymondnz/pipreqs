
import os
import json


# Run iterator across all directories with "_" in name

pipreqs_full_path = os.path.dirname(os.path.abspath(__file__))
pipreqs_executable_full_path = os.path.join(pipreqs_full_path, "pipreqs/pipreqs.py")
print(pipreqs_executable_full_path)
working_full_path = os.getcwd()

current_directory = os.listdir(working_full_path)


# List of Local Packages to analyse
packages = []

# Dictionary containing list of Dependancies
dependencies = {}



for item in current_directory:
    
    if os.path.isdir(item) and item.find("_") != -1:
        packages.append(item)
        
num_packages = len(packages)
        
# For each Package, run the `pipreqs` script and interpolate data into dependencies dict.
for local_package_idx in range(num_packages):
    
    local_package = packages[local_package_idx]
    
    # Run the pipreqs
    full_path_to_package = os.path.join(working_full_path, local_package)
    command = "python3 " + pipreqs_executable_full_path + " " + full_path_to_package + " --force"
    os.system(command)
    
    # Open the text File
    file_created = False
    full_path_to_text_file = os.path.join(full_path_to_package + "/requirements.txt")
    try:
        with open(full_path_to_text_file, 'r') as text_file:
            
            file_created = True
            package_dependancies = text_file.readlines()
    
            # Strips the newline character
            for line in package_dependancies:
                
                dependancy_name = line.split("=")[0]
                if dependancy_name == "\n":
                    continue
                if dependancy_name not in dependencies.keys():
                    dependencies[dependancy_name] = [0] * num_packages
                dependencies[dependancy_name][local_package_idx] = 1
    except:
        continue
    
    # Delete File
    if file_created:
        os.remove(full_path_to_text_file)
    
# Export dependencies
text_export_path = os.path.join(working_full_path, "results.csv")
# with open(text_export_path, "w") as out_file:
#     json.dump(dependencies, out_file)
# print("SUCCESS: " + text_export_path)


import csv

with open(text_export_path, 'w', newline='') as outcsv:
    writer = csv.writer(outcsv)
    writer.writerow(['dependency_name'] + packages)

    for dependency in dependencies.keys():
        writer.writerow([dependency] + dependencies[dependency])
print("SUCCESS: " + text_export_path)        