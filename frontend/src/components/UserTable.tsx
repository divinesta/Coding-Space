import React, { useState } from "react";
import { Table, Thead, Tbody, Tr, Th, Td, Button, Icon, Flex, Avatar, Badge, Spinner, useDisclosure, Modal, ModalOverlay, ModalContent, ModalHeader, ModalFooter, ModalBody, ModalCloseButton } from "@chakra-ui/react";
import { FaTrash } from "react-icons/fa";
import { UserResponse } from "@/interfaces/User";

interface AdminTableProps {
   userResponse?: UserResponse | null;
   onRemoveUser: (id: number) => void;
   isLoading: boolean;
}

const UserTable: React.FC<AdminTableProps> = ({ userResponse, onRemoveUser, isLoading }) => {
   const { isOpen, onOpen, onClose } = useDisclosure();
   const [selectedUserId, setSelectedUserId] = useState<number | null>(null);

   const handleDeleteClick = (userId: number) => {
      setSelectedUserId(userId);
      onOpen();
   };

   const handleConfirmDelete = () => {
      if (selectedUserId !== null) {
         onRemoveUser(selectedUserId);
      }
      onClose();
   };

   // Check if users exists and has items
   const users = userResponse?.results || [];
   const hasUsers = users.length > 0;

   return (
      <>
         <Table variant="simple">
            <Thead>
               <Tr>
                  <Th>User</Th>
                  <Th>Email</Th>
                  <Th>Role</Th>
                  <Th>Action</Th>
               </Tr>
            </Thead>
            {isLoading ? (
               <Tbody>
                  <Tr>
                     <Td colSpan={4} textAlign="center">
                        <Spinner />
                     </Td>
                  </Tr>
               </Tbody>
            ) : (
               <Tbody>
                  {hasUsers ? users.map((user) => (
                     <Tr key={user.id}>
                        <Td>
                           <Flex align="center">
                              <Avatar size="sm" name={user.username} mr={2} />
                              {user.username}
                           </Flex>
                        </Td>
                        <Td>{user.email}</Td>
                        <Td>
                           <Badge colorScheme={user.user_role === "teacher" ? "purple" : "green"}>{user.user_role}</Badge>
                        </Td>
                        <Td>
                           <Button colorScheme="red" size="sm" onClick={() => handleDeleteClick(user.id)} leftIcon={<Icon as={FaTrash} />}>
                              Remove
                           </Button>
                        </Td>
                     </Tr>
                  )) : (
                     <Tr>
                        <Td colSpan={4} textAlign="center">No users found</Td>
                     </Tr>
                  )}
               </Tbody>
            )}
         </Table>

         <Modal isOpen={isOpen} onClose={onClose}>
            <ModalOverlay />
            <ModalContent>
               <ModalHeader>Confirm Delete</ModalHeader>
               <ModalCloseButton />
               <ModalBody>
                  Are you sure you want to delete this user?
               </ModalBody>
               <ModalFooter>
                  <Button colorScheme="red" mr={3} onClick={handleConfirmDelete}>
                     Yes
                  </Button>
                  <Button variant="ghost" onClick={onClose}>No</Button>
               </ModalFooter>
            </ModalContent>
         </Modal>
      </>
   );
};

export default UserTable;
