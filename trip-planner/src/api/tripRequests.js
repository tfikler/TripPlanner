import axios from 'axios';

export const getTrips = async (startDate, endDate, totalBudget, tripType) => {
    try {
        const response = await axios.post('http://localhost:8000/get_trips', {
            start_date: startDate,
            end_date: endDate,
            total_budget: totalBudget,
            trip_type: tripType
        });
        console.log(response.data)
        return response.data;
    } catch (error) {
        console.error(error);
    }
}

export const getDailyPlan = async (startDate, endDate, totalBudget, selected_trip) => {
    console.log(selected_trip['destination'])
    try {
        const response = await axios.post('http://localhost:8000/daily_plan', {
            start_date: startDate,
            end_date: endDate,
            total_budget: totalBudget,
            destination: selected_trip['destination']
        });
        console.log(response.data)
        return response.data;
    } catch (error) {
        console.error(error);
    }
}

export const generateImage = async (startDate, endDate, dailyPlan, destination) => {
    try {
        const response = await axios.post('http://localhost:8000/generate_image', {
            start_date: startDate,
            end_date: endDate,
            daily_plan: dailyPlan,
            destination: destination
        });
        console.log(response.data)
        return response.data;
    } catch (error) {
        console.error(error);
    }
}