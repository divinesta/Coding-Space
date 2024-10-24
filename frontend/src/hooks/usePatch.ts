import { AxiosRequestConfig, CanceledError } from "axios";
import { useState } from "react";
import axiosInstance from "@/api/axios";

// Define a generic hook for sending PATCH requests
const usePatch = <T, R>(endpoint: string, requestConfig?: AxiosRequestConfig) => {
   // State to store the response data
   const [data, setData] = useState<R | null>(null);
   // State to store any error messages
   const [error, setError] = useState("");
   // State to track loading status
   const [isLoading, setIsLoading] = useState(false);

   // Function to send the PATCH request
   const patchData = async (patchData: T) => {
      // Create an AbortController to handle request cancellation
      const controller = new AbortController();

      setIsLoading(true);
      try {
         // Send the PATCH request using axiosInstance
         const response = await axiosInstance.patch<R>(endpoint, patchData, {
            signal: controller.signal,
            headers: {
               "Content-Type": "multipart/form-data",
            },
            ...requestConfig,
         });
         // Update the data state with the response
         setData(response.data);
         setIsLoading(false);
         return response.data;
      } catch (err) {
         // If the request was canceled, don't update state
         if (err instanceof CanceledError) return;
         // Set the error state if there was an error
         setError(err instanceof Error ? err.message : String(err));
         setIsLoading(false);
         throw err;
      }
   };

   // Return the patchData function and state variables
   return { patchData, responseData: data, error, isLoading };
};

export default usePatch;
