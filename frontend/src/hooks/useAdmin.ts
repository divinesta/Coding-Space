import useData from "./useData";
import { Admin } from "@/interfaces/admin";
import { AxiosRequestConfig } from "axios";

const useAdmin = (endpoint: string, requestConfig?: AxiosRequestConfig, deps?: any[]) => {
   const { data, error, isLoading, refetch } = useData<Admin[]>(endpoint, requestConfig, deps);

   return { data, error, isLoading, refetch };
};

export default useAdmin;
