import json  
import requests

def getLinkedPages(entity):
  url = f"https://web-check.xyz/api/linked-pages?url={entity}"

  response = requests.get(url)
  save_file = open("outputs/savedata-linkedPages.json", "w")  
  json.dump(json.loads(response.text), save_file, indent = 6)  
  save_file.close()  
  print("Done!")