import React from 'react';
import { useNavigate } from 'react-router-dom';

function RoleSelectionPage() {
  const navigate = useNavigate();

  const roles = [
    { 
      id: 'nurse', 
      title: 'Nurse', 
      icon: '👩‍⚕️', 
      description: 'Register patients and perform initial risk assessment',
      color: '#8b5cf6',
      bgColor: '#f3e8ff'
    },
    { 
      id: 'lab', 
      title: 'Lab Technician', 
      icon: '🔬', 
      description: 'Upload lab results and manage test data',
      color: '#7c3aed',
      bgColor: '#ede9fe'
    },
    { 
      id: 'doctor', 
      title: 'Doctor', 
      icon: '👨‍⚕️', 
      description: 'Review AI predictions with fairness insights',
      color: '#6d28d9',
      bgColor: '#e9d5ff'
    }
  ];

  return (
    <div style={{ minHeight: '100vh', background: '#f8f7fc' }}>
      {/* Header with gradient */}
      <div style={{
        background: 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)',
        padding: '80px 24px 60px',
        textAlign: 'center'
      }}>
        <button
          onClick={() => navigate('/')}
          style={{
            background: 'rgba(255,255,255,0.2)',
            border: 'none',
            color: 'white',
            padding: '8px 20px',
            borderRadius: '50px',
            cursor: 'pointer',
            fontSize: '14px',
            marginBottom: '24px',
            transition: 'all 0.3s ease'
          }}
          onMouseEnter={(e) => e.target.style.background = 'rgba(255,255,255,0.3)'}
          onMouseLeave={(e) => e.target.style.background = 'rgba(255,255,255,0.2)'}
        >
          ← Back to Home
        </button>
        <h1 style={{ fontSize: '42px', fontWeight: 800, color: 'white', marginBottom: '12px' }}>
          Select Your Role
        </h1>
        <p style={{ fontSize: '18px', color: 'rgba(255,255,255,0.9)' }}>
          Choose your healthcare role to access the dashboard
        </p>
      </div>

      {/* Role Cards */}
      <div style={{ maxWidth: '1100px', margin: '0 auto', padding: '40px 24px' }}>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '32px'
        }}>
          {roles.map((role) => (
            <div
              key={role.id}
              onClick={() => navigate(`/login?role=${role.id}`)}
              style={{
                background: 'white',
                borderRadius: '20px',
                padding: '40px 32px',
                textAlign: 'center',
                cursor: 'pointer',
                border: '2px solid #f3e8ff',
                transition: 'all 0.3s ease',
                boxShadow: '0 4px 20px rgba(0,0,0,0.04)'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = role.color;
                e.currentTarget.style.transform = 'translateY(-8px)';
                e.currentTarget.style.boxShadow = `0 12px 40px ${role.color}20`;
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = '#f3e8ff';
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = '0 4px 20px rgba(0,0,0,0.04)';
              }}
            >
              <div style={{
                width: '80px',
                height: '80px',
                background: role.bgColor,
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 20px',
                fontSize: '40px'
              }}>
                {role.icon}
              </div>
              <h2 style={{ fontSize: '28px', fontWeight: 700, color: role.color, marginBottom: '12px' }}>
                {role.title}
              </h2>
              <p style={{ color: '#6b7280', fontSize: '15px', lineHeight: 1.6, marginBottom: '24px' }}>
                {role.description}
              </p>
              <button
                style={{
                  padding: '10px 32px',
                  background: role.color,
                  color: 'white',
                  border: 'none',
                  borderRadius: '50px',
                  cursor: 'pointer',
                  fontSize: '14px',
                  fontWeight: 600,
                  transition: 'all 0.3s ease'
                }}
                onMouseEnter={(e) => e.target.style.transform = 'scale(1.05)'}
                onMouseLeave={(e) => e.target.style.transform = 'scale(1)'}
              >
                Login as {role.title} →
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default RoleSelectionPage;