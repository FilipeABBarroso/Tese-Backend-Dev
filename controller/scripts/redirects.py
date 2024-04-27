import json  
import requests

def getRedirects(entity):
  url = f"https://web-check.xyz/api/redirects?url={entity}"

  response = requests.get(url)
  save_file = open("outputs/savedata-redirects.json", "w")  
  json.dump(json.loads(response.text), save_file, indent = 6)  
  save_file.close()  
  print("Done!")