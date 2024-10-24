// Import necessary dependencies and components
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
   Avatar,
   Box,
   Button,
   FormControl,
   FormLabel,
   Input,
   Modal,
   ModalBody,
   ModalCloseButton,
   ModalContent,
   ModalFooter,
   ModalHeader,
   ModalOverlay,
   Popover,
   PopoverArrow,
   PopoverBody,
   PopoverCloseButton,
   PopoverContent,
   PopoverHeader,
   PopoverTrigger,
   Spinner,
   Text,
   VStack,
   useColorModeValue,
   useToast,
} from "@chakra-ui/react";
import { FiLock, FiLogOut, FiEdit } from "react-icons/fi";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import useData from "@/hooks/useData";
import usePatch from "@/hooks/usePatch";
import { logout } from "@/utils/auth";
import { institution_id } from "@/utils/constants";
import { ManagerInstitution } from "@/interfaces/ManagerInstitution";

// Update the schema to match the backend structure
const schema = z.object({
   user: z.object({
      username: z.string().min(1, { message: "Username is required" }),
      email: z.string().min(1, { message: "Email is required" }).email({ message: "Invalid email address" }),
   }),
   phone_number: z
      .string()
      .min(1, { message: "Phone number is required" })
      .regex(/^\d+$/, { message: "Phone number must contain only numbers" })
      .min(11, { message: "Phone number must be 11 digits" })
      .max(11, { message: "Phone number must be 11 digits" }),
});

type FormManagerProfile = z.infer<typeof schema>;

const EditManagerProfile = () => {
   // State to control the visibility of the edit profile modal
   const [isEditProfileOpen, setIsEditProfileOpen] = useState(false);
   const toast = useToast();
   const navigate = useNavigate();
   // Fetch manager data using the useData hook
   const { data: managerData, error: fetchError, isLoading: isFetching, refetch } = useData<ManagerInstitution>(`/manager/${institution_id}/profile/`);
   // Setup patch functionality using the usePatch hook
   const { patchData, isLoading: isPatching } = usePatch<FormManagerProfile, unknown>(`/manager/${institution_id}/profile/`);

   // Setup form handling with react-hook-form
   const {
      register,
      handleSubmit,
      reset,
      formState: { errors },
   } = useForm<FormManagerProfile>({
      resolver: zodResolver(schema),
      defaultValues: managerData
         ? {
               user: {
                  username: managerData.user.username,
                  email: managerData.user.email,
               },
               phone_number: managerData.phone_number,
            }
         : undefined,
   });

   // Update the useEffect for form reset
   useEffect(() => {
      if (managerData) {
         reset({
            user: {
               username: managerData.user.username,
               email: managerData.user.email,
            },
            phone_number: managerData.phone_number,
         });
      }
   }, [managerData, reset]);

   // Handle form submission
   const onSubmit = async (data: FormManagerProfile) => {
      try {
         await patchData(data);
         setIsEditProfileOpen(false);
         refetch();
         toast({
            title: "Profile updated successfully!",
            status: "success",
            duration: 2000,
            isClosable: true,
            position: "top",
         });
      } catch (error) {
         toast({
            title: "Error updating profile",
            description: "An unexpected error occurred",
            status: "error",
            duration: 3000,
            position: "top-right",
            isClosable: true,
         });
         console.error("Update error:", error);
      }
   };

   // Open the edit profile modal
   const handleEditProfile = () => {
      setIsEditProfileOpen(true);
   };

   // Handle password change (not implemented)
   const handleChangePassword = () => {
      toast({
         title: "Password change functionality",
         description: "This feature is not implemented yet",
         status: "info",
         duration: 2000,
         isClosable: true,
         position: "top",
      });
   };

   // Handle logout
   const handleLogout = () => {
      logout();
      navigate("/login");
   };

   // Display error toast if there's an error fetching data
   useEffect(() => {
      if (fetchError) {
         toast({
            title: "Error fetching profile",
            description: fetchError,
            status: "error",
            duration: 3000,
            position: "top-right",
            isClosable: true,
         });
      }
   }, [fetchError, toast]);

   return (
      <>
         {/* Edit Profile Modal */}
         <Modal isOpen={isEditProfileOpen} onClose={() => setIsEditProfileOpen(false)} size="md">
            <ModalOverlay />
            <ModalContent>
               <form onSubmit={handleSubmit(onSubmit)}>
                  <ModalHeader>Edit Profile</ModalHeader>
                  <ModalCloseButton />
                  <ModalBody>
                     <VStack spacing={4}>
                        {/* Username Input */}
                        {isFetching ? (
                           <Spinner />
                        ) : (
                           <>
                              <FormControl isInvalid={!!errors.user?.username}>
                                 <FormLabel>Username</FormLabel>
                                 <Input {...register("user.username")} size="md" />
                                 {errors.user?.username && (
                                    <Text fontSize="sm" color="red.500">
                                       {errors.user.username.message}
                                    </Text>
                                 )}
                              </FormControl>

                              <FormControl isInvalid={!!errors.user?.email}>
                                 <FormLabel>Email</FormLabel>
                                 <Input {...register("user.email")} type="email" size="md" />
                                 {errors.user?.email && (
                                    <Text fontSize="sm" color="red.500">
                                       {errors.user.email.message}
                                    </Text>
                                 )}
                              </FormControl>

                              <FormControl isInvalid={!!errors.phone_number}>
                                 <FormLabel>Phone Number</FormLabel>
                                 <Input {...register("phone_number")} size="md" />
                                 {errors.phone_number && (
                                    <Text fontSize="sm" color="red.500">
                                       {errors.phone_number.message}
                                    </Text>
                                 )}
                              </FormControl>
                           </>
                        )}
                     </VStack>
                  </ModalBody>
                  <ModalFooter>
                     {/* Save Button */}
                     <Button colorScheme="blue" type="submit" mr={3} isLoading={isPatching} loadingText="Saving...">
                        {isPatching ? <Spinner /> : "Save"}
                     </Button>
                     {/* Cancel Button */}
                     <Button variant="ghost" onClick={() => setIsEditProfileOpen(false)}>
                        Cancel
                     </Button>
                  </ModalFooter>
               </form>
            </ModalContent>
         </Modal>

         {/* Profile Popover */}
         <Popover placement="bottom-end">
            <PopoverTrigger>
               <Button variant="outline">
                  <Avatar size="sm" name={managerData?.user.username} />
               </Button>
            </PopoverTrigger>
            <PopoverContent bg={useColorModeValue("white", "gray.800")} borderColor={useColorModeValue("gray.200", "gray.600")} boxShadow="lg" _focus={{ boxShadow: "none" }} width="250px">
               <PopoverArrow bg={useColorModeValue("white", "gray.800")} />
               <PopoverCloseButton />
               <PopoverHeader borderBottomWidth="1px" fontWeight="bold" fontSize="md" p={4}>
                  Profile
               </PopoverHeader>
               <PopoverBody p={4}>
                  <VStack align="stretch" spacing={4}>
                     {/* Display Username */}
                     <Box>
                        <Text fontSize="sm" color={useColorModeValue("gray.600", "gray.400")}>
                           Username
                        </Text>
                        <Text fontSize="md" fontWeight="medium">
                           {managerData?.user.username}
                        </Text>
                     </Box>
                     {/* Display Email */}
                     <Box>
                        <Text fontSize="sm" color={useColorModeValue("gray.600", "gray.400")}>
                           Email
                        </Text>
                        <Text fontSize="md" fontWeight="medium">
                           {managerData?.user.email}
                        </Text>
                     </Box>
                     {/* Display Phone Number */}
                     <Box>
                        <Text fontSize="sm" color={useColorModeValue("gray.600", "gray.400")}>
                           Phone Number
                        </Text>
                        <Text fontSize="md" fontWeight="medium">
                           {managerData?.phone_number}
                        </Text>
                     </Box>
                     {/* Edit Profile Button */}
                     <Button leftIcon={<FiEdit />} colorScheme="blue" size="sm" onClick={handleEditProfile} width="full">
                        Edit Profile
                     </Button>
                     {/* Change Password Button */}
                     <Button leftIcon={<FiLock />} colorScheme="blue" size="sm" onClick={handleChangePassword} width="full">
                        Change Password
                     </Button>
                     {/* Logout Button */}
                     <Button leftIcon={<FiLogOut />} colorScheme="red" size="sm" onClick={handleLogout} width="full">
                        Logout
                     </Button>
                  </VStack>
               </PopoverBody>
            </PopoverContent>
         </Popover>
      </>
   );
};

export default EditManagerProfile;
