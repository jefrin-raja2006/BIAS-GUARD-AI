import React, { useState } from 'react';

function PatientForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    gender: '',
    bmi: '',
    bloodPressure: '',
    medicalHistory: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
    setFormData({
      name: '',
      age: '',
      gender: '',
      bmi: '',
      bloodPressure: '',
      medicalHistory: ''
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="form-group">
        <label>Full Name *</label>
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          placeholder="Enter patient's full name"
          required
        />
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
        <div className="form-group">
          <label>Age *</label>
          <input
            type="number"
            name="age"
            value={formData.age}
            onChange={handleChange}
            placeholder="Enter age"
            required
          />
        </div>

        <div className="form-group">
          <label>Gender *</label>
          <select
            name="gender"
            value={formData.gender}
            onChange={handleChange}
            required
          >
            <option value="">Select gender</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </select>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
        <div className="form-group">
          <label>BMI *</label>
          <input
            type="number"
            step="0.1"
            name="bmi"
            value={formData.bmi}
            onChange={handleChange}
            placeholder="Enter BMI (10-50)"
            required
          />
        </div>

        <div className="form-group">
          <label>Blood Pressure (Systolic) *</label>
          <input
            type="number"
            name="bloodPressure"
            value={formData.bloodPressure}
            onChange={handleChange}
            placeholder="Enter BP"
            required
          />
        </div>
      </div>

      <div className="form-group">
        <label>Medical History</label>
        <textarea
          name="medicalHistory"
          value={formData.medicalHistory}
          onChange={handleChange}
          placeholder="Previous conditions, surgeries, allergies..."
          rows="3"
        />
      </div>

      <button
        type="submit"
        className="btn btn-primary"
        style={{ width: '100%' }}
      >
        Register Patient
      </button>
    </form>
  );
}

export default PatientForm;