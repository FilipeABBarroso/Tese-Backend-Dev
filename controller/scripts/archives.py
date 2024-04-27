import json  
import requests

def getArchives(entity):
  url = f"https://web-check.xyz/api/archives?url={entity}"

  response = requests.get(url)
  print("No info in Archives", response.text)
  if response.status_code == 200:
    save_file = open("outputs/savedata-archives.json", "w")  
    json.dump(json.loads(response.text), save_file, indent = 6)  
    save_file.close()  
  else: 
    print("No info in Archives")
  
  print("Done!")