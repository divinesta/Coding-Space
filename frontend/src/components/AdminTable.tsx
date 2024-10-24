
import { Table, Thead, Tbody, Tr, Th, Td, Badge, Button, Icon, useDisclosure, Modal, ModalOverlay, ModalContent, ModalHeader, ModalFooter, ModalBody, ModalCloseButton } from "@chakra-ui/react";
import { FaTrash } from "react-icons/fa";
import { Admin } from "@/interfaces/admin";
import { useState } from "react";

type AdminTableProps = {
   admins: Admin[];
   onDelete: (adminId: number) => void;
};

export const AdminTable = ({ admins, onDelete }: AdminTableProps) => {
   const { isOpen, onOpen, onClose } = useDisclosure();
   const [selectedAdminId, setSelectedAdminId] = useState<number | null>(null);

   const handleDeleteClick = (adminId: number) => {
      setSelectedAdminId(adminId);
      onOpen();
   };

   const handleConfirmDelete = () => {
      if (selectedAdminId !== null) {
         onDelete(selectedAdminId);
      }
      onClose();
   };

   return (
      <>
         <Table variant="simple">
            <Thead>
               <Tr>
                  <Th>Admin Email</Th>
                  <Th>Status</Th>
                  <Th>Delete an Admin</Th>
               </Tr>
            </Thead>
            <Tbody>
               {admins.map((admin) => (
                  <Tr key={admin.id}>
                     <Td>{admin.user.email}</Td>
                     <Td>
                        <Badge colorScheme="green">Active</Badge>
                     </Td>
                     <Td>
                        <Button size="sm" leftIcon={<Icon as={FaTrash}/>} colorScheme="red" onClick={() => handleDeleteClick(admin.id)}>
                           Delete
                        </Button>
                     </Td>
                  </Tr>
               ))}
            </Tbody>
         </Table>

         <Modal isOpen={isOpen} onClose={onClose}>
            <ModalOverlay />
            <ModalContent>
               <ModalHeader>Confirm Delete</ModalHeader>
               <ModalCloseButton />
               <ModalBody>
                  Are you sure you want to delete this admin?
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
