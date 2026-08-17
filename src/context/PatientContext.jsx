import React, { createContext, useState, useContext } from 'react';

const PatientContext = createContext();

export const usePatients = () => {
  const context = useContext(PatientContext);
  if (!context) {
    throw new Error('usePatients must be used within PatientProvider');
  }
  return context;
};

export const PatientProvider = ({ children }) => {
  const [patients, setPatients] = useState([]);

  const addPatient = (patientData) => {
    const newPatient = {
      id: Date.now(),
      ...patientData,
      status: 'pending',
      riskLevel: patientData.bmi > 30 ? 'High' : 'Low',
      riskScore: patientData.bmi > 30 ? 85 : 45,
      createdAt: new Date().toISOString(),
      labResults: null,
      prediction: null
    };
    setPatients(prev => [newPatient, ...prev]);
    return newPatient;
  };

  const updatePatient = (patientId, updates) => {
    setPatients(prev => prev.map(patient => 
      patient.id === patientId ? { ...patient, ...updates } : patient
    ));
  };

  const getPatientsByStatus = (status) => {
    return patients.filter(patient => patient.status === status);
  };

  const getPatientsForDoctor = () => {
    return patients.filter(patient => patient.status === 'lab_completed' || patient.riskLevel === 'High');
  };

  return (
    <PatientContext.Provider value={{
      patients,
      addPatient,
      updatePatient,
      getPatientsByStatus,
      getPatientsForDoctor,
      setPatients
    }}>
      {children}
    </PatientContext.Provider>
  );
};