import {
    Container,
    Flex,
    Text,
    HStack,
    Button,
    useColorMode,
    useColorModeValue,
    Box,
} from "@chakra-ui/react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { IoMoon } from "react-icons/io5";
import { LuSun } from "react-icons/lu";
import { Shield } from "lucide-react";
import { FaSignOutAlt } from "react-icons/fa";
import { useAuth } from "../context/AuthContext";

const Navbar = () => {
    const { colorMode, toggleColorMode } = useColorMode();
    const location = useLocation();
    const navigate = useNavigate();

    // Use AuthContext to access user, session and authentication status
    const { user, sessionCookie, isAuthenticated, logout } = useAuth();

    const isActive = (path) => location.pathname === path;

    const handleSignOut = async () => {
        await logout();
        navigate("/"); // Redirect to home after logout
    };

    const navbarBg = useColorModeValue("blue.50", "gray.800");
    const navbarShadow = useColorModeValue("md", "none");

    return (
        <Box bg={navbarBg} boxShadow={navbarShadow} py={2}>
            <Container maxW={"1280px"} px={4}>
                <Flex
                    h={16}
                    alignItems={"center"}
                    justifyContent={"space-between"}
                    flexDir={{
                        base: "column",
                        sm: "row",
                    }}
                >
                    <Text
                        as="div" 
                        fontSize={{ base: "22", sm: "28" }}
                        fontWeight={"bold"}
                        textTransform={"uppercase"}
                        textAlign={"center"}
                        bgGradient={"linear(to-r, blue.500, blue.300)"}
                        bgClip={"text"}
                    >
                        <Link to={"/"}>
                            <Flex align="center" gap={2}>
                                <Shield size={22} />
                                VulneraScan
                            </Flex>
                        </Link>
                    </Text>


                    <HStack spacing={2} alignItems={"center"}>
                        {[
                            { path: "/", label: "Home", show: true },
                            { path: "/about", label: "About", show: true },
                            {
                                path: user ? `/dashboard/${user.$id}` : "#",
                                label: "Dashboard",
                                show: isAuthenticated,
                            },
                            {
                                path: "/signUp",
                                label: "Sign Up",
                                show: !isAuthenticated,
                            },
                            {
                                path: "/signIn",
                                label: "Sign In",
                                show: !isAuthenticated,
                            },
                        ].map(
                            (link) =>
                                link.show && (
                                    <Link to={link.path} key={link.path}>
                                        <Button
                                            colorScheme={isActive(link.path) ? "blue" : "gray"}
                                            variant={isActive(link.path) ? "solid" : "ghost"}
                                        >
                                            {link.label}
                                        </Button>
                                    </Link>
                                )
                        )}

                        {isAuthenticated && (
                            <Button onClick={handleSignOut} aria-label="Logout">
                                <FaSignOutAlt />
                            </Button>
                        )}

                        <Button onClick={toggleColorMode} aria-label="Toggle Color Mode">
                            {colorMode === "light" ? <IoMoon /> : <LuSun />}
                        </Button>
                    </HStack>
                </Flex>
            </Container>
        </Box>
    );
};

export default Navbar;
