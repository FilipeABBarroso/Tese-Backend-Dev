import json  
import requests

def getQuality(entity):
  url = f"https://web-check.xyz/api/quality?url={entity}"

  response = requests.get(url)
  save_file = open("outputs/savedata-quality.json", "w")  
  json.dump(json.loads(response.text), save_file, indent = 6)  
  save_file.close()  
  print("Done!")