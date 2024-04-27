import json  
import requests

def getRobots(entity):
  url = f"https://web-check.xyz/api/robots-txt?url={entity}"

  response = requests.get(url)
  save_file = open("outputs/savedata-robots.json", "w")  
  json.dump(json.loads(response.text), save_file, indent = 6)  
  save_file.close()  
  print("Done!")