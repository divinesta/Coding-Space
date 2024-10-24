import { Box, Flex, useColorModeValue } from "@chakra-ui/react";
import LogInForm from "../components/LogInForm";
import SignUpImage from "../components/SignUpImage";

const LogIn = () => {
  const bgColor = useColorModeValue("2xl", "dark-lg");

  return (
    <>
      <Flex height={"100vh"} alignItems={"center"} justifyContent={"center"}>
        <Box
          display={"flex"}
          borderRadius={"xl"}
          overflow={"hidden"}
          boxShadow={bgColor}
          width={"80%"}
          height={"70%"}
        >
          <LogInForm></LogInForm>
          <SignUpImage></SignUpImage>
        </Box>
      </Flex>
    </>
  );
};

export default LogIn;
