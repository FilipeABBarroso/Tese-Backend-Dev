import json  
import requests

def getTextSecurity(entity):
  url = f"https://web-check.xyz/api/security-txt?url={entity}"

  response = requests.get(url)
  save_file = open("outputs/savedata-txtSecurity.json", "w")  
  json.dump(json.loads(response.text), save_file, indent = 6)  
  save_file.close()  
  print("Done!")