from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Book model
class Book(BaseModel):
    id: int
    title: str
    author: str
    description: Optional[str] = None
    year: int

# In-memory "database"
books_db: List[Book] = []

# 1. GET all books
@app.get("/books", response_model=List[Book])
def get_books():
    return books_db

# 2. GET single book by ID
@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# 3. POST new book
@app.post("/books", response_model=Book)
def create_book(book: Book):
    for b in books_db:
        if b.id == book.id:
            raise HTTPException(status_code=400, detail="Book ID already exists")
    books_db.append(book)
    return book

# 4. PUT update book
@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(books_db):
        if book.id == book_id:
            books_db[index] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")

# 5. DELETE a book
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            books_db.remove(book)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")

# 6. GET books by author
@app.get("/books/author/{author_name}", response_model=List[Book])
def get_books_by_author(author_name: str):
    result = [book for book in books_db if book.author.lower() == author_name.lower()]
    return result

# 7. GET books by year
@app.get("/books/year/{year}", response_model=List[Book])
def get_books_by_year(year: int):
    result = [book for book in books_db if book.year == year]
    return result
