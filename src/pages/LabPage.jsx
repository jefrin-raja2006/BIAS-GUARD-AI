import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function LabPage({ user, setUser }) {
  const [selectedPatient, setSelectedPatient] = useState(null);
  const navigate = useNavigate();

  const labName = "Lab Technician";

  const handleLogout = () => {
    localStorage.removeItem('user');
    setUser(null);
    navigate('/login');
  };

  const patientsNeedingLab = [
    { id: 1, name: 'John Doe', age: 45, bmi: 32, risk: 'High' },
    { id: 2, name: 'Jane Smith', age: 38, bmi: 31, risk: 'High' },
  ];

  const stats = [
    { label: 'Pending Lab Tests', value: patientsNeedingLab.length, icon: '🧪', color: 'purple' },
    { label: 'Tests Completed', value: '24', icon: '✅', color: 'green' },
    { label: 'High Risk Patients', value: '12', icon: '⚠️', color: 'red' },
    { label: 'Avg Turnaround', value: '24h', icon: '⏱️', color: 'orange' }
  ];

  return (
    <div style={{ minHeight: '100vh', background: '#f8f7fc' }}>
      {/* Navbar */}
      <nav style={{
        background: 'white',
        padding: '16px 32px',
        boxShadow: '0 2px 10px rgba(0,0,0,0.05)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        borderBottom: '2px solid #8b5cf6'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span style={{ fontSize: '24px' }}>🏥</span>
          <span style={{ fontSize: '24px', fontWeight: 800, color: '#8b5cf6' }}>BiasGuard AI</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            padding: '6px 16px 6px 6px',
            background: '#f3e8ff',
            borderRadius: '50px'
          }}>
            <div style={{
              width: '36px',
              height: '36px',
              background: 'linear-gradient(135deg, #8b5cf6, #7c3aed)',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
              fontSize: '16px'
            }}>
              🔬
            </div>
            <div>
              <div style={{ fontWeight: 600, fontSize: '14px', color: '#1f2937' }}>{labName}</div>
              <div style={{ fontSize: '12px', color: '#6b7280' }}>Lab Technician</div>
            </div>
          </div>
          <button onClick={handleLogout} className="btn btn-danger">Logout</button>
        </div>
      </nav>

      <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '32px 24px' }}>
        {/* Welcome */}
        <div style={{ marginBottom: '32px' }}>
          <h1 style={{ fontSize: '32px', fontWeight: 800, color: '#1f2937', marginBottom: '8px' }}>
            Lab Dashboard
          </h1>
          <p style={{ color: '#6b7280', fontSize: '16px' }}>
            Upload and manage laboratory test results
          </p>
        </div>

        {/* Stats */}
        <div className="stats-grid">
          {stats.map((stat, idx) => (
            <div key={idx} className="stat-card">
              <div className={`stat-icon stat-icon-${stat.color}`}>{stat.icon}</div>
              <div className="stat-value">{stat.value}</div>
              <div className="stat-label">{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Patients List */}
        <div className="card">
          <h2 style={{ fontSize: '22px', fontWeight: 700, color: '#1f2937', marginBottom: '24px' }}>
            🔬 Patients Requiring Lab Tests
          </h2>

          {patientsNeedingLab.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '60px 20px', background: '#f8f7fc', borderRadius: '16px' }}>
              <div style={{ fontSize: '64px', marginBottom: '16px' }}>🔬</div>
              <div style={{ fontSize: '16px', color: '#6b7280' }}>No pending lab tests</div>
              <div style={{ fontSize: '14px', color: '#9ca3af', marginTop: '8px' }}>Patients will appear here when lab tests are required</div>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {patientsNeedingLab.map((patient) => (
                <div key={patient.id} style={{
                  padding: '16px',
                  background: '#f8f7fc',
                  borderRadius: '12px',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  cursor: 'pointer',
                  transition: 'all 0.3s ease'
                }}
                onMouseEnter={(e) => e.currentTarget.style.background = '#f3e8ff'}>
                  <div>
                    <div style={{ fontWeight: 600, color: '#1f2937' }}>{patient.name}</div>
                    <div style={{ fontSize: '13px', color: '#6b7280' }}>
                      Age: {patient.age} | BMI: {patient.bmi}
                    </div>
                  </div>
                  <span className="badge badge-danger">High Risk - Lab Required</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default LabPage;