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
    console.log(selected_trip['airline'])
    console.log(selected_trip['departure_time'])
    console.log(selected_trip['flight_price'])
    console.log(selected_trip['hotel_price'])
    const destination = selected_trip['destination']
    const airline = selected_trip['airline']
    const departureTime = selected_trip['departure_time']
    let flightPrice = selected_trip['flight_price']
    let hotelPrice = selected_trip['hotel_price']
    // move to string
    flightPrice = flightPrice.toString()
    hotelPrice = hotelPrice.toString()

    flightPrice = flightPrice.replace('$', '')
    hotelPrice = hotelPrice.replace('$', '')
    // convert prices to floats
    flightPrice = parseFloat(flightPrice)
    hotelPrice = parseFloat(hotelPrice)
    try {
        const response = await axios.post('http://localhost:8000/daily_plan', {
            start_date: startDate,
            end_date: endDate,
            total_budget: totalBudget,
            destination: destination,
            airline: airline,
            departure_time: departureTime,
            flight_price: flightPrice,
            hotel_price: hotelPrice
        });
        return response.data;
    } catch (error) {
        console.error(error);
    }
}

export const generateImage = async (destination, startDate, endDate, dailyPlan) => {
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