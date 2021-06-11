import cx_Oracle
from NewEmployee511 import EmpDetails
import logging

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = logging.getLogger(__name__)

# To override the default severity of logging
logger.setLevel('DEBUG')

# Use FileHandler() to log to a file
file_handler = logging.FileHandler('BankSystem.log')
#234file_handler = logging.StreamHandler()
formatter = logging.Formatter(log_format)
file_handler.setFormatter(formatter)

# Don't forget to add the file handler
logger.addHandler(file_handler)


#connect to Oracle database

try:
    conn = cx_Oracle.connect("peppermint","welcome1","localhost/orcl19c")
    print('Succesfully connected to the Database')

except Exception as err:
    print('Problem connecting to the database')
    logger.info('Problem connecting to the database')

#get customer information to create new customer based on Customer ID.
# This is going to be used  to get when OPENING a new account 
    
class Customer:

    def  __init__(self, customer_name):
        self.customer_name = customer_name
     

    def getName(self,customerid, customer_name):
        self.customerid = customerid
        self.customer_name= customer_name

        while True:
            try:
                self.customerid = int(input("Provide Customer ID: "))
                break
            except ValueError:
                print("Not a valid Customer ID, please enter the number! Please try again ...")
                logger.info("Customer ID not valid ")

        print("The customer ID you entered is: ", self.customerid)
        print('self customer id: ', self.customerid)
        customerid = self.customerid
       
        print('customer id: ', customerid)
        
        try:
            get_name ="select customer_name from customers where customerid = :customerid" 
            cursor = conn.cursor()
            result = cursor.execute(get_name, {"customerid": customerid})
            result = cursor.fetchone()
            self.customer_name = result[0]

            if not cursor.rowcount:
                print('Customer not found')
                return 

        except Exception as err:
            print('Problem retrieving the Customer name for this Customer#', err)
            self.customer_name = []
            logger.info(err)
            return
        finally:
            cursor.close()
        

# This is going to be used  to get customer's info when
# making a deposit, witdrawal, inquiry and closing the account

class CustomerInfo:

    def custinfo(self,acctno, customer_name, balance):

        self.acctno = acctno
        self.customer_name = customer_name
        self.balance = balance

        while True:
            try:
                self.acctno = int(input("Provide account number: "))
                break
            except ValueError:
                print("Not a valid account number! Please try again ...")

        print("The account number you entered is: ", self.acctno)
        acctno = self.acctno
       
        try:
            get_rows = "select customer_name, account_balance from accounts where acctno = :acctno and account_status <> 'CLO'"
            cursor = conn.cursor()
            result = cursor.execute(get_rows, {"acctno": acctno})
            result = cursor.fetchone()

            if not cursor.rowcount:
                print('Customer not found')
                self.acctno = 0
            else:
                self.customer_name = result[0]
                self.balance = result[1]

        except Exception as err:
            print('Problem retrieving this account', err)
            logger.info(err)
        finally:
            cursor.close()
            
#Main Class for Bank System

class BankSystem(Customer, CustomerInfo): 
    def __init__ (self, customerid): 
        super().__init__(self)

        self.customerid = customerid
      
    def selection(self):
        print(           "\n\t\t Main Menu")
        print(" ")
        print("      N for Create a New Customer ")
        print("      O for Open a New Account ")
        print("      D for Deposit ")
        print("      W for Withdrawal")
        print("      I for Balance Inquiry")
        print("      C to Close an Account")
        print("      E to Exit the Banking System")
        print("                                    ")

# When a new customer account is being created.
# A customerID will be generated to be used later to create a new account

    def new_customer(self, customerid=0, customer_name=''):
 
        print('New Account')
        print("CustomerID = ", self.customerid)
        customer_name = input('Customer Name: ')
        customer_address = input('Mailing Address: ')
        phone = input("Phone Number: ")
        email = input("E-mail Address: ")

        confirm_entries = input('Are all details correct (Y/N)? ')
 
        if confirm_entries in ('Y','y'):      
            try:
                cursor = conn.cursor()
                cursor.callproc("add_new_customer", (customer_name, customer_address, phone, email))
                print('New Customer added')
            except Exception as err:
                print('Problem running the new_employee procedure',err)
            finally:
                cursor.close()
        elif confirm_entries in ('N','n'):
            print('Response is N')
            return
        else:
            print('Invalid Input')

# To open a new account a valid customerID is needed.
# New Account number will be generated

    def new_acct(self):

        if self.customer_name == [ ]:
            return 
        
        print(' The Customer Name for this ID is ', self.customer_name)

        account_type = input(' Is this a Saving (S) or Checking (C) account? ')

        if account_type not in ('S','s','C','c'):
            print('Not Valid Account Type')
            return

        while True:
            try:
                self.balance = float(input('How much is your initial deposit?  $'))
                break
            except Exception as err:
                print('Invalid Input, must be numeric', err)
                logger.info(err)

        print("self.balance = ", self.balance)
  

        if self.balance <= float(0):
           print ('Invalid Initial Deposit amount')
           return

        account_status = 'NEW'
        account_status = str(account_status)
        
        print(' Please review the details:')
        print(' Customer ID: ', self.customerid)
        print(' Customer Name: ', self.customer_name)

        print(' Your Initial deposit is $',self.balance )

        
        if account_type in ('s','S'):
            account='Saving Account'
            account_type = 'S' 
        elif account_type in ('c','C'):
            account='Checking Account'
            account_type = 'C'  
        else:
            print('Invalid Account Type') 

        print('The account type is ', account)

        all_correct = input('Everything correct (Y/N)?: ')

        if all_correct in ('Y','y'):      
            try:
                cursor = conn.cursor()
                cursor.callproc("add_new_account", (self.customer_name, self.customerid, account_type, account_status, self.balance))
                print('New Account Successfully')
            except Exception as err:
                print('Problem Adding New account',err)
                logger.info(err)
            finally:
                cursor.close()
        elif all_correct in ('N', 'n'):
            print('Response is N')
            return 
        else:
            print('Invalid Input')
            return 

# Making a Deposit, account number is required when making a deposit

    def deposit(self, deposit_amt=0):
        
        print('Deposit Menu')

        if self.acctno == 0:
            return

        print('The customer for this account number is ', self.customer_name)
        print(' ')
        deposit_amt = float(input(' How much are you going to deposit?:  $'))
        confirm = input(' Are you ready to commit the deposit (Y/N)?:  ')

        account_balance = float(self.balance) + float(deposit_amt)
        account_status = 'ACT'

        trantype = 'DEP'
        tranamt = float(deposit_amt)

        print('account_balance = ', account_balance)
         
        self.acctno = int(self.acctno)
        acctno = self.acctno

        if confirm in ('Y','y'):      
            try:
                cursor = conn.cursor()
                cursor.callproc("insert_transaction", (trantype, tranamt, acctno))
                print('Successfully deposited to the Account Number ', acctno)
                print('New Account Balance is $ ', account_balance)
            except Exception as err:
                print('Problem Occurred while trying to Deposit to the account',err)
                logger.info(err)
            finally:
                pass

            try:
                update_account = "update accounts set account_balance = :account_balance, account_status = :account_status where acctno = :acctno"
                cursor.execute(update_account,{"acctno": acctno, "account_balance": account_balance, "account_status": account_status})
               
                print('Transaction posted')
            except Exception as err:
                print(' Account cannot be updated due to error ', err)
                logger.info(err)
            finally:
                conn.commit()
                cursor.close()

        elif confirm in ('N','n'):
            print('Response is N')
            return
        else:
            print('Invalid Input')
            return

    def withdraw(self, withdraw_amt=0):
        
        print('Witdrawal Menu')

        if self.acctno == 0:
            return

        print('The customer for this account number is ', self.customer_name)
        print('The current balance for this account is $', self.balance)
        print(' ')
        withdraw_amt = input(' How much are you going to withdraw?:  $')
        withdraw_amt = float(withdraw_amt)
        
        if self.balance < withdraw_amt:
            print('Insufficient funds')
            return
        elif self.balance == withdraw_amt:
            print('This is the remaining balance in this account \nif you wish to close the account please choose Close account option')
            return
        elif self.balance > withdraw_amt:
            account_balance = float(self.balance) - float(withdraw_amt)
            account_status = 'ACT'

        confirm = input(' Are you ready to commit the withdrawal (Y/N)?:  ')

        trantype = 'WID'
        tranamt = withdraw_amt

        self.acctno = int(self.acctno)
        acctno = self.acctno

        if confirm in ('Y','y'):      
            try:
                cursor = conn.cursor()
                cursor.callproc("insert_transaction", (trantype, tranamt, acctno))
                print('Successfully deposited to the Account Number ', acctno)
                print('New Account Balance is $ ', account_balance)
            except Exception as err:
                print('Problem Occurred while trying to Deposit to the account',err)
                logger.info(err)
            finally:
                pass

            try:
                update_account = "update accounts set account_balance = :account_balance, account_status = :account_status where acctno = :acctno"
                cursor.execute(update_account,{"acctno": acctno, "account_balance": account_balance, "account_status": account_status})
               
                print('Transaction posted')
            except Exception as err:
                print(' Account cannot be updated due to error ', err)
                logger.info(err)
            finally:
                conn.commit()
                cursor.close()

        elif confirm in ('N','n'):
            print('Withdrawal cancelled')
            return
        else:
            print('Invalid Input')
            return
        
# Checking Balance inquiry

    def inquiry(self):
        
        print('Balance Inquiry')
        
        if self.acctno == 0:
            return

        print('The customer for this account number is ', self.customer_name)
        print('The account Balance is ', self.balance)

# To close, account number is required.

    def close(self):

        
        if self.acctno == 0:
            return
        
        print('Closing Account')
        
   
        print("The account number you entered is: ", self.acctno)
       
        print('The customer for this account number is ', self.customer_name)
        print('CUrrently you have an account balance of  $', self.balance)
         
        account_balance = 0
        account_status = 'CLO'

        confirm_close = input(' Are you sure you want to close the account (Y/N)?:  ')

        trantype = 'CLO'
        tranamt = self.balance

        acctno = int(self.acctno)

        if confirm_close in ('Y','y'):      
            try:
                cursor = conn.cursor()
                cursor.callproc("insert_transaction", (trantype, tranamt, acctno))
                print('Successfully deposited to the Account Number ', acctno)
                print('New Account Balance is $ ', account_balance)
            except Exception as err:
                print('Problem Occurred while trying to Deposit to the account',err)
                logger.info(err)
            finally:
                pass

            try:
                update_account = "update accounts set account_balance = :account_balance, account_status = :account_status where acctno = :acctno"
                cursor.execute(update_account,{"acctno": acctno, "account_balance": account_balance, "account_status": account_status})
               
                print('Transaction posted')
            except Exception as err:
                print(' Account cannot be updated due to error ', err)
                logger.info(err)
            finally:
                conn.commit()
                cursor.close()

        elif confirm_close in ('N','n'):
            print('Response is N')
            return
        else:
            print('Invalid Input')
            return


def main_menu():
    
    action = BankSystem(0)
    
    while True:

         
        action.selection()
        choice = input('What do you want to do?: ')

        if choice in ('N','n'):
            action.new_customer()
            
        elif choice in ('O','o'):
            action.getName(0,'')
            action.new_acct()
             
        elif choice in ('D', 'd'):
            action.custinfo(0,'',0)
            action.deposit()
        elif choice in ('W','w'):
            action.custinfo(0,'',0)
            action.withdraw()    
        elif choice in ('i', 'i'):
            action.custinfo(0,'',0)
            action.inquiry()
        elif choice in ('C','c'):
            action.custinfo(0,'',0)
            action.close()
        elif choice in ('E','e'):
            print('Thank you for Banking with us')
            return
        else:
            print('Invalid Selection')
    
    conn.close()

if __name__ == "__main__":
    main_menu()
            
