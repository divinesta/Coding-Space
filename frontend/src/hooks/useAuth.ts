// Importing the necessary hooks and functions for authentication management
import useAuthStore from "@/store/authStore"; // Import the custom auth store hook
import { useState } from "react"; // Import useState hook from React
import { login as loginAPI } from "@/api/authApi"; // Import the login API function
import { ILogin } from "@/interfaces/auth"; // Import the login interface
import { useNavigate } from "react-router-dom"; // Import useNavigate hook for routing
import { setAuthUser, setUser } from "@/utils/auth"; // Import utility functions for setting auth user

// Custom hook for managing user authentication state
const useAuth = () => {
   // Destructuring user, loading state, and setLoading function from the auth store
   const { user, loading, setLoading } = useAuthStore();
   // State for storing error messages
   const [error, setError] = useState<string | null>(null);
   // Hook for programmatic navigation
   const navigate = useNavigate();

   // Asynchronous function to handle the authentication initialization process
   const initializeAuth = async (data: ILogin) => {
      // Set loading state to true while authentication is being initialized
      setLoading(true);
      // Clear any previous errors
      setError(null);
      try {
         // Call the login API with provided data
         const response = await loginAPI(data);
         // Set authentication tokens and user info
         setAuthUser(response.access, response.refresh, response.user);
         // Store user info in the auth store
         setUser();

         // Redirect based on user role
         switch (response.user.role) {
            case "manager":
               navigate("/manager-dashboard");
               break;
            case "admin":
               navigate("/admin-dashboard");
               break;
            case "teacher":
               navigate("/teacher-dashboard");
               break;
            case "student":
               navigate("/student-dashboard");
               break;
            default:
               navigate("/"); // Fallback to home if role is not recognized
         }
      } catch (err) {
         console.error("Login failed:", err); // Log the error to console
         setError("Login failed. Please check your credentials."); // Set error message for user
      } finally {
         setLoading(false); // Set loading state to false after authentication attempt
      }
   };

   // Returning the user information, loading state, error, and initializeAuth function for use in components
   return { user, loading, error, initializeAuth };
};

// Exporting the useAuth hook for use in other components
export default useAuth;
