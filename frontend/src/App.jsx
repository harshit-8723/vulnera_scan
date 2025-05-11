import React from "react";
import { Box, Button, Heading, Text } from "@chakra-ui/react";

function App() {
  return (
    <>
    <h1 className='text-5xl bg-blue-800 underline flex justify-center p-8'>Hello World!!</h1>
    <Box p={6} bg="gray.50" minH="100vh">
      <Heading mb={4}>Hello from Chakra UI</Heading>
      <Text fontSize="lg" mb={4}>
        Chakra UI is working correctly!
      </Text>
      <Button colorScheme="teal" size="lg">
        Click Me
      </Button>
    </Box>
    </>
  );
}

export default App;
