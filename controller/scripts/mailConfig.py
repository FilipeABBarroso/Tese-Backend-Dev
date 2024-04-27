import json  
import requests

def getMailConfig(entity):
  url = f"https://web-check.xyz/api/mail-config?url={entity}"

  response = requests.get(url)
  save_file = open("outputs/savedata-mail-config.json", "w")  
  json.dump(json.loads(response.text), save_file, indent = 6)  
  save_file.close()  
  print("Done!")