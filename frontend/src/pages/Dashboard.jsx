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

  // Helper component to display key-value pairs in list format
  const KeyValueList = ({ data }) => (
    <List spacing={1}>
      {Object.entries(data).map(([key, value]) => (
        <ListItem key={key}>
          <Text as="span" fontWeight="semibold" textTransform="capitalize">
            {key.replace(/_/g, " ")}:
          </Text>{" "}
          {typeof value === "object" ? JSON.stringify(value) : value?.toString()}
        </ListItem>
      ))}
    </List>
  );

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
        <Card>
          <CardHeader>
            <Text
              fontSize="sm"
              fontWeight="semibold"
              color={useColorModeValue("gray.500", "gray.400")}
            >
              Total Scans
            </Text>
          </CardHeader>
          <CardBody>
            <Text
              fontSize="2xl"
              fontWeight="bold"
              color={useColorModeValue("gray.800", "white")}
            >
              0 {/* Placeholder for scan count */}
            </Text>
          </CardBody>
        </Card>

        <Card>
          <CardHeader>
            <Text
              fontSize="sm"
              fontWeight="semibold"
              color={useColorModeValue("gray.500", "gray.400")}
            >
              Critical/High Vulnerabilities
            </Text>
          </CardHeader>
          <CardBody>
            <Text
              fontSize="2xl"
              fontWeight="bold"
              color={useColorModeValue("red.500", "red.300")}
            >
              {vulnerabilityCounts.critical + vulnerabilityCounts.high}
            </Text>
            <VStack
              spacing={1}
              align="start"
              mt={2}
              fontSize="sm"
              color={useColorModeValue("gray.600", "gray.400")}
            >
              <Text>
                <AlertTriangle size={16} color="red" /> {vulnerabilityCounts.critical}{" "}
                Critical
              </Text>
              <Text>
                <AlertCircle size={16} color="orange" /> {vulnerabilityCounts.high} High
              </Text>
            </VStack>
          </CardBody>
        </Card>

        <Card>
          <CardHeader>
            <Text
              fontSize="sm"
              fontWeight="semibold"
              color={useColorModeValue("gray.500", "gray.400")}
            >
              Medium Vulnerabilities
            </Text>
          </CardHeader>
          <CardBody>
            <Text
              fontSize="2xl"
              fontWeight="bold"
              color={useColorModeValue("yellow.500", "yellow.300")}
            >
              {vulnerabilityCounts.medium}
            </Text>
          </CardBody>
        </Card>

        <Card>
          <CardHeader>
            <Text
              fontSize="sm"
              fontWeight="semibold"
              color={useColorModeValue("gray.500", "gray.400")}
            >
              Low Vulnerabilities
            </Text>
          </CardHeader>
          <CardBody>
            <Text
              fontSize="2xl"
              fontWeight="bold"
              color={useColorModeValue("green.500", "green.300")}
            >
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
          <Card>
            <CardHeader>
              <Heading size="md">IP Info</Heading>
            </CardHeader>
            <CardBody>
              <KeyValueList data={siteData.ip_info || {}} />
            </CardBody>
          </Card>

          {/* DNS Info */}
          <Card>
            <CardHeader>
              <Heading size="md">DNS</Heading>
            </CardHeader>
            <CardBody>
              {/* Display DNS arrays nicely */}
              {siteData.dns ? (
                Object.entries(siteData.dns).map(([recordType, values]) => (
                  <Box key={recordType} mb={2}>
                    <Text fontWeight="semibold" textTransform="uppercase">
                      {recordType}
                    </Text>
                    {values.length > 0 ? (
                      <List spacing={1}>
                        {values.map((v, i) => (
                          <ListItem key={i}>{v}</ListItem>
                        ))}
                      </List>
                    ) : (
                      <Text fontStyle="italic" color="gray.500">
                        No records
                      </Text>
                    )}
                  </Box>
                ))
              ) : (
                <Text>No DNS info available</Text>
              )}
            </CardBody>
          </Card>

          {/* Server Info */}
          <Card>
            <CardHeader>
              <Heading size="md">Server Info</Heading>
            </CardHeader>
            <CardBody>
              <Text>
                <b>Status Code:</b> {siteData.server_info?.status_code || "N/A"}
              </Text>
              <Box maxH="150px" overflowY="auto" mt={2} fontSize="sm" bg="gray.50" p={2} borderRadius="md">
                <KeyValueList data={siteData.server_info?.headers || {}} />
              </Box>
            </CardBody>
          </Card>

          {/* Open Ports */}
          <Card>
            <CardHeader>
              <Heading size="md">Open Ports</Heading>
            </CardHeader>
            <CardBody>
              {siteData.open_ports && siteData.open_ports.length > 0 ? (
                <List spacing={2}>
                  {siteData.open_ports.map(({ port, banner }, idx) => (
                    <ListItem key={idx}>
                      <Text>
                        <b>Port:</b> {port} — <b>Banner:</b> {banner}
                      </Text>
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Text>No open ports detected</Text>
              )}
            </CardBody>
          </Card>

          {/* Whois */}
          <Card>
            <CardHeader>
              <Heading size="md">Whois Info</Heading>
            </CardHeader>
            <CardBody>
              <KeyValueList data={siteData.whois || {}} />
            </CardBody>
          </Card>

          {/* General Info */}
          <Card>
            <CardHeader>
              <Heading size="md">General Info</Heading>
            </CardHeader>
            <CardBody>
              <Text>
                <b>Domain:</b> {siteData.domain || "N/A"}
              </Text>
              <Text>
                <b>URL:</b> {siteData.url || "N/A"}
              </Text>
              <Text>
                <b>IP:</b> {siteData.ip || "N/A"}
              </Text>
              <Text>
                <b>Server:</b> {siteData.server_info?.server || "N/A"}
              </Text>
            </CardBody>
          </Card>
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
