# ATM System Server
## General approach
Attached here is simple ATM system server implementation with RESTful API endpoints for banking operations. In my implementation, I focused on trying to make the ATM as secured as possible, trying to lower security vulnerabilities as much
as possible. Means, I chose to use locks per account so each account will be able to withdraw and deposit atomically, in order
to not have any TOCTOU vulnerabilities that'll make users able to mess with their balance in a way that the system doesn't want
to happen.

## Challanges Faced
The most difficult challange I faced in this assignment was to understand the REST API syntax and how to use it. Although the implementations and the idea of locks was clear to me, deploying the server and writing the system as a server and not just as a script was something I did not face as a student. However, using AI tools, youtube and reading some code, I managed to understand how to write it and I learned a lot from this assignment.

## Features

- **Get Balance**: Retrieve current account balance
- **Withdraw Money**: Withdraw specified amount from account (requires existing account)
- **Deposit Money**: Deposit specified amount to account (creates account if it doesn't exist)
- **Thread Safety**: Account-level locking for concurrent access
- **Automatic Account Creation**: New accounts created automatically on first deposit

## Pre-loaded Accounts 
- Account: `123456789` - Balance: $1,000.00
- Account: `987654321` - Balance: $2,500.00
- Account: `555555555` - Balance: $500.00

## API Endpoints

### 1. Get Balance
- **URL**: `GET /accounts/{account_number}/balance`
- **Description**: Retrieve the current balance of an account
- **Response**: JSON with account number, balance, and success message
- **Simple Response**: Add `?simple=true` to get just the balance number

### 2. Withdraw Money
- **URL**: `POST /accounts/{account_number}/withdraw`
- **Description**: Withdraw a specified amount from an account
- **Request Body**: `{"amount": 100.00}`
- **Response**: JSON with withdrawn amount, new balance, and success message

### 3. Deposit Money
- **URL**: `POST /accounts/{account_number}/deposit`
- **Request Body**: `{"amount": 100.00}`
- **Note**: **Creates account if it doesn't exist**

### 4. List All Accounts
- **URL**: `GET /accounts`

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server**:
   ```bash
   python app.py
   ```

3. **Test with curl**:
   ```bash
   # Get balance
   curl -X GET http://localhost:5000/accounts/123456789/balance
   
   # Deposit money
   curl -X POST http://localhost:5000/accounts/123456789/deposit \
   -H "Content-Type: application/json" \
   -d '{"amount": 200.00}'
   
   # Withdraw money
   curl -X POST http://localhost:5000/accounts/123456789/withdraw \
   -H "Content-Type: application/json" \
   -d '{"amount": 100.00}'
   ```

## Security Features

### **🔒 Account-Level Locking**
- Each account has its own lock to prevent race conditions
- Only one transaction can access an account at a time
- 10-second timeout prevents deadlocks and allows system to run without waiting too much to lock
- Prevents TOCTOU (Time of Check to Time of Use) vulnerabilities

### **⚡ Concurrent Access**
- Multiple users can access different accounts simultaneously
- Same account transactions are serialized for data integrity

## Error Handling
- **404**: Account not found (for withdrawals)
- **400**: Invalid request (missing amount, insufficient balance, negative amounts)
- **423**: Account is busy (locked by another transaction)
- **500**: Server errors

## Testing

```bash
# Basic API tests
python test_api.py

# Concurrent access tests
python test_concurrent.py

# Test automatic account creation
curl -X POST http://localhost:5000/accounts/999999999/deposit \
-H "Content-Type: application/json" \
-d '{"amount": 500.00}'
```

## Project Structure

```
ATM System Project/
├── app.py              # Main Flask application with thread safety
├── requirements.txt    # Python dependencies
├── test_api.py         # Basic API testing script
├── test_concurrent.py  # Concurrent access testing script
├── Procfile           # Cloud deployment configuration
└── README.md          # Project documentation
```


