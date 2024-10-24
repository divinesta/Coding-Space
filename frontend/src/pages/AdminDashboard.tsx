// AdminDashboard.tsx
import { Box, Heading, Tab, TabList, TabPanel, TabPanels, Tabs, VStack, Button, useToast, Container, Icon, useColorModeValue, Text, HStack, useColorMode } from "@chakra-ui/react";
import BulkAddUsers from "@/components/BulkAddUsers";
import { FaUserPlus, FaFileUpload } from "react-icons/fa";
import { z } from "zod";
import UserTable from "@/components/UserTable";
import AddUserForm from "@/components/AddUserForm";
import { User, UserFormData, UserResponse } from "@/interfaces/User";
import useData from "@/hooks/useData";
import useAdd from "@/hooks/useAdd";
import { institution_id, admin_id } from "@/utils/constants";
import { MoonIcon, SunIcon } from "@chakra-ui/icons";
import EditManagerProfile from "@/components/EditManagerProfile";

const schema = z.object({
   email: z.string().min(1, { message: "This field is required" }),
   user_role: z.string(),
});

type FormData = z.infer<typeof schema>;

const AdminDashboard = () => {
   const toast = useToast();
   const { data: userResponse, error: fetchError, isLoading: isFetching, refetch } = useData<UserResponse>(`admin/${institution_id}/teacher-student-list/`);
   const { addData: addUser, isLoading: isAdding } = useAdd(`admin/create-user/`);

   const { colorMode, toggleColorMode } = useColorMode();
   const bgColor = useColorModeValue("white", "gray.800");
   const headingColor = useColorModeValue("purple.600", "purple.300");
   const tabBgColor = useColorModeValue("teal.50", "gray.700");
   const hoverBgColor = useColorModeValue("teal.100", "gray.600");

   const handleAddUser = async (data: FormData) => {
      try {
         const formDataWithIds = {
            ...data,
            institution_id: institution_id,
            admin_id: admin_id
         };
         await addUser(formDataWithIds);
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
            <HStack justifyContent="space-between" p={4}>
               <Heading size={{ base: "md", md: "lg" }} color={headingColor}>
                  Admin Dashboard
               </Heading>
               <HStack>
                  <HStack>
                     <EditManagerProfile />
                     <Button onClick={toggleColorMode} variant="outline">
                        {colorMode === "light" ? <MoonIcon /> : <SunIcon />}
                     </Button>
                  </HStack>
               </HStack>
            </HStack>
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

                        <BulkAddUsers onUploadSuccess={refetch} />

                        <UserTable userResponse={userResponse} onRemoveUser={handleRemoveUser} isLoading={isFetching} />
                     </VStack>
                  </TabPanel>
               </TabPanels>
            </Tabs>
         </Container>
      </Box>
   );
};

export default AdminDashboard;