import pandas as pd
import ast

def fav_csv(user_df,username):
    
    csv_file = input("\nprovide path: ")  
    fav_df = pd.read_csv(csv_file)

    fav_df['favorites'] = fav_df['favorites'].apply(ast.literal_eval)
    
    index = user_df[user_df['username'] == username].index[0]
    fav = user_df.at[index, 'favorites']
    
    for _, val in fav_df.iterrows():        
        new_fav = val['favorites']
        for item in new_fav:
            if item not in fav:
                fav.append(item)
    
    print(fav)
    user_df.at[index, 'favorites'] = fav
    
    return 0

def add_fav(user_df,books_df,username):

    index = user_df[user_df['username'] == username].index[0]
    fav = user_df.loc[index,'favorites']
    print(f'Current favorites: {fav}')

    x = add_entry(index,user_df,books_df)
    if not x:
        print("books does not exist")
        return 1
    user_df.at[index, 'favorites'] = x
    return 0

def add_bal(user_df,username):
    
    bal = int(input('Enter balance you want to add: '))
    index = user_df[user_df['username'] == username].index[0]
    old_bal = int(user_df.at[index,'balance']) 
    new_bal = int(old_bal + bal)
    user_df.at[index,'balance'] = new_bal
    
    return 0

def modify_user(user_df,username):
    
    index = user_df[user_df['username'] == username].index[0]
        
    while True:
        new_username = input(f"\nEnter new username (press enter to keep current '{username}'): ")
        if not new_username == '':
            if new_username not in user_df['username'].values:
                user_df.at[index, 'username'] = new_username
                print(f"Username updated to: {new_username}")
                break
            else:
                print("Username already exists. Please choose a different username.")
        else:
            break
              
    while True:
        new_password = input("Enter new password (press enter to keep current password): ")
        if not new_password == '':
            if len(new_password) >= 8 and any(not c.isalnum() for c in new_password):
                user_df.at[index, 'password'] = new_password
                print("Password updated.")
                break
            else:
                print("Password must be at least 8 characters long and contain at least one special character.")
        else:
            break
        
    curr_address = user_df.at[index , 'address']   
    new_address = input(f"Enter new address (press enter to keep current '{curr_address}'): ")
    
    if not new_address == '':
        user_df.at[index, 'address'] = new_address
        print(f"City updated to: {new_address}")
    
    curr_city = user_df.at[index , 'city']   
    new_city = input(f"Enter new city (press enter to keep current '{curr_city}'): ")
    
    if not new_city == '':
        user_df.at[index, 'city'] = new_city
        print(f"City updated to: {new_city}")
        
    return 0

def rem_fav(user_df,username):
    
    index = user_df[user_df['username'] == username].index[0]

    curr_favorites = user_df.at[index, 'favorites']
    print(f"Current favorites: {curr_favorites}")
    
    books = input("Enter book IDs to remove (comma-separated, e.g., 77,88,99): ").strip()

    books_list = books.split(',')
    books_list = [int(x) for x in books_list]

    new_fav = [fav for fav in curr_favorites if fav not in books_list]
    
    user_df.at[index, 'favorites'] = new_fav
    
    return 0
  
def check_balance(user_df,username):

    index = user_df[user_df['username'] == username].index[0]
    print(f"Your balance is: {user_df.at[index , 'balance']}")
     
def check_fav(user_df,books_df,username):
       
    index = user_df[user_df['username'] == username].index[0]
    fav = user_df.at[index, 'favorites']
    print(f'\nYour favorites: {fav}').strip()
    ids = input("Write fav you want to check price(as 88,77,23) or enter for all")
    if ids:
        ids = fav
    ids = ids.split(',')
    ids = [int(x) for x in ids]
    for x in ids:
        total_cost,avai = check_avai_price(books_df,x)
        print(f'For book {x}.The price is: {total_cost} and availabilty: {avai}')
        
def check_orders(user_df,books_df,username):
    
    index = user_df[user_df['username'] == username].index[0]
    bal = float(user_df.at[index,'balance'])
    ord = user_df.at[index, 'orders']
    
    print(f'Your orders: {ord}')            
    ids = input('Write orders you want to add or delete(99,77,55)').strip()
    ids = ids.split(',')     
    ids = [int(x) for x in ids]
    print(ids)
    
    ch = input('Want to (a)dd or (d)elete')
    sum = 0.0
    if ch == 'a':
        available_ids = []
        for id in ids:
            print(id)
            total_cost,avai = check_avai_price(books_df,id)
            if avai:               
                sum += total_cost
                available_ids.append(id)
            else:
                print(f'book {id} is not available removing it from the list')
                
    
        if bal - sum < 0:
            print("insufficient funds for order")
            return 1
        
        new_ord = ord + available_ids
        bal = bal - sum
        
        user_df.at[index,'balance'] = bal
        user_df.at[index,'orders'] = new_ord
        return 0
    
    elif ch == 'd':
        if all(x in ord for x in ids):
            for id in ids:
                total_cost,_ = check_avai_price(books_df,id)
                sum += total_cost
        else:
            print("books were not in original order")
            return 1 
        
        new_ord = [x for x in ord if x not in ids]
        bal = bal + sum
        
        user_df.at[index,'balance'] = bal
        user_df.at[index,'orders'] = new_ord
        return 0   
                
def check_avai_price(books_df,index):
    
    cost = float(books_df.loc[index,'shipping_cost'])
    shi_cost = float(books_df.loc[index,'cost'])
    total_cost = cost + shi_cost
    avai = books_df.loc[index,'availability']
  
    return total_cost,avai

def add_entry(index,user_df,books_df):
               
    title = input(f"\nWrite the title of the book you want to add to the favorites: ")
    if title not in books_df['title'].values:
        return False
         
    id = books_df.loc[books_df['title'] == title, 'id'].values[0]
    x = user_df.at[index, 'favorites']
        
    if id not in x:
        x.append(id)
    return x
