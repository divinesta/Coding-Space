import { Box, Flex, Heading, Tab, TabList, TabPanel, TabPanels, Tabs, VStack, Button, Text, useToast, Icon, useColorModeValue, HStack, useColorMode, Tooltip, Spinner } from "@chakra-ui/react";
import { FaUserPlus, FaBuilding, FaCreditCard } from "react-icons/fa";
import { MoonIcon, SunIcon } from "@chakra-ui/icons";
import useData from "@/hooks/useData";
import { ResultList } from "@/interfaces/admin";
import { institution_id } from "@/utils/constants";
import { AddAdminForm } from "@/components/AddAdminForm";
import { AdminTable } from "@/components/AdminTable";
import { deleteAdmin } from "@/utils/adminUtils";
import EditInstitutionDetail from "@/components/EditInstitutionDetail";
import { PaymentInformation } from "@/components/PaymentInformation";
import EditManagerProfile from "@/components/EditManagerProfile";


const ModularManagerDashboard = () => {
   const { data, error, isLoading, refetch } = useData<ResultList>(`/manager/${institution_id}/admins-list/`);
   console.log(data?.results);
   const { colorMode, toggleColorMode } = useColorMode();
   const toast = useToast();
   const headingColor = useColorModeValue("purple.600", "purple.300");
   const sidebarWidth = { base: "70px", md: "200px" };
   const tabBgColor = useColorModeValue("purple.50", "gray.700");

   const handleDeleteAdmin = async (adminId: number) => {
      try {
         await deleteAdmin(adminId);
         refetch();
         toast({
            title: "Admin deleted successfully",
            status: "success",
            duration: 3000,
            position: "top-right",
            isClosable: true,
         });
      } catch (error) {
         toast({
            title: "Error deleting admin",
            description: "An unexpected error occurred",
            status: "error",
            duration: 3000,
            position: "top-right",
            isClosable: true,
         });
      }
   };

   if (error) return null;
   if (isLoading) return <Spinner />;

   return (
      <Box minH="100vh">
         <Flex direction="column" h="100vh">
            <HStack justifyContent="space-between" p={4}>
               <Heading size={{ base: "md", md: "lg" }} color={headingColor}>
                  Welcome backing
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
            <Flex flex={1} overflow="hidden">
               <Tabs variant="soft-rounded" size="md" orientation="vertical" display="flex" flexDirection="row" h="100%" width="100%">
                  <VStack
                     spacing={4}
                     bg={tabBgColor}
                     height="100%"
                     p={4}
                     borderRadius="md"
                     alignItems="flex-start"
                     minW={sidebarWidth}
                     transition="min-width 0.3s ease, opacity 0.3s ease, bg 0.3s ease"
                     overflowY="auto"
                  >
                     <TabList>
                        <Tooltip label="Manage Admins" placement="right">
                           <Tab>
                              <Flex alignItems="center">
                                 <Icon as={FaUserPlus} boxSize={5} mr={3} />
                                 <Text display={{ base: "none", md: "block" }}>Manage Admins</Text>
                              </Flex>
                           </Tab>
                        </Tooltip>
                        <Tooltip label="Institution Details" placement="right">
                           <Tab>
                              <Flex alignItems="center">
                                 <Icon as={FaBuilding} boxSize={5} mr={3} />
                                 <Text display={{ base: "none", md: "block" }}>Institution Details</Text>
                              </Flex>
                           </Tab>
                        </Tooltip>
                        <Tooltip label="Payment Information" placement="right">
                           <Tab>
                              <Flex alignItems="center">
                                 <Icon as={FaCreditCard} boxSize={5} mr={3} />
                                 <Text display={{ base: "none", md: "block" }}>Payment Information</Text>
                              </Flex>
                           </Tab>
                        </Tooltip>
                     </TabList>
                  </VStack>

                  <Box
                     flex={1}
                     overflowY="auto"
                     p={4}
                     width={{
                        base: `calc(100% - ${sidebarWidth.base})`,
                        md: `calc(100% - ${sidebarWidth.md})`,
                     }}
                  >
                     <TabPanels>
                        <TabPanel>
                           <VStack align="stretch" spacing={6}>
                              <AddAdminForm onSuccess={refetch} />
                              {/* <Box>Number of admins: {data?.length}</Box> */}
                              {data && <AdminTable admins={data?.results} onDelete={handleDeleteAdmin} />}
                           </VStack>
                        </TabPanel>
                        <TabPanel>
                           <EditInstitutionDetail />
                        </TabPanel>
                        <TabPanel>
                           <PaymentInformation />
                        </TabPanel>
                     </TabPanels>
                  </Box>
               </Tabs>
            </Flex>
         </Flex>
      </Box>
   );
};

export default ModularManagerDashboard;
