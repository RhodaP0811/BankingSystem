create table employees(
empid integer generated always as IDENTITY start with 100 increment by 10,
empname varchar(30) not null,
password varchar(10) not null,
PRIMARY KEY(EMPID))
tablespace bank
;
create table accounts(
  acctno INTEGER GENERATED ALWAYS AS IDENTITY start with 1000 increment by 100,
  customer_name char(30) not null,
  account_type char(1) not null,
  account_status char(3) not null,
  account_balance number(10,2) not null,
  Account_created timestamp,
  PRIMARY KEY(acctno), 
  tranid int constraint fk references services(tranid)
  customerID int constraint fk references customers(customerID))
  tablespace bank
  ;
create table customers(
  customerID integer generated always as IDENTITY start with 100 increment by 3,
  customer_name char(30) not null,
  customer_address varchar(50),
  phone varchar(15) not null,
  email varchar(70) not null,
  PRIMARY KEY(customerID),
  acctno int constraint fk references accounts(acctno))
  tablespace bank
;
  
create table transaction(
  tranid INTEGER GENERATED ALWAYS AS IDENTITY start with 5 increment by 3,
  trandate timestamp,
  trantype char(10) not null,
  tranamt number(10,2) not null,
  acctno int constraint fk references accounts(acctno),
  PRIMARY KEY(tranid))
tablespace bank
;
