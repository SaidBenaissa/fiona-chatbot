const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";

export const fetchData = async (endpoint, options = {}) => {
  const response = await fetch(`${API_BASE_URL}/${endpoint}`, options);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
};

// Ensure `fetchData` is exported as the default export
export default fetchData;