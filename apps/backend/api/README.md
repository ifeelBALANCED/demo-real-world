# Consider using a repository pattern in FastAPI instead of ORM wrapper



In FastAPI, the term "repository" usually refers to the Repository Pattern, which is a design pattern used to abstract database access logic. This pattern helps separate the database logic from the business logic, making the code more maintainable, testable, and reusable.

🏛 What is the Repository Pattern?
The repository acts as an intermediary between the database (ORM models) and the business logic (service layer or API endpoints). Instead of directly performing CRUD operations in your routes or services, you define them in a repository.

🎯 Benefits of Using a Repository in FastAPI:
Encapsulation – Hides database logic from the business layer.
Easier Unit Testing – You can mock the repository without needing a real database.
Flexibility – You can switch between different databases (PostgreSQL, MySQL, SQLite, etc.).
Reusability – Use the same repository in different parts of the application.
🛠 Example of Using a Repository in FastAPI with SQLAlchemy
Let's say we have a User model, and we want to create a repository for user-related operations.

1️⃣ Define the SQLAlchemy User Model
```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
```

2️⃣ Set Up Database Session
```python
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://user:password@localhost/db_name"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
```

3️⃣ Create the User Repository
This repository will handle all database operations related to users.
```python
from sqlalchemy.orm import Session
from models import User  # Import your model

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, name: str, email: str):
        new_user = User(name=name, email=email)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def delete_user(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            self.db.delete(user)
            self.db.commit()
        return user
```

4️⃣ Using the Repository in FastAPI Routes
```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from repositories import UserRepository

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    existing_user = user_repo.get_user_by_email(email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    return user_repo.create_user(name, email)

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

🚀 Summary:
A repository is a class that abstracts database operations (CRUD).
It separates database logic from business logic, making the code more structured and testable.
Using SQLAlchemy, we created a UserRepository to handle user-related queries.
FastAPI routes depend on the repository, making the API cleaner and more modular.
Let me know if you need a repository for other cases (e.g., async database, NoSQL, etc.)! 🚀
