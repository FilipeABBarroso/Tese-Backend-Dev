import json  
import requests

def runTest(entity):
  url = f"https://web-check.xyz/api/txt-records?url={entity}"

  response = requests.get(url)
  '''save_file = open("outputs/savedata-txtRecords.json", "w")  
  json.dump(json.loads(response.text), save_file, indent = 6)  
  save_file.close()  '''
  data = json.loads(response.text)
  dataToOutput = {"entity": entity}
  try:
    dataToOutput["v"] = data["v"]
    
  except:
    dataToOutput["error"] = "Data not found"
  return dataToOutput