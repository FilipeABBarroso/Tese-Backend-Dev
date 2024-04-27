import json  
import requests

def getStatus(entity):
  url = f"https://web-check.xyz/api/status?url={entity}"

  response = requests.get(url)
  save_file = open("outputs/savedata-status.json", "w")  
  json.dump(json.loads(response.text), save_file, indent = 6)  
  save_file.close()  
  print("Done!")