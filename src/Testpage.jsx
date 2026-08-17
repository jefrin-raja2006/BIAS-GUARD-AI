import React from 'react';

function TestPage() {
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
        borderRadius: '16px',
        padding: '48px',
        textAlign: 'center',
        border: '1px solid #f3e8ff',
        maxWidth: '600px',
        boxShadow: '0 4px 6px rgba(0,0,0,0.05)'
      }}>
        <div style={{ fontSize: '80px', marginBottom: '20px' }}>🏥</div>
        <h1 style={{ fontSize: '36px', fontWeight: 700, color: '#111827' }}>BiasGuard AI</h1>
        <p style={{ fontSize: '18px', color: '#6b7280', margin: '16px 0' }}>
          Fair & Unbiased Clinical Decisions
        </p>
        <button
          style={{
            padding: '12px 32px',
            background: '#8b5cf6',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            fontSize: '16px',
            fontWeight: 600,
            cursor: 'pointer',
            transition: 'background 0.2s'
          }}
          onMouseEnter={(e) => e.target.style.background = '#7c3aed'}
          onMouseLeave={(e) => e.target.style.background = '#8b5cf6'}
        >
          Get Started →
        </button>
        <div style={{ marginTop: '20px', fontSize: '12px', color: '#9ca3af' }}>
          Violet theme applied ✓
        </div>
      </div>
    </div>
  );
}

export default TestPage;