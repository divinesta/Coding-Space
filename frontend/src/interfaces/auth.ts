export interface User {
   id: number;
   username: string;
   email: string;
   user_role: string;
   institution: string | null;
   teacher_id: number | null;
   student_id: number | null;
   admin_id: number | null;
   manager_id: number | null;
}

export interface AuthState {
   user: User | null;
   accessToken: string | null;
   refreshToken: string | null;
}

export interface IAuthResponse {
   access: string;
   refresh: string;
   user: User;
}


export interface IRegister {
   name: string;
   manager_email: string;
   manager_contact: string;
   manager_password: string;
   manager_confirm_password: string;
}

export interface ILogin {
   email: string;
   password: string;
}

export interface IChangePassword {
   old_password: string;
   new_password: string;
}

export interface IForgotPassword {
   email: string;
}

export interface IResetPassword {
   email: string;
   password: string;
}

