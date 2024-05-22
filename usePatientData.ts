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

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await axios.get<PatientData[]>(`${process.env.REACT_APP_BACKEND_URL}/patients`);
      setPatientData(response.data);
    } catch (err) {
      if (axios.isAxiosError(err)) {
        // This checks if the error is from Axios, providing more information
        setError(err.response?.data || 'Failed to fetch patient data.');
      } else {
        setError('An unexpected error occurred.');
      }
    } finally {
      setLoading(false);
    }
  };

  const updateData = async (patientId: string, newData: Partial<PatientData>) => {
    setLoading(true);
    try {
      await axios.put(`${process.env.REACT_APP_BACKEND_URL}/patients/${patientId}`, newData);
      await fetchData();
    } catch (err) {
      if (axios.isAxiosError(err)) {
        // More detailed error information from Axios
        setError(err.response?.data || 'Failed to update patient data.');
      } else {
        setError('An unexpected error occurred during update.');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    // Although the original code didn't include `fetchData` in the dependency array,
    // it's a common recommendation to include functions used inside useEffect
    // unless you are absolutely sure they will not change or cause re-renders.
  }, [fetchData]);

  return { patientData, error, loading, updatePatientData: updateData };
};