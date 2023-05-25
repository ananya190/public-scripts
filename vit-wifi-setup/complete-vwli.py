import os

# get user name and password from the .secret file
with open(os.path.expanduser('~/.scripts/vit-wifi-setup/.secret')) as f:
    user, password = f.read().splitlines()

user = user.split('"')[1]
password = password.split('"')[1]

# set curl request string interpolated with user and password
curl_request = """
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
    --data-raw 'userId={user_name}&password={password}&serviceName=ProntoAuthentication&Submit22=Login' \
    --compressed \
    --insecure
    """.format(user_name=user, password=password)

flag = 0
# use bash to run networksetup -setairportnetwork en0 "VIT2.4G" and
# networksetup -setairportnetwork en0 "VIT5G" if the first one fails connect to
# VIT2.4G
v24_response = os.popen("""
networksetup -setairportnetwork en0 "VIT2.4G"
""").read()

if v24_response == "":
    print("Connected to VIT2.4G")
else:
    print("Failed to connect to VIT2.4G")
    flag = 1

# connect to VIT5G
if flag == 1:
    v5_response = os.popen("""
    networksetup -setairportnetwork en0 "VIT5G"
    """).read()

    if v5_response == "":
        print("Connected to VIT5G")
        flag = 0
    else:
        print("Failed to connect to VIT5G")
        flag = 1


# curl response
if flag == 0:

    # close Captive Network Assistant
    os.system("""
    sleep 5
    killall "Captive Network Assistant"
    """)

    # wait for keyboard input indicating pop up has been displayed
    print("Waiting for input")
    x = input()
    print("Running curl")
    curl_response = os.popen(curl_request).read()

    if "Successful Pronto Authentication" in curl_response:
        print("Login Successful")
    elif "http-equiv=\"refresh\"" in curl_response:
        print("Already Logged In")
    else:
        print("Login Failed")
else:
    print("Failed to connect to VIT2.4G and VIT5G")
