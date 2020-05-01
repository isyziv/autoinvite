import sys
from django.shortcuts import render
from django.views.generic import TemplateView
import requests
from subprocess import run, PIPE


# Create your views here.
class HomePage(TemplateView):
    template_name = 'index.html'


class SuccessPage(TemplateView):
    template_name = 'success.html'


class ErrorPage(TemplateView):
    template_name = 'error.html'


# def add(request):
#     url = 'https://api.github.com/orgs/gdgikorodu/memberships/geektutor'
#     r = requests.get(url, headers={'Authorization': 'Bearer %s' % 'ed4daa9aa17780a960297976ee8bdbb82f54a390'})
#     main = r.json()
#     if r.status_code == 200 and main['state'] == 'pending':
#         pass
#     if r.status_code == 200 and main['state'] == 'active':
#         pass


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
    url = 'https://api.github.com/orgs/gdgikorodu/memberships/' + username + '?role=member'
    if user_exists(username):
        r = requests.put(url, headers={'Authorization': 'Bearer %s' % 'ed4daa9aa17780a960297976ee8bdbb82f54a390'})
        main = r.json()
        if 'state' in main and main['state'] == 'pending':
            return "OK, Check your EMAIL"
        else:
            return main['message']
    else:
        return 'User not found. Please check your spelling'


def output(request):
    inp = request.POST.get('github')
    out = run([sys.executable, './somescript.py', inp], shell=False, stdout=PIPE)
    print(out.stdout.decode())
    if out.stdout.decode() == "User not found. Please check your spelling\r\n":
        return render(request, "error.html", {'data': inp})
    elif out.stdout.decode() == "You cannot demote yourself. Admins must be demoted by another admin.\r\n":
        return render(request, "erroradmin.html", {'data': inp})
    elif out.stdout.decode() == "OK, Check your EMAIL\r\n":
        return render(request, "success.html", {'data': inp})
    else:
        return render(request, "erroroccur.html")
