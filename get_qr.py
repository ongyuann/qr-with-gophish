#!/usr/bin/python3

import requests
import os,sys

######################
## things to change ##
######################
campaign_id = '12' #change this - take from campaign url
phishing_url = 'http://j4ck1e.xyz/?rid=' #change to landing page url (don't touch the '?rid='!)
ur_api_token = '489de2cc780b60779cbc984f9aa42327416dfac0899b49e29c4882d19c479ae0' # change this - take from gophish account page

#####################
## things to check ##
#####################
gophish_webroot = '/home/ubuntu/go/src/github.com/gophish/gophish' #check this - make sure it's right
http_or_https = 'http' #check! if gophish mgmt instance is on HTTPS, change to 'https'

####################
## all systems go ##
####################
static_images_dir = '/static/endpoint/qr/'

auth_header = {'Authorization':ur_api_token}
local_url = http_or_https + '://127.0.0.1:3333/api/campaigns/' + campaign_id + "/results"

try:
    r = requests.get(local_url,headers=auth_header,verify=False)
except:
    print ("[!] something went wrong - we can't connect to your gophish API. check if you can connect to API manually and troubleshoot:\n[+] curl localhost:3333/api/campaigns/" + campaign_id + "/results -H 'Authorization: " + ur_api_token + "' | grep 'id' | grep -v 'campaign' | cut -d':' -f2 | cut -d'\"' -f2")
    sys.exit()

if "Invalid" in r.text:
    print ("[!] something went wrong - gophish rejected your API key. is this API key correct?\n[+] " + ur_api_token)
    sys.exit()

def grep_rid(r):
    rid = []
    for i in r.iter_lines():
        i = i.decode('utf-8')
        if "details" in i:
            continue
        if "id" in i:
            if "campaign" in i:
                continue
            else:
                i = i.split()[1].replace('"','').replace(',','')
                if len(i) <= 6:
                    continue
                rid.append(i)
    #print (rid)
    return rid

rid = grep_rid(r) #array of rids from chosen campaign

def make_qr(rid):
    qr_dir = gophish_webroot + static_images_dir
    print ('[+] checking if static images directory exists')
    if not os.path.exists(qr_dir):
        print ('[+] creating static images directory for qr code')
        os.makedirs(qr_dir)
    else:
        print ('[+] removing old qr codes from static images directory')
        os.system('rm ' + qr_dir + '*')

    for i in rid:
        qr_file = qr_dir + i + '.png'
        url = phishing_url + i
        url = '"'+'https://qr-generator.qrcode.studio/qr/custom?download=true&file=png&data=' + url
        url += '&size=1000&config=%7B%22body%22%3A%22square%22%2C%22eye%22%3A%22frame0%22%2C%22eyeBall%22%3A%22ball0%22%2C%22erf1%22%3A%5B%5D%2C%22erf2%22%3A%5B%5D%2C%22erf3%22%3A%5B%5D%2C%22brf1%22%3A%5B%5D%2C%22brf2%22%3A%5B%5D%2C%22brf3%22%3A%5B%5D%2C%22bodyColor%22%3A%22%23000000%22%2C%22bgColor%22%3A%22%23FFFFFF%22%2C%22eye1Color%22%3A%22%23000000%22%2C%22eye2Color%22%3A%22%23000000%22%2C%22eye3Color%22%3A%22%23000000%22%2C%22eyeBall1Color%22%3A%22%23000000%22%2C%22eyeBall2Color%22%3A%22%23000000%22%2C%22eyeBall3Color%22%3A%22%23000000%22%2C%22gradientColor1%22%3A%22%22%2C%22gradientColor2%22%3A%22%22%2C%22gradientType%22%3A%22linear%22%2C%22gradientOnEyes%22%3A%22true%22%2C%22logo%22%3A%22%22%2C%22logoMode%22%3A%22default%22%7D'
        url = url + '"' + ' --output ' + qr_file
        os.system('curl -s -X GET ' + url)
        print ('[+] created qr code at ' + qr_file)
    print ('[+] done.')
    pass

make_qr(rid)
