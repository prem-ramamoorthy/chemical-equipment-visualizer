import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import Login from './pages/Login';
import NotFound from './pages/NotFound';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Signup from './pages/Signup';

const router = createBrowserRouter([
  { path: '/', element: <Login />, errorElement: <NotFound /> },
  { path: '/dashboard', element: <Dashboard /> },
  { path: '/signup', element: <Signup /> },
]);

const rootEl = document.getElementById('root');
if (!rootEl) throw new Error('Root element not found');

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)