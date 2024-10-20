// Import axios library for making HTTP requests
import axios from "axios";
// Import utility functions for authentication
import { isAccessTokenExpired, setAuthUser, getRefreshToken } from "@/utils/auth";
// Import the base URL for API requests
import { API_BASE_URL } from "@/utils/constants";
// Import Cookies library for handling browser cookies
import Cookies from "js-cookie";

// Create an axios instance with default configuration
const axiosInstance = axios.create({
   baseURL: API_BASE_URL,
   headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
   },
});

// Add a request interceptor to handle authentication
axiosInstance.interceptors.request.use(async (req) => {
   // Get access and refresh tokens from cookies
   const access_token = Cookies.get("access_token");
   const refresh_token = Cookies.get("refresh_token");

   // If either token is missing, proceed with the request as is
   if (!access_token || !refresh_token) {
      return req;
   }

   // Check if the access token is expired
   if (isAccessTokenExpired(access_token)) {
      try {
         // Attempt to refresh the token
         const response = await getRefreshToken(refresh_token);
         // Update the auth user with new tokens
         setAuthUser(response.access, response.refresh, response.user);
         // Set the new access token in the request headers
         req.headers.Authorization = `Bearer ${response.access}`;
      } catch (error) {
         // Handle refresh token failure (e.g., logout user)
         console.error("Token refresh failed:", error);
      }
   } else {
      // If the access token is still valid, use it in the request headers
      req.headers.Authorization = `Bearer ${access_token}`;
   }

   // Return the modified request
   return req;
});

// Export the configured axios instance
export default axiosInstance;
