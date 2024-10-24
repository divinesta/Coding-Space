import axiosInstance from "@/api/axios";
import { institution_id } from "./constants";

export const deleteAdmin = async (adminId: number) => {
   try {
      await axiosInstance.delete(`/manager/${institution_id}/admin-detail/${adminId}/`);
   } catch (error) {
      console.error("Error deleting admin:", error);
      throw error;
   }
};
