
"""
blind sql injection
"""

from urllib.parse import quote

def main():
    """
    main function
    :return:
    """

    url = "http://127.0.0.1:8000/sqli?cmd=1' and '1'=1"

    encoded_url = quote(url)
    print(encoded_url)





if __name__ == '__main__':
    main()