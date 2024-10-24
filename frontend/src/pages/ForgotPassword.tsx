import {
  Box,
  Button,
  FormLabel,
  Heading,
  Input,
  Text,
  VStack,
} from "@chakra-ui/react";
import React from "react";
import { Link, useNavigate } from "react-router-dom";

const ForgotPasswordForm = () => {
  const navigate = useNavigate(); // Hook for navigation

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault(); // Prevent default form submission
    // Logic to handle password reset email sending goes here
    alert("Password reset link sent to your email!"); // Placeholder alert
    navigate("/login"); // Redirect to login after submission
  };

  return (
    <Box flex={"1"} padding={5} width={600} margin={"auto"} maxWidth={600} boxShadow="md" borderRadius="lg" bg="white" _dark={{ bg: "gray.900" }}>
      <Heading color={"brand.400"} mb={"3"}>
        Forgot Password
      </Heading>

      <Text mb={5}>
        Please enter your email address below to receive a password reset link.
      </Text>

      <form onSubmit={handleSubmit}>
        <VStack alignItems={"flex-start"} spacing={3} marginBottom={3}>
          <FormLabel>Email</FormLabel>
          <Input placeholder="Email" type="email" isRequired={true} />
        </VStack>

        <Button
          colorScheme="blue"
          size={"lg"}
          width={"100%"}
          mb={4}
          type="submit"
        >
          Send Reset Link
        </Button>
      </form>

      <Text fontSize={"sm"} textAlign={"right"}>
        Remembered your password?{" "}
        <Text _hover={{ textDecor: "underline" }}>
          <Link to={"/login"}>Log In</Link>
        </Text>
      </Text>
    </Box>
  );
};

export default ForgotPasswordForm;
