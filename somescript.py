import os
import requests
import sys


# check if user exists
def user_exists(user):
    url = 'https://api.github.com/search/users?q=' + user
    r = requests.get(url)
    main = r.json()
    if main['total_count'] == 0:
        return False
    else:
        return True


# check if organization exists
def get_org_exists(org_name):
    url = 'https://api.github.com/orgs/' + org_name
    r = requests.get(url)
    org = r.json()
    if org['avatar_url']:
        return True
    else:
        return False


# check organization avatar
def get_org_avatar_url(org_name):
    url = 'https://api.github.com/orgs/' + org_name
    r = requests.get(url)
    org = r.json()
    if 'avatar_url' in org:
        return org['avatar_url']
    elif 'message' in org:
        return org['message']


# check organization id
def get_org_id(org_name):
    url = 'https://api.github.com/orgs/' + org_name
    r = requests.get(url)
    org = r.json()
    if 'id' in org:
        return org['id']
    elif 'message' in org:
        return org['message']


# adding user to organization
def add_to_org(username):
    GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
    # GITHUB_TOKEN = config('GITHUB_TOKEN', default='')
    ORGANIZATION_NAME = os.environ['ORGANIZATION_NAME']
    # ORGANIZATION_NAME = config('ORGANIZATION_NAME', default='')
    url = 'https://api.github.com/orgs/' + ORGANIZATION_NAME + '/memberships/' + username + '?role=member'
    if user_exists(username):
        r = requests.put(url, headers={'Authorization': 'Bearer %s' % GITHUB_TOKEN})
        main = r.json()
        if 'state' in main and main['state'] == 'pending':
            return "OK, Check your EMAIL"
        else:
            return main['message']
    else:
        return 'User not found. Please check your spelling'


output = add_to_org(sys.argv[1])
# print(sys.argv[1])
print(output)
