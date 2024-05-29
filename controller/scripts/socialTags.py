import json  
import requests

def runTest(entity):
  dataToOutput = {"entity": entity}
  try:
    url = f"https://web-check.xyz/api/social-tags?url={entity}"

    response = requests.get(url)
    data = json.loads(response.text)
    if "error" in data:
      dataToOutput["error"] = data
    else:
      if "title" in data:
        dataToOutput["title"] = data["title"]
      if "description" in data:
        dataToOutput["description"] = data["description"]
      if "canonicalUrl" in data:
        dataToOutput["canonical Url"] = data["canonicalUrl"]
      if "ogTitle" in data:
        dataToOutput["og Title"] = data["ogTitle"]
      if "ogType" in data:
        dataToOutput["og Type"] = data["ogType"]
      if "ogUrl" in data:
        dataToOutput["og Url"] = data["ogUrl"]
      if "ogDescription" in data:
        dataToOutput["og Description"] = data["ogDescription"]
      if "ogSiteName" in data:
        dataToOutput["og SiteName"] = data["ogSiteName"]
      if "twitterCard" in data:
        dataToOutput["twitter Card"] = data["twitterCard"]
      if "twitterTitle" in data:
        dataToOutput["twitte Title"] = data["twitterTitle"]
      if "twitterDescription" in data:
        dataToOutput["twitter Description"] = data["twitterDescription"]
      if "robots" in data:
        dataToOutput["robots"] = data["robots"]
      if "generator" in data:
        dataToOutput["generator"] = data["generator"]
      if "viewport" in data:
        dataToOutput["viewport"] = data["viewport"]
      if "favicon" in data:
        dataToOutput["favicon"] = data["favicon"]
    
  except:
    dataToOutput["error"] = "Data not found"
  return dataToOutput