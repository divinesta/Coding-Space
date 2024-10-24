import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { Button, Input, Flex, useToast, Spinner } from "@chakra-ui/react";
import useAdd from "@/hooks/useAdd";
import { institution_id } from "@/utils/constants";

const schema = z.object({
   email: z.string().email({ message: "Invalid email address" }).min(1, { message: "This field is required" }),
});

type FormData = z.infer<typeof schema>;

export const AddAdminForm = ({ onSuccess }: { onSuccess: () => void }) => {
   const {
      register,
      handleSubmit,
      reset,
      formState: { errors },
   } = useForm<FormData>({ resolver: zodResolver(schema) });
   const { addData, isLoading: isAdding } = useAdd<FormData, any>(`/manager/create-admin/`);
   const toast = useToast();

   const onSubmit = async (formData: FormData) => {
      try {
         const postData = {
            ...formData,
            institution_id: institution_id,
            user_role: "admin",
         };
         // console.log("Submitting admin data:", postData);
         const response = await addData(postData);
         console.log("Add admin response:", response);
         toast({
            title: "Admin added successfully",
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
               title: "Error adding admin",
               description: error.message,
               status: "error",
               duration: 3000,
               position: "top-right",
               isClosable: true,
            });
         } else {
            toast({
               title: "Error adding admin",
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
      <form onSubmit={handleSubmit(onSubmit)}>
         <Flex gap={2}>
            <Flex width={"100%"} flexDirection={"column"}>
               <Input placeholder="Enter admin email" type="email" {...register("email")} mr={2} size="lg" />
               {errors.email && <p style={{ fontSize: "14px", color: "red" }}>{errors.email.message}</p>}
            </Flex>
            <Button colorScheme="purple" width={"100%"} size="lg" type="submit" disabled={isAdding}>
               {isAdding ? <Spinner /> : "Add Admin"}
            </Button>
         </Flex>
      </form>
   );
};
