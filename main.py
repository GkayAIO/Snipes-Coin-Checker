import requests, re, time, csv, tls_client
from bs4 import BeautifulSoup
from sty import Style, RgbFg, fg 
from fake_useragent import UserAgent
ua = UserAgent()
fg.light_red = Style(RgbFg(208, 31, 39))
fg.dark_grey = Style(RgbFg(110, 110, 110))

def login(email, password, region, proxy, s):
    r__ = ua.random
    if region.lower() == "de" or region.lower() == "at":
        region = "com"
    region = region.lower()
    print(fg.light_red + f"[ Snipes ] [ {time.strftime('%H:%M:%S', time.localtime())} ]" + fg.dark_grey + " • " + fg.rs + f"Logging in...")
    headers = {
        "authority": f"www.snipes.{region}",
        "method": "GET",
        "path": "/login",
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-GB,en;q=0.9",
        "sec-ch-ua": '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent":r__
    }
    r = s.get(f"https://www.snipes.{region}/login", headers=headers, proxy=proxy)
    try:
        csrf_token = re.findall('name="csrf_token" value="(.*?)"', str(r.text))[0]
        register_token1 = re.findall('<span data-id="(.*?)" data-value', str(r.text))[0]
        register_token2 =re.findall('" data-value="(.*?)"></span>', str(r.text))[0]
    except:
        print(fg.light_red + f"[ Snipes ] [ {time.strftime('%H:%M:%S', time.localtime())} ]" + fg.dark_grey + " • " + fg.red + f"Error getting token!")
        return -1
    headers = {
        "user-agent": r__,
        "x-requested-with": "XMLHttpRequest"
    }
    payload = {
        register_token1: register_token2,
        "dwfrm_profile_customer_email": email,
        "dwfrm_profile_login_password": password,
        "csrf_token": csrf_token
    }
    r = s.post(f"https://www.snipes.{region}/authentication?rurl=1&format=ajax", headers=headers, data=payload, proxy=proxy)
    if '"userLoginStatus": true,' in r.text:
        print(fg.light_red + f"[ Snipes ] [ {time.strftime('%H:%M:%S', time.localtime())} ]" + fg.dark_grey + " • " + fg.green + f"Successfully logged in!")
        time.sleep(3)
        return 1
    else:
        print(fg.light_red + f"[ Snipes ] [ {time.strftime('%H:%M:%S', time.localtime())} ]" + fg.dark_grey + " • " + fg.red + f"Error logging in, check your credentials")
        time.sleep(3)

def check_coins(email, password, region, proxy, s):
    if region.lower() == "de" or region.lower() == "at":
        region = "com"
    region = region.lower()
    print(fg.light_red + f"[ Snipes ] [ {time.strftime('%H:%M:%S', time.localtime())} ]" + fg.dark_grey + " • " + fg.rs + f"Checking coins...")
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    r = s.get(f"https://www.snipes.{region}/cliqueoverview", headers=headers, proxy=proxy)
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, features="lxml")
        value = soup.find_all("div", {"class": "b-account-clique-info-data-value"})[0]
        value2 = re.findall('<div class="b-account-clique-info-data-value">\n<span class="b-account-clique-info-data-title">Deine COINS:</span>\n(.*?) COINS\n</div>', str(value))[0]
        print(fg.light_red + f"[ Snipes ] [ {time.strftime('%H:%M:%S', time.localtime())} ]" + fg.dark_grey + " • " + fg.green + f"You have {value2} COINS in your account!")
        data_export = [email, password, proxy, value2]
        with open("output.csv", 'a+', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data_export)
    else:
        data_export = [email, password, proxy, "Error/0"]
        with open("output.csv", 'a+', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data_export)
        print(fg.light_red + f"[ Snipes ] [ {time.strftime('%H:%M:%S', time.localtime())} ]" + fg.dark_grey + " • " + fg.red + f"Error checking snipes coin amount!")

with open('input.csv', newline='') as input_file:
    csv_file = csv.reader(input_file)
    next(csv_file)
    for row in csv_file:
        proxy = row[2].split(":")
        proxy = proxy[2]+":"+proxy[3]+"@"+proxy[0]+":"+proxy[1]
        proxy_ = {"http": f"http://{proxy}"}
        s = tls_client.Session(client_identifier="chrome_108")
        if login(row[0], row[1], row[3], proxy_, s) == 1:
            check_coins(row[0], row[1], row[3], proxy_, s)
            pass
