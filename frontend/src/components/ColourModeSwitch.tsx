import { HStack, Switch, Text, useColorMode } from "@chakra-ui/react";

const ColourModeSwitch = () => {
   const { toggleColorMode, colorMode } = useColorMode();

   return (
      <HStack>
         <Switch colorScheme="blue" isChecked={colorMode === "dark"} onChange={toggleColorMode}>
            {" "}
         </Switch>
         <Text>Dark Mode</Text>
      </HStack>
   );
};

export default ColourModeSwitch;
