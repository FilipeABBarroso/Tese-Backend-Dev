import json  
import requests

def runTest(entity):
  dataToOutput = {"entity": entity}
  try:
    url = f"https://web-check.xyz/api/headers?url={entity}"

    response = requests.get(url)
    data = json.loads(response.text)
    if "error" in data:
      dataToOutput["error"] = data["error"]
    else:
      if "date" in data:
        dataToOutput["date"] = data["date"]
      if "server" in data:
        dataToOutput["server"] = data["server"]
      if "content-type" in data:
        dataToOutput["content-type"] = data["content-type"]
      if "content-length" in data:
        dataToOutput["content-length"] = data["content-length"]
      if "connection" in data:
        dataToOutput["connection"] = data["connection"]
      if "strict-transport-security" in data:
        dataToOutput["strict-transport-security"] = data["strict-transport-security"]
      if "x-frame-options" in data:
        dataToOutput["x-frame-options"] = data["x-frame-options"]
      if "vary" in data:
        dataToOutput["vary"] = data["vary"]
      if "last-modified" in data:
        dataToOutput["last-modified"] = data["last-modified"]
      if "etag" in data:
        dataToOutput["etag"] = data["etag"]
      if "accept-ranges" in data:
        dataToOutput["accept-ranges"] = data["accept-ranges"]
      if "x-content-type-options" in data:
        dataToOutput["x-content-type-options"] = data["x-content-type-options"]
      if "x-xss-protection" in data:
        dataToOutput["x-xss-protection"] = data["x-xss-protection"]
      if "referrer-policy" in data:
        dataToOutput["referrer-policy"] = data["referrer-policy"]
      if "permissions-policy" in data:
        dataToOutput["permissions-policy"] = data["permissions-policy"]
      if "content-security-policy" in data:
        dataToOutput["content-security-policy"] = data["content-security-policy"]
      if "feature-policy" in data:
        dataToOutput["feature-policy"] = data["feature-policy"]
      if "cache-control" in data:
        dataToOutput["cache-control"] = data["cache-control"]
      if "x-drupal-dynamic-cache" in data:
        dataToOutput["x-drupal-dynamic-cache"] = data["x-drupal-dynamic-cache"]
      if "content-language" in data:
        dataToOutput["content-language"] = data["content-language"]
      if "expires" in data:
        dataToOutput["expires"] = data["expires"]
      if "x-generator" in data:
        dataToOutput["x-generator"] = data["x-generator"]
      if "x-drupal-cache" in data:
        dataToOutput["x-drupal-cache"] = data["x-drupal-cache"]
      if "last-modified" in data:
        dataToOutput["last-modified"] = data["last-modified"]
      if "x-sharepointhealthscore" in data:
        dataToOutput["x-sharepointhealthscore"] = data["x-sharepointhealthscore"]
      if "x-aspnet-version" in data:
        dataToOutput["x-aspnet-version"] = data["x-aspnet-version"]
      if "sprequestguid" in data:
        dataToOutput["sprequestguid"] = data["sprequestguid"]
      if "request-id" in data:
        dataToOutput["request-id"] = data["request-id"]
      if "sprequestduration" in data:
        dataToOutput["sprequestduration"] = data["sprequestduration"]
      if "spiislatency" in data:
        dataToOutput["spiislatency"] = data["spiislatency"]
      if "x-powered-by" in data:
        dataToOutput["x-powered-by"] = data["x-powered-by"]
      if "microsoftsharepointteamservices" in data:
        dataToOutput["microsoftsharepointteamservices"] = data["microsoftsharepointteamservices"]
      if "x-ms-invokeapp" in data:
        dataToOutput["x-ms-invokeapp"] = data["x-ms-invokeapp"]
      if "set-cookie" in data:
        dataToOutput["set-cookie"] = data["set-cookie"]
      if "transfer-encoding" in data:
        dataToOutput["transfer-encoding"] = data["transfer-encoding"]
      if "cf-cache-status" in data:
        dataToOutput["cf-cache-status"] = data["cf-cache-status"]
      if "cf-ray" in data:
        dataToOutput["cf-ray"] = data["cf-ray"]
      if "alt-svc" in data:
        dataToOutput["alt-svc"] = data["alt-svc"]
      if "link" in data:
        dataToOutput["link"] = data["link"]
      if "nel" in data:
        dataToOutput["nel"] = data["nel"]
      if "expect-ct" in data:
        dataToOutput["expect-ct"] = data["expect-ct"]
      if "x-permitted-cross-domain-policies" in data:
        dataToOutput["x-permitted-cross-domain-policies"] = data["x-permitted-cross-domain-policies"]
      if "p3p" in data:
        dataToOutput["p3p"] = data["p3p"]
      if "pragma" in data:
        dataToOutput["pragma"] = data["pragma"]
    
  except:
    dataToOutput["error"] = "Data not found"
  return dataToOutput