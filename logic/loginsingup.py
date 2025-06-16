import pandas as pd
import getpass

def admin_login(admin_df):
    """Είσοδος διαχειριστή με έλεγχο ταυτοποίησης και μέγιστο 3 προσπάθειες."""
    attempts = 0
    while attempts < 3:
        username = input("Name: ")
        password = getpass.getpass("Inster password: ")

        admin = admin_df[admin_df['username'] == username]
        if not admin.empty and admin['password'].values[0] == password:
            print("Succsesfull login!")
            return True,username
        else:
            print("Wrong name or password.")
            attempts += 1
    
    print("Too many attempts.")
    return False,None

def user_login(user_df):
    
    attempts = 0
    while attempts < 3:
        username = input("Username: ")
        password = getpass.getpass("password: ")

        user = user_df[user_df['username'] == username]
        if not user.empty and user['password'].values[0] == password:
            print(f"Καλώς ήλθατε, {username}!")
            return True,username
        else:
            print("Wrong Username or password")
            attempts += 1

    print("Too many attempts.")
    return None  

def user_signup(user_df):
    
    while True:
        username = input("Chosse Username: ")
        if username in user_df['username'].values:
            print("Name already exist try anoher one.")
        else:
            break

    while True:
        password = getpass.getpass("Chosse a password(at lest >8 characters and one special character): ")
        if len(password) < 8 or not any(not c.isalnum() for c in password):
            print("Password doesent pass requirments")
        else:
            break

    id = len(user_df)
    city = input("City:")
    address = input("Address:")
    new_user = pd.DataFrame({
        'id': [id], 'username': [username], 'password': [password], 
        'address': [address], 'city': [city], 'orders': [[]],
        'favorites': [[]], 'balance': 0.0
    })
    
    user_df = pd.concat([user_df, new_user], ignore_index=True)                 
    print("User created Succsesfully")            
    return user_df