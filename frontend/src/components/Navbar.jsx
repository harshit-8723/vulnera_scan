import React from "react";
import { Link } from "react-router-dom";
import { Box, Flex, Button, IconButton, Menu, MenuButton, MenuList, MenuItem, Heading } from "@chakra-ui/react";
import { Menu as MenuIcon, Shield } from "lucide-react";

const Navbar = () => {
    return (
        <Box as="nav" bg="blue.500" color="white" px={4} py={3} shadow="md">
            <Flex maxW="7xl" mx="auto" align="center" justify="space-between">
                <Link to="/">
                    <Flex align="center">
                        <Shield size={24} />
                        <Heading as="h1" size="md" ml={2}>SecureWatch</Heading>
                    </Flex>
                </Link>
                <Flex display={{ base: "none", md: "flex" }} align="center">
                    <Button as={Link} to="/auth" variant="ghost" colorScheme="whiteAlpha" mr={2}>Login</Button>
                    <Button as={Link} to="/auth" variant="solid" colorScheme="whiteAlpha">Sign Up</Button>
                </Flex>
                <Box display={{ base: "block", md: "none" }}>
                    <Menu>
                        <MenuButton as={IconButton} icon={<MenuIcon size={24} />} variant="outline" colorScheme="whiteAlpha" />
                        <MenuList bg="blue.500" color="white">
                            <MenuItem as={Link} to="/auth">Login</MenuItem>
                            <MenuItem as={Link} to="/auth">Sign Up</MenuItem>
                        </MenuList>
                    </Menu>
                </Box>
            </Flex>
        </Box>
    );
};

export default Navbar;