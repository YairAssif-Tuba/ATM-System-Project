import requests
import threading
import time
import random

def test_deposits():
    """Test 50 concurrent deposits of $1 each to a random account"""
    # Generate random account number
    account_number = str(random.randint(100000, 999999))
    print("Testing 50 Concurrent Deposits of $1 each")
    print(f"Account: {account_number} (random account)")
    
    def make_deposit(thread_id):
        try:
            response = requests.post(
                f"https://atm-system-project.ew.r.appspot.com/accounts/{account_number}/deposit",
                json={"amount": 1.00},
                timeout=15
            )
            print(f"Deposit Thread {thread_id}: {response.text}")
            return response.status_code
        except Exception as e:
            print(f"Deposit Thread {thread_id}: Error - {e}")
            return None
    
    # Create 50 threads for deposits with random thread IDs
    threads = []
    thread_ids = random.sample(range(1, 101), 50)  # Random 50 IDs from 1-100
    
    for i, thread_id in enumerate(thread_ids):
        thread = threading.Thread(target=make_deposit, args=(thread_id,))
        threads.append(thread)
    
    # Start all threads at the same time
    print("Starting 50 concurrent deposit requests...")
    start_time = time.time()
    
    for thread in threads:
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    print(f"⏱️  Total time: {end_time - start_time:.2f} seconds")
    
    # Check final balance
    try:
        response = requests.get(f"https://atm-system-project.ew.r.appspot.com/accounts/{account_number}/balance", timeout=15)
        print(f"💰 Final balance after deposits: {response.text}")
    except Exception as e:
        print(f"Error getting final balance: {e}")
    
    return account_number

def test_withdrawals(account_number):
    """Test 20 concurrent withdrawals of $1 each from the same account"""
    print(f"\n🧪 Testing 20 Concurrent Withdrawals of $1 each...")
    print(f"Account: {account_number}")
    
    def make_withdrawal(thread_id):
        try:
            response = requests.post(
                f"https://atm-system-project.ew.r.appspot.com/accounts/{account_number}/withdraw",
                json={"amount": 1.00},
                timeout=15
            )
            print(f"Withdrawal Thread {thread_id}: {response.text}")
            return response.status_code
        except Exception as e:
            print(f"Withdrawal Thread {thread_id}: Error - {e}")
            return None
    
    # Create 20 threads for withdrawals with random thread IDs
    threads = []
    thread_ids = random.sample(range(1, 51), 20)  # Random 20 IDs from 1-50
    
    for i, thread_id in enumerate(thread_ids):
        thread = threading.Thread(target=make_withdrawal, args=(thread_id,))
        threads.append(thread)
    
    # Start all threads at the same time
    print("Starting 20 concurrent withdrawal requests...")
    start_time = time.time()
    
    for thread in threads:
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    print(f"⏱️  Total time: {end_time - start_time:.2f} seconds")
    
    # Check final balance
    try:
        response = requests.get(f"https://atm-system-project.ew.r.appspot.com/accounts/{account_number}/balance", timeout=15)
        print(f"💰 Final balance after withdrawals: {response.text}")
    except Exception as e:
        print(f"Error getting final balance: {e}")

if __name__ == "__main__":
    print("🔒 ATM System Locking Test - Random Account & Thread IDs")
    print("=" * 60)
    
    # Run deposit test and get the account number
    account_number = test_deposits()
    
    # Run withdrawal test on the same account
    test_withdrawals(account_number)
    
    print("\n✅ Locking test completed!")
    print("\n📊 Expected Results:")
    print("- If locking works: Should see some 'Account is busy' messages")
    print("- Final balance should be: $50 - $20 = $30")
    print("- Operations should take longer due to serialization")
    print("- If locking fails: All operations succeed quickly, final balance = $50")
    print(f"- Random account used: {account_number}")
