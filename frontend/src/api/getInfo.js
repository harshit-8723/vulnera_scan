import axios from "axios";

const baseUrl = import.meta.env.VITE_BACKEND_URL;

export const fetchSiteInfo = async (url) => {
  const response = await axios.get(`${baseUrl}/api/get_info`, {
    params: { url },
  });
  return response.data;
};
