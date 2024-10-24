import React from "react";
import { Flex, Input, Select, Button, Spinner } from "@chakra-ui/react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const schema = z.object({
   email: z.string().min(1, { message: "This field is required" }).email("Invalid email address"),
   user_role: z.string(),
});

type FormData = z.infer<typeof schema>;

interface AddUserFormProps {
   onSubmit: (data: FormData) => void;
   isLoading: boolean;
}

const AddUserForm: React.FC<AddUserFormProps> = ({ onSubmit, isLoading }) => {
   const {
      register,
      handleSubmit,
      formState: { errors },
   } = useForm<FormData>({ resolver: zodResolver(schema) });

   return (
      <form onSubmit={handleSubmit(onSubmit)}>
         <Flex gap={2}>
            <Flex width={"100%"} flexDirection={"column"}>
               <Input {...register("email")} type="email" placeholder="Email" mr={2} size="lg" />
               {errors.email && <p style={{ fontSize: "14px", color: "red" }}>{errors.email.message}</p>}
            </Flex>

            <Select {...register("user_role")} mr={2} size="lg">
               <option value="student">Student</option>
               <option value="teacher">Teacher</option>
            </Select>
            <Button colorScheme="teal" size="lg" width={"100%"} type="submit" isLoading={isLoading}>
               {isLoading ? <Spinner /> : "Add User"}
            </Button>
         </Flex>
      </form>
   );
};

export default AddUserForm;
