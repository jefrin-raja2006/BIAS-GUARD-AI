import React from 'react';
import { useNavigate } from 'react-router-dom';

function LandingPage() {
  const navigate = useNavigate();

  const features = [
    { icon: '🎯', title: 'AI-Powered Predictions', description: '99% accurate disease prediction using advanced ML models.' },
    { icon: '⚖️', title: 'Bias Detection', description: 'Real-time fairness analysis across all demographic groups.' },
    { icon: '🔄', title: 'Two-Stage Process', description: 'Risk screening + mandatory lab tests for clinical validity.' },
    { icon: '🔬', title: 'Lab Integration', description: 'Seamless integration with laboratory systems.' },
    { icon: '👥', title: 'Role-Based Access', description: 'Dedicated portals for Nurses, Lab Techs, and Doctors.' },
    { icon: '📊', title: 'Real-Time Analytics', description: 'Instant fairness metrics and bias reports.' }
  ];

  const stats = [
    { value: '99.9%', label: 'Uptime' },
    { value: '<2s', label: 'Response Time' },
    { value: '50K+', label: 'Patients Processed' },
    { value: '99%', label: 'Accuracy' }
  ];

  return (
    <div style={{ minHeight: '100vh', background: '#f8f7fc' }}>
      {/* Hero Section */}
      <div style={{
        background: 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)',
        padding: '100px 24px 80px',
        position: 'relative',
        overflow: 'hidden'
      }}>
        {/* Background Decoration */}
        <div style={{
          position: 'absolute',
          top: '-100px',
          right: '-100px',
          width: '400px',
          height: '400px',
          background: 'rgba(255,255,255,0.1)',
          borderRadius: '50%'
        }}></div>
        <div style={{
          position: 'absolute',
          bottom: '-150px',
          left: '-150px',
          width: '500px',
          height: '500px',
          background: 'rgba(255,255,255,0.05)',
          borderRadius: '50%'
        }}></div>

        <div style={{ maxWidth: '1200px', margin: '0 auto', position: 'relative', zIndex: 1 }}>
          <div style={{ textAlign: 'center', maxWidth: '800px', margin: '0 auto' }}>
            <div style={{
              display: 'inline-block',
              background: 'rgba(255,255,255,0.2)',
              padding: '8px 20px',
              borderRadius: '50px',
              marginBottom: '24px'
            }}>
              <span style={{ color: 'white', fontWeight: 600, fontSize: '14px' }}>
                Healthcare AI Platform
              </span>
            </div>

            <h1 style={{
              fontSize: '52px',
              fontWeight: 800,
              color: 'white',
              marginBottom: '20px',
              lineHeight: 1.2
            }}>
              Fair & Unbiased
              <br />
              <span style={{ color: '#f3e8ff' }}>Clinical Decisions</span>
            </h1>

            <p style={{
              fontSize: '18px',
              color: 'rgba(255,255,255,0.9)',
              marginBottom: '32px',
              lineHeight: 1.6
            }}>
              BiasGuard AI helps healthcare professionals make accurate, transparent,
              and bias-free predictions using advanced machine learning.
            </p>

            <button
              onClick={() => navigate('/roles')}
              style={{
                padding: '14px 40px',
                background: 'white',
                color: '#8b5cf6',
                border: 'none',
                borderRadius: '50px',
                fontSize: '16px',
                fontWeight: 600,
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                boxShadow: '0 4px 16px rgba(0,0,0,0.1)'
              }}
              onMouseEnter={(e) => {
                e.target.style.transform = 'scale(1.05)';
                e.target.style.boxShadow = '0 8px 32px rgba(0,0,0,0.2)';
              }}
              onMouseLeave={(e) => {
                e.target.style.transform = 'scale(1)';
                e.target.style.boxShadow = '0 4px 16px rgba(0,0,0,0.1)';
              }}
            >
              Get Started →
            </button>
          </div>

          {/* Stats */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(4, 1fr)',
            gap: '24px',
            marginTop: '60px',
            paddingTop: '40px',
            borderTop: '1px solid rgba(255,255,255,0.2)'
          }}>
            {stats.map((stat, index) => (
              <div key={index} style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '32px', fontWeight: 800, color: 'white' }}>{stat.value}</div>
                <div style={{ fontSize: '14px', color: 'rgba(255,255,255,0.8)' }}>{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div style={{ padding: '80px 24px', maxWidth: '1200px', margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '60px' }}>
          <h2 style={{ fontSize: '36px', fontWeight: 800, color: '#1f2937', marginBottom: '16px' }}>
            Enterprise-Grade Healthcare AI
          </h2>
          <p style={{ fontSize: '18px', color: '#6b7280', maxWidth: '600px', margin: '0 auto' }}>
            Comprehensive solution for fair and accurate clinical decisions
          </p>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '24px'
        }}>
          {features.map((feature, index) => (
            <div
              key={index}
              style={{
                background: 'white',
                borderRadius: '16px',
                padding: '32px',
                boxShadow: '0 2px 10px rgba(0,0,0,0.05)',
                border: '1px solid #f3e8ff',
                transition: 'all 0.3s ease'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-4px)';
                e.currentTarget.style.boxShadow = '0 8px 30px rgba(139,92,246,0.12)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = '0 2px 10px rgba(0,0,0,0.05)';
              }}
            >
              <div style={{ fontSize: '48px', marginBottom: '16px' }}>{feature.icon}</div>
              <h3 style={{ fontSize: '18px', fontWeight: 700, color: '#1f2937', marginBottom: '12px' }}>
                {feature.title}
              </h3>
              <p style={{ fontSize: '14px', color: '#6b7280', lineHeight: 1.6 }}>
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Workflow Section */}
      <div style={{ background: '#f3f0ff', padding: '80px 24px' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', textAlign: 'center' }}>
          <h2 style={{ fontSize: '36px', fontWeight: 800, color: '#1f2937', marginBottom: '16px' }}>
            How It Works
          </h2>
          <p style={{ fontSize: '18px', color: '#6b7280', marginBottom: '60px' }}>
            Simple 4-step workflow from registration to final diagnosis
          </p>

          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(4, 1fr)',
            gap: '24px'
          }}>
            {[
              { step: '01', title: 'Patient Registration', icon: '👩‍⚕️', color: '#8b5cf6' },
              { step: '02', title: 'Risk Assessment', icon: '🤖', color: '#7c3aed' },
              { step: '03', title: 'Lab Tests', icon: '🔬', color: '#6d28d9' },
              { step: '04', title: 'Final Diagnosis', icon: '👨‍⚕️', color: '#5b21b6' }
            ].map((item, index) => (
              <div key={index}>
                <div style={{
                  width: '80px',
                  height: '80px',
                  background: item.color,
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto 20px',
                  color: 'white',
                  fontSize: '24px',
                  fontWeight: 700,
                  boxShadow: `0 4px 16px ${item.color}40`
                }}>
                  {item.step}
                </div>
                <div style={{ fontSize: '40px', marginBottom: '12px' }}>{item.icon}</div>
                <div style={{ fontSize: '16px', fontWeight: 600, color: '#1f2937' }}>{item.title}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div style={{ padding: '80px 24px', maxWidth: '900px', margin: '0 auto', textAlign: 'center' }}>
        <h2 style={{ fontSize: '36px', fontWeight: 800, color: '#1f2937', marginBottom: '16px' }}>
          Ready to Transform Healthcare?
        </h2>
        <p style={{ fontSize: '18px', color: '#6b7280', marginBottom: '32px' }}>
          Join leading healthcare organizations using BiasGuard AI for fair and accurate predictions.
        </p>
        <button
          onClick={() => navigate('/roles')}
          className="btn btn-primary"
          style={{ padding: '16px 48px', fontSize: '18px' }}
        >
          Get Started Now
        </button>
      </div>

      {/* Footer */}
      <footer style={{ background: '#1f2937', color: '#9ca3af', padding: '48px 24px', textAlign: 'center' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px', marginBottom: '24px' }}>
            <span style={{ fontSize: '24px' }}>🏥</span>
            <span style={{ fontSize: '20px', fontWeight: 700, color: 'white' }}>BiasGuard AI</span>
          </div>
          <p style={{ fontSize: '14px', marginBottom: '16px' }}>
            Empowering fair and accurate healthcare decisions through AI
          </p>
          <p style={{ fontSize: '12px' }}>
            © 2025 BiasGuard AI. All rights reserved. | HIPAA Compliant | ISO 27001 Certified
          </p>
        </div>
      </footer>
    </div>
  );
}

export default LandingPage;