import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  CardHeader,
} from '@mui/material';
import {
  People as PeopleIcon,
  Business as BusinessIcon,
  Notifications as NotificationsIcon,
} from '@mui/icons-material';
import axios from 'axios';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalStudents: 0,
    totalDrives: 0,
    upcomingDrives: 0,
    placedStudents: 0,
  });

  useEffect(() => {
    fetchDashboardStats();
  }, []);

  const fetchDashboardStats = async () => {
    try {
      const [studentsRes, drivesRes] = await Promise.all([
        axios.get('http://localhost:5000/api/students'),
        axios.get('http://localhost:5000/api/admin/drives'),
      ]);

      const students = studentsRes.data;
      const drives = drivesRes.data;

      setStats({
        totalStudents: students.length,
        totalDrives: drives.length,
        upcomingDrives: drives.filter(drive => drive.status === 'upcoming').length,
        placedStudents: students.filter(student => student.is_placed).length,
      });
    } catch (error) {
      console.error('Error fetching dashboard stats:', error);
    }
  };

  const StatCard = ({ title, value, icon, color }) => (
    <Card sx={{ height: '100%' }}>
      <CardHeader
        avatar={icon}
        title={title}
        titleTypographyProps={{ variant: 'h6' }}
      />
      <CardContent>
        <Typography variant="h4" component="div" color={color}>
          {value}
        </Typography>
      </CardContent>
    </Card>
  );

  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Dashboard Overview
      </Typography>
      
      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Students"
            value={stats.totalStudents}
            icon={<PeopleIcon color="primary" />}
            color="primary"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Drives"
            value={stats.totalDrives}
            icon={<BusinessIcon color="secondary" />}
            color="secondary"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Upcoming Drives"
            value={stats.upcomingDrives}
            icon={<NotificationsIcon color="info" />}
            color="info"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Placed Students"
            value={stats.placedStudents}
            icon={<PeopleIcon color="success" />}
            color="success"
          />
        </Grid>
      </Grid>

      <Paper sx={{ p: 3, mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Recent Activities
        </Typography>
        <Typography variant="body1" color="text.secondary">
          No recent activities to display.
        </Typography>
      </Paper>
    </Box>
  );
};

export default Dashboard; 