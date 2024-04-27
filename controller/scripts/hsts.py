import json  
import requests

def gethsts(entity):
  url = f"https://web-check.xyz/api/hsts?url={entity}"

  response = requests.get(url)
  save_file = open("outputs/savedata-hsts.json", "w")  
  json.dump(json.loads(response.text), save_file, indent = 6)  
  save_file.close()  
  print("Done!")