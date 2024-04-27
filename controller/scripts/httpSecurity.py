import json  
import requests

def getHttpSecurity(entity):
  url = f"https://web-check.xyz/api/http-security?url={entity}"

  response = requests.get(url)
  save_file = open("outputs/savedata-httpSecurity.json", "w")  
  json.dump(json.loads(response.text), save_file, indent = 6)  
  save_file.close()  
  print("Done!")