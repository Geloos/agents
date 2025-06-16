from dataloader import load_data
from loginsingup import admin_login,user_signup,user_login
from adminactions import load_books_from_csv,add_individual_entry,modify_entries,delete_entries,check_availability,check_availability_bookstore,calculate_cost,calculate_total_cost,delete_user,graph_pub_auth,graph_categories,graph_bookstores,graph_av_cost,graph_city
from useractions import fav_csv,add_fav,modify_user,rem_fav,check_balance,check_fav,check_orders,add_bal

def menu():
        
    print("\nMenu:")
    print("1. Load book data from a CSV file into books_df")
    print("2. Add individual entries to books_df")
    print("3. Modify entries of books_df")
    print("4. Delete entries from books_df")
    print("5. Export the updated books_df to a .csv file")
    print("6. Check the availability of a book by title")
    print("7. Check the availability of a book by title in specific bookstores")
    print("8. Calculate the cost of a book (cost + shipping cost)")
    print("9. Calculate the total cost of all available books by publisher/by author/total")
    print("10. Delete users by their username")
    print("11. Graphics menu")
    print("12. Exit")
    choice = input("\nEnter your choice: ")
    return choice

def graphichal_menu():
    
    print("1.Show publisher")
    print("2.Show author")
    print("3.Show by category")
    print("4.Show by store")
    print("5.cost of each available book")
    print("6.User city poppulation")
    
    choice = input("\nEnter your choice: ")
    return choice 

def user_menu():
    
    print("1.update orders from csv")
    print("2.add favrorites")
    print("3.Change attributes")
    print("4.remove favorites")
    print("5.check balance")
    print("6.check price for favorites")
    print("7.place orders or delete")
    print("8.add bal")
    print("9.logout")
    choice = input("\nEnter your choice: ")
    return choice

def main():

    user_df, admin_df, books_df = load_data()

    while True:
        user_type = input("(For admin press a) (For user press u) (For exit press q)")

        if user_type == 'a':
            flag,username = admin_login(admin_df)

            if flag:         
                while True:
                    print(username)
                    choice = menu()
                    if choice == '1':
                        print(books_df)                        
                        books_df = load_books_from_csv(books_df)
                        print(books_df)
                        
                    elif choice == '2':
                        print(books_df)
                        books_df = add_individual_entry(books_df)
                        print(books_df)
                    
                    elif choice == '3':
                        print(books_df)
                        books_df = modify_entries(admin_df,books_df,username)
                        print(books_df)
                     
                    elif choice == '4':
                        print(books_df)
                        books_df = delete_entries(admin_df,books_df, username)
                        print(books_df)                        
                     
                    elif choice == '5':
                        books_df.to_csv('updated_books.csv',index=False)
                      
                    elif choice == '6':
                        check_availability(books_df)
                      
                    elif choice == '7':
                        check_availability_bookstore(books_df)
                        
                    elif choice == '8':
                        calculate_cost(books_df)
                       
                    elif choice == '9':
                        calculate_total_cost(books_df)

                    elif choice == '10':
                        print(user_df)
                        delete_user(user_df)
                        print(user_df)
                        
                    elif choice == '11':
                        ch = graphichal_menu()
                        if ch == '1':                            
                            graph_pub_auth(books_df,'publisher')
                        elif ch == '2':
                            graph_pub_auth(books_df,'author')
                        elif ch == '3':
                            graph_categories(books_df)
                        elif ch == '4':
                            graph_bookstores(books_df)
                        elif ch == '5':
                            graph_av_cost(books_df)
                        elif ch == '6':
                            graph_city(user_df)
                        else:
                            print("chosse numbers between 1-6")
                    elif choice == '12':
                        break
                    else:
                        print("Invalid choice. Please enter a number between 1 and 11.")            
        elif user_type == 'u':           
            while True:
                flag = False
                choice = input("Choose (l)ogin or (S)ingup or (E)xit: ")
                if choice.lower() == 'l':
                    flag,username = user_login(user_df)                   
                elif choice.lower() == 's':
                    user_df = user_signup(user_df)                
                    print(user_df)
                if flag:
                    while True:
                        us_ch = user_menu()
                        if us_ch == '1':
                            print(user_df)
                            fav_csv(user_df,username)
                            print(user_df)
                        if us_ch == '2':
                            print(user_df)
                            add_fav(user_df,books_df,username)
                            print(user_df)
                        if us_ch == '3':
                            print(user_df)
                            modify_user(user_df,username)
                            print(user_df)
                        if us_ch == '4':
                            print(user_df)
                            rem_fav(user_df,username)
                            print(user_df)
                        if us_ch == '5':                        
                            check_balance(user_df,username)
                        if us_ch == '6':
                            check_fav(user_df,books_df,username)
                        if us_ch == '7':
                            print(user_df)
                            check_orders(user_df,books_df,username)
                            print(user_df)
                        if us_ch == '8':
                            print(user_df)
                            add_bal(user_df,username)
                            print(user_df)
                        if us_ch == '9':
                            break
                elif choice.lower() == 'e':
                    break
                else:
                    print("Invalid input pls Choose 'l' 's' 'e'.")
                    
                
        elif user_type == 'q':
            break
        else:
            print("Invalid input press a, u, q.")
    

    
    try:
        
        user_df.to_csv('Updated_User.csv', index=False)
        books_df.to_csv('Updated_Books.csv', index=False)
        admin_df.to_csv('Updated_Admin.csv', index=False)
    
    except Exception as e:
        print(f"An error occurred: {e}")
    try:
 
        user_df.to_json('Updated_User.json', orient='records', indent=4)
        books_df.to_json('Updated_Books.json', orient='records', indent=4)
        admin_df.to_json('Updated_Admin.json', orient='records', indent=4)
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return 0
    
if __name__ == "__main__":
    main()
    print("Program Terminated Sucsefully")