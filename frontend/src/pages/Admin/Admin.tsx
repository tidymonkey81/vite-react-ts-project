import React, { useState } from 'react';
import { Button, TextField, Container, Box, Typography, Input } from '@mui/material';

function Admin() {
  const [file, setFile] = useState(null);
  const [backendUrl, setBackendUrl] = useState(`http://localhost:${import.meta.env.VITE_BACKEND_PORT}`);

  async function createGlobalSchoolDB() {
    try {
      const response = await fetch(`${backendUrl}/admin/create-global-school-db`, {
        method: 'POST',
      });
      if (response.status === 200) {
        const result = await response.json();
        console.log(result);
        alert('Global school DB created!');
      } else {
        alert('Global school DB creation failed!');
      }
    } catch (error) {
      console.error('Error creating global school db:', error);
      alert('Global school DB creation failed!');
    }
  }

  async function createSchoolNode() {
    if (!file) {
      alert('Please select a file first!');
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${backendUrl}/school/create-school`, {
        method: 'POST',
        body: formData,
      });

      if (response.status === 200) {
        const result = await response.json();
        console.log(result);
        alert('Upload Successful!');
      } else {
        alert('Upload failed!');
      }
    } catch (error) {
      console.error('Error creating school node:', error);
      alert('Creation failed!');
    }
  }

  async function uploadCurriculum() {
    if (!file) {
      alert('Please select a file first!');
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${backendUrl}/curriculum/upload-curriculum`, {
        method: 'POST',
        body: formData,
      });

      if (response.status === 200) {
        const result = await response.json();
        console.log(result);
        alert('Upload Successful!');
      } else {
        alert('Upload failed!');
      }
    } catch (error) {
      console.error('Error uploading curriculum:', error);
      alert('Upload failed!');
    }
  }

  async function uploadSubjectCurriculum() {
    if (!file) {
      alert('Please select a file first!');
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${backendUrl}/curriculum/upload-subject-curriculum`, {
        method: 'POST',
        body: formData,
      });

      if (response.status === 200) {
        const result = await response.json();
        console.log(result);
        alert('Upload Successful!');
      } else {
        alert('Upload failed!');
      }
    } catch (error) {
      console.error('Error uploading curriculum:', error);
      alert('Upload failed!');
    }
  }

  function handleFileChange(event) {
    setFile(event.target.files[0]);
  }

  function handleBackendUrlChange(event) {
    setBackendUrl(event.target.value);
  }

  return (
    <Container maxWidth="md" style={{ marginTop: '20px' }}>
      <Typography variant="h4" gutterBottom>Admin Management</Typography>
      <Box display="flex" flexDirection="column" alignItems="center" gap={2}>
        <TextField
          label="Backend URL"
          variant="outlined"
          value={backendUrl}
          onChange={handleBackendUrlChange}
          fullWidth
        />
        <Button variant="contained" color="primary" onClick={createGlobalSchoolDB}>
          Create Global School DB
        </Button>
        <Input
          type="file"
          onChange={handleFileChange}
          disableUnderline
          inputProps={{ 'aria-label': 'Upload file' }}
        />
        <Button variant="contained" color="secondary" onClick={createSchoolNode}>
          Create School Node
        </Button>
        <Button variant="contained" color="secondary" onClick={uploadCurriculum}>
          Upload Curriculum
        </Button>
        <Button variant="contained" color="secondary" onClick={uploadSubjectCurriculum}>
          Upload Subject Curriculum
        </Button>
      </Box>
    </Container>
  );
}

export default Admin;