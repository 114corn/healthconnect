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

  const baseURL = process.env.REACT_APP_BACKEND_URL;

  const handleError = (err: any) => {
    if (axios.isAxiosError(err)) {
      setError(err.response?.data.message || 'An error occurred while processing your request.');
    } else {
      setError('An unexpected error occurred.');
    }
  };

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await axios.get<PatientData[]>(`${baseURL}/patients`);
      setPatientData(response.data);
    } catch (err) {
      handleError(err);
    } finally {
      setLoading(false);
    }
  };

  const updateData = async (patientId: string, newData: Partial<PatientData>) => {
    setLoading(true);
    try {
      await axios.put(`${baseURL}/patients/${patientId}`, newData);
      await fetchData(); // Refresh data after update
    } catch (err) {
      handleError(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return { patientData, error, loading, updatePatientData: updateData };
};