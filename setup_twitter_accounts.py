#!/usr/bin/env python3
"""
Twitter Account Setup Script for twscrape
This script helps you add Twitter accounts to twscrape for scraping data
"""

import asyncio
import sys
from twscrape import API

async def setup_accounts():
    """Interactive setup for Twitter accounts"""
    api = API()
    
    print("=== Twitter Account Setup for Football Bot ===")
    print("You need to add at least one Twitter account to enable tweet scraping.")
    print("This account will be used to access Twitter data (read-only).")
    print()
    
    while True:
        print("Options:")
        print("1. Add new Twitter account")
        print("2. List existing accounts")
        print("3. Remove account")
        print("4. Test accounts")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            await add_account(api)
        elif choice == "2":
            await list_accounts(api)
        elif choice == "3":
            await remove_account(api)
        elif choice == "4":
            await test_accounts(api)
        elif choice == "5":
            print("Setup complete!")
            break
        else:
            print("Invalid choice. Please try again.")

async def add_account(api):
    """Add a new Twitter account"""
    print("\n=== Add Twitter Account ===")
    print("You'll need a Twitter account's login credentials.")
    print("Note: Use a secondary account, not your main account.")
    
    username = input("Twitter username (without @): ").strip()
    email = input("Email address: ").strip()
    password = input("Password: ").strip()
    
    if not all([username, email, password]):
        print("All fields are required!")
        return
    
    try:
        print("Adding account...")
        await api.pool.add_account(username, password, email, password)
        print(f"✓ Account @{username} added successfully!")
        
        # Try to login to verify
        print("Verifying account...")
        await api.pool.login_all()
        print("✓ Account verified and logged in!")
        
    except Exception as e:
        print(f"✗ Failed to add account: {e}")
        print("Make sure the credentials are correct and the account exists.")

async def list_accounts(api):
    """List all configured accounts"""
    print("\n=== Current Accounts ===")
    try:
        accounts = await api.pool.accounts()
        if not accounts:
            print("No accounts configured.")
        else:
            for i, account in enumerate(accounts, 1):
                status = "✓ Active" if account.active else "✗ Inactive"
                print(f"{i}. @{account.username} - {status}")
    except Exception as e:
        print(f"Error listing accounts: {e}")

async def remove_account(api):
    """Remove an account"""
    print("\n=== Remove Account ===")
    try:
        accounts = await api.pool.accounts()
        if not accounts:
            print("No accounts to remove.")
            return
        
        print("Current accounts:")
        for i, account in enumerate(accounts, 1):
            print(f"{i}. @{account.username}")
        
        try:
            choice = int(input("Enter account number to remove: ")) - 1
            if 0 <= choice < len(accounts):
                username = accounts[choice].username
                await api.pool.delete_account(username)
                print(f"✓ Account @{username} removed successfully!")
            else:
                print("Invalid account number.")
        except ValueError:
            print("Please enter a valid number.")
            
    except Exception as e:
        print(f"Error removing account: {e}")

async def test_accounts(api):
    """Test account functionality"""
    print("\n=== Testing Accounts ===")
    try:
        accounts = await api.pool.accounts()
        if not accounts:
            print("No accounts to test.")
            return
        
        print("Logging in to all accounts...")
        await api.pool.login_all()
        
        print("Testing with a simple search...")
        async for tweet in api.search("football", limit=1):
            print(f"✓ Successfully fetched tweet: {tweet.rawContent[:100]}...")
            break
        else:
            print("✗ No tweets found. Accounts might need verification.")
            
    except Exception as e:
        print(f"✗ Test failed: {e}")
        print("You may need to verify your accounts or wait for rate limits to reset.")

def print_instructions():
    """Print setup instructions"""
    print("\n=== Setup Instructions ===")
    print("1. Create a new Twitter account (don't use your main account)")
    print("2. Verify the email address")
    print("3. Add the account using this script")
    print("4. The account will be used for read-only access to tweets")
    print()
    print("Important notes:")
    print("- Use a secondary Twitter account, not your personal one")
    print("- The account might need phone verification")
    print("- Keep credentials secure")
    print("- Twitter may require CAPTCHA verification occasionally")
    print()

if __name__ == "__main__":
    print_instructions()
    
    try:
        asyncio.run(setup_accounts())
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)