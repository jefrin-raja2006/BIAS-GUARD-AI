import React from 'react';
import './index.css';

function App() {
  return (
    <div style={{
      minHeight: '100vh',
      background: '#faf9fe',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px'
    }}>
      <div style={{
        background: 'white',
        borderRadius: '24px',
        padding: '60px 48px',
        textAlign: 'center',
        border: '1px solid #f3e8ff',
        maxWidth: '700px',
        width: '100%',
        boxShadow: '0 4px 20px rgba(0,0,0,0.04)'
      }}>
        {/* Logo */}
        <div style={{
          width: '80px',
          height: '80px',
          background: 'linear-gradient(135deg, #8b5cf6, #7c3aed)',
          borderRadius: '20px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          margin: '0 auto 24px'
        }}>
          <span style={{ fontSize: '40px' }}>🏥</span>
        </div>

        <h1 style={{
          fontSize: '42px',
          fontWeight: 700,
          color: '#111827',
          marginBottom: '12px'
        }}>
          BiasGuard AI
        </h1>

        <p style={{
          fontSize: '20px',
          color: '#6b7280',
          marginBottom: '8px'
        }}>
          Fair & Unbiased Clinical Decisions
        </p>

        <p style={{
          fontSize: '16px',
          color: '#8b5cf6',
          fontWeight: 500,
          marginBottom: '32px'
        }}>
          Healthcare AI with Integrity
        </p>

        <button
          style={{
            padding: '14px 40px',
            background: 'linear-gradient(135deg, #8b5cf6, #7c3aed)',
            color: 'white',
            border: 'none',
            borderRadius: '40px',
            fontSize: '16px',
            fontWeight: 600,
            cursor: 'pointer',
            transition: 'all 0.3s ease',
            boxShadow: '0 4px 14px rgba(139, 92, 246, 0.3)'
          }}
          onMouseEnter={(e) => {
            e.target.style.transform = 'scale(1.02)';
            e.target.style.boxShadow = '0 6px 20px rgba(139, 92, 246, 0.4)';
          }}
          onMouseLeave={(e) => {
            e.target.style.transform = 'scale(1)';
            e.target.style.boxShadow = '0 4px 14px rgba(139, 92, 246, 0.3)';
          }}
        >
          Get Started →
        </button>

        <div style={{
          marginTop: '32px',
          paddingTop: '24px',
          borderTop: '1px solid #f3e8ff',
          display: 'flex',
          justifyContent: 'center',
          gap: '40px',
          fontSize: '14px',
          color: '#9ca3af'
        }}>
          <span>✓ HIPAA Compliant</span>
          <span>✓ ISO 27001</span>
          <span>✓ 99% Accuracy</span>
        </div>
      </div>
    </div>
  );
}

export default App;