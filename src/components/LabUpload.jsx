import React, { useState } from 'react';

function LabUpload({ patient, onSubmit }) {
  const [formData, setFormData] = useState({
    bloodGlucose: '',
    cholesterol: '',
    hemoglobin: '',
    testDate: '',
    notes: ''
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
  };

  return (
    <div>
      <h3 style={{ marginBottom: '20px' }}>Upload Lab Results for {patient.name}</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Blood Glucose (mg/dL) *</label>
          <input
            type="number"
            step="0.1"
            name="bloodGlucose"
            value={formData.bloodGlucose}
            onChange={handleChange}
            placeholder="Enter blood glucose level"
            required
          />
        </div>

        <div className="form-group">
          <label>Cholesterol (mg/dL) *</label>
          <input
            type="number"
            name="cholesterol"
            value={formData.cholesterol}
            onChange={handleChange}
            placeholder="Enter cholesterol level"
            required
          />
        </div>

        <div className="form-group">
          <label>Hemoglobin (g/dL) *</label>
          <input
            type="number"
            step="0.1"
            name="hemoglobin"
            value={formData.hemoglobin}
            onChange={handleChange}
            placeholder="Enter hemoglobin level"
            required
          />
        </div>

        <div className="form-group">
          <label>Test Date</label>
          <input
            type="date"
            name="testDate"
            value={formData.testDate}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label>Additional Notes</label>
          <textarea
            name="notes"
            value={formData.notes}
            onChange={handleChange}
            rows="3"
            placeholder="Any additional observations..."
          />
        </div>

        <button type="submit" className="btn btn-primary" style={{ width: '100%' }}>
          Upload Lab Results & Request Prediction
        </button>
      </form>
    </div>
  );
}

export default LabUpload;