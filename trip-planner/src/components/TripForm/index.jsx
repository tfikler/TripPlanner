'use client';
import { useState } from 'react';
import styles from './TripForm.module.css';
// import { useRouter } from 'next/router';

function TripForm() {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [totalBudget, setTotalBudget] = useState('');
  const [tripType, setTripType] = useState('');
  const today = new Date().toISOString().split('T')[0];
  // const router = useRouter();

  // const handleSubmit = (e) => {
  //   e.preventDefault();
  //   router.push({
  //     pathname: '/results',
  //     query: { startDate, endDate, totalBudget, tripType },
  //   });
  // };
    const handleSubmit = (e) => {
    e.preventDefault();
    alert(`Start Date: ${startDate}, End Date: ${endDate}, Total Budget: ${totalBudget}, Trip Type: ${tripType}`)
    }

  return (
    <form onSubmit={handleSubmit} className={styles.form}>
      <div>
        <label>Start Date:</label>
        <input
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
          required
          min={today}
        />
      </div>
      <div>
        <label>End Date:</label>
        <input
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
          required
          min={startDate || today}
        />
      </div>
      <div>
        <label>Total Budget:</label>
        <input
          type="number"
          value={totalBudget}
          onChange={(e) => setTotalBudget(e.target.value)}
          required
          min="0"
        />
      </div>
      <div>
        <label>Trip Type:</label>
        <select
          value={tripType}
          onChange={(e) => setTripType(e.target.value)}
          required
        >
          <option value="">Select</option>
          <option value="ski">Ski</option>
          <option value="beach">Beach</option>
          <option value="city">City</option>
        </select>
      </div>
      <button type="submit">Find Trips</button>
    </form>
  );
};

export default TripForm;