// Importing the necessary hooks and functions for authentication management
import useAuthStore from "@/store/authStore";
import { useEffect } from "react";
import { setUser } from "@/utils/auth";

// Custom hook for managing user authentication state
const useAuth = () => {
   // Destructuring user, loading state, and setLoading function from the auth store
   const { user, loading, setLoading } = useAuthStore();
   
   // useEffect hook to initialize authentication when the component mounts
   useEffect(() => {
      // Asynchronous function to handle the authentication initialization process
      const initializeAuth = async () => {
         // Set loading state to true while authentication is being initialized
         setLoading(true);

         // Call the setUser function to retrieve and set the user information
         await setUser();

         // Set loading state to false after the user information has been set
         setLoading(false);
      }

      // Invoke the initializeAuth function
      initializeAuth();
   }, []);

   // Returning the user information and loading state for use in components
   return { user, loading };
};

// Exporting the useAuth hook for use in other components
export default useAuth;
