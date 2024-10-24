// Import necessary dependencies from axios and React
import { AxiosRequestConfig, CanceledError } from "axios";
import { useState } from "react";
// Import custom axios instance
import axiosInstance from "@/api/axios";

// Define a generic hook for adding data
const useAdd = <T, R>(endpoint: string, requestConfig?: AxiosRequestConfig) => {
   // State to store the response data
   const [data, setData] = useState<R | null>(null);
   // State to store any error messages
   const [error, setError] = useState("");
   // State to track loading status
   const [isLoading, setIsLoading] = useState(false);

   // Function to add data
   const addData = async (postData: T) => {
      // Create an AbortController to handle request cancellation
      const controller = new AbortController();

      // Set loading state to true
      setIsLoading(true);
      try {
         // Send POST request using axiosInstance
         const response = await axiosInstance.post<R>(endpoint, postData, {
            signal: controller.signal,
            ...requestConfig,
         });
         // Update the data state with the response
         setData(response.data);
         // Set loading state to false
         setIsLoading(false);
         // Return the response data
         return response.data;
      } catch (err) {
         // If the request was canceled, do nothing
         if (err instanceof CanceledError) return;
         // Set the error state
         setError(err instanceof Error ? err.message : String(err));
         // Set loading state to false
         setIsLoading(false);
         // Re-throw the error
         throw err;
      }
   };

   // Return the addData function and state variables
   return { addData, responseData: data, error, isLoading };
};

// Export the useAdd hook as the default export
export default useAdd;
