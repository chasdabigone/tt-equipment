import sys
import argparse
import re
import collections
from collections import OrderedDict
import json



#create dictionary from database file
result = []
with open("Equip_DB.txt", "r", encoding='utf-8') as infile:
    for line in infile:
        if line.startswith("Object"):             #Check if line starts with 'Object'
            result.append([line, []])        #Create new list with format --> [key, [list of corresponding text]]
        else:
            result[-1][1].append(line)       #Append text to previously found key. 

eqDict ={k: "".join(v) for k, v in result}   #Form required dictionary.

#build wearing equipment list

wearLocs = ["light","finger1","finger2","neck1","neck2","body1","body2","body3","body4","body5","body6","head","legs","feet","hands1","hands2","arms","about1","about2","about3","about4","waist","shield","hold","wrist1","wrist2","wield1","wield2","ears","eyes","back","face","ankle1","ankle2"]
charStats = ["hp","mana","str","int","wis","dex","con","cha","lck"]
finalDict = collections.defaultdict(list)



def save_json(entries):
    name = charname.get()
    field1 = list()
    text1 = list()
    for entry in entries:
        field1.append(entry[0])
        text1.append(entry[1].get())
    
    equip = dict(zip(field1, text1))

    with open(name+".char", "w") as f:
        json.dump(equip, f)

def searcheq(entries):
  """
  Compares entries to keys in eqDict (case-insensitive) and returns matching key-value pairs.

  Args:
      entries: A list of tuples containing key-value pairs.

  Returns:
      A list of tuples containing matching key-value pairs from eqDict.
  """
  itemdata = []
  for key, value in eqDict.items():
    # Convert key and entries to lowercase for case-insensitive comparison
    lower_key = key.lower()
    if entries.lower() in lower_key:  # Check if entry is in any part of the key (case-insensitive)
        key = key.rstrip('\n')
        value = value.rstrip('\n')
        itemdata.append((key, value))

  if len(itemdata) > 5:
      print("More than 5 items matched. Narrow your search.")
  elif len(itemdata) < 1:
      print("No items matched.")
  else:
    for k, v in itemdata:
        print(k)
        print(v)
        print('')

def fetch(entries):

    global dic
    dic = OrderedDict()
    dic['hp'] = 0
    dic['mana'] = 0
    dic[' '] = ' '
    dic['damage roll'] = 0
    dic['hit roll'] = 0
    dic['  '] = ' '
    dic['strength'] = 0
    dic['intelligence'] = 0
    dic['wisdom'] = 0
    dic['dexterity'] = 0
    dic['constitution'] = 0
    dic['charisma'] = 0
    dic['luck'] = 0
    dic['   '] = ' '
    
    hp = 0
    mana = 0
    strength = 0
    intelligence = 0
    wisdom = 0
    dexterity = 0
    constitution = 0
    charisma = 0
    luck = 0


    for entry in entries:
    
        wearingDict = eqDict.copy()
        field = entry[0]
        text  = entry[1]
        if text != "":
            if field in wearLocs:

                for key, value in list(wearingDict.items()):
                    if text not in key:
                        del wearingDict[key]

                if len(wearingDict) < 1:
                    print (str(text) + " error: no items matched")
                else:
                    
                    if next(iter(wearingDict)) in finalDict:
                    
                        searchKey = list(wearingDict.keys())[0]
                        searchVal = list(wearingDict.values())[0]
                    
                        finalDict[searchKey] = finalDict[searchKey] + searchVal
                    else:
                        finalDict.update(wearingDict)
            if field in charStats:

                if field == 'hp':
                    hp = text
                if field == 'mana':
                    mana = text
                if field == 'str':
                    strength = text
                if field == 'int':
                    intelligence = text
                if field == 'wis':
                    wisdom = text
                if field == 'dex':
                    dexterity = text
                if field == 'con':
                    constitution = text
                if field == 'cha':
                    charisma = text
                if field == 'lck':
                    luck = text

                
                
    armorClassList = [] # to tally equip armor class
    affectList = [] # affects by number
    affectList2 = [] # affects with class restrict
    otherAffs = [] # word affects
    resistList = [] # list of resists
    susceptList = [] # list of suscepts
    statAffs = ['hp','mana','strength','intelligence','wisdom','dexterity','constitution','charisma','luck'] #affects from stats and base
    
    for key, value in list(finalDict.items()):
        
        armorClassList = armorClassList + re.findall(r'Armor class is (-?[0-9]+) of (-?[0-9]+)', value)
        affectList = affectList + re.findall(r'Affects (.*) by (-?[0-9]+|-?[0-9]+%)\.', value)
        affectList2 = affectList2 + re.findall(r'Affects (.*) by (-?[0-9]+) if class is (.*)\.', value)
        otherAffs = otherAffs + re.findall(r'Affects affected_by by (.*)', value)
        resistList = resistList + re.findall(r'Affects resistant:(.*) by (-?[0-9]+)', value)
        susceptList = susceptList + re.findall(r'Affects susceptible:(.*) by (-?[0-9]+)', value)
       
    # create dictionary of resists
    resDic = {}
    # combine like items
    for item in resistList:
        if item[0] in resDic:
            resDic[item[0]] = resDic[item[0]] + int(item[1])
        else:
            resDic[item[0]] = int(item[1])
    
    susDic = {}
    for item in susceptList:
        if item[0] in susDic:
            susDic[item[0]] = susDic[item[0]] + int(item[1])
        else:
            susDic[item[0]] = int(item[1])

    dmgDic = {}      
    for item in affectList:
        if "resistant" in item[0] or "susceptible" in item[0]:
            pass
        elif "wait time" in item[0] or "damage of" in item[0]:
            change = float(item[1].rstrip("%")) 
            dmgDic[item[0]] = dmgDic.get(item[0], 0) + int(change)
            
        else: 
            dic[item[0]] = dic.get(item[0], 0) + int(item[1])
    
    for item in armorClassList:

        dic['Equipment AC'] = dic.get('Equipment AC', 0) + int(item[1])
        
    
    # new dictionary for affectList2
    affectList2Dic = {}
    for item in affectList2:
        affectList2Dic[item[0]] = str(affectList2Dic.get(item[0], '')) + str(item[1])
        affectList2Dic[item[0]] = str(affectList2Dic.get(item[0], 0)) + " if " + str(item[2])

    for k in statAffs:
        
        if k == 'hp':
            dic[k] = dic.get(k, 0) + int(hp)
        if k == 'mana':
            dic[k] = dic.get(k, 0) + int(mana)
        if k == 'strength':
            dic[k] = dic.get(k, 0) + int(strength)
        if k == 'intelligence':
            dic[k] = dic.get(k, 0) + int(intelligence)
        if k == 'wisdom':
            dic[k] = dic.get(k, 0) + int(wisdom)
        if k == 'dexterity':
            dic[k] = dic.get(k, 0) + int(dexterity)
        if k == 'constitution':
            dic[k] = dic.get(k, 0) + int(constitution)
        if k == 'charisma':
            dic[k] = dic.get(k, 0) + int(charisma)
        if k == 'luck':
            dic[k] = dic.get(k, 0) + int(luck)

    

    #otherAffs = str(otherAffs).replace(' ', '\n')
       

    output = []

    # Collecting numerical stats
    for k, v in dic.items():
        if isinstance(v, int):
            output.append(f"\033[1;33m{k}:\033[0m {v}")  # Red color for numerical stats

    # Collecting affects with numerical values
    for k, v in affectList2Dic.items():
        output.append(f"\033[1;33mAffects {k}:\033[0m {v}")  # Green color for affects with numerical values

    # Collecting resistances
    for item, value in resDic.items():
        output.append(f"\033[1;33mResist {item}:\033[0m {value}%")  # Red color for resistances
    # Collecting suscepts
    for item, value in susDic.items():
        output.append(f"\033[1;33mSuscept {item}:\033[0m {value}%")  # Red color for resistances
    # Collecting wait time and dmg
    for item, value in dmgDic.items():
        if "damage of" in item:
            value = str(value) + "%"
            output.append(f"\033[1;33m{item}:\033[0m {value}")
        else:
          output.append(f"\033[1;33m{item}:\033[0m {value}")

    # Handling other affects
    if otherAffs:
        output.append(f"\033[1;33mAffects affected_by:\033[0m {otherAffs}")  # Yellow color for other affects

    # Calculate maximum width for the first column
    max_width = max(len(line.split(":")[0]) for line in output) + 8  # add 5 for spacing

    # Combine elements to take up 2 per line with evenly spaced columns
    combined_output = []
    for i in range(0, len(output), 2):
        if i + 1 < len(output):
            first_col = output[i].ljust(max_width)
            second_col = output[i + 1]
            combined_output.append(f"{first_col}    {second_col}")
        else:
            combined_output.append(output[i])
    # add a blank line to the end
    combined_output.append("")

    return combined_output
                                             
def parse_input(input_str):
    # Define a regex pattern to extract key-value pairs
    pattern = r'\{(\w+)\}(\{.*?\})'
    matches = re.findall(pattern, input_str)
    if matches:
        # Create a dictionary from the matches
        data = {}
        for key, value in matches:
            key = key.strip('{}')
            value = value.strip('{}')
            key = key.strip(' ')
            value = value.strip(' ')
            data[key] = value
    
        return data 
    else:
        # Fallback to splitting by whitespace
        return input_str.split() 

def main():

  entries = []

  try:
    parser = argparse.ArgumentParser(description='Process equipment data.')
    parser.add_argument('input_data', type=str, nargs='?', help='Input data string (optional)')  # Make it optional
    parser.add_argument('keywords', type=str, nargs='*', help='Keywords to search for (optional)')  # New optional argument
    args = parser.parse_args()

    if args.keywords:
      keywords = args.keywords  # Join keywords with spaces
    elif args.input_data:
      input_str = args.input_data
    else:
      raise ValueError("Please provide either input data or keywords")

    # Parse the input data
    if not args.keywords:
        equipment_data = parse_input(input_str)

        # Populate equipment entries for 'fetch' or 'searcheq' function
        for key, value in equipment_data.items():
            entries.append((key, value))
        
        result = fetch(entries)    # Call fetch otherwise
        for line in result:
            print(line)
    else:
        combined_keywords = " ".join(keywords)
        result = searcheq(combined_keywords)


  except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)

main()
