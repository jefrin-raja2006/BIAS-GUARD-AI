import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import PatientForm from '../components/PatientForm';

function NursePage({ user, setUser }) {
  const [showForm, setShowForm] = useState(false);
  const [patients, setPatients] = useState([]);
  const [message, setMessage] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const nurseName = "Kiki";

  useEffect(() => {
    loadPatients();
  }, []);

  const loadPatients = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/patients');
      const data = await response.json();
      console.log('Patients loaded:', data);
      if (data.success && data.data) {
        setPatients(data.data);
      } else if (Array.isArray(data)) {
        setPatients(data);
      }
    } catch (error) {
      console.error('Error loading patients:', error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('user');
    setUser(null);
    navigate('/login');
  };

  const handlePatientSubmit = async (patientData) => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/patients', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(patientData),
      });
      const data = await response.json();
      console.log('Create response:', data);
      
      if (data.success) {
        await loadPatients();
        setShowForm(false);
        setMessage({
          type: 'success',
          text: `✅ Patient ${patientData.name} registered successfully! (${data.data.risk_level} Risk)`
        });
        setTimeout(() => setMessage(null), 3000);
      } else {
        setMessage({
          type: 'error',
          text: `❌ ${data.error || 'Failed to save patient'}`
        });
      }
    } catch (error) {
      console.error('Error:', error);
      setMessage({
        type: 'error',
        text: '❌ Error saving patient to database'
      });
    } finally {
      setLoading(false);
    }
  };

  const stats = [
    { label: 'Total Patients', value: patients.length, icon: '👥', color: 'purple' },
    { label: 'High Risk', value: patients.filter(p => p.risk_level === 'High').length, icon: '⚠️', color: 'red' },
    { label: 'Low Risk', value: patients.filter(p => p.risk_level === 'Low').length, icon: '✅', color: 'green' },
    { label: 'Medium Risk', value: patients.filter(p => p.risk_level === 'Medium').length, icon: '📊', color: 'orange' }
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
              👩‍⚕️
            </div>
            <div>
              <div style={{ fontWeight: 600, fontSize: '14px', color: '#1f2937' }}>{nurseName}</div>
              <div style={{ fontSize: '12px', color: '#6b7280' }}>Senior Nurse</div>
            </div>
          </div>
          <button onClick={handleLogout} style={{
            padding: '8px 20px',
            background: 'linear-gradient(135deg, #ef4444, #dc2626)',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            fontSize: '14px',
            fontWeight: 600
          }}>Logout</button>
        </div>
      </nav>

      <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '32px 24px' }}>
        {/* Welcome */}
        <div style={{ marginBottom: '32px' }}>
          <h1 style={{ fontSize: '32px', fontWeight: 800, color: '#1f2937', marginBottom: '8px' }}>
            Welcome back, {nurseName}! 👋
          </h1>
          <p style={{ color: '#6b7280', fontSize: '16px' }}>
            Manage patient registrations and initial health assessments
          </p>
          <div style={{ marginTop: '8px', padding: '8px 16px', background: '#f3e8ff', borderRadius: '8px', display: 'inline-block' }}>
            <span style={{ fontSize: '13px', color: '#7c3aed' }}>
              💡 High risk patients will appear in Doctor's dashboard
            </span>
          </div>
        </div>

        {/* Stats */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(4, 1fr)',
          gap: '24px',
          marginBottom: '32px'
        }}>
          {stats.map((stat, idx) => (
            <div key={idx} style={{
              background: 'white',
              borderRadius: '20px',
              padding: '24px',
              boxShadow: '0 4px 20px rgba(139, 92, 246, 0.06)',
              border: '1px solid #f3e8ff',
              transition: 'all 0.3s ease'
            }}>
              <div style={{
                width: '48px',
                height: '48px',
                borderRadius: '12px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '24px',
                marginBottom: '16px',
                background: stat.color === 'purple' ? '#f3e8ff' : 
                           stat.color === 'green' ? '#ecfdf5' : 
                           stat.color === 'orange' ? '#fffbeb' : '#fef2f2'
              }}>{stat.icon}</div>
              <div style={{ fontSize: '32px', fontWeight: 800, color: '#1f2937', marginBottom: '4px' }}>{stat.value}</div>
              <div style={{ fontSize: '14px', color: '#6b7280' }}>{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Main Content */}
        <div style={{ display: 'grid', gridTemplateColumns: showForm ? '1fr 1fr' : '1fr', gap: '24px' }}>
          {showForm && (
            <div style={{
              background: 'white',
              borderRadius: '20px',
              padding: '32px',
              boxShadow: '0 4px 20px rgba(139, 92, 246, 0.08)',
              border: '1px solid #f3e8ff'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                <h2 style={{ fontSize: '22px', fontWeight: 700, color: '#1f2937' }}>✨ New Patient Registration</h2>
                <button
                  onClick={() => setShowForm(false)}
                  style={{ background: 'none', border: 'none', fontSize: '24px', cursor: 'pointer', color: '#6b7280' }}
                >
                  ✕
                </button>
              </div>
              <PatientForm onSubmit={handlePatientSubmit} loading={loading} />
            </div>
          )}

          <div style={{
            background: 'white',
            borderRadius: '20px',
            padding: '32px',
            boxShadow: '0 4px 20px rgba(139, 92, 246, 0.08)',
            border: '1px solid #f3e8ff'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
              <h2 style={{ fontSize: '22px', fontWeight: 700, color: '#1f2937' }}>📋 Recent Patients</h2>
              {!showForm && (
                <button onClick={() => setShowForm(true)} style={{
                  padding: '10px 24px',
                  background: 'linear-gradient(135deg, #8b5cf6, #7c3aed)',
                  color: 'white',
                  border: 'none',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  fontSize: '14px',
                  fontWeight: 600
                }}>
                  + New Patient
                </button>
              )}
            </div>

            {message && (
              <div style={{
                padding: '12px',
                borderRadius: '8px',
                marginBottom: '16px',
                background: message.type === 'success' ? '#ecfdf5' : '#fef2f2',
                color: message.type === 'success' ? '#065f46' : '#991b1b',
                border: message.type === 'success' ? '1px solid #a7f3d0' : '1px solid #fca5a5'
              }}>
                {message.text}
              </div>
            )}

            {patients.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '60px 20px', background: '#f8f7fc', borderRadius: '16px' }}>
                <div style={{ fontSize: '64px', marginBottom: '16px' }}>📋</div>
                <div style={{ fontSize: '16px', color: '#6b7280' }}>No patients registered yet</div>
                <div style={{ fontSize: '14px', color: '#9ca3af', marginTop: '8px' }}>Click "New Patient" to get started</div>
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {patients.slice(0, 10).map((patient) => (
                  <div key={patient.id} style={{
                    padding: '16px',
                    background: '#f8f7fc',
                    borderRadius: '12px',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                  }}>
                    <div>
                      <div style={{ fontWeight: 600, color: '#1f2937' }}>{patient.name}</div>
                      <div style={{ fontSize: '13px', color: '#6b7280' }}>
                        Age: {patient.age} | BMI: {patient.bmi} | BP: {patient.blood_pressure}
                      </div>
                      <div style={{ fontSize: '11px', color: '#9ca3af' }}>
                        Status: {patient.status} | ID: #{patient.id}
                      </div>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <span style={{
                        padding: '4px 12px',
                        borderRadius: '50px',
                        fontSize: '12px',
                        fontWeight: 600,
                        background: patient.risk_level === 'High' ? '#fef2f2' : 
                                   patient.risk_level === 'Medium' ? '#fffbeb' : '#ecfdf5',
                        color: patient.risk_level === 'High' ? '#991b1b' : 
                               patient.risk_level === 'Medium' ? '#92400e' : '#065f46'
                      }}>
                        {patient.risk_level} Risk
                      </span>
                      {patient.risk_level === 'High' && (
                        <div style={{ fontSize: '11px', color: '#7c3aed', marginTop: '4px' }}>
                          👨‍⚕️ Sent to Doctor
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default NursePage;