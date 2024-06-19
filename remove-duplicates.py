# Step 1: Create dictionary from database file
result = []
with open("Equip_DB.txt", "r", encoding='utf-8') as infile:
    for line in infile:
        if line.startswith("Object"):
            result.append([line.strip(), []])  # Strip to remove any extra whitespace/newlines
        else:
            result[-1][1].append(line)  # Append text to the last found key.


# Initialize an empty dictionary to store the results
eqDict = {}
dupeCount = 0
# Iterate through each key-value pair in the 'result' dictionary
for k, v in result:
  # Check if the value is not None
  if k not in eqDict:
    # Join the elements of the value (assuming it's iterable) into a string
    joined_value = "".join(v)
    # Remove leading/trailing whitespace from the joined string
    stripped_value = joined_value.strip()
    # Add the key-value pair to the eqDict dictionary
    eqDict[k] = stripped_value
  else:
    dupeCount = +1
        
# Step 3: Write updated eqDict back to Equip_DB.txt, overwriting the old file
with open("Equip_DB.txt", "w", encoding='utf-8') as outfile:
    for key, value in eqDict.items():
        outfile.write(key + "\n")  # Write the key
        outfile.write(value + "\n\n")  # Write the corresponding text

if dupeCount > 0:
   print("Duplicate item not added to Equip_DB.txt")
else:
   print("Equip_DB.txt updated with new item")