import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Account Manager")
        self.setGeometry(100, 100, 400, 300)

        self.create_widgets()
        self.show()

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
        name = self.account_name_input.text()
        balance = self.retrieve_balance(name)
        if balance:
            self.withdraw_button.setVisible(True)
            self.deposit_button.setVisible(True)
            self.submit_button.setVisible(False)
            self.account_name_input.setVisible(False)
            self.label.setText("Balance for account name, {} is {} dollars".format(name, balance))
        else:
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

        '''
        try:
            startbalance = int(self.input_field_startbal.text())
            name = str(self.account_name_input.text())
            if startbalance >= 1:
                startbalance = self.input_field_startbal.text()
                name = str(self.account_name_input.text())
                print(name, "create_account_clicked has variables", startbalance)
                if True:
                    self.add_balance(name, startbalance)
                    self.input_field_startbal.setVisible(False)
                    self.ballabel.setVisible(False)
                    self.create_account_button.setVisible(False)
                    self.submit_button.setVisible(True)
                    self.label.setText("Account for {} created".format(name))
            else:
                print("Account balance not greater than 0")
                self.ballabel.setText("Starting balance must be more than 0")
        except ValueError:
            self.ballabel.setText("Non Number given, try again")




            

    def retrieve_balance(self, name):
        """
        attr: name - string, persons name
        return: int - balance of the persons account

        This fuction takes a name as an arg and return balance

        """
        with open("balance.txt", "r") as f:
            for line in f:
                account = line.strip().split(":")
                if account[0] == name:
                    return int(account[1])
        return None

    def add_balance(self, name, amount):
        print(name, "add balance has variables", amount)
        with open("balance.txt", "a") as f:
            if f.write("{}:{}\n".format(name, amount)):
                print("added succesfully {} {}".format(name, amount))
                f.close()
                return True
            else:
                f.close()
                return False

    
    def update_balance(self, name, amount):
        accounts = []
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
            with open("balance.txt", "w") as f:
                for account in accounts:
                    f.write("{}\n".format(account))

    def withdraw_clicked(self):
        self.withsub_button.setVisible(True)
        self.withdraw_button.setVisible(False)
        self.deposit_button.setVisible(False)
        self.input_field_with.setVisible(True)

    def deposit_clicked(self):
        print("Deposit button clicked.")
        self.depsub_button.setVisible(True)
        self.withdraw_button.setVisible(False)
        self.deposit_button.setVisible(False)
        self.input_field_with.setVisible(True)

    def depsub_clicked(self):
        print(type(self.input_field_with.text()))
        try: 
            deposit = int(self.input_field_with.text())
            name = str(self.account_name_input.text())
            amount = self.retrieve_balance(name)
            if deposit >= 1:
                if amount >= 0:
                    self.update_balance(name, +deposit)
                    balance = self.retrieve_balance(name)
                    self.depsub_button.setVisible(False)
                    self.input_field_with.setVisible(False)
                    self.deposit_button.setVisible(True)
                    self.withdraw_button.setVisible(True)
                    self.label.setText("Deposit complete your balance is now {} dollars".format(balance))
            else:
                self.label.setText("Cannot deposit less than 1 dollar")
        except ValueError:
            print("non int given")
            print(self.input_field_with.text())
            self.label.setText("Non number given, try again")
        
    def withsub_clicked(self):
        try:
            name = str(self.account_name_input.text())
            amount = self.retrieve_balance(name)
            withdraw = int(self.input_field_with.text())
            if withdraw >= 1:
                if amount - withdraw >= 0:
                    self.update_balance(name, -withdraw)
                    balance = self.retrieve_balance(name)
                    self.withsub_button.setVisible(False)
                    self.input_field_with.setVisible(False)
                    self.deposit_button.setVisible(True)
                    self.withdraw_button.setVisible(True)
                    self.label.setText("Withdrawl complete your balance is now {} dollars".format(balance))
            else:
                self.label.setText("Can not withdraw less than 1 dollar")
        except ValueError:
            self.label.setText("Non number given, try again")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
