"""
MySQL Connection Tester
Purpose: Test MySQL connection with different passwords
"""

import pymysql

def test_mysql_connection(password=''):
    """Test MySQL connection with given password"""
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password=password,
            port=3306
        )
        print(f"✅ SUCCESS! Connected to MySQL")
        print(f"   Password: '{password if password else '(EMPTY/BLANK)'}'")
        
        # Get MySQL version
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"   MySQL Version: {version[0]}")
        
        # Get databases
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        print(f"   Databases: {len(databases)} found")
        
        connection.close()
        return True, password
    except Exception as e:
        return False, str(e)

def main():
    """Main function to test common passwords"""
    print("=" * 60)
    print("MySQL Connection Tester")
    print("=" * 60)
    print("\nTesting MySQL connection with common passwords...")
    print("-" * 60)
    
    # Common passwords to try (in order of likelihood)
    passwords_to_test = [
        ('', 'Empty/Blank (No Password)'),
        ('root', 'root'),
        ('admin', 'admin'),
        ('password', 'password'),
        ('mysql', 'mysql'),
        ('123456', '123456'),
        ('12345', '12345'),
    ]
    
    success = False
    working_password = None
    
    for pwd, description in passwords_to_test:
        print(f"\n🔍 Trying: {description}")
        print(f"   Password value: '{pwd if pwd else '(empty string)'}'")
        
        is_success, result = test_mysql_connection(pwd)
        
        if is_success:
            success = True
            working_password = pwd
            print("\n" + "=" * 60)
            print("🎉 CONNECTION SUCCESSFUL!")
            print("=" * 60)
            print(f"\n📝 Your MySQL password is: '{pwd if pwd else '(EMPTY)'}'")
            print("\n💡 Update your ETL script with:")
            print("-" * 60)
            print(f"DB_CONFIG = {{")
            print(f"    'host': 'localhost',")
            print(f"    'user': 'root',")
            print(f"    'password': '{pwd}',  # ← Use this")
            print(f"    'database': 'airpure_aqi_db',")
            print(f"    'port': 3306")
            print(f"}}")
            print("-" * 60)
            break
        else:
            print(f"   ❌ Failed: {result[:100]}...")
    
    if not success:
        print("\n" + "=" * 60)
        print("⚠️ NONE OF THE COMMON PASSWORDS WORKED")
        print("=" * 60)
        print("\n📋 Next steps:")
        print("1. Check MySQL Workbench connections")
        print("2. Try manually entering your password")
        print("3. Reset MySQL password (see FIND_MYSQL_PASSWORD.md)")
        print("\n💡 Or enter your password manually:")
        
        try:
            manual_password = input("\nEnter your MySQL password (or press Enter to skip): ")
            if manual_password:
                is_success, result = test_mysql_connection(manual_password)
                if is_success:
                    print("\n✅ Success with your manually entered password!")
                    working_password = manual_password
                else:
                    print(f"\n❌ Still failed: {result}")
        except KeyboardInterrupt:
            print("\n\nTest cancelled by user.")
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("Test Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()
