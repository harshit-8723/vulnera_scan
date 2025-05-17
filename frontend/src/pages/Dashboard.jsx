import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Button,
  Input,
  Box,
  Grid,
  Text,
  VStack,
  Heading,
  Card,
  CardHeader,
  CardBody,
  Spinner,
  useColorModeValue,
  SimpleGrid,
  List,
  ListItem,
} from "@chakra-ui/react";
import { Search, AlertTriangle, AlertCircle } from "lucide-react";
import { fetchSiteInfo } from "../api/getInfo.js";
import SQLInjection from "../components/SQLInjection.jsx";
import XSSInjection from "../components/XSSInjection.jsx";
import KeyValueList from "../components/KeyValueList.jsx";
import IPInfoCard from "../components/cards/IPInfoCard.jsx";
import DNSCard from "../components/cards/DNSCard.jsx";
import ServerInfoCard from "../components/cards/ServerInfoCard.jsx";
import OpenPortsCard from "../components/cards/OpenPortsCard.jsx";
import WhoisCard from "../components/cards/WhoisCard.jsx";
import GeneralInfoCard from "../components/cards/GeneralInfoCard.jsx";
import TotalScansCard from "../components/cards/TotalScansCard.jsx";
import CriticalHighCard from "../components/cards/CriticalHighCard.jsx";
import MediumCard from "../components/cards/MediumCard.jsx";
import LowCard from "../components/cards/LowCard.jsx";
// import QuickScanForm from "../components/QuickScanForm.jsx";

const Dashboard = () => {
  const navigate = useNavigate();
  const [url, setUrl] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [vulnerabilityCounts, setvulnerabilityCounts] = useState({
    critical: 0,
    high: 0,
    medium: 0,
    low: 0,
  });

  const [loading, setLoading] = useState(false);
  const [siteData, setSiteData] = useState(null);
  const [error, setError] = useState(null);

  const handleNewScan = async (e) => {
    e.preventDefault();
    if (!url) return;

    let scanUrl = url;
    if (!url.startsWith("http://") && !url.startsWith("https://")) {
      scanUrl = `https://${url}`;
    }

    setLoading(true);
    setError(null);
    setSiteData(null);

    try {
      const data = await fetchSiteInfo(scanUrl);
      setSiteData(data);
    } catch (err) {
      setError("Failed to fetch site info.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };


  return (
    <Box maxW="7xl" mx="auto" px={{ base: 4, sm: 6, lg: 8 }} py={8}>
      {/* Header Section */}
      <VStack spacing={4} align="start" mb={8}>
        <Heading
          as="h1"
          size="2xl"
          fontWeight="bold"
          color={useColorModeValue("gray.800", "white")}
        >
          Dashboard
        </Heading>
        <Text fontSize="lg" color={useColorModeValue("gray.600", "gray.400")}>
          Welcome back, User
        </Text>
      </VStack>

      {/* Overview Cards */}
      <Grid
        templateColumns={{ base: "1fr", md: "1fr 1fr", lg: "1fr 1fr 1fr 1fr" }}
        gap={6}
        mb={8}
      >
        <TotalScansCard />
        <CriticalHighCard vulnerabilityCounts={vulnerabilityCounts} />
        <MediumCard vulnerabilityCounts={vulnerabilityCounts} />
        <LowCard vulnerabilityCounts={vulnerabilityCounts} />
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
                isLoading={loading}
                spinner={<Spinner size="sm" />}
                isDisabled={!url || loading}
                size="lg"
                width="full"
              >
                Scan Now
              </Button>
            </VStack>
          </form>
        </CardBody>
      </Card>

      {/* Display site info below Quick Scan */}
      {error && (
        <Box mb={8} p={4} bg="red.100" color="red.700" borderRadius="md">
          {error}
        </Box>
      )}

      {siteData && (
        <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6} mb={8}>
          {/* IP Info */}
          <IPInfoCard siteData={siteData} />
          {/* DNS Info */}
          <DNSCard siteData={siteData} />
          {/* Server Info */}
          <ServerInfoCard siteData={siteData} />
          {/* Open Ports */}
          <OpenPortsCard siteData={siteData} />
          {/* Whois */}
          <WhoisCard siteData={siteData} />
          {/* General Info */}
          <GeneralInfoCard siteData={siteData} />
        </SimpleGrid>
      )}

      {/* section for sql in xss  */}
      <SQLInjection />
      <XSSInjection />

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
