import requests
import json

url = "https://www.virustotal.com/api/v3/urls"
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
    result = response.text
    print(result)
    result = json.loads(result)
    result_after_scan = {}
    result_release = {}
    antiVirusCompany = list(result["data"]["attributes"]["results"].keys())
    # for item in antiVirusCompany:
    #     result_by_company = result["data"]["attributes"]["results"][item]["engine_name"]
    #     result_confirm_by_company = result["data"]["attributes"]["results"][item]["result"]

    #     result_after_scan[result_by_company] = result_confirm_by_company
    result_summary = result["data"]["attributes"]["stats"]
    result_release["Short_result"] = result_summary
    return result_release


result = get_link_result(post_link(
    "https://github.com/porhong/Project-Badbot.YT/blob/main/tt.py"))
print(result)
