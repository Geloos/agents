import pandas as pd
import ast

def load_data():
    user_df = pd.read_csv("../csvs/user_data.csv")
    admin_df = pd.read_csv("../csvs/admin_data.csv")
    books_df = pd.read_csv("../csvs/book_data.csv")
    
    user_df['orders'] = user_df['orders'].apply(ast.literal_eval)
    user_df['favorites'] = user_df['favorites'].apply(ast.literal_eval)
    books_df['categories'] = books_df['categories'].apply(ast.literal_eval) 
    books_df['bookstores'] = books_df['bookstores'].apply(ast.literal_eval)  

    return user_df, admin_df, books_df
