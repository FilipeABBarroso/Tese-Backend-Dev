import json  
import requests

def getCookies(entity):
  url = f"https://web-check.xyz/api/cookies?url={entity}"
  response = requests.get(url)
  save_file = open("outputs/savedata-cookies.json", "w")  
  json.dump(json.loads(response.text), save_file, indent = 6)  
  save_file.close()  
  print("Done!")