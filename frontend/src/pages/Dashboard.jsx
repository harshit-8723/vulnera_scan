import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Input, Box, Grid, Text, VStack, Heading, Card, CardHeader, CardBody, Spinner, useColorModeValue } from "@chakra-ui/react";
import { Shield, Search, AlertTriangle, AlertCircle, Info, CheckCircle } from "lucide-react";

const Dashboard = () => {
  const navigate = useNavigate();
  const [url, setUrl] = useState("");
  const [searchQuery, setSearchQuery] = useState("");

  const vulnerabilityCounts = {
    critical: 0,
    high: 0,
    medium: 0,
    low: 0,
  };

  const handleNewScan = async (e) => {
    e.preventDefault();
    if (!url) return;

    let scanUrl = url;
    if (!url.startsWith("http://") && !url.startsWith("https://")) {
      scanUrl = `https://${url}`;
    }

    // todo : Add  scan logic here ( initiate a scan and navigate to the scan page)
    try {
      console.log("Scan started for:", scanUrl);
      // Mock scan result
      navigate(`/scan/1`);
    } catch (error) {
      console.error("Scan error:", error);
    }
  };

  return (
    <Box maxW="7xl" mx="auto" px={{ base: 4, sm: 6, lg: 8 }} py={8}>
      {/* Header Section */}
      <VStack spacing={4} align="start" mb={8}>
        <Heading as="h1" size="2xl" fontWeight="bold" color={useColorModeValue("gray.800", "white")}>
          Dashboard
        </Heading>
        <Text fontSize="lg" color={useColorModeValue("gray.600", "gray.400")}>
          Welcome back, User
        </Text>
      </VStack>
      
      {/* Overview Cards */}
      <Grid templateColumns={{ base: "1fr", md: "1fr 1fr", lg: "1fr 1fr 1fr 1fr" }} gap={6} mb={8}>
        <Card>
          <CardHeader>
            <Text fontSize="sm" fontWeight="semibold" color={useColorModeValue("gray.500", "gray.400")}>
              Total Scans
            </Text>
          </CardHeader>
          <CardBody>
            <Text fontSize="2xl" fontWeight="bold" color={useColorModeValue("gray.800", "white")}>
              0 {/* Placeholder for scan count */}
            </Text>
          </CardBody>
        </Card>

        <Card>
          <CardHeader>
            <Text fontSize="sm" fontWeight="semibold" color={useColorModeValue("gray.500", "gray.400")}>
              Critical/High Vulnerabilities
            </Text>
          </CardHeader>
          <CardBody>
            <Text fontSize="2xl" fontWeight="bold" color={useColorModeValue("red.500", "red.300")}>
              {vulnerabilityCounts.critical + vulnerabilityCounts.high}
            </Text>
            <VStack spacing={1} align="start" mt={2} fontSize="sm" color={useColorModeValue("gray.600", "gray.400")}>
              <Text>
                <AlertTriangle size={16} color="red" /> {vulnerabilityCounts.critical} Critical
              </Text>
              <Text>
                <AlertCircle size={16} color="orange" /> {vulnerabilityCounts.high} High
              </Text>
            </VStack>
          </CardBody>
        </Card>

        <Card>
          <CardHeader>
            <Text fontSize="sm" fontWeight="semibold" color={useColorModeValue("gray.500", "gray.400")}>
              Medium Vulnerabilities
            </Text>
          </CardHeader>
          <CardBody>
            <Text fontSize="2xl" fontWeight="bold" color={useColorModeValue("yellow.500", "yellow.300")}>
              {vulnerabilityCounts.medium}
            </Text>
          </CardBody>
        </Card>

        <Card>
          <CardHeader>
            <Text fontSize="sm" fontWeight="semibold" color={useColorModeValue("gray.500", "gray.400")}>
              Low Vulnerabilities
            </Text>
          </CardHeader>
          <CardBody>
            <Text fontSize="2xl" fontWeight="bold" color={useColorModeValue("green.500", "green.300")}>
              {vulnerabilityCounts.low}
            </Text>
          </CardBody>
        </Card>
      </Grid>

      {/* Quick Scan Section */}
      <Card mb={8}>
        <CardHeader>
          <Heading as="h3" size="lg">
            Quick Scan
          </Heading>
        </CardHeader>
        <CardBody>
          <form onSubmit={handleNewScan}>
            <VStack spacing={4}>
              <Input
                placeholder="Enter website URL (e.g. example.com)"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                size="lg"
              />
              <Button
                type="submit"
                colorScheme="blue"
                isLoading={false} // Update when I will implement actual scanning logic
                spinner={<Spinner size="sm" />}
                isDisabled={!url}
                size="lg"
                width="full"
              >
                Scan Now
              </Button>
            </VStack>
          </form>
        </CardBody>
      </Card>

      {/* Scan History Section */}
      <Box mb={8}>
        <VStack spacing={4} align="start" mb={4}>
          <Heading as="h2" size="lg" fontWeight="bold">
            Scan History
          </Heading>
          <Box position="relative" width="100%">
            <Input
              placeholder="Search scans..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              size="lg"
              pl={10}
            />
            <Box position="absolute" top={2} left={2} pointerEvents="none">
              <Search size={20} color={useColorModeValue("gray.500", "gray.300")} />
            </Box>
          </Box>
        </VStack>
        {/* I will replace this with actual table when functionality is added */}
      </Box>
    </Box>
  );
};

export default Dashboard;
