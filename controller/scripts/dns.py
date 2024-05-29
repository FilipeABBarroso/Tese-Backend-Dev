import json  
import requests

def flatten_dict(d, parent_key='', sep='_'):
  items = []
  for k, v in d.items():
    new_key = f"{parent_key}{sep}{k}" if parent_key else k
    if isinstance(v, dict):
      items.extend(flatten_dict(v, new_key, sep=sep).items())
    elif isinstance(v, list):
      for i, item in enumerate(v, start=1):
        if isinstance(item, dict):
          items.extend(flatten_dict(item, f"{new_key}{sep}{i}", sep=sep).items())
        else:
          items.append((f"{new_key}{sep}{i}", item))
    else:
      items.append((new_key, v))
  return dict(items)

def runTest(entity):
  dataToOutput = {"entity": entity}
  try:
    url = f"https://web-check.xyz/api/dns?url={entity}"

    response = requests.get(url)
    data = json.loads(response.text)
    if "error" in data:
      dataToOutput["error"] = data["error"]
    else:
      for key, value in data.items():
        dataToOutput.update(flatten_dict({key: value}))
    
  except:
    dataToOutput["error"] = "Data not found"
  return dataToOutput