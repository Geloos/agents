import pandas as pd
import matplotlib.pyplot as plt
import ast

def load_books_from_csv(books_df):

    file = input("provide csv file path")
    try:
        new_books_df = pd.read_csv(file)
    except Exception as e:
        print("Worng File")
    new_books_df = new_books_df.reindex(columns=books_df.columns)
    new_books_df['bookstores'] = new_books_df['bookstores'].apply(ast.literal_eval)  

    existing_titles = set(books_df['title'])
    
    for _, new_book in new_books_df.iterrows():
        if new_book['title'] in existing_titles:
            
            existing_bookstores = books_df.loc[books_df['title'] == new_book['title'], 'bookstores'].values[0]
            existing_book_index = books_df.index[books_df['title'] == new_book['title']][0]  
            print(existing_bookstores)
            for key,value in new_book['bookstores'].items():
                if key in existing_bookstores:
                    
                    existing_bookstores[key] += value
                else:
                    existing_bookstores[key] = value
                                                            
            books_df.loc[existing_book_index, 'copies'] = sum(existing_bookstores.values())
               
    new_books_df = new_books_df[~new_books_df['title'].isin(existing_titles)]
    for i in range(len(new_books_df)):
        new_books_df.iloc[i, new_books_df.columns.get_loc('id')] = len(books_df) + i
    
    books_df = pd.concat([books_df, new_books_df], ignore_index=True) 
   
    return books_df

def add_individual_entry(books_df):
    
    id = len(books_df)
    print(id)
    
    title = input("Enter book title: ")
    title = title + '.'
    
    if title in books_df['title'].values:
        print("This book already exists in the database. Updating the entry.")
        existing_book_index = books_df.index[books_df['title'] == title ][0]
        print(existing_book_index)
        existing_bookstores = books_df.at[existing_book_index, 'bookstores']
        bookstore = input("in which bookstore would you like to put the entry?")
        existing_bookstores[bookstore] += 1    
        books_df.loc[existing_book_index,'copies'] += 1
        return books_df
    
    author = input("Enter book author: ")
    publisher = input("Enter book publisher: ")

    categories = input("Enter book categories (as commedy,action): ")
    if not isinstance(categories, list):
        categories_list = [category.strip() for category in categories.split(',')]
    
    
    cost = float(input("Enter book cost: "))
    shipping_cost = float(input("Enter shipping cost: "))
    availability = bool(input("Enter book availability (True or False): "))
    copies = int(input("Enter number of copies: "))

    bookstores = input("Enter bookstores (as bookstore1:2 bookstore2:3): ")
    try:
       
        bookstores_list = bookstores.split()
        
        bookstores_dict = {}
        for item in bookstores_list:
            split_item = item.split(':') 
            key = split_item[0]
            value = int(split_item[1])
            bookstores_dict[key.strip()] = value
    
    except Exception as e:
        print("Invalid input for bookstores. Please enter in the format 'bookstore1:2 bookstore2:3, ...'") 

    new_entry = pd.DataFrame([[id, title, author, publisher, categories_list, cost, shipping_cost, availability, copies, bookstores_dict]], 
                            columns=books_df.columns)
    
    books_df = pd.concat([books_df, new_entry], ignore_index=True)

    return books_df

def modify_entries(admin_df, books_df, username):
    
    admin_bookstores = admin_df.loc[admin_df['username'] == username, 'bookstores'].values[0]
    print(admin_bookstores)
    
    title = input("Enter the title of the book you want to modify: ")
    title = title + '.'
    
    if title in books_df['title'].values:
        book_index = books_df.index[books_df['title'] == title][0]
        book_bookstores = books_df.loc[book_index, 'bookstores']
        print(book_bookstores)
        print(book_index)
        for bookstore in book_bookstores:
            if bookstore not in admin_bookstores:
                print("You do not have access to modify this book.")
                return books_df 
    else:
        print("Book does not exist")
        return books_df 
    
    title = input("Enter new title: ")
    title = title + '.'
    books_df.loc[book_index, 'title'] =  title
    books_df.loc[book_index, 'author'] = input("Enter new author: ")
    books_df.loc[book_index, 'publisher'] = input("Enter new publisher: ")
    categories = input("Enter new categories (separated by commas): ")
    categories_list = [category.strip() for category in categories.split(',')]
    books_df.at[book_index, 'categories'] = categories_list
    books_df.loc[book_index, 'cost'] = float(input("Enter new cost: "))
    books_df.loc[book_index, 'shipping_cost'] = float(input("Enter new shipping cost: "))
    books_df.loc[book_index, 'availability'] = bool(input("Enter av: "))
    
    for bookstore in book_bookstores:
        print(bookstore)
        new_copies = int(input(f"Enter new value for {bookstore}"))
        book_bookstores[bookstore] = new_copies    
    
    books_df.at[book_index, 'bookstores'] = book_bookstores
    books_df.loc[book_index, 'copies'] = sum(book_bookstores.values())
                 
    return books_df

def check_availability(books_df):
    
    title = input("give me the title you are searching ")
    existing_titles = set(books_df['title'])
    if title not in existing_titles:
        print("book does not exist")
        return 0

    x = books_df.loc[books_df['title'] == title, 'availability'].values[0]
    print(x)
     
def check_availability_bookstore(books_df):
    title = input("give me title: ")
    bookstore = input("give me bookstore: ")
    existing_titles = set(books_df['title'])
    if title not in existing_titles:
        print("Book does not exist")
        return 0
    else:
        bookstore_availability = books_df.loc[books_df['title'] == title, 'bookstores'].values[0]
        if bookstore in bookstore_availability:
            if bookstore_availability[bookstore] > 0:
                print(f"The book '{title}' is available in {bookstore}.")
                return 1
            else:
                print(f"The book '{title}' is not available in {bookstore}.")
                return 0
        else:
            print(f"The book '{title}' is not available in {bookstore}.")
            return 0

def delete_entries(admin_df,books_df, username):
    
    admin_bookstores = admin_df.loc[admin_df['username'] == username, 'bookstores'].values[0]
    title = input("Enter the title of the book you want to delete: ")
    
    if title in books_df['title'].values:
        book_index = books_df.index[books_df['title'] == title][0]
        book_bookstores = books_df.loc[book_index, 'bookstores']
        print(book_bookstores)
        print(book_index)
        for bookstore in book_bookstores:
            if bookstore not in admin_bookstores:
                print("You do not have access to modify this book.")
                return books_df 
    else:
        print("Book does not exist")
        return books_df 
    
        
    books_df.drop(book_index,inplace = True)
                       
    return books_df

def calculate_cost_t(books_df):
    title = input("Give me the title: ")
    if title not in books_df['title'].values:
        print("Book does not exist")
        return 
    book_index = books_df.index[books_df['title'] == title][0]
    cost = float(books_df.at[book_index, 'cost'])
    shi_cost = float(books_df.at[book_index, 'shipping_cost'])
    total_cost = cost + shi_cost
    print(f"Tota cost is:{total_cost}")

def calculate_total_cost(books_df): 
    
    available_books = books_df[books_df['availability'] == True]
    print(available_books)
    author = input("Give me author: ")
    publisher = input("Give me publisher: ")
    a = calculate_cost(author,'author',available_books)
    p = calculate_cost(publisher,'publisher',available_books)
    print(f"Total cost by author: {a}")
    print(f"Total cost by publisher: {p}")
    total_cost = a + p
    print(f"Total cost : {total_cost}")
    
def calculate_cost(x,y,available_books):
    
    filtered = available_books[available_books[y] == x]
    print(filtered)
    cost = filtered['cost'].sum()
    shi_cost = filtered['shipping_cost'].sum()
    total_cost = float(cost + shi_cost)
    return total_cost

def delete_user(user_df):
    
    u = input("Give Username you want to Delete: ")
    u_index = user_df.index[user_df['username'] == u][0]
    print(u_index)
    user_df = user_df.drop(u_index,inplace = True)
    
    return user_df

def graph_pub_auth(books_df,str):
   
    x = input("press 1 with copies 0 for no copies")
    if x == '1':      
        totals = books_df.groupby(str)['copies'].sum()
    else:
        totals = books_df.groupby(str)['id'].count()
    
    graph(totals,str)
    
def graph_categories(books_df):
    
    exploded_df = books_df.explode('categories')
    print(exploded_df['categories'].to_string(index=False))
    category_totals = exploded_df.groupby('categories')['id'].count()
    
    graph(category_totals,'categories')

def graph_bookstores(books_df):
     
    bookstore_totals = pd.Series(dtype=int)

    for bookstores in books_df['bookstores']:
        for store, copies in bookstores.items():
            if store in bookstore_totals:
                bookstore_totals[store] += copies
            else:
                bookstore_totals[store] = copies
    
    graph(bookstore_totals,'bookstores')

def graph_av_cost(books_df):

    available_books = books_df[books_df['availability']]
    grouped_books = available_books.groupby('title').agg({'cost': 'sum'}).reset_index()

    sorted_books = grouped_books.sort_values(by='cost', ascending=True)
    sorted_books = sorted_books.reset_index(drop=True)

    plt.figure(figsize=(20, 12))
    ax = sorted_books.plot(kind='barh', x='title', y='cost', color='skyblue', legend=False)

    plt.xlabel('Cost')
    plt.ylabel('Book Title')
    plt.title('Total Cost of Books by Title')

    for index, value in enumerate(sorted_books['cost']):
        ax.text(value, index, f'${value:.2f}', va='center', ha='left', color='black', fontsize=10)

    plt.tight_layout()
    plt.show()

def graph_city(user_df):
    
    cities_group = user_df.groupby('city')['id'].count()
    graph(cities_group,'city')
    
    pass

def graph(x,str):
    
    plt.figure(figsize=(12, 8))
    ax = x.sort_values().plot(kind='barh', color='skyblue')

    for index, value in enumerate(x.sort_values()):
        ax.text(value, index, f'{value}', va='center', ha='left', color='black', fontsize=10)

    plt.title(f'Total Number of Book Copies by {str}')
    plt.xlabel('Total Copies')
    plt.ylabel(f'{str}')

    plt.tight_layout()
    plt.show()