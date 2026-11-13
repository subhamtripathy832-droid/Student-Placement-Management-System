import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-development-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:password@localhost/placement_db?charset=utf8mb4",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
