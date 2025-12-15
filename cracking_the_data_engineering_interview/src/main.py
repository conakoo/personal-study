"""Main entry point for the data engineer project.

This script executes the data ingestion and storage pipeline, 
first pushing processed data to Azure Blob Storage and then 
to a PostgreSQL database.

Reference:
    https://github.com/PacktPublishing/Cracking-Data-Engineering-Interview-Guide
"""
import os

os.system("python push_to_blob.py")
os.system("python push_to_database.py")
