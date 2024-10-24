// Import the axios instance for making HTTP requests
import axiosInstance from "./axios";
// Import interfaces for type checking
import { IRegister, ILogin, IForgotPassword} from "@/interfaces/auth";


// Function to register a new user
export const register = async (data: IRegister) => {
   // Send a POST request to the registration endpoint
   const response = await axiosInstance.post("user/register/", data);
   // Return the response data
   return response.data;
};

// Function to log in a user
export const login = async (data: ILogin) => {
   // Send a POST request to the login endpoint
   const response = await axiosInstance.post("user/login/", data);
   // Return the response data
   return response.data;
};


// Function to initiate the forgot password process
export const forgotPassword = async (data: IForgotPassword) => {
   // Send a POST request to the forgot password endpoint with the user's email
   const response = await axiosInstance.post(`/user/forgot-password/${data.email}/`, data);
   // Return the response data
   return response.data;
};

// // Function to reset the user's password
// export const resetPassword = async (data: IResetPassword)=> {
//    // Send a POST request to the password reset endpoint
//    const response = await axiosInstance.post("/user/password-reset/", data);
//    // Return the response data
//    return response.data;
// };

// // Function to change the user's password
// export const changePassword = async (data: IChangePassword) => {
//    // Send a POST request to the password change endpoint
//    const response = await axiosInstance.post("/user/password-change/", data);
//    // Return the response data
//    return response.data;
// };

// Function to refresh the authentication token
export const refreshToken = async (refresh: string) => {
   // Send a POST request to the token refresh endpoint with the refresh token
   const response = await axiosInstance.post("/user/refresh-token/", { refresh });
   // Return the response data
   return response.data;
};
