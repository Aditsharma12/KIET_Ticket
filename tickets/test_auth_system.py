"""
Test script for authentication system
Tests MongoDB connection and user authentication functions
"""

from mongodb_utils import create_user, authenticate_user, get_user_by_username, get_users_collection

def test_auth_system():
    print("="*50)
    print("TESTING AUTHENTICATION SYSTEM")
    print("="*50)
    
    # Test 1: Create a test user
    print("\n1. Testing user creation...")
    test_username = "test_user_demo"
    test_password = "password123"
    
    # Clean up any existing test user
    users = get_users_collection()
    users.delete_one({'username': test_username})
    
    result = create_user(test_username, test_password)
    if result:
        print("✅ User created successfully!")
    else:
        print("❌ Failed to create user")
    
    # Test 2: Try to create duplicate user
    print("\n2. Testing duplicate prevention...")
    result = create_user(test_username, test_password)
    if not result:
        print("✅ Duplicate prevention works!")
    else:
        print("❌ Duplicate user was created (should not happen)")
    
    # Test 3: Authenticate user with correct password
    print("\n3. Testing authentication with correct password...")
    user = authenticate_user(test_username, test_password)
    if user and user['username'] == test_username:
        print("✅ Authentication successful!")
        print(f"   User data: {user}")
    else:
        print("❌ Authentication failed")
    
    # Test 4: Authenticate user with wrong password
    print("\n4. Testing authentication with wrong password...")
    user = authenticate_user(test_username, "wrongpassword")
    if user is None:
        print("✅ Correctly rejected wrong password!")
    else:
        print("❌ Wrong password was accepted (security issue!)")
    
    # Test 5: Get user by username
    print("\n5. Testing user retrieval...")
    user = get_user_by_username(test_username)
    if user and user['username'] == test_username:
        print("✅ User retrieval successful!")
        print(f"   User data: {user}")
    else:
        print("❌ User retrieval failed")
    
    # Test 6: Check password is hashed
    print("\n6. Testing password hashing...")
    users = get_users_collection()
    user_doc = users.find_one({'username': test_username})
    if user_doc and 'password_hash' in user_doc:
        password_hash = user_doc['password_hash']
        if password_hash != test_password.encode():
            print("✅ Password is properly hashed!")
            print(f"   Hash (first 30 chars): {str(password_hash)[:30]}...")
        else:
            print("❌ Password is stored in plain text (SECURITY ISSUE!)")
    
    # Clean up
    print("\n7. Cleaning up test user...")
    users.delete_one({'username': test_username})
    print("✅ Test user deleted")
    
    print("\n" + "="*50)
    print("ALL TESTS COMPLETED!")
    print("="*50)

if __name__ == "__main__":
    try:
        test_auth_system()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
