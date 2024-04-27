import json  
import requests

def getFeatures(entity):
  url = f"https://web-check.xyz/api/features?url={entity}"

  response = requests.get(url)
  save_file = open("outputs/savedata-features.json", "w")  
  json.dump(json.loads(response.text), save_file, indent = 6)  
  save_file.close()  
  print("Done!")