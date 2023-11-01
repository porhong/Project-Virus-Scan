import requests
import json
import time
import operator

url = "https://www.virustotal.com/api/v3/urls"
treat_url = "https://www.virustotal.com/api/v3/popular_threat_categories"
headers = {
    "accept": "application/json",
    "x-apikey": "2162a3224e1b3688e7daf893f9178caa72699e6ba3231214276816181410314c",
    "content-type": "application/x-www-form-urlencoded"
}


def post_link(link_check):
    payload = {"url": link_check}
    response = requests.post(url, data=payload, headers=headers)
    result = response.text
    result_link = json.loads(result)
    result_link = result_link["data"]["links"]["self"]
    return result_link


def get_link_result(result_link):
    response = requests.get(result_link, headers=headers)
    threat_categories = requests.get(treat_url, headers=headers)
    threat_categories = json.loads(threat_categories.text)
    result = response.text
    # print(result)
    result = json.loads(result)
    result_after_scan = {}
    result_release = {}
    result_treat = []
    antiVirusCompany = list(result["data"]["attributes"]["results"].keys())
    treat = list(threat_categories["data"])
    for item in antiVirusCompany:
        result_by_company = result["data"]["attributes"]["results"][item]["engine_name"]
        result_confirm_by_company = result["data"]["attributes"]["results"][item]["result"]
        if result_confirm_by_company in treat:
            result_treat.append(result_confirm_by_company)
    result_treat = list(set(result_treat))
    result_summary = result["data"]["attributes"]["stats"]
    result_status = result["data"]["attributes"]["status"]
    result_release["Short_result"] = result_summary
    result_release["result_status"] = result_status
    result_release["treat_status"] = result_treat
    return result_release


def result_control(link):
    request_link = post_link(link)
    result = get_link_result(request_link)
    result_status = result["result_status"]
    while result_status == "queued":
        time.sleep(1)
        result = get_link_result(request_link)
        result_status = result["result_status"]
    return result


# a = result_control("https://kraitstones.help/")
# print(a)
