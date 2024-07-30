import json
import os
import re
import requests
from requests.auth import HTTPBasicAuth
import json

JIRA_BASE_URL = os.environ['JIRA_BASE_URL']
JIRA_API_TOKEN = os.environ['JIRA_API_TOKEN']
JIRA_USER_EMAIL = os.environ['JIRA_USER_EMAIL']


def post_jira_comment(issue_key, comment):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/comment"
    auth = HTTPBasicAuth(JIRA_USER_EMAIL, JIRA_API_TOKEN)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "body": {
            "content": [
                {
                    "content": [
                        {
                            "text": comment,
                            "type": "text"
                        }
                    ],
                    "type": "paragraph"
                }
            ],
            "type": "doc",
            "version": 1
        }
    })
    response = requests.post(url, headers=headers,
                             auth=auth, data=payload)
    return response


def lambda_handler(event, context):
    body = json.loads(event['body'])
    print(body)

    if 'object_kind' in body and body['object_kind'] == 'merge_request':
        # mr_title = body['object_attributes']['title']
        # mr_url = body['object_attributes']['url']

        # jira_issue_match = re.search(r'\b[A-Z]{2,}-\d+\b', mr_title)
        # if jira_issue_match:
        # jira_issue_key = jira_issue_match.group(0)
        comment = f"A new merge request has been raised: {'MR-1'}\n{'MR_LINK'}"
        response = post_jira_comment('KAN-2', comment)
        return {
            "statusCode": response.status_code,
            "body": response.text
        }

    return {
        "statusCode": 200,
        "body": json.dumps("No action taken")
    }
