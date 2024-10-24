import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { ChakraProvider, ColorModeScript } from "@chakra-ui/react";
import { RouterProvider } from "react-router-dom";
import router from "./routes";
import theme from "./theme";

createRoot(document.getElementById("root")!).render(
   <StrictMode>
      <ChakraProvider theme={theme}>
         <ColorModeScript initialColorMode={theme.config.initialColorMode} />
         <RouterProvider router={router}></RouterProvider>
      </ChakraProvider>
   </StrictMode>
);
