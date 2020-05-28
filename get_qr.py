#!/usr/bin/python3

import requests
import os

campaign_id = '12' #change this - take from campaign url
phishing_url = 'http://<ur_phishing_site>/?rid=' #change to landing page url

gophish_webroot = '/home/ubuntu/go/src/github.com/gophish/gophish' #check this - make sure it's right
static_images_dir = '/static/endpoint/qr/'

auth_header = {'Authorization':'<ur_api_token>'} #check this - take from gophish account page
local_url = 'http://127.0.0.1:3333/api/campaigns/' + campaign_id + "/results"

r = requests.get(local_url,headers=auth_header)

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
    if not os.path.exists(qr_dir):
        os.makedirs(qr_dir)
        print ('[+] created qr directory at ' + qr_dir)
    else:
        os.system('rm ' + qr_dir + '*') #comment this if running multiple qr-code campaigns simultaneously
        print ('[+] cleared files at ' + qr_dir) #this too

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
