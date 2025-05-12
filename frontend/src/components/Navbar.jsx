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
import { Link, useLocation } from "react-router-dom";
import { IoMoon } from "react-icons/io5";
import { LuSun } from "react-icons/lu";
import { Shield } from "lucide-react";

const Navbar = () => {
    const { colorMode, toggleColorMode } = useColorMode();
    const location = useLocation();

    const isActive = (path) => location.pathname === path;

    // Background color and shadow for better contrast in light mode
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
                                SecureWatch
                            </Flex>
                        </Link>
                    </Text>

                    <HStack spacing={2} alignItems={"center"}>
                        {[
                            { path: "/", label: "Home" },
                            { path: "/about", label: "About" },
                            { path: "/signUp", label: "Sign Up" },
                            { path: "/signIn", label: "Sign In" },
                        ].map((link) => (
                            <Link to={link.path} key={link.path}>
                                <Button
                                    colorScheme={isActive(link.path) ? "blue" : "gray"}
                                    variant={isActive(link.path) ? "solid" : "ghost"}
                                >
                                    {link.label}
                                </Button>
                            </Link>
                        ))}

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
