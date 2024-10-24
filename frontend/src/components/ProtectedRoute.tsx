// frontend/src/components/ProtectedRoute.tsx
import React from "react";
import { Navigate } from "react-router-dom";
import useAuthStore from "@/store/authStore";

interface ProtectedRouteProps {
   children: React.ReactElement;
   allowedRoles: string[];
}

const ProtectedRoute = ({ children, allowedRoles }: ProtectedRouteProps) => {
   const { user } = useAuthStore();

   if (!user) {
      return <Navigate to="/login" replace />;
   }

   if (!allowedRoles.includes(user.user_role)) {
      return <Navigate to="/" replace />; // Redirect to home or an unauthorized page
   }

   return children;
};

export default ProtectedRoute;
