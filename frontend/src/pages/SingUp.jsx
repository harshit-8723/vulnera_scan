import { useState } from "react";
import {
  Box,
  FormControl,
  FormLabel,
  Input,
  FormErrorMessage,
  Button,
  Spinner,
  VStack,
  Center,
  useColorModeValue,
  Text,
} from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";

const SignUp = () => {
  const navigate = useNavigate();
  const { signup, isLoading } = useAuth();

  // Signup State
  const [signupName, setSignupName] = useState("");
  const [signupEmail, setSignupEmail] = useState("");
  const [signupPassword, setSignupPassword] = useState("");
  const [signupConfirmPassword, setSignupConfirmPassword] = useState("");
  const [signupErrors, setSignupErrors] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const validateSignupForm = () => {
    let valid = true;
    const newErrors = { name: "", email: "", password: "", confirmPassword: "" };

    if (!signupName) {
      newErrors.name = "Name is required";
      valid = false;
    }

    if (!signupEmail) {
      newErrors.email = "Email is required";
      valid = false;
    } else if (!/\S+@\S+\.\S+/.test(signupEmail)) {
      newErrors.email = "Invalid email";
      valid = false;
    }

    if (!signupPassword) {
      newErrors.password = "Password is required";
      valid = false;
    } else if (signupPassword.length < 8) {
      newErrors.password = "Password must be at least 8 characters";
      valid = false;
    }

    if (signupPassword !== signupConfirmPassword) {
      newErrors.confirmPassword = "Passwords do not match";
      valid = false;
    }

    setSignupErrors(newErrors);
    return valid;
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    if (validateSignupForm()) {
      await signup(signupName, signupEmail, signupPassword);
      navigate("/dashboard");
    }
  };

  return (
    <Center h="100vh" bg={useColorModeValue("gray.100", "gray.700")}>
      <Box
        as="form"
        onSubmit={handleSignup}
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
            Create Account
          </Text>

          <FormControl isInvalid={!!signupErrors.name}>
            <FormLabel>Name</FormLabel>
            <Input
              value={signupName}
              onChange={(e) => setSignupName(e.target.value)}
              placeholder="John Doe"
            />
            <FormErrorMessage>{signupErrors.name}</FormErrorMessage>
          </FormControl>

          <FormControl isInvalid={!!signupErrors.email} mt={4}>
            <FormLabel>Email</FormLabel>
            <Input
              type="email"
              value={signupEmail}
              onChange={(e) => setSignupEmail(e.target.value)}
              placeholder="you@example.com"
            />
            <FormErrorMessage>{signupErrors.email}</FormErrorMessage>
          </FormControl>

          <FormControl isInvalid={!!signupErrors.password} mt={4}>
            <FormLabel>Password</FormLabel>
            <Input
              type="password"
              value={signupPassword}
              onChange={(e) => setSignupPassword(e.target.value)}
              placeholder="••••••••"
            />
            <FormErrorMessage>{signupErrors.password}</FormErrorMessage>
          </FormControl>

          <FormControl isInvalid={!!signupErrors.confirmPassword} mt={4}>
            <FormLabel>Confirm Password</FormLabel>
            <Input
              type="password"
              value={signupConfirmPassword}
              onChange={(e) => setSignupConfirmPassword(e.target.value)}
              placeholder="••••••••"
            />
            <FormErrorMessage>{signupErrors.confirmPassword}</FormErrorMessage>
          </FormControl>

          <Button
            type="submit"
            colorScheme="blue"
            width="full"
            isLoading={isLoading}
            mt={4}
            spinner={<Spinner size="sm" />}
          >
            Create Account
          </Button>
        </VStack>
      </Box>
    </Center>
  );
};

export default SignUp;
