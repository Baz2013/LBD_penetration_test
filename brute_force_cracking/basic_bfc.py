
# very basic brute force cracking method
# brute force cracking the login page of DVWA

class BasicBFC:
    password_file = ""
    def __init__(self, password_file):
        self.password_file = password_file



def main():
    """
    basic brute force cracking algorithm
    :return:
    """
    password_file = "../data/top1000_passwords.txt"
    basic_bfc = BasicBFC(password_file=password_file)




if __name__ == '__main__':
    main()