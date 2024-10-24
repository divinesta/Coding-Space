import { createBrowserRouter } from "react-router-dom"

import HomePage from "./pages/HomePage"
import LogIn from "./pages/LogInPage";
import SignUp from "./pages/SignUpPage";
import ForgotPasswordForm from "./pages/ForgotPassword";
import ProtectedRoute from "./components/ProtectedRoute";

import ManagerDashboard from "./pages/ManagerDashboard";
import AdminDashboard from "./pages/AdminDashboard";
// import TeacherDashboard from "./pages/TeacherDashboard";
// import StudentDashboard from "./pages/StudentDashboard";


const router = createBrowserRouter([
   { path: "/", element: <HomePage /> },
   { path: "/login", element: <LogIn /> },
   { path: "/signup", element: <SignUp /> },
   { path: "/forgot-password", element: <ForgotPasswordForm /> },

   {
      path: "/manager-dashboard",
      element: (
         <ProtectedRoute allowedRoles={["manager"]}>
            <ManagerDashboard />
         </ProtectedRoute>
      ),
   },
   {
      path: "/admin-dashboard",
      element: (
         <ProtectedRoute allowedRoles={["admin"]}>
            <AdminDashboard />
         </ProtectedRoute>
      ),
   },
   // {
   //    path: "/teacher-dashboard",
   //    element: (
   //       <ProtectedRoute allowedRoles={["teacher"]}>
   //          <TeacherDashboard />
   //       </ProtectedRoute>
   //    ),
   // },
   // {
   //    path: "/student-dashboard",
   //    element: (
   //       <ProtectedRoute allowedRoles={["student"]}>
   //          <StudentDashboard />
   //       </ProtectedRoute>
   //    ),
   // },
]);

export default router;