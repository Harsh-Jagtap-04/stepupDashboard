# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
from database import save_to_db

app = Flask(__name__)
CORS(app)

# Folder to store uploaded files
UPLOAD_FOLDER = "uploaded_files"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Table mappings for uploaded files
TABLE_MAPPINGS = {
    "invitesTable": "invites_table",
    "testTables": "test_table",
    "consolidatedTable": "consolidated_table",
    "batchInformation": "batch_information"
}

@app.route("/upload", methods=["POST"])
def upload_files():
    files = request.files
    responses = {}

    for file_key, table_name in TABLE_MAPPINGS.items():
        if file_key in files:
            file = files[file_key]
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            # Process Excel file
            df = pd.read_excel(file_path)

            # Convert DataFrame to dictionary and save to the database
            data = df.to_dict(orient="records")
            save_to_db(table_name, data)

            responses[file_key] = f"Uploaded and saved to {table_name} successfully."

    return jsonify(responses)

if __name__ == "__main__":
    app.run(debug=True)
