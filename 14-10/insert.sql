-- Reset
DROP TABLE IF EXISTS Customers;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Receipts;

-- Section 1
-- Customers table
CREATE TABLE Customers (
    cust_key int primary key not null,
    mkt_segment varchar(255) not null
);

-- Orders Table
CREATE TABLE Orders (
    order_key int primary key not null,
    cust_key int not null
);

INSERT INTO Customers(cust_key,mkt_segment)
VALUES 
    (0, 'shoes'),
    (1, 'shoes'),
    (2, 'pencil')
;

INSERT INTO Orders(order_key,cust_key)
VALUES
    (0, 0),
    (1, 0),
    (2, 1),
    (3, 2)
;

-- Section 2

CREATE TABLE Receipts (
    receipt_key int primary key not null,
    user_key int not null,
    receipt_amount double not null,
    timestamp timestamp default current_timestamp
)

INSERT INTO Receipts(receipt_key, user_key, receipt_amount, payment_date)
VALUES
    (0,0,2.23),
    (1,0,0.55),
    (2,0,1.53),
    (3,1,0.0)
);
