// Import necessary dependencies from axios and React
import { AxiosRequestConfig, CanceledError } from "axios";
import { useEffect, useState, useCallback } from "react";
import axiosInstance from "@/api/axios";

// Define a generic type for the hook
const useData = <T>(endpoint: string, requestConfig?: AxiosRequestConfig, deps: any[] = []) => {
   // State to store the fetched data
   const [data, setData] = useState<T | null>(null);
   // State to store any error messages
   const [error, setError] = useState<string>("");
   // State to track loading status
   const [isLoading, setIsLoading] = useState<boolean>(false);

   // Function to refetch data
   const refetch = useCallback(async () => {
      setIsLoading(true);
      try {
         const response = await axiosInstance.get<T>(endpoint, requestConfig);
         setData(response.data);
         setError("");
      } catch (err) {
         setError(err instanceof Error ? err.message : String(err));
      } finally {
         setIsLoading(false);
      }
   }, [endpoint, requestConfig]);

   // Effect hook to fetch data when component mounts or dependencies change
   useEffect(() => {
      const controller = new AbortController();
      const fetchData = async () => {
         setIsLoading(true);
         try {
            const response = await axiosInstance.get<T>(endpoint, { signal: controller.signal, ...requestConfig });
            setData(response.data);
            setError("");
         } catch (err) {
            if (err instanceof CanceledError) return;
            setError(err instanceof Error ? err.message : String(err));
         } finally {
            setIsLoading(false);
         }
      };

      fetchData();

      return () => controller.abort();
   }, [endpoint, requestConfig, ...deps]);

   return { data, error, isLoading, refetch };
};

export default useData;