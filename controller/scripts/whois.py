import urllib.parse, http.client
import json  

def runTest(entity):
  p = { 'key': '48F8616E8A28B2EDA79B6C4CB11C0BD1', 'domain': entity, 'format': 'json' }

  conn = http.client.HTTPSConnection("api.ip2whois.com")
  conn.request("GET", "/v2?" + urllib.parse.urlencode(p))
  res = conn.getresponse()
  jsonRes = json.loads(res.read())
  '''save_file = open("outputs/savedata-whois.json", "w")  
  json.dump(jsonRes, save_file, indent = 6)  
  save_file.close()  '''
  return jsonRes