import json
import os
import re
import requests
from requests.auth import HTTPBasicAuth
import json

JIRA_BASE_URL = os.environ['JIRA_BASE_URL']
JIRA_API_TOKEN = os.environ['JIRA_API_TOKEN']
JIRA_USER_EMAIL = os.environ['JIRA_USER_EMAIL']
JIRA_COMMENT_IDENTIFIER = "merge request"


def post_jira_comment(jira_issue_id, comment, mr_url):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{jira_issue_id}/comment"
    auth = HTTPBasicAuth(JIRA_USER_EMAIL, JIRA_API_TOKEN)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "text": comment,
                            "type": "text"
                        },
                        {
                            "type": "hardBreak"
                        },
                        {
                            "text": "MR link - ",
                            "type": "text"
                        },
                        {
                            "type": "text",
                            "text": mr_url,
                            "marks": [
                                {
                                    "type": "link",
                                    "attrs": {
                                        "href": mr_url
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    })

    response = requests.post(url, headers=headers,
                             auth=auth, data=payload)
    return response


def lambda_handler(event, context):
    body = json.loads(event['body'])

    if 'object_kind' in body and body['object_kind'] == 'merge_request':
        jira_issue_id = body['object_attributes']['title'].strip()
        mr_url = body['object_attributes']['url']

        if jira_issue_id:
            comment = f"Merge request for this issue has been updated."
            response = post_jira_comment(jira_issue_id, comment, mr_url)
            return {
                "statusCode": response.status_code,
                "body": response.json()
            }

    return {
        "statusCode": 200,
        "body": json.dumps("No action taken")
    }
