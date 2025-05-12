import React from "react";
import { Link } from "react-router-dom";
import {
  Box,
  Flex,
  Stack,
  Text,
  IconButton,
  useColorModeValue,
  Divider,
} from "@chakra-ui/react";
import { FaGithub, FaLinkedin, FaTwitter } from "react-icons/fa";

function Footer() {
  const footerLinks = [
    { name: "Privacy Policy", href: "#" },
    { name: "Terms of Service", href: "#" },
    { name: "Responsible Disclosure", href: "#" },
    { name: "Contact", href: "#" },
  ];

  const socialLinks = [
    { icon: FaGithub, label: "GitHub", href: "https://github.com" },
    { icon: FaLinkedin, label: "LinkedIn", href: "https://linkedin.com" },
    { icon: FaTwitter, label: "Twitter", href: "https://twitter.com" },
  ];

  const getCurrentYear = () => new Date().getFullYear();

  return (
    <Box
      as="footer"
      bg={useColorModeValue("blue.50", "gray.800")}
      color={useColorModeValue("gray.900", "gray.400")}
      py={1}
      px={4}
    >
      <Flex
        direction={{ base: "column", md: "row" }}
        justify="space-between"
        align="center"
        maxW="6xl"
        mx="auto"
        gap={4}
      >
        <Text fontWeight="bold" fontSize="lg" color="blue.400">
          <Link to="/">VulneraScan © {getCurrentYear()}</Link>
        </Text>

        <Stack
          direction={{ base: "column", md: "row" }}
          spacing={4}
          align="center"
        >
          {footerLinks.map((item) => (
            <Link key={item.name} to={item.href}>
              <Text
                _hover={{ color: "blue.300" }}
                transition="color 0.2s ease"
                fontSize="md"
              >
                {item.name}
              </Text>
            </Link>
          ))}
        </Stack>

        <Stack direction="row" spacing={3}>
          {socialLinks.map((link) => (
            <IconButton
              as="a"
              key={link.label}
              href={link.href}
              aria-label={link.label}
              icon={<link.icon />}
              variant="ghost"
              size="lg"
              color="gray.400"
              _hover={{ color: "blue.400" }}
            />
          ))}
        </Stack>
      </Flex>

      <Divider mt={6} borderColor="gray.700" />
      <Text textAlign="center" fontSize="md" mt={2} color="gray.500">
        Built with ❤️ by the VulneraScan Team. Secure your web, effortlessly.
      </Text>
    </Box>
  );
}

export default Footer;
