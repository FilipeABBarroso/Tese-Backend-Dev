import json  
import requests

def getSocialTags(entity):
  url = f"https://web-check.xyz/api/social-tags?url={entity}"

  response = requests.get(url)
  save_file = open("outputs/savedata-socialTags.json", "w")  
  json.dump(json.loads(response.text), save_file, indent = 6)  
  save_file.close()  
  print("Done!")