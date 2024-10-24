import { Box, Image } from "@chakra-ui/react";
import image from "../assets/START YOUR CODING JOURNEY TODAY (2).svg";

const SignUpImage = () => {
  return (
    <Box flex={"1"}>
      <Image
        src={image}
        alt="Signup Image"
        objectFit={"cover"}
        height={"100%"}
        width={"100%"}
      ></Image>
    </Box>
  );
};

export default SignUpImage;
