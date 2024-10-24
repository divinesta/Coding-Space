import { Box, Button, FormLabel, Heading, Input, Icon, InputGroup, InputRightElement, Text, VStack, Spinner } from "@chakra-ui/react";
import { zodResolver } from "@hookform/resolvers/zod/dist/zod.js";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { z } from "zod";
import { register as registerInstitution } from "@/api/authApi";

import { useForm } from "react-hook-form";
import { FaUserGraduate } from "react-icons/fa";

const schema = z
   .object({
      name: z.string().min(1, { message: "Institution name is required" }),
      manager_email: z.string().email({ message: "Invalid email address" }),
      manager_contact: z.string().min(1, { message: "Manager contact is required" }),
      manager_password: z.string().min(8, { message: "Password must be at least 8 characters" }),
      manager_confirm_password: z.string().min(8, { message: "Please confirm your password" }),
   })
   .refine((data) => data.manager_password === data.manager_confirm_password, {
      path: ["manager_confirm_password"],
      message: "Passwords do not match",
   });

type FormData = z.infer<typeof schema>;


const SignUpForm = () => {
   const {
      register,
      handleSubmit,
      reset,
      setError,
      formState: { errors, isValid },
   } = useForm<FormData>({ resolver: zodResolver(schema), mode: "onChange" });

   const [loading, setLoading] = useState(false);
   const [show, setShow] = useState(false);
   const handleClick = () => setShow(!show);

   const navigate = useNavigate();

   const onSubmit = async (data: FormData) => {
      try {
         setLoading(true);
         await registerInstitution(data);
         reset();
         navigate("/login");
      } catch (error: any) {
         if (error.response && error.response.data) {
            const serverErrors = error.response.data;
            Object.keys(serverErrors).forEach((key) => {
               setError(key as keyof FormData, {
                  type: "server",
                  message: serverErrors[key].join(", "),
               });
            });
         } else {
            console.log(error);
         }
      } finally {
         setLoading(false);
      }
   };

   return (
      <Box flex={"1"} padding={5}>
         <Heading color={"brand.400"} mb={"1.5"}>
            Register Your Institution
         </Heading>
         <form onSubmit={handleSubmit(onSubmit)}>
            <VStack alignItems={"flex-start"} spacing={2} width={"100%"}>
               <FormLabel fontSize={"sm"}>Institution Name</FormLabel>
               <Input {...register("name")} id="name" placeholder="Institution name" width={"100%"} />
               {errors.name && (
                  <Text fontSize="11px" color="red" fontWeight={"bold"}>
                     {errors.name.message}
                  </Text>
               )}

               <FormLabel fontSize={"sm"}>Manager Email</FormLabel>
               <Input {...register("manager_email")} id="manager_email" type="email" placeholder="Manager email" width={"100%"} />
               {errors.manager_email && (
                  <Text fontSize="11px" color="red" fontWeight={"bold"}>
                     {errors.manager_email.message}
                  </Text>
               )}

               <FormLabel fontSize={"sm"}>Manager Contact</FormLabel>
               <Input {...register("manager_contact")} id="manager_contact" placeholder="Manager contact" width={"100%"} />
               {errors.manager_contact && (
                  <Text fontSize="11px" color="red" fontWeight={"bold"}>
                     {errors.manager_contact.message}
                  </Text>
               )}

               <FormLabel fontSize={"sm"}>Password</FormLabel>
               <InputGroup size="md">
                  <Input {...register("manager_password")} id="manager_password" pr="4.5rem" type={show ? "text" : "password"} placeholder="Enter password" />
                  <InputRightElement width="4.5rem">
                     <Button h="1.75rem" size="sm" onClick={handleClick}>
                        {show ? "Hide" : "Show"}
                     </Button>
                  </InputRightElement>
               </InputGroup>
               {errors.manager_password && (
                  <Text fontSize="11px" color="red" fontWeight={"bold"}>
                     {errors.manager_password.message}
                  </Text>
               )}

               <FormLabel fontSize={"sm"}>Confirm Password</FormLabel>
               <InputGroup size="md">
                  <Input {...register("manager_confirm_password")} id="manager_confirm_password" pr="4.5rem" type={show ? "text" : "password"} placeholder="Confirm password" />
                  <InputRightElement width="4.5rem">
                     <Button h="1.75rem" size="sm" onClick={handleClick}>
                        {show ? "Hide" : "Show"}
                     </Button>
                  </InputRightElement>
               </InputGroup>
               {errors.manager_confirm_password && (
                  <Text fontSize="11px" color="red" fontWeight={"bold"}>
                     {errors.manager_confirm_password.message}
                  </Text>
               )}
            </VStack>

            <Button 
               colorScheme="blue" 
               size={"lg"} 
               width={"100%"} 
               mt={6} 
               mb={2} 
               type="submit" 
               leftIcon={<Icon as={FaUserGraduate} />}
               isDisabled={!isValid || loading}
            >
               {loading ? <Spinner /> : "Register Institution"}
            </Button>
         </form>
         <Text fontSize={"sm"}>
            Already have an account?{" "}
            <Text as="span" _hover={{ textDecor: "underline" }}>
               <Link to={"/login"} className="text-blue-700 hover:text-blue-700">
                  Log in
               </Link>
            </Text>
         </Text>
      </Box>
   );
};

export default SignUpForm;
