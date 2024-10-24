import React, { useState } from 'react';

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState('');
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setPreviewUrl(URL.createObjectURL(selectedFile));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      if (res.ok) {
        setMessage(`File uploaded successfully: ${data.filename}`);
      } else {
        setMessage(`Error: ${data.error}`);
      }
    } catch (error) {
      setMessage('Error uploading file');
    }
  };

  return (
    <div>
      <h2>Upload a PDF File</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" accept=".pdf" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
      {previewUrl && (
        <div className="file-preview">
          <h3>File Preview:</h3>
          <iframe src={previewUrl} width="100%" height="500px" title="File Preview"></iframe>
        </div>
      )}
      {message && <p>{message}</p>}
    </div>
  );
};

export default FileUpload;
