import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/';

export const getData = async () => {
    try {
        const response = await axios.get(`${API_URL}example/`);
        return response.data;
    } catch (error) {
        console.error("Error fetching data", error);
        return [];
    }
};
