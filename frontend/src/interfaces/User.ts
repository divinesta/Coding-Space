export interface User {
   id: number;
   name: string;
   email: string;
   role: "teacher" | "student";
}

export interface UserResponse {
   count: number;
   results: UserFormData[];
}


export interface UserFormData {
   id: number;
   username: string;
   email: string;
   user_role: "teacher" | "student";
   institution_id: number;
   admin_id: number;
}
