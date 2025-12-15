from src.infrastructure.database import engine, Base
from src.domain import models

Base.metadata.create_all(bind=engine)
print("Database tables created successfully.")
