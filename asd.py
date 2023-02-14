import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

#Main Class, Widgets and fucntions

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Account Manager")
        self.setGeometry(100, 100, 400, 300)

        self.create_widgets()
        self.show()

    #Makes the Widgets

    def create_widgets(self):
        self.label = QLabel("Enter the account holder's name: ")
        self.account_name_input = QLineEdit()
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_clicked)

        self.ballabel = QLabel("Starting Balance")
        self.input_field_startbal = QLineEdit()
        self.create_account_button = QPushButton("Create account")
        self.create_account_button.clicked.connect(lambda: self.create_account_clicked(self.account_name_input, self.input_field_startbal))
        self.input_field_startbal.setVisible(False)
        self.create_account_button.setVisible(False)
        self.ballabel.setVisible(False)

        self.withdraw_button = QPushButton("Withdraw")
        self.withdraw_button.clicked.connect(self.withdraw_clicked)
        self.withdraw_button.setVisible(False)

        self.deposit_button = QPushButton("Deposit")
        self.deposit_button.clicked.connect(self.deposit_clicked)
        self.deposit_button.setVisible(False)

        
        self.input_field_with = QLineEdit()
        self.withsub_button = QPushButton("Submit Withdrawl")
        self.withsub_button.clicked.connect(self.withsub_clicked)
        self.withsub_button.setVisible(False)
        self.input_field_with.setVisible(False)

        self.depsub_button = QPushButton("Submit Deposit")
        self.depsub_button.clicked.connect(self.depsub_clicked)
        self.depsub_button.setVisible(False)

        #Layout of the widgets from top to bottom

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.account_name_input)
        layout.addWidget(self.ballabel)
        layout.addWidget(self.input_field_startbal)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.withdraw_button)
        layout.addWidget(self.deposit_button)
        layout.addWidget(self.input_field_with)
        layout.addWidget(self.withsub_button)
        layout.addWidget(self.depsub_button)
        layout.addWidget(self.create_account_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def submit_clicked(self):
        #Search file for the balance of the input
        name = self.account_name_input.text()
        balance = self.retrieve_balance(name)
        #If a balance is found
        if balance:
            #set next frame of widgets
            self.withdraw_button.setVisible(True)
            self.deposit_button.setVisible(True)
            self.submit_button.setVisible(False)
            self.account_name_input.setVisible(False)
            #Change Label
            self.label.setText("Balance for account name, {} is {} dollars".format(name, balance))
        else:
            #If balance not found ask to create an account
            self.withdraw_button.setVisible(False)
            self.deposit_button.setVisible(False)
            print("balance for that account not found")
            self.label.setText("Account for {} not found, would you like to create one?".format(name))
            self.input_field_startbal.setVisible(True)
            self.create_account_button.setVisible(True)
            self.ballabel.setVisible(True)
            self.submit_button.setVisible(False)

    def create_account_clicked(self, name, startbalance):
        '''
        attr: name - string, new account name
        attr: startbalance - int, the starting balance fo the account

        This function takes attr and calls add_balance to write the account to balance.txt file
        '''
        #attempt to turn start balance into an in
        try:
            startbalance = int(self.input_field_startbal.text())
            name = str(self.account_name_input.text())
            if startbalance >= 1:
                #stops from creating a negative balance account
                startbalance = self.input_field_startbal.text()
                name = str(self.account_name_input.text())
                print(name, "create_account_clicked has variables", startbalance)
                if True:
                    #write to file with add_balance function then reset gui
                    self.add_balance(name, startbalance)
                    self.input_field_startbal.setVisible(False)
                    self.ballabel.setVisible(False)
                    self.create_account_button.setVisible(False)
                    self.submit_button.setVisible(True)
                    self.label.setText("Account for {} created".format(name))
            else:
                #tells user to not give a negative number
                print("Account balance not greater than 0")
                self.ballabel.setText("Starting balance must be more than 0")
        except ValueError:
            #if failed then startbalance isnt a number
            self.ballabel.setText("Non Number given, try again")




            

    def retrieve_balance(self, name):
        """
        attr: name - string, persons name
        return: int - balance of the persons account

        This fuction takes a name as an arg and return balance

        """
        #opens and reads file
        with open("balance.txt", "r") as f:
            for line in f:
                account = line.strip().split(":")
                if account[0] == name:
                    return int(account[1])
        return None

    def add_balance(self, name, amount):
        '''
        attr: name - string, new account name
        return: - True/False, for succesful or failure write to file

        This file takes two variables and writes them to balance.txt file
        '''
        print(name, "add balance has variables", amount)
        with open("balance.txt", "a") as f:
            #attempts to write to file
            if f.write("{}:{}\n".format(name, amount)):
                print("added succesfully {} {}".format(name, amount))
                f.close()
                return True
            else:
                #if fails returns false
                f.close()
                return False

    
    def update_balance(self, name, amount):
        """
        attr: name - string, name of the account being updated
        return: True/False, if fails returns False else: returns True
        """
        accounts = []
        #haven't found account
        found = False
        with open("balance.txt", "r") as f:
            for line in f:
                account = line.strip().split(":")
                if account[0] == name:
                    found = True
                    accounts.append("{}:{}".format(name, str(int(account[1]) + amount)))
                else:
                    accounts.append(line.strip())
        if found:
            #if balance found update balance
            with open("balance.txt", "w") as f:
                for account in accounts:
                    f.write("{}\n".format(account))

    def withdraw_clicked(self):
        #button sets visible
        self.withsub_button.setVisible(True)
        self.withdraw_button.setVisible(False)
        self.deposit_button.setVisible(False)
        self.input_field_with.setVisible(True)

    def deposit_clicked(self):
        #button sets visible
        print("Deposit button clicked.")
        self.depsub_button.setVisible(True)
        self.withdraw_button.setVisible(False)
        self.deposit_button.setVisible(False)
        self.input_field_with.setVisible(True)

    def depsub_clicked(self):
        """
        attr: name - string, name of the accounts balance being changed
        """
        print(type(self.input_field_with.text()))
        try: 
            #attempts to turn deposit amount into int
            deposit = int(self.input_field_with.text())
            name = str(self.account_name_input.text())
            amount = self.retrieve_balance(name)
            if deposit >= 1:
                #stops negative deposits
                if amount >= 0:
                    #updates balance by adding deposit (name, "+deposit")
                    self.update_balance(name, +deposit)
                    #finds and returns balance after deposit
                    balance = self.retrieve_balance(name)
                    self.depsub_button.setVisible(False)
                    self.input_field_with.setVisible(False)
                    self.deposit_button.setVisible(True)
                    self.withdraw_button.setVisible(True)
                    self.label.setText("Deposit complete your balance is now {} dollars".format(balance))
            else:
                self.label.setText("Cannot deposit less than 1 dollar")
        except ValueError:
            #if failed return "non int given" to user
            print("non int given")
            print(self.input_field_with.text())
            self.label.setText("Non number given, try again")
        
    def withsub_clicked(self):
        try:
            name = str(self.account_name_input.text())
            amount = self.retrieve_balance(name)
            withdraw = int(self.input_field_with.text())
            if withdraw >= 1:
                if amount - withdraw >= 1:
                    self.update_balance(name, -withdraw)
                    balance = self.retrieve_balance(name)
                    self.withsub_button.setVisible(False)
                    self.input_field_with.setVisible(False)
                    self.deposit_button.setVisible(True)
                    self.withdraw_button.setVisible(True)
                    self.label.setText("Withdrawl complete your balance is now {} dollars".format(balance))
                else:
                    self.label.setText("Cannot have less than 1 dollar in your account")
            else:
                self.label.setText("Can not withdraw less than 1 dollar")
        except ValueError:
            self.label.setText("Non number given, try again")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
