import React from 'react'
import {
    Box,
    Heading,
    Text,
    VStack,
    Image,
    useColorModeValue,
} from "@chakra-ui/react";

const About = () => {
    const textColor = useColorModeValue("gray.700", "gray.300");

    return (
        <Box
            maxW="full"
            mx="auto"
            px={4}
            py={8}
            textAlign="center"
            color="white"
            borderRadius="md"
            bg={useColorModeValue("gray.100", "gray.700")}
        >
            <VStack spacing={6}>
                <Heading size="2xl" textTransform="uppercase" color={"blue.400"}>
                    About VulneraScan 🛡️
                </Heading>
                <Text fontSize="lg" color={textColor} maxW="800px">
                    VulneraScan is your go-to platform for automated website vulnerability
                    assessment. Designed for developers, security analysts, and ethical
                    hackers, VulneraScan helps you identify common security flaws with
                    ease and efficiency—before attackers do.
                </Text>
                <Image
                    src="vulnerascanImage.jpeg"
                    alt="VulneraScan Overview"
                    borderRadius="lg"
                    shadow="md"
                    maxW="40%"
                />
                <Text fontSize="lg" color={textColor} maxW="800px">
                    Our mission is to empower individuals and organizations with easy-to-use,
                    powerful scanning tools that proactively detect weaknesses in web
                    applications. VulneraScan simplifies security auditing and contributes
                    to a safer internet for everyone.
                </Text>
            </VStack>
        </Box>
    );
};

export default About;
