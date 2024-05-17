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

interface CombinedData {
  doctorVisits: DoctorVisit[];
  medications: Medication[];
  appointments: Appointment[];
}

interface PatientDashboardProps {}

const PatientDashboard: React.FC<PatientDashboardProps> = () => {
  const [combinedData, setCombinedData] = useState<CombinedData>({ doctorVisits: [], medications: [], appointments: [] });
  const [message, setMessage] = useState<string>('');

  useEffect(() => {
    fetchCombinedData();
  }, []);

  const fetchCombinedData = async () => {
    try {
      const { data } = await axios.get<CombinedData>(`${process.env.REACT_APP_API_URL}/combinedData`);
      setCombinedData(data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleSendMessage = async () => {
    await axios.post(`${process.env.REACT_APP_API_URL}/sendMessage`, { message });
    setMessage('');
  };

  const handleBookAppointment = async (appointment: Appointment) => {
    await axios.post(`${process.env.REACT_APP_API_URL}/bookAppointment`, appointment);
    setCombinedData({
      ...combinedData,
      appointments: [...combinedData.appointments, appointment],
    });
  };

  return (
    <div>
      <Section title="Recent Doctor Visits">
        {combinedData.doctorVisits.map(visit => (
          <ListItem key={visit.date} content={`${visit.date} - ${visit.doctorName}: ${visit.reason}`} />
        ))}
      </Section>

      <Section title="Medication Schedule">
        {combinedData.medications.map(medication => (
          <ListItem key={medication.name} content={`${medication.name}: ${medication.dosage} - ${medication.schedule}`} />
        ))}
      </Section>

      <Section title="Upcoming Appointments">
        {combinedData.appointments.map(appointment => (
          <ListItem key={appointment.date} content={`${appointment.date} - ${appointment.doctorName}: ${appointment.purpose}`} />
        ))}
      </Section>

      <MessagePanel value={message} onChange={setMessage} onSubmit={handleSendMessage} />

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

interface SectionProps {
  title: string;
  children: React.ReactNode;
}

const Section: React.FC<SectionProps> = ({ title, children }) => (
  <div>
    <h2>{title}</h2>
    <ul>{children}</ul>
  </div>
);

interface ListItemProps {
  content: string;
}

const ListItem: React.FC<ListItemProps> = ({ content }) => (
  <li>{content}</li>
);

interface MessagePanelProps {
  value: string;
  onChange: (newValue: string) => void;
  onSubmit: () => void;
}

const MessagePanel: React.FC<MessagePanelProps> = ({ value, onChange, onSubmit }) => (
  <div>
    <h2>Send a Message to Your Healthcare Provider</h2>
    <input type="text" value={value} onChange={(e) => onChange(e.target.value)} />
    <button onClick={onSubmit}>Send Message</button>
  </div>
);

export default PatientDashboard;