export interface ResultList {
   count: number;
   results: Admin[];
}

export interface Admin {
   id: number;
   user: {
      id: number;
      email: string;
      username: string;
      user_role: string;
      institution: string;
   };
   institution: string;
   image: string;
   date: string;
}