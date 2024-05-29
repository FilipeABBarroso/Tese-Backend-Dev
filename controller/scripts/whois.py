import urllib.parse, http.client
import json  

def runTest(entity):
  p = { 'key': '48F8616E8A28B2EDA79B6C4CB11C0BD1', 'domain': entity, 'format': 'json' }

  conn = http.client.HTTPSConnection("api.ip2whois.com")
  conn.request("GET", "/v2?" + urllib.parse.urlencode(p))
  res = conn.getresponse()
  data = json.loads(res.read())
  dataToOutput = {"entity": entity}
  try:
    dataToOutput["create date"] = data["create_date"]
    dataToOutput["update date"] = data["update_date"]
    dataToOutput["expire date"] = data["expire_date"]
    dataToOutput["domain age"] = data["domain_age"]
    dataToOutput["registrant name"] = data["registrant"]["name"]
    dataToOutput["registrant organization"] = data["registrant"]["organization"]
    dataToOutput["registrant country"] = data["registrant"]["country"]
    dataToOutput["admin name"] = data["admin"]["name"]
    dataToOutput["admin organization"] = data["admin"]["organization"]
    dataToOutput["admin country"] = data["admin"]["country"]
    
  except:
    if "error code" in data:
      dataToOutput["error code"] = data["error"]["error_code"]
      dataToOutput["error message"] = data["error"]["error_message"]
    else:
      dataToOutput["error"] = "Data not found"
  return dataToOutput