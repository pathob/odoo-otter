import requests
import sys

from otter.config import deserialize
from otter.odoo import cookies


def login(url, db, username, password):
    request_json = {
        "jsonrpc": "2.0",
        "params": {
            "db": db,
            "login": username,
            "password": password
        }
    }

    response = requests.post(url + '/web/session/authenticate', json=request_json)

    # before: and 'result' in response.json():
    if response.status_code != 200 or 'session_id' not in response.cookies:
        print("ERROR DURING LOGIN")
        sys.exit(1)

    uid = response.json()['result']['uid']
    session = response.cookies['session_id']

    return uid, session


def get_databases_json(url):
    request_json = {
        "jsonrpc": "2.0",
        "context": {}
    }

    # endpoint only for Odoo version >= 10
    response = requests.get(url + '/web/database/list', json=request_json)

    if response.status_code != 200 or 'result' not in response.json():
        print("ERROR FETCHING DATABASES")
        sys.exit(1)

    return response.json()['result']


def get_projects_json():
    cfg = deserialize()

    url = cfg['url']

    request_json = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "model": "project.project",
            "fields": [
                "id",
                "name",
                "active"
            ],
            "sort": "id ASC"
        }
    }

    response = requests.post(f"{url}/web/dataset/search_read", json=request_json, cookies=cookies())

    if response.status_code != 200 or 'result' not in response.json():
        print("ERROR")
        return None

    return response.json()['result']['records']


def get_project_tasks_json():
    cfg = deserialize()

    url = cfg['url']

    request_json = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "model": "project.task",
            "domain": [
                ["project_id", "!=", False]
            ],
            "fields": [
                "id",
                "name",
                "active",
                "project_id"
            ],
            "sort": "id ASC"
        }
    }

    response = requests.post(f"{url}/web/dataset/search_read", json=request_json, cookies=cookies())

    if response.status_code != 200 or 'result' not in response.json():
        print("ERROR")
        return None

    return response.json()['result']['records']


def get_records_json():
    cfg = deserialize()

    url = cfg['url']
    uid = cfg['uid']

    request_json = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "model": "account.analytic.line",
            "domain": [
                ["project_id", "!=", False],
                ["task_id", "!=", False],
                ["user_id", "=", uid]
            ],
            'date': '2021-01-04',
            "sort": "id ASC"
        }
    }

    response = requests.post(f"{url}/web/dataset/search_read", json=request_json, cookies=cookies())

    if response.status_code != 200 or 'result' not in response.json():
        print("ERROR")
        return None

    return response.json()['result']['records']


def post_record(record):
    cfg = deserialize()

    url = cfg['url']
    uid = cfg['uid']

    request_json = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "args": [
                {
                    "date": str(record['date']),
                    "unit_amount": record['duration'],
                    "name": record['names'],
                    "project_id": record['project_id'],
                    "task_id": record['task_id']
                }
            ],
            "model": "account.analytic.line",
            "method": "create",
            "kwargs": {
                "context": {
                    "uid": uid,
                }
            }
        }
    }

    response = requests.post(f"{url}/web/dataset/call_kw/account.analytic.line/create", json=request_json,
                             cookies=cookies())

    if response.status_code != 200 or 'result' not in response.json():
        print("ERROR")
        return None

    return response.json()['result']
