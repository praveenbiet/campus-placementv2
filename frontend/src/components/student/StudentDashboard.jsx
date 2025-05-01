import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  Chip,
  Avatar,
  Divider,
  Stack,
  IconButton,
  Tooltip,
} from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import {
  Business as BusinessIcon,
  Work as WorkIcon,
  Event as EventIcon,
  CheckCircle as CheckCircleIcon,
  Pending as PendingIcon,
  Cancel as CancelIcon,
  Edit as EditIcon,
} from '@mui/icons-material';
import { useAuth } from '../../context/AuthContext';

const StudentDashboard = () => {
  const { api } = useAuth();
  const [drives, setDrives] = useState([]);
  const [applications, setApplications] = useState([]);
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [drivesRes, applicationsRes, profileRes] = await Promise.all([
        api.get('/api/student/drives'),
        api.get('/api/student/applications'),
        api.get('/api/student/profile'),
      ]);

      setDrives(drivesRes.data);
      setApplications(applicationsRes.data);
      setProfile(profileRes.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };

  const handleApply = async (driveId) => {
    try {
      await api.post(`/api/student/drives/${driveId}/apply`);
      fetchData();
    } catch (error) {
      console.error('Error applying to drive:', error);
    }
  };

  const getStatusIcon = (status) => {
    switch (status.toLowerCase()) {
      case 'accepted':
        return <CheckCircleIcon color="success" />;
      case 'pending':
        return <PendingIcon color="warning" />;
      case 'rejected':
        return <CancelIcon color="error" />;
      default:
        return null;
    }
  };

  const drivesColumns = [
    { 
      field: 'company_name', 
      headerName: 'Company', 
      width: 200,
      renderCell: (params) => (
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <BusinessIcon sx={{ mr: 1, color: 'primary.main' }} />
          {params.value}
        </Box>
      ),
    },
    { 
      field: 'job_title', 
      headerName: 'Job Title', 
      width: 200,
      renderCell: (params) => (
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <WorkIcon sx={{ mr: 1, color: 'secondary.main' }} />
          {params.value}
        </Box>
      ),
    },
    { 
      field: 'drive_date', 
      headerName: 'Drive Date', 
      width: 150,
      renderCell: (params) => (
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <EventIcon sx={{ mr: 1, color: 'info.main' }} />
          {new Date(params.value).toLocaleDateString()}
        </Box>
      ),
    },
    { 
      field: 'status', 
      headerName: 'Status', 
      width: 120,
      renderCell: (params) => (
        <Chip
          label={params.value}
          color={
            params.value === 'upcoming' ? 'primary' :
            params.value === 'ongoing' ? 'warning' :
            'error'
          }
          size="small"
        />
      ),
    },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 150,
      renderCell: (params) => (
        <Button
          variant="contained"
          color="primary"
          size="small"
          onClick={() => handleApply(params.row.id)}
          disabled={params.row.status !== 'upcoming'}
          startIcon={<CheckCircleIcon />}
        >
          Apply
        </Button>
      ),
    },
  ];

  const applicationsColumns = [
    { 
      field: 'company_name', 
      headerName: 'Company', 
      width: 200,
      renderCell: (params) => (
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <BusinessIcon sx={{ mr: 1, color: 'primary.main' }} />
          {params.value}
        </Box>
      ),
    },
    { 
      field: 'job_title', 
      headerName: 'Job Title', 
      width: 200,
      renderCell: (params) => (
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <WorkIcon sx={{ mr: 1, color: 'secondary.main' }} />
          {params.value}
        </Box>
      ),
    },
    { 
      field: 'application_date', 
      headerName: 'Applied On', 
      width: 150,
      renderCell: (params) => (
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <EventIcon sx={{ mr: 1, color: 'info.main' }} />
          {new Date(params.value).toLocaleDateString()}
        </Box>
      ),
    },
    { 
      field: 'status', 
      headerName: 'Status', 
      width: 120,
      renderCell: (params) => (
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          {getStatusIcon(params.value)}
          <Chip
            label={params.value}
            color={
              params.value === 'accepted' ? 'success' :
              params.value === 'pending' ? 'warning' :
              'error'
            }
            size="small"
            sx={{ ml: 1 }}
          />
        </Box>
      ),
    },
  ];

  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      <Typography variant="h4" gutterBottom sx={{ mb: 4 }}>
        Student Dashboard
      </Typography>

      {profile && (
        <Paper sx={{ p: 3, mb: 4, borderRadius: 2, boxShadow: 3 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h5" component="h2">
              Your Profile
            </Typography>
            <Tooltip title="Edit Profile">
              <IconButton color="primary">
                <EditIcon />
              </IconButton>
            </Tooltip>
          </Box>
          <Divider sx={{ mb: 3 }} />
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <Avatar
                  sx={{ width: 120, height: 120, mb: 2, bgcolor: 'primary.main' }}
                >
                  {profile.first_name[0]}{profile.last_name[0]}
                </Avatar>
                <Typography variant="h6">
                  {profile.first_name} {profile.last_name}
                </Typography>
                <Typography color="text.secondary">
                  {profile.roll_number}
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} md={8}>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Typography variant="subtitle1" color="text.secondary">
                    Department
                  </Typography>
                  <Typography variant="body1" sx={{ mb: 2 }}>
                    {profile.department}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="subtitle1" color="text.secondary">
                    Graduation Year
                  </Typography>
                  <Typography variant="body1" sx={{ mb: 2 }}>
                    {profile.year_of_graduation}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="subtitle1" color="text.secondary">
                    CGPA
                  </Typography>
                  <Typography variant="body1" sx={{ mb: 2 }}>
                    {profile.cgpa}
                  </Typography>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="subtitle1" color="text.secondary">
                    Skills
                  </Typography>
                  <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
                    {profile.skills.map((skill, index) => (
                      <Chip
                        key={index}
                        label={skill}
                        color="primary"
                        variant="outlined"
                        sx={{ mb: 1 }}
                      />
                    ))}
                  </Stack>
                </Grid>
              </Grid>
            </Grid>
          </Grid>
        </Paper>
      )}

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 3, borderRadius: 2, boxShadow: 3 }}>
            <Typography variant="h5" gutterBottom>
              Available Drives
            </Typography>
            <DataGrid
              rows={drives}
              columns={drivesColumns}
              pageSize={5}
              rowsPerPageOptions={[5]}
              autoHeight
              disableSelectionOnClick
              sx={{
                '& .MuiDataGrid-cell:focus': {
                  outline: 'none',
                },
                '& .MuiDataGrid-columnHeader:focus': {
                  outline: 'none',
                },
              }}
            />
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 3, borderRadius: 2, boxShadow: 3 }}>
            <Typography variant="h5" gutterBottom>
              Your Applications
            </Typography>
            <DataGrid
              rows={applications}
              columns={applicationsColumns}
              pageSize={5}
              rowsPerPageOptions={[5]}
              autoHeight
              disableSelectionOnClick
              sx={{
                '& .MuiDataGrid-cell:focus': {
                  outline: 'none',
                },
                '& .MuiDataGrid-columnHeader:focus': {
                  outline: 'none',
                },
              }}
            />
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default StudentDashboard; 