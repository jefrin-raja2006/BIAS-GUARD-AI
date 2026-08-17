import React from 'react';

function PredictionResult({ prediction, patient }) {
  return (
    <div>
      <h3 style={{ marginBottom: '20px' }}>Diagnosis Results for {patient.name}</h3>
      
      <div style={{ background: '#f7fafc', padding: '24px', borderRadius: '16px' }}>
        {/* Disease */}
        <div style={{ marginBottom: '24px', textAlign: 'center' }}>
          <div style={{ fontSize: '14px', color: '#718096', marginBottom: '8px' }}>Primary Diagnosis</div>
          <div style={{ fontSize: '32px', fontWeight: '700', color: '#667eea' }}>
            {prediction.disease}
          </div>
        </div>

        {/* Confidence Score */}
        <div style={{ marginBottom: '24px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
            <strong>Confidence Score</strong>
            <span>{(prediction.confidence * 100).toFixed(1)}%</span>
          </div>
          <div style={{ 
            width: '100%', 
            height: '8px', 
            background: '#e2e8f0', 
            borderRadius: '4px',
            overflow: 'hidden'
          }}>
            <div style={{ 
              width: `${prediction.confidence * 100}%`, 
              height: '100%', 
              background: '#48bb78',
              transition: 'width 0.5s ease'
            }}></div>
          </div>
        </div>

        {/* Risk Score */}
        <div style={{ marginBottom: '24px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
            <strong>Risk Score</strong>
            <span>{prediction.riskScore}%</span>
          </div>
          <div style={{ 
            width: '100%', 
            height: '8px', 
            background: '#e2e8f0', 
            borderRadius: '4px',
            overflow: 'hidden'
          }}>
            <div style={{ 
              width: `${prediction.riskScore}%`, 
              height: '100%', 
              background: prediction.riskScore > 70 ? '#f56565' : prediction.riskScore > 40 ? '#ed8936' : '#48bb78',
              transition: 'width 0.5s ease'
            }}></div>
          </div>
        </div>

        {/* Bias Detection */}
        {prediction.biasDetected && (
          <div className="alert alert-warning" style={{ marginBottom: '24px' }}>
            <strong>⚠️ Bias Detected!</strong>
            <p style={{ marginTop: '8px', fontSize: '14px' }}>
              This prediction shows potential bias. Please review carefully before making final decision.
            </p>
          </div>
        )}

        {/* Recommendations */}
        <div>
          <strong style={{ display: 'block', marginBottom: '12px' }}>Recommendations:</strong>
          <ul style={{ marginLeft: '20px', color: '#4a5568' }}>
            {prediction.recommendations.map((rec, index) => (
              <li key={index} style={{ marginBottom: '8px' }}>{rec}</li>
            ))}
          </ul>
        </div>
      </div>

      <div className="alert alert-success" style={{ marginTop: '20px' }}>
        <strong>✅ Clinical Decision Support:</strong><br />
        This prediction is based on complete patient data and lab results.
        {prediction.biasDetected && " Please review the bias analysis before making final decision."}
      </div>
    </div>
  );
}

export default PredictionResult;