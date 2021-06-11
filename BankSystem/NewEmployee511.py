import cx_Oracle
import logging

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = logging.getLogger(__name__)

# To override the default severity of logging
logger.setLevel('DEBUG')

# Use FileHandler() to log to a file
file_handler = logging.FileHandler('employee.log')
 
formatter = logging.Formatter(log_format)
file_handler.setFormatter(formatter)

# Don't forget to add the file handler
logger.addHandler(file_handler)

conn = cx_Oracle.connect("peppermint","welcome1","localhost/orcl19c")
cursor = conn.cursor()

print('Successfully Connected to the Database')

def EmpDetails():
    

    isempty = False

    while True:
        try:
           empid = int(input("Provide Employee ID: "))
           break
        except ValueError:
           print("Not a valid Customer ID, please enter the number! Please try again ...")
           logger.info("Not a Valid Customer ID entered")

    
    try:

        check_password ="SELECT password, empname FROM employees where empid = :empid"
        result_pw =  cursor.execute(check_password,{"empid": empid})
        result_pw = cursor.fetchone()
        empname = result_pw[1]

        if not cursor.rowcount:
            print('Employee not found')
            logger.info('Employee not found')
            isempty = True
            return EmpDetails()

    except Exception as err:
        print('Problem retrieving the Employee name for this ID', err)
        logger.info('Problem retrieving the customer name')
        return EmpDetails()
    
    finally:
#            cursor.close()
        pass
    
    
    
    while True:
        try:
            password = input("Please provide password:  ")
            break
        except:
            print('Password required') 
             
    if result_pw[0] == password:
        print('Welcome ', empname)
        print('You are an authorized user ')
        
        
    else:    
        print('Invalid password')
        logger.info('Invalid Password entered')
        return EmpDetails()
        
    if isempty == True:
        print('You are not an invalid user')
        logger.info('Invalid user')
        return EmpDetails()
                

EmpDetails()
