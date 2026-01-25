import React, { useState } from 'react';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import type { User } from './types/dataset';

const App: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);

  const handleLogin = (username: string) => {
    setUser({
      username,
      isAuthenticated: true,
    });
  };

  const handleLogout = () => {
    setUser(null);
  };

  if (!user || !user.isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }

  return <Dashboard username={user.username} onLogout={handleLogout} />;
};

export default App;
