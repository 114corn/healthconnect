import { useEffect, useState } from 'react';
import axios from 'axios';

interface PatientData {
  id: string;
  name: string;
  age: number;
  condition: string;
}

export const usePatientData = () => {
  const [patientData, setPatientData] = useState<PatientData[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchPatientData = async () => {
    try {
      setLoading(true);
      const response = await axios.get<PatientData[]>(`${process.env.REACT_APP_BACKEND_URL}/patients`);
      setPatientData(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch patient data.');
      setLoading(false);
    }
  };

  const updatePatientData = async (patientId: string, newData: Partial<PatientData>) => {
    try {
      setLoading(true);
      await axios.put(`${process.env.REACT_APP_BACKEND_URL}/patients/${patientId}`, newData);
      await fetchPatientData();
    } catch (err) {
      setError('Failed to update patient data.');
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPatientData();
  }, []);

  return { patientData, error, loading, updatePatientData };
};