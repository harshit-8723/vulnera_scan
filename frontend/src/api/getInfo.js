import axios from "axios";

const baseUrl = import.meta.env.VITE_BACKEND_URL;

// fetch the site for the basic information 
const fetchSiteInfo = async (url) => {
  const response = await axios.get(`${baseUrl}/api/get_info`, {
    params: { url },
  });
  return response.data;
};

// make a get request to the api endpoint with the url and get the result for sql injection on the site
const scanSQLInjection = async (url) => {
  const response = await axios.get(`${baseUrl}/api/sql_scan`, {
    params: { url },
  });
  return response.data;
};

// make a get request to the api endpoint with the url and get the result for xss injection on the site
const scanXSSInjection = async (url) => {
  const response = await axios.get(`${baseUrl}/api/xss_scan`, {
    params: { url },
  });
  return response.data;
};


export {fetchSiteInfo, scanSQLInjection, scanXSSInjection }
