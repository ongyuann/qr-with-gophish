# qr-with-gophish

## purpose: what the title says

## pre-reqs:
- gophish installed
- gophish campaign created
- python3

## installation:
- copy and save `get_qr.py` on your home folder

## use:
- insert the following to your email template:
```
<img src="http://j4ck1e.xyz/static/qr/{{.RId}}.png" alt="it works!" width="500" height="500">
```
- (replace with your own phishing url and alt message)
- run get_qr.py

## misc: manual curls:

grabbing rid from campaign '1' via API:
```
curl localhost:3333/api/campaigns/1/results -H "Authorization: f1e1285cf68ec419174dcce5251523c8b169842e655eed3b4995bf4a5d4627f7" | grep "id" | grep -v "campaign" | cut -d":" -f2 | cut -d'"' -f2
```

generating QR code via API and saving to 'test.png':
```
curl -X GET "https://qr-generator.qrcode.studio/qr/custom?download=true&file=png&data=https%3A%2F%2Fwww.qrcode-monkey.com&size=1000&config=%7B%22body%22%3A%22square%22%2C%22eye%22%3A%22frame0%22%2C%22eyeBall%22%3A%22ball0%22%2C%22erf1%22%3A%5B%5D%2C%22erf2%22%3A%5B%5D%2C%22erf3%22%3A%5B%5D%2C%22brf1%22%3A%5B%5D%2C%22brf2%22%3A%5B%5D%2C%22brf3%22%3A%5B%5D%2C%22bodyColor%22%3A%22%23000000%22%2C%22bgColor%22%3A%22%23FFFFFF%22%2C%22eye1Color%22%3A%22%23000000%22%2C%22eye2Color%22%3A%22%23000000%22%2C%22eye3Color%22%3A%22%23000000%22%2C%22eyeBall1Color%22%3A%22%23000000%22%2C%22eyeBall2Color%22%3A%22%23000000%22%2C%22eyeBall3Color%22%3A%22%23000000%22%2C%22gradientColor1%22%3A%22%22%2C%22gradientColor2%22%3A%22%22%2C%22gradientType%22%3A%22linear%22%2C%22gradientOnEyes%22%3A%22true%22%2C%22logo%22%3A%22%22%2C%22logoMode%22%3A%22default%22%7D" --output test.png
```

