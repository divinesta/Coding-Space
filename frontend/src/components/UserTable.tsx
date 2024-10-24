import React from "react";
import { Table, Thead, Tbody, Tr, Th, Td, Button, Icon, Flex, Avatar, Badge, Spinner } from "@chakra-ui/react";
import { FaTrash } from "react-icons/fa";

interface User {
   id: number;
   name: string;
   email: string;
   role: "teacher" | "student";
}

interface AdminTableProps {
   users: User[];
   onRemoveUser: (id: number) => void;
   isLoading: boolean;
}

const UserTable: React.FC<AdminTableProps> = ({ users, onRemoveUser, isLoading }) => {
   return (
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
               {users.map((user) => (
                  <Tr key={user.id}>
                  <Td>
                     <Flex align="center">
                        <Avatar size="sm" name={user.name} mr={2} />
                        {user.name}
                     </Flex>
                  </Td>
                  <Td>{user.email}</Td>
                  <Td>
                     <Badge colorScheme={user.role === "teacher" ? "purple" : "green"}>{user.role}</Badge>
                  </Td>
                  <Td>
                     <Button colorScheme="red" size="sm" onClick={() => onRemoveUser(user.id)} leftIcon={<Icon as={FaTrash} />}>
                        Remove
                     </Button>
                  </Td>
               </Tr>
            ))}
            </Tbody>
         )}
      </Table>
   );
};

export default UserTable;
