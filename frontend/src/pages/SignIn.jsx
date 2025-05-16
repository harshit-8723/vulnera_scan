import { useState } from "react";
import {
  Box,
  FormControl,
  FormLabel,
  Input,
  FormErrorMessage,
  Button,
  HStack,
  Spinner,
  Text,
  VStack,
  Center,
  useColorModeValue,
} from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const SignIn = () => {
  const navigate = useNavigate();
  const { login, setUser } = useAuth(); 

  // Login State
  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [loginErrors, setLoginErrors] = useState({ email: "", password: "" });
  const [isLoading, setIsLoading] = useState(false);

  const validateLoginForm = () => {
    let valid = true;
    const newErrors = { email: "", password: "" };

    if (!loginEmail) {
      newErrors.email = "Email is required";
      valid = false;
    } else if (!/\S+@\S+\.\S+/.test(loginEmail)) {
      newErrors.email = "Invalid email";
      valid = false;
    }

    if (!loginPassword) {
      newErrors.password = "Password is required";
      valid = false;
    }

    setLoginErrors(newErrors);
    return valid;
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    if (!validateLoginForm()) return;

    try {
      setIsLoading(true);
      const response = await login({
        email: loginEmail,
        password: loginPassword,
      });

      if (response?.success) {
        setUser(response); // store user info
        navigate(`/dashboard/${response.userId}`);
      } else if (response?.err) {
        alert(`Login failed: ${response.message}`);
      }
    } catch (error) {
      console.error("Login failed:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Center h="100vh" bg={useColorModeValue("gray.100", "gray.700")}>
      <Box
        as="form"
        onSubmit={handleLogin}
        w={["full", "md"]}
        p={8}
        bg={useColorModeValue("white", "gray.800")}
        boxShadow="xl"
        borderRadius="lg"
        maxW="400px"
        width="100%"
      >
        <VStack spacing={4} align="stretch">
          <Text
            fontSize="2xl"
            fontWeight="bold"
            color={useColorModeValue("blue.600", "blue.300")}
            textAlign="center"
          >
            Sign In
          </Text>

          <FormControl isInvalid={!!loginErrors.email}>
            <FormLabel>Email</FormLabel>
            <Input
              type="email"
              value={loginEmail}
              onChange={(e) => setLoginEmail(e.target.value)}
              placeholder="you@example.com"
            />
            <FormErrorMessage>{loginErrors.email}</FormErrorMessage>
          </FormControl>

          <FormControl isInvalid={!!loginErrors.password}>
            <HStack justify="space-between">
              <FormLabel>Password</FormLabel>
              <Button variant="link" size="xs" colorScheme="blue">
                Forgot password?
              </Button>
            </HStack>
            <Input
              type="password"
              value={loginPassword}
              onChange={(e) => setLoginPassword(e.target.value)}
              placeholder="••••••••"
            />
            <FormErrorMessage>{loginErrors.password}</FormErrorMessage>
          </FormControl>

          <Button
            type="submit"
            colorScheme="blue"
            width="full"
            isLoading={isLoading}
            mt={4}
            spinner={<Spinner size="sm" />}
          >
            Sign In
          </Button>
        </VStack>
      </Box>
    </Center>
  );
};

export default SignIn;
