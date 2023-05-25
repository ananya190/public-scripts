#!/bin/zsh
# set USER and PASSWD from .secret file
VIT_USER=$(head -n 1 ~/.scripts/vit-wifi-setup/.secret | cut -d'"' -f2)
VIT_PASSWD=$(tail -n 1 ~/.scripts/vit-wifi-setup/.secret | cut -d'"' -f2)
# set flag = 0
FLAG=0

# run networksetup -setairportnetwork en0 "VIT2.4G" and read response
RESPONSE=`networksetup -setairportnetwork en0 "VIT2.4G"`

# if response is empty, it was successful. otherwise try to connect to VIT5G. if that fails too, set FLAG to 1.
if [ -z "$RESPONSE" ]; then
    echo "Connected to VIT2.4G"
else
    RESPONSE=`networksetup -setairportnetwork en0 "VIT5G"`
    if [ -z "$RESPONSE" ]; then
        echo "Connected to VIT5G"
    else
        FLAG=1
    fi
fi

# if FLAG is 1, VIT WiFi is not available. Display a message saying so.
if [ $FLAG -eq 1 ]; then
    echo "VIT WiFi is not available"
fi

# save curl response once. if "http-equiv="refresh"" is found, it means the user is is already logged in. set the flag to 1 and display so.
sleep 1
RESPONSE=`curl -s 'http://phc.prontonetworks.com/cgi-bin/authlogin?URI=http://captive.apple.com/hotspot-detect.html' \
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
    --data-raw 'userId='$VIT_USER'&password='$VIT_PASSWD'&serviceName=ProntoAuthentication&Submit22=Login' \
    --compressed \
    --insecure`

# if the RESPONSE contains "http-equiv="refresh"", set the flag to 1 and display so.
if [[ $RESPONSE == *"http-equiv=\"refresh\""* ]]; then
    FLAG=1
    echo "Already logged in"
fi

# if the flag is 0, it means the user is not logged in. so, log in.
# if FLAG is 0, send the curl request to log in to the captive portal.
if [ $FLAG -eq 0 ]; then
    # if pgrep doesnt find captive network assistant, wait until it does
    while ! pgrep "Captive Network Assistant" > /dev/null; do
        sleep 1
    done
    # once it does, kill it 
    killall "Captive Network Assistant"
    # wait 2 seconds
    sleep 2

    # save the curl response to a variable
    # the curl request is a multiline string
    RESPONSE=`curl -s 'http://phc.prontonetworks.com/cgi-bin/authlogin?URI=http://captive.apple.com/hotspot-detect.html' \
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
    --data-raw 'userId='$VIT_USER'&password='$VIT_PASSWD'&serviceName=ProntoAuthentication&Submit22=Login' \
    --compressed \
    --insecure`

    # display the response
    # echo $RESPONSE

    # if "Successful Pronto Authentication" is in the response, it was successful. otherwise, if "http-equiv="refresh"" is in the response, it was successful. otherwise, it was not successful.
    if [[ $RESPONSE == *"Successful Pronto Authentication"* ]]; then
        echo "Login successful"
    elif [[ $RESPONSE == *"http-equiv="refresh""* ]]; then
        echo "Already logged in"
    else
        echo "Login failed"
    fi
fi
