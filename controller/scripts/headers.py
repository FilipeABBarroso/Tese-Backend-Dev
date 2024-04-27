import json  
import requests

def getHeaders(entity):
  url = f"https://web-check.xyz/api/headers?url={entity}"

  response = requests.get(url)
  save_file = open("outputs/savedata-headers.json", "w")  
  json.dump(json.loads(response.text), save_file, indent = 6)  
  save_file.close()  
  print("Done!")