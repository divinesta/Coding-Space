// AdminDashboard.tsx
import React from "react";
import { Box, Heading, Tab, TabList, TabPanel, TabPanels, Tabs, VStack, Button, useToast, Container, Icon, useColorModeValue, FormLabel, Input, FormControl, Text } from "@chakra-ui/react";
import { FaUserPlus, FaFileUpload } from "react-icons/fa";
import { z } from "zod";
import UserTable from "@/components/UserTable";
import AddUserForm from "@/components/AddUserForm";
import { User } from "@/interfaces/User";
import useData from "@/hooks/useData";
import useAdd from "@/hooks/useAdd";
import { institution_id } from "@/utils/constants";

const schema = z.object({
   email: z.string().min(1, { message: "This field is required" }),
   user_role: z.string(),
});

type FormData = z.infer<typeof schema>;

const AdminDashboard: React.FC = () => {
   const toast = useToast();
   const { data: users, error: fetchError, isLoading: isFetching, refetch } = useData<User[]>(`admin/${institution_id}/teacher-student-list/`);
   const { addData: addUser, isLoading: isAdding } = useAdd<FormData, User>(`admin/${institution_id}/teacher-student-list/`);

   const bgColor = useColorModeValue("white", "gray.800");
   const headerColor = useColorModeValue("teal.600", "teal.300");
   const tabBgColor = useColorModeValue("teal.50", "gray.700");
   const hoverBgColor = useColorModeValue("teal.100", "gray.600");

   const handleAddUser = async (data: FormData) => {
      try {
         await addUser(data);
         refetch();
         toast({
            title: `${data.user_role.charAt(0).toUpperCase() + data.user_role.slice(1)} added`,
            status: "success",
            duration: 2000,
            isClosable: true,
         });
      } catch (error) {
         toast({
            title: "Error adding user",
            description: "An unexpected error occurred",
            status: "error",
            duration: 2000,
            isClosable: true,
         });
      }
   };

   const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
      // Here you would handle the file upload and processing
      toast({
         title: "File uploaded",
         description: "User list has been updated",
         status: "success",
         duration: 2000,
         isClosable: true,
      });
   };

   const handleRemoveUser = async (id: number) => {
      // Implement user removal logic here
      // After successful removal, call refetch() to update the user list
   };

   if (fetchError) {
      return <Text>Error loading users: {fetchError}</Text>;
   }

   return (
      <Box bg={bgColor} minHeight="100vh" py={8}>
         <Container maxW="container.xl">
            <Heading mb={8} color={headerColor} fontSize="4xl" textAlign="center">
               Admin Dashboard
            </Heading>
            <Tabs variant="soft-rounded" colorScheme="teal">
               <TabList mb={8} justifyContent="center">
                  <Tab _selected={{ bg: tabBgColor }} _hover={{ bg: hoverBgColor }}>
                     <Icon as={FaUserPlus} mr={2} />
                     Manage Users
                  </Tab>
               </TabList>

               <TabPanels>
                  <TabPanel>
                     <VStack align="stretch" spacing={6}>
                        <AddUserForm onSubmit={handleAddUser} isLoading={isAdding} />

                        <Box border="1px" borderColor="gray.200" borderRadius="md" p={4}>
                           <FormControl>
                              <FormLabel htmlFor="file-upload">Upload User List</FormLabel>
                              <Button as="label" htmlFor="file-upload" colorScheme="teal" variant="outline" leftIcon={<Icon as={FaFileUpload} />} cursor="pointer" mb={2}>
                                 Choose File
                              </Button>
                              <Input id="file-upload" type="file" onChange={handleFileUpload} accept=".csv,.xlsx,.xls" display="none" />
                              <Text fontSize="sm" color="gray.500" mt={1}>
                                 Supported formats: CSV, Excel (.xlsx, .xls)
                              </Text>
                           </FormControl>
                        </Box>

                        <UserTable users={users || []} onRemoveUser={handleRemoveUser} isLoading={isFetching} />
                     </VStack>
                  </TabPanel>
               </TabPanels>
            </Tabs>
         </Container>
      </Box>
   );
};

export default AdminDashboard;