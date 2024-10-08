'use client';
import { useState } from 'react';
import { TextField, Button, Select, MenuItem, InputLabel, FormControl, Container, Typography, Box } from '@mui/material';
import styles from './TripForm.module.css';
import {getTrips, getDailyPlan, generateImage} from '../../api/tripRequests';
import ImageGallery from "react-image-gallery";
import "react-image-gallery/styles/css/image-gallery.css";
function TripForm() {
    const [step, setStep] = useState(1);
    const [showGallery, setShowGallery] = useState(false);
    const [formData, setFormData] = useState({
        startDate: '',
        endDate: '',
        totalBudget: '',
        tripType: '',
        selectedTrip: null,
        dailyPlan: [],
        img: '',
        totalExpenses: 0,
    });
    const [trips, setTrips] = useState([]);
    const today = new Date().toISOString().split('T')[0];
    const [images, setImages] = useState([]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleToggleGallery = () => {
        setShowGallery(prevShowGallery => !prevShowGallery);
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
            const response = await getDailyPlan(formData.startDate, formData.endDate, formData.totalBudget, formData.selectedTrip);
            console.log((JSON.parse(response)));
            const promiseImages = await Promise.all([
                generateImage(formData.startDate, formData.endDate, response, formData.selectedTrip.destination),
                generateImage(formData.startDate, formData.endDate, response, formData.selectedTrip.destination),
                generateImage(formData.startDate, formData.endDate, response, formData.selectedTrip.destination),
                generateImage(formData.startDate, formData.endDate, response, formData.selectedTrip.destination),
            ])
            const imgs = [
                {
                    original: promiseImages[0],
                    thumbnail: promiseImages[0]
                },
                {
                    original: promiseImages[1],
                    thumbnail: promiseImages[1],
                },
                {
                    original: promiseImages[2],
                    thumbnail: promiseImages[2],
                },
                {
                    original: promiseImages[3],
                    thumbnail: promiseImages[3],
                },
            ];
            setImages(imgs);
            const parsedResponse = JSON.parse(response);
            // const dailyPlan = parsedResponse.find(trip => trip.destination === formData.selectedTrip.destination).dailyPlan;
            const dailyPlan = parsedResponse.dailyPlan;
            const { flight_price, hotel_price } = parsedResponse;
            // Sum up the expenses for each day
            const totalDailyExpenses = dailyPlan.reduce((total, day) => total + day.expenses, 0);

            // Calculate the total cost
            const totalCost = flight_price + hotel_price + totalDailyExpenses;
            setFormData(prev => ({ ...prev, dailyPlan }));
            setFormData(prev => ({ ...prev, imgs }));
            setFormData(prev => ({ ...prev, totalExpenses: totalCost }));
            setStep(3); // Move to daily plan view
        }
    };

    const handleTripSelect = (trip) => {
        setFormData(prev => ({ ...prev, selectedTrip: trip }));
    };

    const DailyPlanItem = ({ date, activities, expenses }) => (
        <div className={styles.dailyPlanItem}>
            <Typography variant="h6">{date}</Typography>
            <ul>
                {activities.map((activity, index) => (
                    <li key={index}>{activity}</li>
                ))}
            </ul>
            <Typography>Expenses: ${expenses}</Typography>
        </div>
    );

    return (
        <Container className={styles.tripFormContainer}>
            {step === 1 && (
                <form onSubmit={handleSubmit} className={styles.form}>
                    <Box sx={{width: '100%', textAlign: 'center'}}>
                    <Typography variant="h4" component="h2" gutterBottom>
                        Plan Your Trip
                    </Typography>
                    </Box>
                    <div className={styles.formGroup}>
                        <TextField
                            label="Start Date"
                            type="date"
                            name="startDate"
                            className={styles.formInput}
                            value={formData.startDate}
                            onChange={handleChange}
                            required
                            InputLabelProps={{
                                shrink: true,
                            }}
                            inputProps={{
                                min: today,
                            }}
                        />
                    </div>
                    <div className={styles.formGroup}>
                        <TextField
                            label="End Date"
                            type="date"
                            name="endDate"
                            className={styles.formInput}
                            value={formData.endDate}
                            onChange={handleChange}
                            required
                            InputLabelProps={{
                                shrink: true,
                            }}
                            inputProps={{
                                min: formData.startDate || today,
                            }}
                        />
                    </div>
                    <div className={styles.formGroup}>
                        <TextField
                            label="Total Budget"
                            type="number"
                            name="totalBudget"
                            className={styles.formInput}
                            value={formData.totalBudget}
                            onChange={handleChange}
                            required
                            inputProps={{
                                min: "0",
                            }}
                        />
                    </div>
                    <div className={styles.formGroup}>
                        <TextField
                            id="tripType"
                            select
                            required
                            label="Trip Type"
                            defaultValue="Trip Type">
                            <MenuItem value="Ski">Ski</MenuItem>
                            <MenuItem value="Beach">Beach</MenuItem>
                            <MenuItem value="City">City</MenuItem>
                        </TextField>

                    </div>
                    <Button
                        type="submit"
                        variant="contained"
                        color="primary"
                        className={styles.submitButton}
                    >
                        Find Trips
                    </Button>
                </form>
            )}

            {step === 2 && trips.length > 0 && (
                <Box className={styles.tripSelection}>
                    <Typography variant="h4">Select a Trip</Typography>
                        <Box className={styles.tripItems}>
                        {trips.map(trip => (
                            <Box
                                key={trip.destination}
                                className={`${styles.tripItem} ${formData.selectedTrip?.destination === trip.destination ? styles.selected : ''}`}
                                onClick={() => handleTripSelect(trip)}
                            >
                                <Typography variant="h6">{trip.destination}</Typography>
                                <Typography>You'll stay at {trip.hotel}</Typography>
                                <Typography>Flight will depart at: {trip.departure_time}</Typography>
                                <Typography>Flight will cost {trip.flight_price}$</Typography>
                            </Box>
                        ))}
                    </Box>
                    <Button
                        onClick={handleNext}
                        variant="contained"
                        color="primary"
                        className={styles.nextButton}
                        disabled={!formData.selectedTrip}
                    >
                        Next
                    </Button>
                </Box>
            )}
            {step === 2 && trips.length === 0 && (
                <Box className={styles.tripItem}>
                <Typography>No 5 trips available for the selected criteria</Typography>
                <Typography>Try reset the search for different values</Typography>
                </Box>
                    )}

            {step === 3 && formData.dailyPlan && (
                <Box className={styles.dailyPlan}>
                    <Box sx={{width: '100%', textAlign: 'center'}}>
                    <Typography variant="h4">Daily Plan for {formData.selectedTrip.destination}</Typography>
                    <Typography variant="h6">Total Expenses: ${formData.totalExpenses}</Typography>
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={handleToggleGallery}
                            sx={{ position: 'absolute', top: 0, right: 0 }}
                        >
                            {showGallery ? 'Hide Gallery' : 'Show Gallery'}
                        </Button>
                    </Box>
                        {formData.dailyPlan.length > 0 ? (
                        formData.dailyPlan.map((plan, index) => (
                            <Box key={index} className={styles.dailyPlanItem}>
                                <Typography variant="h6">{plan.date}</Typography>
                                <ul>
                                    {plan.activities.map((activity, idx) => (
                                        <li key={idx}>{activity}</li>
                                    ))}
                                </ul>
                                <Typography>Expenses: ${plan.expenses}</Typography>
                            </Box>
                        ))
                    ) : (
                        <Typography>No daily plan available</Typography>
                    )}
                    {showGallery && (
                        <Box className={styles.galleryOverlay}>
                            <ImageGallery items={images} />
                        </Box>
                    )}
                </Box>
            )}
        </Container>
    );
}

export default TripForm;
