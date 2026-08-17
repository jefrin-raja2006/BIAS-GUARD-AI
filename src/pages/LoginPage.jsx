import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

function LoginPage({ setUser }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('nurse');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const roleParam = params.get('role');
    if (roleParam) setRole(roleParam);
  }, [location]);

  const handleLogin = (e) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => {
      const mockUser = { username: username || role, role: role, name: role === 'nurse' ? 'Kiki' : role === 'lab' ? 'Lab Tech' : 'Dr. Jefrin' };
      localStorage.setItem('user', JSON.stringify(mockUser));
      setUser(mockUser);
      navigate(`/${role}`);
      setLoading(false);
    }, 800);
  };

  const roleInfo = {
    nurse: { icon: '👩‍⚕️', title: 'Nurse Portal', color: '#8b5cf6' },
    lab: { icon: '🔬', title: 'Lab Technician Portal', color: '#a78bfa' },
    doctor: { icon: '👨‍⚕️', title: 'Doctor Portal', color: '#7c3aed' }
  };

  const currentRole = roleInfo[role];

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#faf9fe' }}>
      <div style={{ background: 'white', borderRadius: '16px', padding: '40px', maxWidth: '400px', width: '100%', border: '1px solid #f3e8ff' }}>
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <button onClick={() => navigate('/roles')} style={{ background: 'none', border: 'none', color: '#8b5cf6', cursor: 'pointer' }}>← Back</button>
          <div style={{ fontSize: '48px', marginBottom: '12px' }}>{currentRole.icon}</div>
          <h1 style={{ fontSize: '24px', fontWeight: 700, color: currentRole.color }}>{currentRole.title}</h1>
        </div>
        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label>Username</label>
            <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Enter username" required />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Enter password" required />
          </div>
          <button type="submit" style={{ width: '100%', padding: '12px', background: currentRole.color, color: 'white', border: 'none', borderRadius: '8px', fontSize: '16px', fontWeight: 600, cursor: 'pointer' }} disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default LoginPage;