import cx_Oracle

conn = cx_Oracle.connect("myproject","welcome1","localhost/orcl19c")
cursor = conn.cursor()

print('Successfully Connected to the Database')

def InsEmp():

    empname = input('Employee Name: ')
    lname = input('Employee Lastname: ')
    password = input('Please input Password: ')
    Passverify = input('Verify Password: ')

    if password == Passverify:
        Save_verify = input('Everything correct?  You wish to save now? (Y/N) ')
        if Save_verify == 'Y' or 'y':
           insert_sql = """INSERT INTO employee (firstname, lastname, password) values(:empname, :lname, :password)"""

           cursor.execute(insert_sql,{"empname": empname, "lname": lname, "password": password})    
            
           conn.commit()
           cursor.close()               
           conn.close()
            
           print('New Employee added Successfully')
        else:
           print('Employee not added')
           return
    else:
        print(' Password does not match')
        return




InsEmp()
