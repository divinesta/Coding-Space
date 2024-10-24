import { Box, Flex, useColorModeValue } from "@chakra-ui/react";
import SignUpForm from "../components/SignUpForm";
import SignUpImage from "../components/SignUpImage";

const SignUp = () => {
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
          height={"auto"}
        >
          <SignUpForm></SignUpForm>
          <SignUpImage></SignUpImage>
        </Box>
      </Flex>
    </>
  );
};

export default SignUp;
