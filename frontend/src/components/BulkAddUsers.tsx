import React from "react";
import {
   Button,
   Modal,
   ModalOverlay,
   ModalContent,
   ModalHeader,
   ModalCloseButton,
   ModalBody,
   ModalFooter,
   VStack,
   Box,
   FormControl,
   FormLabel,
   Input,
   Text,
   UnorderedList,
   ListItem,
   Icon,
   useDisclosure,
   useToast,
} from "@chakra-ui/react";
import { FaFileUpload } from "react-icons/fa";

interface BulkAddUsersProps {
   onUploadSuccess: () => void;
}

const BulkAddUsers: React.FC<BulkAddUsersProps> = ({ onUploadSuccess }) => {
   const { isOpen, onOpen, onClose } = useDisclosure();
   const toast = useToast();

   const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
      // Here you would handle the file upload and processing
      toast({
         title: "File uploaded",
         description: "User list has been updated",
         status: "success",
         duration: 2000,
         isClosable: true,
      });
      onUploadSuccess();
   };

   return (
      <Box>
         <Button leftIcon={<Icon as={FaFileUpload} />} colorScheme="teal" onClick={onOpen} size="lg" mb={4}>
            Bulk Import Users
         </Button>

         <Modal isOpen={isOpen} onClose={onClose} size="lg">
            <ModalOverlay />
            <ModalContent>
               <ModalHeader>Import Multiple Users</ModalHeader>
               <ModalCloseButton />

               <ModalBody>
                  <VStack align="flex-start" spacing={4}>
                     <Box border="1px" borderColor="gray.200" borderRadius="md" p={4} width="100%">
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
                     <Text fontSize="sm" color="gray.600" fontWeight="medium">
                        File Requirements:
                     </Text>
                     <UnorderedList fontSize="sm" color="gray.600" pl={4}>
                        <ListItem>Must include "email" and "user_role" column headers</ListItem>
                        <ListItem>Ensure data is correctly formatted to avoid processing errors</ListItem>
                     </UnorderedList>
                  </VStack>
               </ModalBody>

               <ModalFooter>
                  <Button colorScheme="teal" mr={3} onClick={() => document.getElementById("file-upload")?.click()}>
                     Upload File
                  </Button>
                  <Button variant="ghost" onClick={onClose}>
                     Cancel
                  </Button>
               </ModalFooter>
            </ModalContent>
         </Modal>
      </Box>
   );
};

export default BulkAddUsers;
