import random
import sqlite3


class DBase:
    __DB_NAME = 'card.s3db'
    __CREATE_TABLE_QUERY = '''
    CREATE TABLE IF NOT EXISTS card (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number TEXT,
        pin TEXT,
        balance INTEGER DEFAULT 0,
        iin TEXT,
        customer_id TEXT
    );'''
    __INSERT_RECORD_QUERY = 'INSERT INTO card (number, pin, balance, iin, ' \
                            'customer_id) VALUES (?, ?, ?, ?, ?);'
    __UPDATE_BALANCE_QUERY = 'UPDATE card SET balance = ? WHERE number = ?;'
    __DELETE_RECORD_QUERY = 'DELETE FROM card WHERE number = ?;'
    __CHK_EXISTS_QUERY = 'SELECT EXISTS (SELECT 1 FROM card WHERE number = ?);'
    __CHK_AUTH_QUERY = 'SELECT EXISTS (SELECT 1 FROM card WHERE number = ? ' \
                       'AND pin = ?);'
    __GET_ALL_INFO_QUERY = 'SELECT * FROM card WHERE number = ?;'

    def __init__(self):
        self.__con = sqlite3.connect(self.__DB_NAME)
        self.__cur = self.__con.cursor()

    def __del__(self):
        self.__con.close()

    def start(self):
        self.create_table()

    def chk_exists(self, number):
        self.__cur.execute(self.__CHK_EXISTS_QUERY, (number,))
        return self.__cur.fetchone()[0]

    def chk_auth(self, number, pin):
        self.__cur.execute(self.__CHK_AUTH_QUERY, (number, pin))
        return self.__cur.fetchone()[0]

    def get_all_info(self, number):
        self.__cur.execute(self.__GET_ALL_INFO_QUERY, (number,))
        return self.__cur.fetchone()

    def create_table(self):
        self.__cur.execute(self.__CREATE_TABLE_QUERY)
        self.__con.commit()

    def insert_record(self, card):
        self.__cur.execute(self.__INSERT_RECORD_QUERY,
                           (card.get_card_number(), card.get_card_pin(),
                            card.get_card_balance(), CardGenerator.IIN,
                            card.get_card_customer_id()))
        self.__con.commit()

    def upd_balance(self, number, amount):
        self.__cur.execute(self.__UPDATE_BALANCE_QUERY, (amount, number))
        self.__con.commit()

    def delete_record(self, number):
        self.__cur.execute(self.__DELETE_RECORD_QUERY, (number,))
        self.__con.commit()


class Bank:
    MAIN_MENU = ("1. Create an account\n"
                 "2. Log into account\n"
                 "0. Exit\n"
                 ">")
    ACC_MENU = ("1. Balance\n"
                "2. Add income\n"
                "3. Do transfer\n"
                "4. Close account\n"
                "5. Log out\n"
                "0. Exit\n"
                ">")
    MESSAGE_LOGIN = "You have successfully logged in!"
    MESSAGE_LOGOUT = "You have successfully logged out!"
    MESSAGE_CLOSE_ACCOUNT = "The account has been closed!"
    running_status = True

    @classmethod
    def main_menu(cls):
        while cls.running_status:
            main_item = input(cls.MAIN_MENU)
            if main_item == "0":
                cls.running_status = False
            elif main_item == "1":
                CardStorage.add_card()
            elif main_item == "2":
                cls.acc_validation()
        print("Bye!")

    @classmethod
    def acc_actions(cls, card):
        while True:
            acc_item = input(cls.ACC_MENU)
            if acc_item == "0":
                cls.running_status = False
                return None
            elif acc_item == "1":
                print(card.get_card_balance())
            elif acc_item == "2":
                card.add_amount(int(input("Enter income:\n>")))
                print("Income was added!")
            elif acc_item == "3":
                card.do_transfer()
            elif acc_item == "4":
                card.delete_account()
                print(cls.MESSAGE_CLOSE_ACCOUNT)
                return None
            elif acc_item == "5":
                print(cls.MESSAGE_LOGOUT)
                return None

    @classmethod
    def acc_validation(cls):
        card = CardStorage.login_card(input("Enter your card number:\n>"),
                                      input("Enter your PIN:\n>"))
        if card:
            cls.acc_actions(card)


class CardProc:

    def __init__(self, number):
        card = db.get_all_info(number)
        self.number = card[1]
        self.pin = card[2]
        self.balance = card[3]
        self.iin = card[4]
        self.customer_id = card[5]

    def get_card_customer_id(self):
        return self.customer_id

    def get_card_number(self):
        return self.number

    def get_card_balance(self):
        return self.balance

    def get_card_pin(self):
        return self.pin

    def add_amount(self, amount):
        self.balance += amount
        db.upd_balance(self.number, self.balance)

    def deduct_amount(self, amount):
        self.balance -= amount
        db.upd_balance(self.number, self.balance)

    def do_transfer(self):
        card_to = input("Transfer\nEnter card number:\n>")
        if CardStorage.check_card_number(card_to) is True:
            if db.chk_exists(card_to) == 1 and self.number != card_to:
                amount = int(input("Enter how much money you want to "
                                   "transfer:\n>"))
                if self.balance >= amount:
                    self.deduct_amount(amount)
                    card_tr = CardProc(card_to)
                    card_tr.add_amount(amount)
                    print("Success!")
                else:
                    print("Not enough money!")
            elif db.chk_exists(card_to) == 1 and self.number == card_to:
                print("You can't transfer money to the same account!")
            else:
                print("Such a card does not exist.")
        else:
            print("Probably you made a mistake in the card number. "
                  "Please try again!")

    def delete_account(self):
        db.delete_record(self.number)


class CardGenerator:
    IIN = 400000

    @staticmethod
    def new_card():
        while True:
            customer_id = CardGenerator.new_customer_id()
            checksum = CardGenerator.new_checksum(customer_id)
            if db.chk_exists(f'{CardGenerator.IIN}'
                             f'{customer_id}'
                             f'{checksum}') == 0:
                return Card(customer_id, checksum, CardGenerator.new_pin())

    @staticmethod
    def new_customer_id():
        return ''.join(str(random.randint(0, 9)) for _ in range(9))

    @staticmethod
    def new_pin():
        return ''.join(str(random.randint(0, 9)) for _ in range(4))

    @staticmethod
    def new_checksum(customer_id):
        return CardStorage.checksum(list(f"{CardGenerator.IIN}{customer_id}"))


class Card:

    def __init__(self, customer_id, checksum, pin, balance=0):
        self.iin = CardGenerator.IIN
        self.customer_id = customer_id
        self.checksum = checksum
        self.pin = pin
        self.balance = balance

    def get_card_number(self):
        return f"{self.iin}{self.customer_id}{self.checksum}"

    def get_card_pin(self):
        return self.pin

    def get_card_customer_id(self):
        return self.customer_id

    def get_card_balance(self):
        return self.balance


class CardStorage:

    @staticmethod
    def add_card():
        new_card = CardGenerator.new_card()
        db.insert_record(new_card)
        print("Your card has been created\n"
              "Your card number:\n"
              "{}\n"
              "Your card PIN:\n"
              "{}".format(new_card.get_card_number(), new_card.get_card_pin()))

    @staticmethod
    def login_card(card_number, pin):
        if db.chk_auth(card_number, pin) == 1:
            card = CardProc(card_number)
            print("You have successfully logged in!")
            return card
        print("Wrong card number or PIN!")
        return False

    @staticmethod
    def check_card_number(number):
        if number[-1] == CardStorage.checksum(list(number[:-1])):
            return True
        return False

    @staticmethod
    def checksum(lst):
        summary = 0
        for i in range(len(lst)):
            if (i + 1) % 2 != 0:
                if int(lst[i]) * 2 > 9:
                    lst[i] = str(int(lst[i]) * 2 - 9)
                else:
                    lst[i] = str(int(lst[i]) * 2)
            summary += int(lst[i])
        checksum = 10 - summary % 10
        if checksum == 10:
            checksum = 0
        return str(checksum)


db = DBase()
db.start()
Bank.main_menu()
del db
