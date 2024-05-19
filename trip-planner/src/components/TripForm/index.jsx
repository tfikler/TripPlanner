'use client';
import { useState } from 'react';
import styles from './TripForm.module.css';
import { useRouter } from 'next/navigation';
import { getTrips, generateImage, getDailyPlan } from '../../api/tripRequests';


function TripForm() {
    const [step, setStep] = useState(1);
    const [formData, setFormData] = useState({
        startDate: '',
        endDate: '',
        totalBudget: '',
        tripType: '',
        selectedTrip: null,
        dailyPlan: null,
    });
    const [trips, setTrips] = useState([]);
    const today = new Date().toISOString().split('T')[0];

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (step === 1) {
            const results = await getTrips(formData.startDate, formData.endDate, formData.totalBudget, formData.tripType);
            setTrips(results);
            setStep(2); // Move to trip selection step
        }
    };

    const handleNext = async () => {
        if (step === 2 && formData.selectedTrip) {
            setStep(3); // Move to daily plan view
            const dailyPlay = await getDailyPlan(formData.startDate, formData.endDate, formData.totalBudget, formData.selectedTrip).then(plan => setFormData(prev => ({ ...prev, dailyPlan: plan })));
            console.log(dailyPlay)
        }
    };

    const handleTripSelect = (trip) => {
        setFormData(prev => ({ ...prev, selectedTrip: trip }));
    };

    return (
        <div className={styles.tripFormContainer}>
            {step === 1 && (
                <form onSubmit={handleSubmit} className={styles.form}>
                    <div>
                        <label>Start Date:</label>
                        <input
                            type="date"
                            name="startDate"
                            className={styles.formInput}
                            value={formData.startDate}
                            onChange={handleChange}
                            required
                            min={today}
                        />
                    </div>
                    <div>
                        <label>End Date:</label>
                        <input
                            type="date"
                            name="endDate"
                            className={styles.formInput}
                            value={formData.endDate}
                            onChange={handleChange}
                            required
                            min={formData.startDate || today}
                        />
                    </div>
                    <div>
                        <label>Total Budget:</label>
                        <input
                            type="number"
                            name="totalBudget"
                            className={styles.formInput}
                            value={formData.totalBudget}
                            onChange={handleChange}
                            required
                            min="0"
                        />
                    </div>
                    <div>
                        <label>Trip Type:</label>
                        <select
                            name="tripType"
                            className={styles.formSelect}
                            value={formData.tripType}
                            onChange={handleChange}
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
            )}

            {step === 2 && (
                <>
                <div className={styles.tripSelection}>
                    {trips.map(trip => (
                        <div key={trip.id}
                             className={`${styles.tripItem} ${formData.selectedTrip?.id === trip.id ? styles.selected : ''}`}
                             onClick={() => handleTripSelect(trip)}>
                            <p>{trip.destination}</p>
                            <p>${trip.price}</p>
                        </div>
                    ))}
                </div>
                <button onClick={handleNext} className={styles.nextButton} disabled={!formData.selectedTrip}>Next</button>
                </>
                )}


            {step === 3 && formData.dailyPlan && (
                <div className={styles.dailyPlan}>
                    <h2>Daily Plan for {formData.selectedTrip.destination}</h2>
                    <div>{JSON.stringify(formData.dailyPlan)}</div>
                </div>
            )}
        </div>
    );
}

export default TripForm;