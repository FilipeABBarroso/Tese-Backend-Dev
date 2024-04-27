import json  
import requests

def getThreats(entity):
  url = f"https://web-check.xyz/api/threats?url={entity}"

  response = requests.get(url)
  save_file = open("outputs/savedata-threats.json", "w")  
  json.dump(json.loads(response.text), save_file, indent = 6)  
  save_file.close()  
  print("Done!")