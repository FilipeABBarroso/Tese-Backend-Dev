import json  
import requests

def runTest(entity):
  dataToOutput = {"entity": entity}
  try:
    url = f"https://web-check.xyz/api/quality?url={entity}"

    response = requests.get(url)
    data = json.loads(response.text)
    dataToOutput["data"] = data
    if "error" in data:
      dataToOutput["error"] = data["error"]
    else:
      if "captchaResult" in data:
        dataToOutput["captcha result"] = data["captchaResult"]
      if "loadingExperience" in data and "metrics" in data["loadingExperience"]:
        if "mCUMULATIVE_LAYOUT_SHIFT_SCOREetrics" in data["loadingExperience"]["metrics"]:
          dataToOutput["loading-cumulative layout shift score"] = data["loadingExperience"]["metrics"]["CUMULATIVE_LAYOUT_SHIFT_SCORE"]["category"]
        if "EXPERIMENTAL_TIME_TO_FIRST_BYTE" in data["loadingExperience"]["metrics"]:
          dataToOutput["loading-experimental time to first byte"] = data["loadingExperience"]["metrics"]["EXPERIMENTAL_TIME_TO_FIRST_BYTE"]["category"]
        if "FIRST_CONTENTFUL_PAINT_MS" in data["loadingExperience"]["metrics"]:
          dataToOutput["loading-first contentful paint ms"] = data["loadingExperience"]["metrics"]["FIRST_CONTENTFUL_PAINT_MS"]["category"]
        if "FIRST_INPUT_DELAY_MS" in data["loadingExperience"]["metrics"]:
          dataToOutput["loading-first input delay ms"] = data["loadingExperience"]["metrics"]["FIRST_INPUT_DELAY_MS"]["category"]
        if "FIRST_INPUT_DELAY_MS" in data["loadingExperience"]["metrics"]:
          dataToOutput["loading-interaction to next paint"] = data["loadingExperience"]["metrics"]["FIRST_INPUT_DELAY_MS"]["category"]
        if "LARGEST_CONTENTFUL_PAINT_MS" in data["loadingExperience"]["metrics"]:
          dataToOutput["loading-largest contentful paint ms"] = data["loadingExperience"]["metrics"]["LARGEST_CONTENTFUL_PAINT_MS"]["category"]
      if "lighthouseResult" in data and "audits" in data["lighthouseResult"]:
        if "network" in data["lighthouseResult"]["audits"]:
          dataToOutput["network-rtt"] = data["lighthouseResult"]["audits"]["network-rtt"]["numericValue"]
        if "unused-javascript" in data["lighthouseResult"]["audits"]:
          dataToOutput["unused-javascript"] = data["lighthouseResult"]["audits"]["unused-javascript"]["numericValue"]
        if "duplicated-javascript" in data["lighthouseResult"]["audits"]:
          dataToOutput["duplicated-javascript"] = data["lighthouseResult"]["audits"]["duplicated-javascript"]["numericValue"]
        if "unminified-javascript" in data["lighthouseResult"]["audits"]:
          dataToOutput["unminified-javascript"] = data["lighthouseResult"]["audits"]["unminified-javascript"]["numericValue"]
        if "legacy-javascript" in data["lighthouseResult"]["audits"]:
          dataToOutput["legacy-javascript"] = data["lighthouseResult"]["audits"]["legacy-javascript"]["numericValue"]
        if "bootup-time" in data["lighthouseResult"]["audits"]:
          dataToOutput["bootup-time"] = data["lighthouseResult"]["audits"]["bootup-time"]["numericValue"]
        if "network-server-latency" in data["lighthouseResult"]["audits"]:
          dataToOutput["network-server-latency"] = data["lighthouseResult"]["audits"]["network-server-latency"]["numericValue"]
        if "uses-optimized-images" in data["lighthouseResult"]["audits"]:
          dataToOutput["uses-optimized-images"] = data["lighthouseResult"]["audits"]["uses-optimized-images"]["numericValue"]
        if "mainthread-work-breakdown" in data["lighthouseResult"]["audits"]:
          dataToOutput["mainthread-work-breakdown"] = data["lighthouseResult"]["audits"]["mainthread-work-breakdown"]["numericValue"]
        if "server-response-time" in data["lighthouseResult"]["audits"]:
          dataToOutput["server-response-time"] = data["lighthouseResult"]["audits"]["server-response-time"]["numericValue"]
        if "offscreen-images" in data["lighthouseResult"]["audits"]:
          dataToOutput["offscreen-images"] = data["lighthouseResult"]["audits"]["offscreen-images"]["numericValue"]
        if "unminified-css" in data["lighthouseResult"]["audits"]:
          dataToOutput["unminified-css"] = data["lighthouseResult"]["audits"]["unminified-css"]["numericValue"]
        if "total-byte-weight" in data["lighthouseResult"]["audits"]:
          dataToOutput["total-byte-weight"] = data["lighthouseResult"]["audits"]["total-byte-weight"]["numericValue"]
        if "uses-text-compression" in data["lighthouseResult"]["audits"]:
          dataToOutput["uses-text-compression"] = data["lighthouseResult"]["audits"]["uses-text-compression"]["numericValue"]
        if "dom-size" in data["lighthouseResult"]["audits"]:
          dataToOutput["dom-size"] = data["lighthouseResult"]["audits"]["dom-size"]["numericValue"]
        if "categories" in data["lighthouseResult"]:
          if "performance" in data["lighthouseResult"]["categories"]:
            dataToOutput["performance score"] = data["lighthouseResult"]["categories"]["performance"]["score"]
          if "accessibility" in data["lighthouseResult"]["categories"]:
            dataToOutput["accessibility score"] = data["lighthouseResult"]["categories"]["accessibility"]["score"]
          if "best-practices" in data["lighthouseResult"]["categories"]:
            dataToOutput["best-practices score"] = data["lighthouseResult"]["categories"]["best-practices"]["score"]
          if "seo" in data["lighthouseResult"]["categories"]:
            dataToOutput["seo score"] = data["lighthouseResult"]["categories"]["seo"]["score"]
          if "pwa" in data["lighthouseResult"]["categories"]:
            dataToOutput["pwa score"] = data["lighthouseResult"]["categories"]["pwa"]["score"]
        if "timing" in data["lighthouseResult"]:
          dataToOutput["total timing"] = data["lighthouseResult"]["timing"]["total"]
  except Exception as error:
    print(error)
    dataToOutput["error"] = "Data not found"
  return dataToOutput