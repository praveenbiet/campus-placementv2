import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import DashboardLayout from './components/layout/DashboardLayout';
import Students from './components/admin/Students';
import Drives from './components/admin/Drives';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        <Routes>
          <Route path="/" element={<Navigate to="/admin" replace />} />
          <Route path="/admin" element={<DashboardLayout />}>
            <Route path="students" element={<Students />} />
            <Route path="drives" element={<Drives />} />
            <Route index element={<Students />} />
          </Route>
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App; 