import { useState } from "react";
import { useForm } from "react-hook-form"
import { z } from "zod";
import { Button, Input, Flex, useToast, Spinner, Select } from "@chakra-ui/react";
import { zodResolver } from "@hookform/resolvers/zod";
import { institution_id, admin_id } from "@/utils/constants";
import useAdd from "@/hooks/useAdd";


interface User {
   id: number;
   name: string;
   email: string;
   role: "teacher" | "student";
}

const schema = z.object({
   // name: z.string().min(1, { message: "This field is required" }),
   email: z.string().min(1, { message: "This field is required" }),
   user_role: z.string(),
});

type FormData = z.infer<typeof schema>;


export const AddUserForm = ({ onSuccess }: { onSuccess: () => void}) => {
   const [newUser, setNewUser] = useState({
      name: "",
      email: "",
      role: "student" as "teacher" | "student",
   });

   const {
      register,
      handleSubmit,
      reset,
      formState: { errors },
   } = useForm<FormData>({ resolver: zodResolver(schema) });
   const { addData, isLoading: isAdding } = useAdd<FormData, any>(`/admin/create-user/`);
   const toast = useToast();

   const onSubmit = async (formData: FormData) => {
      try {
         const postData = {
            ...formData,
            institution_id: institution_id,
            admin_id: admin_id
         }
         console.log("Submitting user data: ", postData)
         const response = await addData(postData);
         console.log("Add user response: ", response);
         toast({
            title: `${newUser.role} added successfully`,
            status: "success",
            duration: 3000,
            position: "top-right",
            isClosable: true,
         });
         reset();
         onSuccess();
      } catch (error: unknown) {
         if (error instanceof Error) {
            toast({
               title: "Error adding user",
               description: error.message,
               status: "error",
               duration: 3000,
               position: "top-right",
               isClosable: true,
            });
         } else {
            toast({
               title: "Error adding user",
               description: "An unexpected error occurred",
               status: "error",
               duration: 3000,
               position: "top-right",
               isClosable: true,
            });
         }
      }
   };

   return (
      <form action="" onSubmit={handleSubmit(onSubmit)}>
         <Flex gap={2}>
            <Flex width={"100%"} flexDirection={"column"}>
               <Input {...register("email")} type="email" placeholder="Email" value={newUser.email} onChange={(e) => setNewUser({ ...newUser, email: e.target.value })} mr={2} size="lg" />
               {errors.email && <p style={{ fontSize: "14px", color: "red" }}>{errors.email.message}</p>}
            </Flex>

            <Select
               value={newUser.role}
               {...register("user_role")}
               onChange={(e) =>
                  setNewUser({
                     ...newUser,
                     role: e.target.value as "teacher" | "student",
                  })
               }
               mr={2}
               size="lg"
            >
               <option value="student">Student</option>
               <option value="teacher">Teacher</option>
            </Select>
            <Button colorScheme="teal" size="lg" width={"100%"} type="submit">
               {isAdding ? <Spinner /> : "Add User"}
            </Button>
         </Flex>
      </form>
   );
}
