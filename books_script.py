import csv
from books.models import Book


def load_books():
    csv_path = "books/books.csv"
    with open(csv_path, "r") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            book, created = Book.objects.get_or_create(
                title=row[0],
                author=row[1],
                genre=row[2],
                description=row[3],
                publisher=row[4],
                date_published=row[5],
                img_url=row[6],
                buy_link=row[7],
            )
            if created:
                book.save()
                print(f"{book.title} has been added to the DB.")
            else:
                print(f"{book.title} already exists in the DB. Skipping.")


def delete_books():
    Book.objects.all().delete()
    print("All books from the DB have been deleted.")
