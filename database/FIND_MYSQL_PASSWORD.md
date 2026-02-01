# How to Find or Reset MySQL Password

## Method 1: Check MySQL Workbench Saved Connections ✅ (Easiest)

### Steps:

1. **Open MySQL Workbench**

2. **Look at the home screen**
   - You'll see saved connections (usually "Local instance MySQL80" or similar)
   - Click on the connection name

3. **Check if password is saved**
   - If you're prompted for a password, your password is NOT saved
   - If it connects automatically, the password might be saved in the connection

4. **View saved password** (if stored):
   - Right-click on the connection → **"Edit Connection"**
   - Click **"Test Connection"**
   - If prompted, the password field might show dots
   - Unfortunately, MySQL Workbench doesn't show saved passwords directly

---

## Method 2: Try Common Default Passwords

Many users set simple passwords during installation. Try these:

- **Empty password** (no password) - Very common!
- `root`
- `admin`
- `password`
- `mysql`
- `123456`

### Test in PowerShell:

```powershell
# Try with no password (most common)
mysql -u root -p
# When prompted, just press Enter (blank password)

# Or try directly:
mysql -u root
```

If you get in, your password is **blank/empty**!

---

## Method 3: Test Connection from Python

Let me create a quick test script:

```python
import pymysql

# Test different passwords
passwords_to_try = ['', 'root', 'admin', 'password', 'mysql']

for pwd in passwords_to_try:
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password=pwd,
            database='mysql'
        )
        print(f"✅ SUCCESS! Password is: '{pwd}' {'(empty/blank)' if pwd == '' else ''}")
        connection.close()
        break
    except Exception as e:
        print(f"❌ Failed with password: '{pwd if pwd else '(empty)'}'")
```

---

## Method 4: Reset MySQL Password (If you forgot it)

### Option A: Using MySQL Workbench

1. **Stop MySQL Service**:
   - Press `Win + R`
   - Type: `services.msc`
   - Find "MySQL80" (or your version)
   - Right-click → **Stop**

2. **Start MySQL in Safe Mode**:
   ```powershell
   # Run as Administrator
   mysqld --skip-grant-tables --skip-networking
   ```

3. **Reset Password in Workbench**:
   - Open new PowerShell window
   - Connect without password:
   ```powershell
   mysql -u root
   ```
   
   - Run these commands:
   ```sql
   FLUSH PRIVILEGES;
   ALTER USER 'root'@'localhost' IDENTIFIED BY 'your_new_password';
   FLUSH PRIVILEGES;
   EXIT;
   ```

4. **Restart MySQL Service Normally**

### Option B: Using Command Line (Easier)

1. Open **PowerShell as Administrator**

2. Run:
   ```powershell
   # Stop MySQL
   net stop MySQL80
   
   # Start in safe mode
   mysqld --skip-grant-tables
   ```

3. **Open NEW PowerShell window**, run:
   ```powershell
   mysql -u root
   ```

4. In MySQL prompt:
   ```sql
   FLUSH PRIVILEGES;
   ALTER USER 'root'@'localhost' IDENTIFIED BY 'newpassword123';
   FLUSH PRIVILEGES;
   EXIT;
   ```

5. **Restart MySQL**:
   ```powershell
   # In admin PowerShell, press Ctrl+C to stop safe mode
   # Then start normally:
   net start MySQL80
   ```

---

## Method 5: Check MySQL Configuration Files

Sometimes the password is in config files (rare):

```powershell
# Check if mysql config exists
Get-Content "C:\ProgramData\MySQL\MySQL Server 8.0\my.ini" | Select-String "password"
```

---

## 🎯 Quick Test Script

I'll create a script to test your connection:

### File: `test_mysql_connection.py`

```python
import pymysql

def test_mysql_connection(password=''):
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
        
        connection.close()
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

# Test with common passwords
print("Testing MySQL connection...")
print("-" * 50)

passwords = [
    '',           # Empty password
    'root',
    'admin', 
    'password',
    'mysql',
    '123456'
]

for pwd in passwords:
    print(f"\nTrying password: '{pwd if pwd else '(empty)'}'")
    if test_mysql_connection(pwd):
        print(f"\n🎉 Use this password in your ETL script: '{pwd}'")
        break
else:
    print("\n⚠️ None of the common passwords worked.")
    print("You may need to reset your MySQL password.")
```

---

## 📝 Recommendation

**Most likely scenario**: Your MySQL password is **EMPTY (blank)**.

### Update your ETL script with:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # ← Empty string (no password)
    'database': 'airpure_aqi_db',
    'port': 3306
}
```

---

## 🆘 Still Can't Connect?

Let me know and I can:
1. Help you reset the password step-by-step
2. Create a test script to try common passwords
3. Help troubleshoot MySQL service issues

---

*Created: February 1, 2026*
