import json  
import requests

def getBlockLists(entity):
  url = f"https://web-check.xyz/api/block-lists?url={entity}"

  response = requests.get(url)
  save_file = open("outputs/savedata-blockLists.json", "w")  
  json.dump(json.loads(response.text), save_file, indent = 6)  
  save_file.close()  
  print("Done!")