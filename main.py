import uvicorn
from fastapi import FastAPI
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configurations
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# SQLAlchemy models
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    phone = Column(String, index=True)


Base.metadata.create_all(bind=engine)

# FastAPI app instance
app = FastAPI()


# CRUD operations
# Create (Create)
@app.post("/users/")
async def create_user(firstname: str, lastname: str, phone: str):
	db = SessionLocal()
	db_users = Users(firstname=firstname, lastname=lastname , phone=phone)
	db.add(db_users)
	db.commit()
	db.refresh(db_users)
	return db_users


# Read (GET)
@app.get("/users/{user_id}")
async def read_user(user_id: int):
	db = SessionLocal()
	user = db.query(Users).filter(Users.id == user_id).first()
	return user


# Update (PUT)
@app.put("/users/{user_id}")
async def update_item(user_id: int, firstname: str, lastname: str, phone: str):
    db = SessionLocal()
    db_users = db.query(Users).filter(Users.id == user_id).first()
    db_users.firstname = firstname
    db_users.lastname = lastname
    db_users.phone = phone
    db.commit()
    return db_users


# Delete (DELETE)
@app.delete("/users/{user_id}")
async def delete_item(user_id: int):
	db = SessionLocal()
	db_users = db.query(Users).filter(Users.id == user_id).first()
	db.delete(db_users)
	db.commit()
	return {"message": "User deleted successfully"}


if __name__ == "__main__":
	uvicorn.run(app)
