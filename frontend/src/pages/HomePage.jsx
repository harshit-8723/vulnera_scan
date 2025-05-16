import {
    Box,
    Heading,
    Text,
    VStack,
    HStack,
    Button,
    Image,
    Flex,
    Divider,
    useColorModeValue,
    Icon,
    Spinner,
  } from "@chakra-ui/react";
  import { useNavigate } from "react-router-dom";
  import { FaChevronDown, FaChevronUp } from "react-icons/fa";
  import { useState } from "react";
  import { useAuth } from "../context/AuthContext";
  
  const HomePage = () => {
    const { user } = useAuth();
    const [openFaqIndex, setOpenFaqIndex] = useState(null);
    const navigate = useNavigate();
  
    const faqData = [
      {
        question: "What is VulneraScan?",
        answer:
          "VulneraScan is a tool designed to scan and identify security vulnerabilities in your website, helping you keep your site secure.",
      },
      {
        question: "How do I use VulneraScan?",
        answer:
          "Simply sign up, enter your website URL, and run a scan to get detailed vulnerability reports.",
      },
      {
        question: "Is VulneraScan free?",
        answer:
          "VulneraScan offers both free and premium plans, with enhanced features in the premium version.",
      },
    ];
  
    const toggleFAQ = (index) => {
      setOpenFaqIndex(openFaqIndex === index ? null : index);
    };
  
    const cardBg = useColorModeValue("white", "gray.600");
    const dividerColor = useColorModeValue("gray.300", "gray.600");
  
    return (
      <Box w="full">
        {/* Hero Section */}
        <Box w="full" bg={useColorModeValue("gray.100", "gray.700")} py={12}>
          <Flex
            direction={{ base: "column", lg: "row" }}
            maxW="7xl"
            mx="auto"
            align="center"
            justify="space-between"
            px={4}
            gap={8}
          >
            <VStack align="flex-start" spacing={6} flex={1}>
              <Heading size="2xl" color="blue.400">
                Scan Your Website for Vulnerabilities
              </Heading>
              <Text
                fontSize="lg"
                color={useColorModeValue("gray.600", "gray.300")}
              >
                VulneraScan helps identify security vulnerabilities in your website, giving you peace of mind with detailed reports.
              </Text>
              <Button
                colorScheme="blue"
                size="lg"
                onClick={() => navigate(user ? `/dashboard/${user.$id}`: "#")}
              >
                Start a Scan
              </Button>
            </VStack>
            <Box flex={1} w="full" h={{ base: "200px", md: "400px" }}>
              <Image
                src="vulnerascan-hero-image.png"
                alt="VulneraScan Hero Image"
                borderRadius="lg"
                shadow="md"
                maxW="100%"
                h="full"
                objectFit="cover"
              />
            </Box>
          </Flex>
        </Box>
  
        {/* Features Section */}
        <Box py={12} bg={useColorModeValue("gray.50", "gray.800")}>
          <Box maxW="7xl" mx="auto" px={4}>
            <Heading textAlign="center" size="lg" color="blue.400">
              Key Features
            </Heading>
            <Divider my={6} borderColor={dividerColor} />
            <Flex
              direction={{ base: "column", md: "row" }}
              justify="space-between"
              gap={8}
            >
              <Box flex={1} bg={cardBg} p={6} borderRadius="md" boxShadow="md">
                <Heading size="md" color="blue.500">
                  Comprehensive Scans
                </Heading>
                <Text mt={4}>
                  Scan your website for a wide range of security vulnerabilities, including cross-site scripting (XSS), SQL injections, and more.
                </Text>
              </Box>
              <Box flex={1} bg={cardBg} p={6} borderRadius="md" boxShadow="md">
                <Heading size="md" color="blue.500">
                  Detailed Reports
                </Heading>
                <Text mt={4}>
                  Get detailed vulnerability reports with actionable steps to help you resolve issues.
                </Text>
              </Box>
              <Box flex={1} bg={cardBg} p={6} borderRadius="md" boxShadow="md">
                <Heading size="md" color="blue.500">
                  Real-Time Updates
                </Heading>
                <Text mt={4}>
                  Receive real-time notifications on any new vulnerabilities found during scans and updates on their status.
                </Text>
              </Box>
            </Flex>
          </Box>
        </Box>
  
        {/* FAQs Section */}
        <Box bg={useColorModeValue("gray.100", "gray.700")} py={10}>
          <Box maxW="7xl" mx="auto" px={4}>
            <Heading textAlign="center" size="lg" color="blue.400">
              Frequently Asked Questions
            </Heading>
            <Divider my={6} borderColor={dividerColor} />
            <VStack spacing={4}>
              {faqData.map((faq, index) => (
                <Box
                  key={index}
                  bg={cardBg}
                  p={4}
                  w="full"
                  borderRadius="md"
                  cursor="pointer"
                  onClick={() => toggleFAQ(index)}
                  boxShadow="sm"
                  _hover={{ boxShadow: "md" }}
                >
                  <Flex justify="space-between" align="center">
                    <Text fontWeight="bold">{faq.question}</Text>
                    <Icon
                      as={openFaqIndex === index ? FaChevronUp : FaChevronDown}
                      boxSize={6}
                    />
                  </Flex>
                  {openFaqIndex === index && (
                    <Text mt={2} fontSize="sm">
                      {faq.answer}
                    </Text>
                  )}
                </Box>
              ))}
            </VStack>
          </Box>
        </Box>
      </Box>
    );
  };
  
  export default HomePage;
  