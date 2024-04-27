import json  
import requests

def getRank(entity):
  url = f"https://web-check.xyz/api/rank?url={entity}"

  response = requests.get(url)
  save_file = open("outputs/savedata-rank.json", "w")  
  json.dump(json.loads(response.text), save_file, indent = 6)  
  save_file.close()  
  print("Done!")