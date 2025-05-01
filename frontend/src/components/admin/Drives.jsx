import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Typography,
  Paper,
  MenuItem,
} from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import axios from 'axios';

const Drives = () => {
  const [drives, setDrives] = useState([]);
  const [open, setOpen] = useState(false);
  const [selectedDrive, setSelectedDrive] = useState(null);
  const [formData, setFormData] = useState({
    company_name: '',
    job_title: '',
    job_description: '',
    eligibility_criteria: '',
    required_skills: '',
    package_details: '',
    drive_date: new Date(),
    registration_deadline: new Date(),
    status: 'upcoming',
  });

  useEffect(() => {
    fetchDrives();
  }, []);

  const fetchDrives = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/admin/drives');
      setDrives(response.data);
    } catch (error) {
      console.error('Error fetching drives:', error);
    }
  };

  const handleOpen = (drive = null) => {
    if (drive) {
      setSelectedDrive(drive);
      setFormData({
        ...drive,
        drive_date: new Date(drive.drive_date),
        registration_deadline: new Date(drive.registration_deadline),
        required_skills: JSON.stringify(drive.required_skills),
      });
    } else {
      setSelectedDrive(null);
      setFormData({
        company_name: '',
        job_title: '',
        job_description: '',
        eligibility_criteria: '',
        required_skills: '',
        package_details: '',
        drive_date: new Date(),
        registration_deadline: new Date(),
        status: 'upcoming',
      });
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setSelectedDrive(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = {
        ...formData,
        required_skills: JSON.parse(formData.required_skills),
        drive_date: formData.drive_date.toISOString(),
        registration_deadline: formData.registration_deadline.toISOString(),
      };

      if (selectedDrive) {
        await axios.put(`http://localhost:5000/api/admin/drives/${selectedDrive.id}`, data);
      } else {
        await axios.post('http://localhost:5000/api/admin/drives', data);
      }

      fetchDrives();
      handleClose();
    } catch (error) {
      console.error('Error saving drive:', error);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this drive?')) {
      try {
        await axios.delete(`http://localhost:5000/api/admin/drives/${id}`);
        fetchDrives();
      } catch (error) {
        console.error('Error deleting drive:', error);
      }
    }
  };

  const handleNotifyStudents = async (id) => {
    try {
      await axios.post(`http://localhost:5000/api/admin/drives/${id}/notify-matching-students`);
      alert('Notifications sent to matching students!');
    } catch (error) {
      console.error('Error notifying students:', error);
    }
  };

  const columns = [
    { field: 'company_name', headerName: 'Company', width: 200 },
    { field: 'job_title', headerName: 'Job Title', width: 200 },
    { field: 'drive_date', headerName: 'Drive Date', width: 200 },
    { field: 'status', headerName: 'Status', width: 150 },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 300,
      renderCell: (params) => (
        <Box>
          <Button
            variant="contained"
            color="primary"
            size="small"
            onClick={() => handleOpen(params.row)}
            sx={{ mr: 1 }}
          >
            Edit
          </Button>
          <Button
            variant="contained"
            color="secondary"
            size="small"
            onClick={() => handleNotifyStudents(params.row.id)}
            sx={{ mr: 1 }}
          >
            Notify Students
          </Button>
          <Button
            variant="contained"
            color="error"
            size="small"
            onClick={() => handleDelete(params.row.id)}
          >
            Delete
          </Button>
        </Box>
      ),
    },
  ];

  return (
    <Box sx={{ height: 600, width: '100%' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h4">Drives Management</Typography>
        <Button variant="contained" color="primary" onClick={() => handleOpen()}>
          Add New Drive
        </Button>
      </Box>

      <Paper sx={{ height: '100%' }}>
        <DataGrid
          rows={drives}
          columns={columns}
          pageSize={10}
          rowsPerPageOptions={[10]}
          checkboxSelection
          disableSelectionOnClick
        />
      </Paper>

      <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
        <DialogTitle>
          {selectedDrive ? 'Edit Drive' : 'Add New Drive'}
        </DialogTitle>
        <DialogContent>
          <Box component="form" sx={{ mt: 2 }}>
            <TextField
              fullWidth
              label="Company Name"
              value={formData.company_name}
              onChange={(e) => setFormData({ ...formData, company_name: e.target.value })}
              margin="normal"
              required
            />
            <TextField
              fullWidth
              label="Job Title"
              value={formData.job_title}
              onChange={(e) => setFormData({ ...formData, job_title: e.target.value })}
              margin="normal"
              required
            />
            <TextField
              fullWidth
              label="Job Description"
              multiline
              rows={3}
              value={formData.job_description}
              onChange={(e) => setFormData({ ...formData, job_description: e.target.value })}
              margin="normal"
              required
            />
            <TextField
              fullWidth
              label="Eligibility Criteria"
              multiline
              rows={2}
              value={formData.eligibility_criteria}
              onChange={(e) => setFormData({ ...formData, eligibility_criteria: e.target.value })}
              margin="normal"
              required
            />
            <TextField
              fullWidth
              label="Required Skills (JSON array)"
              value={formData.required_skills}
              onChange={(e) => setFormData({ ...formData, required_skills: e.target.value })}
              margin="normal"
              helperText="Enter skills as JSON array, e.g., ['python', 'javascript']"
              required
            />
            <TextField
              fullWidth
              label="Package Details"
              value={formData.package_details}
              onChange={(e) => setFormData({ ...formData, package_details: e.target.value })}
              margin="normal"
              required
            />
            <LocalizationProvider dateAdapter={AdapterDateFns}>
              <DateTimePicker
                label="Drive Date"
                value={formData.drive_date}
                onChange={(newValue) => setFormData({ ...formData, drive_date: newValue })}
                renderInput={(params) => <TextField {...params} fullWidth margin="normal" required />}
              />
              <DateTimePicker
                label="Registration Deadline"
                value={formData.registration_deadline}
                onChange={(newValue) => setFormData({ ...formData, registration_deadline: newValue })}
                renderInput={(params) => <TextField {...params} fullWidth margin="normal" required />}
              />
            </LocalizationProvider>
            <TextField
              fullWidth
              select
              label="Status"
              value={formData.status}
              onChange={(e) => setFormData({ ...formData, status: e.target.value })}
              margin="normal"
              required
            >
              <MenuItem value="upcoming">Upcoming</MenuItem>
              <MenuItem value="ongoing">Ongoing</MenuItem>
              <MenuItem value="completed">Completed</MenuItem>
            </TextField>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={handleSubmit} variant="contained" color="primary">
            {selectedDrive ? 'Update' : 'Add'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Drives; 