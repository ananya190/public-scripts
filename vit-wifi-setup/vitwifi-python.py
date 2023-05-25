import os

with open (os.path.expanduser('~/.scripts/vit-wifi-setup/.secret')) as f:
    user, password = f.read().splitlines()

user = user.split('"')[1]
password = password.split('"')[1]

curl_response = os.popen("""
curl -s 'http://phc.prontonetworks.com/cgi-bin/authlogin?URI=http://captive.apple.com/hotspot-detect.html' \
-H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
-H 'Accept-Language: en-US,en;q=0.9' \
-H 'Cache-Control: max-age=0' \
-H 'Connection: keep-alive' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-H 'Origin: http://phc.prontonetworks.com' \
-H 'Referer: http://phc.prontonetworks.com/cgi-bin/authlogin?URI=http://www.msftconnecttest.com/redirect' \
-H 'Sec-GPC: 1' \
-H 'Upgrade-Insecure-Requests: 1' \
-H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36' \
--data-raw 'userId={user}&password={password}&serviceName=ProntoAuthentication&Submit22=Login' \
--compressed \
--insecure
""".format(user=user, password=password)).read()

if "Successful Pronto Authentication" in curl_response:
    print("Login Successful")
elif "http-equiv=\"refresh\"" in curl_response:
    print("Already Logged In")
else:
    print("Login Failed")