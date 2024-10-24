import { Heading, HStack, IconButton, useColorMode } from "@chakra-ui/react";
import { Link } from "react-router-dom";
import { FaMoon, FaSun } from "react-icons/fa";

const NavBar = () => {
  const { colorMode, toggleColorMode } = useColorMode();

  return (
    <HStack justifyContent={"space-between"}>
      <Link to={"/login"}>
        <Heading>LOGO</Heading>
      </Link>
      <IconButton
        color={"blue.400"}
        aria-label="Toggle Color Mode"
        icon={colorMode === "light" ? <FaMoon /> : <FaSun />} // Switch icons
        onClick={toggleColorMode}
        bg="transparent"
      />
    </HStack>
  );
};

export default NavBar;
