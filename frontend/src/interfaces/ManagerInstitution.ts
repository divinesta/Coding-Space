
export interface ManagerInstitution {
   id: number;
   user: {
      id: number;
      username: string;
      email: string;
   };
   phone_number: string;
   institution: number;
}

// interface User {
//    id: number;
//    email: string;
//    username: string;
//    user_role: string;
//    institution: string;
// }

// interface Institution {
//    id: number;
//    name: string;
//    logo: string | null;
//    date_registered: string;
//    subscription_status: string;
//    subscription_end_date: string | null;
// }
