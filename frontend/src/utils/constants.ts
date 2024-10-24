import UserData from "@/plugin/userData";


// const userData = UserData();
// console.log(userData);


export const institution_id = (UserData() as { institution_id?: string })?.institution_id;
export const user_id = (UserData() as { user_id?: string })?.user_id;
export const admin_id = (UserData() as { admin_id?: string })?.admin_id;
export const student_id = (UserData() as { student_id?: string })?.student_id;
export const teacher_id = (UserData() as { teacher_id?: string })?.teacher_id;

export const API_BASE_URL = "http://127.0.0.1:8000/api/";
export const SERVER_URL = "http://127.0.0.1:8000/";
