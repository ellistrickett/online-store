import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient

env_path = Path(__file__).resolve().parent / "atlas-credentials.env"
load_dotenv(dotenv_path=env_path)

MONGO_URI = os.getenv("MONGODB_URI")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI was not found in atlas-credentials.env")


def get_mongo_collection(collection_name="products"):
    """Connect to the Atlas cluster and return the requested collection."""
    cluster = MongoClient(MONGO_URI)
    db = cluster["pymongodb"]
    return db[collection_name]