// Import necessary dependencies
import { create } from "zustand"; // Zustand library for state management
import { AuthState, User } from "@/interfaces/auth"; // Import types from auth interface
import Cookies from "js-cookie"; // Library for handling cookies

// Define the AuthStore interface extending AuthState
interface AuthStore extends AuthState {
   // Function to set user
   setUser: (user: User | null) => void;
   // Function to set tokens
   setTokens: (access: string, refresh: string) => void;
   // Function to handle login
   login: (user: User) => void;
   // Function to handle logout
   logout: () => void;
   // Loading state
   loading: boolean;
   // Function to set loading state
   setLoading: (loading: boolean) => void;
   // Function to check if user is logged in
   isLoggedIn: () => boolean;
}

// Create the auth store using Zustand
const useAuthStore = create<AuthStore>((set, get) => ({
   // Initial user state is null
   user: null,
   // Initial access token state is null
   accessToken: null,
   // Initial refresh token state is null
   refreshToken: null,
   // Initial loading state is false
   loading: false,
   // Function to update user state
   setUser: (user) => set(() => ({ user })),
   // Function to set tokens
   setTokens: (access: string, refresh: string) => {
      // Set access token in cookies
      Cookies.set("access_token", access, { secure: true, sameSite: "strict" });
      // Set refresh token in cookies
      Cookies.set("refresh_token", refresh, { secure: true, sameSite: "strict" });
      // Update token states in the store
      set({ accessToken: access, refreshToken: refresh });
   },
   // Function to set user state on login
   login: (user: User) => set({ user }),
   // Function to handle logout
   logout: () => {
      // Remove access token from cookies
      Cookies.remove("access_token");
      // Remove refresh token from cookies
      Cookies.remove("refresh_token");
      // Reset user and token states
      set({ user: null, accessToken: null, refreshToken: null });
   },
   // Function to update loading state
   setLoading: (loading) => set(() => ({ loading })),
   // Function to check if user is logged in
   isLoggedIn: () => {
      // Get current user and accessToken states
      const { user, accessToken } = get();
      // Return true if both user and accessToken exist
      return !!user && !!accessToken;
   },
}));

// Export the auth store for use in other components
export default useAuthStore;
