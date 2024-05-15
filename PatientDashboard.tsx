import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface DoctorVisit {
  date: string;
  doctorName: string;
  reason: string;
}

interface Medication {
  name: string;
  dosage: string;
  schedule: string;
}

interface Appointment {
  date: string;
  doctorName: string;
  purpose: string;
}

interface PatientDashboardProps {}

const PatientDashboard: React.FC<PatientDashboardProps> = () => {
  const [doctorVisits, setDoctorVisits] = useState<DoctorVisit[]>([]);
  const [medications, setMedications] = useState<Medication[]>([]);
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [message, setMessage] = useState<string>('');

  useEffect(() => {
    const fetchData = async () => {
      const doctorVisitsResponse = await axios.get(`${process.env.REACT_APP_API_URL}/doctorVisits`);
      const medicationsResponse = await axios.get(`${process.env.REACT_APP_API_URL}/medications`);
      const appointmentsResponse = await axios.get(`${process.env.REACT_APP_API_URL}/appointments`);
      
      setDoctorVisits(doctorVisitsResponse.data);
      setMedications(medicationsResponse.data);
      setAppointments(appointmentsResponse.data);
    };

    fetchData().catch(console.error);
  }, []);

  const handleMessageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setMessage(event.target.value);
  };

  const handleSendMessage = async () => {
    await axios.post(`${process.env.REACT_APP_API_URL}/sendMessage`, { message });
    setMessage('');
  };

  const handleBookAppointment = async (appointment: Appointment) => {
    await axios.post(`${process.env.REACT_APP_API_URL}/bookAppointment`, appointment);
    setAppointments([...appointments, appointment]);
  };

  return (
    <div>
      <h2>Recent Doctor Visits</h2>
      <ul>
        {doctorVisits.map(visit => (
          <li key={visit.date}>{`${visit.date} - ${visit.doctorName}: ${visit.reason}`}</li>
        ))}
      </ul>

      <h2>Medication Schedule</h2>
      <ul>
        {medications.map(medication => (
          <li key={medication.name}>{`${medication.name}: ${medication.dosage} - ${medication.schedule}`}</li>
        ))}
      </ul>

      <h2>Upcoming Appointments</h2>
      <ul>
        {appointments.map(appointment => (
          <li key={appointment.date}>{`${appointment.date} - ${appointment.doctorName}: ${appointment.purpose}`}</li>
        ))}
      </ul>

      <div>
        <h2>Send a Message to Your Healthcare Provider</h2>
        <input type="text" value={message} onChange={handleMessageChange} />
        <button onClick={handleSendMessage}>Send Message</button>
      </div>

      <div>
        <h2>Book an Appointment</h2>
        <button onClick={() => handleBookAppointment({
          date: new Date().toISOString(),
          doctorName: "Dr. Example",
          purpose: "Routine Check-up",
        })}>Book Appointment</button>
      </div>
    </div>
  );
};

export default PatientDashboard;