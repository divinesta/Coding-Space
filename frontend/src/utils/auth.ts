// Import the auth store for managing authentication state
import useAuthStore from "@/store/authStore";
// Import jwt-decode library for decoding JWT tokens
import { jwtDecode } from "jwt-decode";
// Import user and authentication interfaces
import { User, IRegister, ILogin } from "@/interfaces/auth";
// Import API functions for user authentication
import { login as loginUser, register as registerUser, refreshToken as refreshTokenUser } from "@/api/authApi";

// Function to handle user login
export const login = async (data: ILogin) => {
   try {
      // Call the loginUser function to authenticate the user
      const { access, refresh, user } = await loginUser(data);
      // Set the authenticated user and tokens in the auth store
      setAuthUser(access, refresh, user);
   } catch (error) {
      // Throw any errors that occurred during the login process
      throw error;
   }
}

// Function to handle user registration
export const register = async (data: IRegister) => {
   try {
      // Call the registerUser function to register the user
      await registerUser(data);
   } catch (error) {
      // Throw any errors that occurred during the registration process
      throw error;
   }
}

// Function to handle user logout
export const logout = () => {
   // Call the logout function from the auth store
   useAuthStore.getState().logout();
}

// Function to set the user in the auth store
export const setUser = async () => {
   // Get the current access and refresh tokens from the auth store
   const { accessToken, refreshToken } = useAuthStore.getState();

   // Check if the access token or refresh token is missing
   if (!accessToken || !refreshToken) {
      return;
   }

   // Check if the access token is expired
   if (isAccessTokenExpired(accessToken)) {
      try {
         // Attempt to refresh the token
         const response = await getRefreshToken(refreshToken);
         // Update the auth user with new tokens
         setAuthUser(response.access, response.refresh, response.user);
      } catch (error) {
         // Log any errors that occurred during the token refresh process
         console.error("Token refresh failed:", error);
         // Log the user out if the token refresh fails
         logout();
      }
   } else {
      // Decode the access token and set the user in the auth store
      const user = decodeToken(accessToken);
      useAuthStore.getState().setUser(user);
   }
};

// Function to set the authenticated user and tokens in the auth store
export const setAuthUser = (access: string, refresh: string, user: User) => {
   // Set the access and refresh tokens in the auth store
   useAuthStore.getState().setTokens(access, refresh);
   // Set the user in the auth store
   useAuthStore.getState().login(user);
};

// Function to get a new refresh token
export const getRefreshToken = async (refresh: string) => {
   // Call the refreshTokenUser function to get a new refresh token
   const response = await refreshTokenUser(refresh);
   // Return the response data
   return response.data;
}

// Function to check if the access token is expired
export const isAccessTokenExpired = (accessToken: string): boolean => {
   try {
      // Decode the access token and extract the expiration time
      const { exp } = jwtDecode<{ exp: number }>(accessToken);
      // Check if the current time is greater than or equal to the expiration time
      return Date.now() >= exp * 1000;
   } catch (error) {
      // Log any errors that occurred during the token decoding process
      console.error("Token decode error:", error);
      // Return true if there was an error decoding the token
      return true;
   }
};

// Function to decode the access token and extract user information
const decodeToken = (token: string): User => {
   // Decode the access token and extract user information
   const decoded: any = jwtDecode(token);
   // Return the user information
   return {
      id: decoded.user_id,
      email: decoded.email,
      username: decoded.username,
      user_role: decoded.user_role,
      institution: decoded.institution || null,
      teacher_id: decoded.teacher_id || null,
      student_id: decoded.student_id || null,
      admin_id: decoded.admin_id || null,
      manager_id: decoded.manager_id || null,
   };
};



