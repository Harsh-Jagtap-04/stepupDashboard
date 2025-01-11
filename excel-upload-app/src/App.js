import React, { useState } from "react";
import axios from "axios";

const FileUpload = () => {
    const [files, setFiles] = useState({
        invitesTable: null,
        testTables: null,
        consolidatedTable: null,
        batchInformation: null,
    });

    const handleFileChange = (e, fileKey) => {
        setFiles({ ...files, [fileKey]: e.target.files[0] });
    };

    const handleSubmit = async () => {
        const formData = new FormData();
        Object.keys(files).forEach(key => {
            if (files[key]) formData.append(key, files[key]);
        });

        try {
            const response = await axios.post("http://localhost:5000/upload", formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });
            alert("Files uploaded successfully!");
        } catch (err) {
            console.error(err);
            alert("Error uploading files.");
        }
    };

    return (
        <div>
            <h2>Upload Excel Files</h2>
            <div>
                <label>Invites Table:</label>
                <input type="file" onChange={(e) => handleFileChange(e, "invitesTable")} />
            </div>
            <div>
                <label>Test Tables:</label>
                <input type="file" onChange={(e) => handleFileChange(e, "testTables")} />
            </div>
            <div>
                <label>Consolidated Table:</label>
                <input type="file" onChange={(e) => handleFileChange(e, "consolidatedTable")} />
            </div>
            <div>
                <label>Batch Information:</label>
                <input type="file" onChange={(e) => handleFileChange(e, "batchInformation")} />
            </div>
            <button onClick={handleSubmit}>Upload</button>
        </div>
    );
};

export default FileUpload;
