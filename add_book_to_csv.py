import csv
from get_book import get_book
import pandas as pd

def add_book_to_csv(isbn):
    # Check if the book already exists in the CSV file
    file_pd = pd.read_csv("res/book_df.csv")
    with open("res/book_df.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row["isbn13"]) == int(isbn):
                print("Book already exists in the CSV file")
                return False

    # If book does not exist in the CSV file, get the book information and add it to the CSV file
    book_info = get_book(isbn)
    print()

    with open("res/book_df.csv", "a", encoding='utf-8-sig', newline='') as file:

        writer = csv.writer(file)
        writer.writerow([len(file_pd), book_info["no"]
                  , ""
                  , book_info["bookname"]
                  , book_info["authors"]
                  , book_info["publisher"]
                  , book_info["publication_year"]
                  , book_info["isbn13"]
                  , ""
                  , ""
                  , book_info["class_no"]
                  , book_info["class_nm"]
                  , ""
                  , book_info["bookImageURL"]
                  , ""])

        print("Book added to CSV file")
        return True
