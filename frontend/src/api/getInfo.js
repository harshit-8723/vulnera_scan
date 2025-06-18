import axios from "axios";

const baseUrl = import.meta.env.VITE_BACKEND_URL;

// Fetch the site for the basic information 
const fetchSiteInfo = async (url) => {
  const response = await axios.get(`${baseUrl}/api/get_info`, {
    params: { url },
  });
  return response.data;
};

// Make a GET request to the API endpoint with the URL and get the result for SQL injection on the site
const scanSQLInjection = async (url) => {
  const response = await axios.get(`${baseUrl}/api/sql_scan`, {
    params: { url },
  });
  return response.data;
};

// Make a GET request to the API endpoint with the URL and get the result for XSS injection on the site
const scanXSSInjection = async (url) => {
  const response = await axios.get(`${baseUrl}/api/xss_scan`, {
    params: { url },
  });
  return response.data;
};

// Request the AI-generated summary report of the recon scan (returns a downloadable file link or blob)
const getAISummaryReport = async (reconData) => {
  const response = await axios.post(
    `${baseUrl}/api/generate_summary`,
    reconData,
    { responseType: "blob" } // to download it as a file
  );
  return response;
};


export {
  fetchSiteInfo,
  scanSQLInjection,
  scanXSSInjection,
  getAISummaryReport
};
