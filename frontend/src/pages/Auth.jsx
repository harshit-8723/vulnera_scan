import React from 'react'
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";
import { Box, VStack, Heading, Tabs, TabList, Tab, TabPanels, TabPanel, FormControl, FormLabel, Input, Button, Text } from "@chakra-ui/react";
import { useToast } from "../hooks/useToast.js";

const Auth = () => {
    const [isLogin, setIsLogin] = useState(true);
    const [formData, setFormData] = useState({ email: "", password: "", name: "" });
    const { login, signup } = useAuth();
    const navigate = useNavigate();
    const { toast } = useToast();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const { email, password, name } = formData;
        try {
            if (isLogin) {
                const success = await login(email, password);
                if (success) navigate("/dashboard");
            } else {
                const success = await signup(email, password, name);
                if (success) navigate("/dashboard");
            }
        } catch (error) {
            toast({ title: "Error", description: error.message, status: "error" });
        }
    };

    return (
        <Box maxW="md" mx="auto" mt={8} p={6} bg="white" shadow="md" rounded="md">
            <Heading size="lg" textAlign="center" mb={6}>
                {isLogin ? "Login" : "Sign Up"}
            </Heading>
            <Tabs isFitted variant="enclosed" onChange={(index) => setIsLogin(index === 0)}>
                <TabList>
                    <Tab>Login</Tab>
                    <Tab>Sign Up</Tab>
                </TabList>
                <TabPanels>
                    <TabPanel>
                        <VStack as="form" onSubmit={handleSubmit} spacing={4}>
                            <FormControl>
                                <FormLabel>Email</FormLabel>
                                <Input
                                    type="email"
                                    name="email"
                                    value={formData.email}
                                    onChange={handleChange}
                                    placeholder="Enter your email"
                                />
                            </FormControl>
                            <FormControl>
                                <FormLabel>Password</FormLabel>
                                <Input
                                    type="password"
                                    name="password"
                                    value={formData.password}
                                    onChange={handleChange}
                                    placeholder="Enter your password"
                                />
                            </FormControl>
                            <Button type="submit" colorScheme="blue" w="full">
                                Login
                            </Button>
                        </VStack>
                    </TabPanel>
                    <TabPanel>
                        <VStack as="form" onSubmit={handleSubmit} spacing={4}>
                            <FormControl>
                                <FormLabel>Name</FormLabel>
                                <Input
                                    type="text"
                                    name="name"
                                    value={formData.name}
                                    onChange={handleChange}
                                    placeholder="Enter your name"
                                />
                            </FormControl>
                            <FormControl>
                                <FormLabel>Email</FormLabel>
                                <Input
                                    type="email"
                                    name="email"
                                    value={formData.email}
                                    onChange={handleChange}
                                    placeholder="Enter your email"
                                />
                            </FormControl>
                            <FormControl>
                                <FormLabel>Password</FormLabel>
                                <Input
                                    type="password"
                                    name="password"
                                    value={formData.password}
                                    onChange={handleChange}
                                    placeholder="Enter your password"
                                />
                            </FormControl>
                            <Button type="submit" colorScheme="blue" w="full">
                                Sign Up
                            </Button>
                        </VStack>
                    </TabPanel>
                </TabPanels>
            </Tabs>
            <Text mt={4} textAlign="center">
                {isLogin ? "Don't have an account?" : "Already have an account?"}
                <Button
                    variant="link"
                    colorScheme="blue"
                    ml={1}
                    onClick={() => setIsLogin(!isLogin)}
                >
                    {isLogin ? "Sign Up" : "Login"}
                </Button>
            </Text>
        </Box>
    );
};

export default Auth;