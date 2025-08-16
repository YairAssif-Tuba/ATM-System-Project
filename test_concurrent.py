import requests
import threading
import time
import json

# Base URL for the API
BASE_URL = "http://localhost:5000"

def test_concurrent_withdrawals():
    """Test concurrent withdrawals on the same account"""
    print("🧪 Testing Concurrent Withdrawals...\n")
    
    # Reset account balance first
    initial_balance = 1000.00
    account_number = "123456789"
    
    # Function for withdrawal thread
    def withdraw_money(thread_id, amount):
        try:
            print(f"   Thread {thread_id}: Attempting to withdraw ${amount:.2f}")
            response = requests.post(
                f"{BASE_URL}/accounts/{account_number}/withdraw",
                json={"amount": amount},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   Thread {thread_id}: ✅ Success! Withdrew ${data['withdrawn_amount']:.2f}, New Balance: ${data['new_balance']:.2f}")
            elif response.status_code == 423:
                print(f"   Thread {thread_id}: 🔒 Account locked, retrying...")
                # Retry after a short delay
                time.sleep(0.2)
                response = requests.post(
                    f"{BASE_URL}/accounts/{account_number}/withdraw",
                    json={"amount": amount},
                    headers={"Content-Type": "application/json"}
                )
                if response.status_code == 200:
                    data = response.json()
                    print(f"   Thread {thread_id}: ✅ Success on retry! Withdrew ${data['withdrawn_amount']:.2f}, New Balance: ${data['new_balance']:.2f}")
                else:
                    print(f"   Thread {thread_id}: ❌ Failed on retry: {response.json()}")
            else:
                print(f"   Thread {thread_id}: ❌ Failed: {response.json()}")
                
        except Exception as e:
            print(f"   Thread {thread_id}: ❌ Error: {e}")
    
    # Create multiple threads for concurrent withdrawals
    threads = []
    withdrawal_amounts = [50.00, 75.00, 100.00, 25.00, 60.00]
    
    print(f"Starting {len(withdrawal_amounts)} concurrent withdrawals from account {account_number}")
    print(f"Initial balance: ${initial_balance:.2f}")
    print("-" * 60)
    
    # Start all threads
    for i, amount in enumerate(withdrawal_amounts):
        thread = threading.Thread(target=withdraw_money, args=(i+1, amount))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Check final balance
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/accounts/{account_number}/balance")
    if response.status_code == 200:
        final_balance = response.json()['balance']
        total_withdrawn = initial_balance - final_balance
        print(f"Final balance: ${final_balance:.2f}")
        print(f"Total withdrawn: ${total_withdrawn:.2f}")
        print(f"Expected withdrawn: ${sum(withdrawal_amounts):.2f}")
        
        if abs(total_withdrawn - sum(withdrawal_amounts)) < 0.01:
            print("✅ Concurrent withdrawals working correctly!")
        else:
            print("❌ Concurrent withdrawals may have race conditions!")
    else:
        print("❌ Could not check final balance")

def test_concurrent_deposits():
    """Test concurrent deposits on the same account"""
    print("\n🧪 Testing Concurrent Deposits...\n")
    
    account_number = "987654321"
    
    # Function for deposit thread
    def deposit_money(thread_id, amount):
        try:
            print(f"   Thread {thread_id}: Attempting to deposit ${amount:.2f}")
            response = requests.post(
                f"{BASE_URL}/accounts/{account_number}/deposit",
                json={"amount": amount},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   Thread {thread_id}: ✅ Success! Deposited ${data['deposited_amount']:.2f}, New Balance: ${data['new_balance']:.2f}")
            elif response.status_code == 423:
                print(f"   Thread {thread_id}: 🔒 Account locked, retrying...")
                # Retry after a short delay
                time.sleep(0.2)
                response = requests.post(
                    f"{BASE_URL}/accounts/{account_number}/deposit",
                    json={"amount": amount},
                    headers={"Content-Type": "application/json"}
                )
                if response.status_code == 200:
                    data = response.json()
                    print(f"   Thread {thread_id}: ✅ Success on retry! Deposited ${data['deposited_amount']:.2f}, New Balance: ${data['new_balance']:.2f}")
                else:
                    print(f"   Thread {thread_id}: ❌ Failed on retry: {response.json()}")
            else:
                print(f"   Thread {thread_id}: ❌ Failed: {response.json()}")
                
        except Exception as e:
            print(f"   Thread {thread_id}: ❌ Error: {e}")
    
    # Get initial balance
    response = requests.get(f"{BASE_URL}/accounts/{account_number}/balance")
    if response.status_code == 200:
        initial_balance = response.json()['balance']
    else:
        print("❌ Could not get initial balance")
        return
    
    # Create multiple threads for concurrent deposits
    threads = []
    deposit_amounts = [100.00, 150.00, 200.00, 75.00, 125.00]
    
    print(f"Starting {len(deposit_amounts)} concurrent deposits to account {account_number}")
    print(f"Initial balance: ${initial_balance:.2f}")
    print("-" * 60)
    
    # Start all threads
    for i, amount in enumerate(deposit_amounts):
        thread = threading.Thread(target=deposit_money, args=(i+1, amount))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Check final balance
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/accounts/{account_number}/balance")
    if response.status_code == 200:
        final_balance = response.json()['balance']
        total_deposited = final_balance - initial_balance
        print(f"Final balance: ${final_balance:.2f}")
        print(f"Total deposited: ${total_deposited:.2f}")
        print(f"Expected deposited: ${sum(deposit_amounts):.2f}")
        
        if abs(total_deposited - sum(deposit_amounts)) < 0.01:
            print("✅ Concurrent deposits working correctly!")
        else:
            print("❌ Concurrent deposits may have race conditions!")
    else:
        print("❌ Could not check final balance")

def test_mixed_operations():
    """Test mixed deposit and withdrawal operations"""
    print("\n🧪 Testing Mixed Operations (Deposits + Withdrawals)...\n")
    
    account_number = "555555555"
    
    # Function for mixed operations
    def mixed_operation(thread_id, operation_type, amount):
        try:
            print(f"   Thread {thread_id}: Attempting {operation_type} of ${amount:.2f}")
            
            if operation_type == "deposit":
                response = requests.post(
                    f"{BASE_URL}/accounts/{account_number}/deposit",
                    json={"amount": amount},
                    headers={"Content-Type": "application/json"}
                )
            else:  # withdrawal
                response = requests.post(
                    f"{BASE_URL}/accounts/{account_number}/withdraw",
                    json={"amount": amount},
                    headers={"Content-Type": "application/json"}
                )
            
            if response.status_code == 200:
                data = response.json()
                if operation_type == "deposit":
                    print(f"   Thread {thread_id}: ✅ Success! Deposited ${data['deposited_amount']:.2f}, New Balance: ${data['new_balance']:.2f}")
                else:
                    print(f"   Thread {thread_id}: ✅ Success! Withdrew ${data['withdrawn_amount']:.2f}, New Balance: ${data['new_balance']:.2f}")
            elif response.status_code == 423:
                print(f"   Thread {thread_id}: 🔒 Account locked, retrying...")
                time.sleep(0.2)
                if operation_type == "deposit":
                    response = requests.post(
                        f"{BASE_URL}/accounts/{account_number}/deposit",
                        json={"amount": amount},
                        headers={"Content-Type": "application/json"}
                    )
                else:
                    response = requests.post(
                        f"{BASE_URL}/accounts/{account_number}/withdraw",
                        json={"amount": amount},
                        headers={"Content-Type": "application/json"}
                    )
                
                if response.status_code == 200:
                    data = response.json()
                    if operation_type == "deposit":
                        print(f"   Thread {thread_id}: ✅ Success on retry! Deposited ${data['deposited_amount']:.2f}, New Balance: ${data['new_balance']:.2f}")
                    else:
                        print(f"   Thread {thread_id}: ✅ Success on retry! Withdrew ${data['withdrawn_amount']:.2f}, New Balance: ${data['new_balance']:.2f}")
                else:
                    print(f"   Thread {thread_id}: ❌ Failed on retry: {response.json()}")
            else:
                print(f"   Thread {thread_id}: ❌ Failed: {response.json()}")
                
        except Exception as e:
            print(f"   Thread {thread_id}: ❌ Error: {e}")
    
    # Get initial balance
    response = requests.get(f"{BASE_URL}/accounts/{account_number}/balance")
    if response.status_code == 200:
        initial_balance = response.json()['balance']
    else:
        print("❌ Could not get initial balance")
        return
    
    # Create mixed operations
    operations = [
        ("deposit", 100.00),
        ("withdraw", 50.00),
        ("deposit", 75.00),
        ("withdraw", 25.00),
        ("deposit", 200.00)
    ]
    
    print(f"Starting {len(operations)} mixed operations on account {account_number}")
    print(f"Initial balance: ${initial_balance:.2f}")
    print("-" * 60)
    
    # Start all threads
    threads = []
    for i, (operation_type, amount) in enumerate(operations):
        thread = threading.Thread(target=mixed_operation, args=(i+1, operation_type, amount))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Check final balance
    print("-" * 60)
    response = requests.get(f"{BASE_URL}/accounts/{account_number}/balance")
    if response.status_code == 200:
        final_balance = response.json()['balance']
        expected_change = sum(amount if op == "deposit" else -amount for op, amount in operations)
        actual_change = final_balance - initial_balance
        
        print(f"Final balance: ${final_balance:.2f}")
        print(f"Expected change: ${expected_change:.2f}")
        print(f"Actual change: ${actual_change:.2f}")
        
        if abs(actual_change - expected_change) < 0.01:
            print("✅ Mixed operations working correctly!")
        else:
            print("❌ Mixed operations may have race conditions!")
    else:
        print("❌ Could not check final balance")

if __name__ == "__main__":
    print("🚀 ATM System Concurrent Access Testing")
    print("Make sure the server is running on http://localhost:5000\n")
    
    try:
        # Test concurrent withdrawals
        test_concurrent_withdrawals()
        
        # Test concurrent deposits
        test_concurrent_deposits()
        
        # Test mixed operations
        test_mixed_operations()
        
        print("\n✅ All concurrent access tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the server is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
