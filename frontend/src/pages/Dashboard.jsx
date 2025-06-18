import React, { useState } from "react";
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
} from "@chakra-ui/react";
import { fetchSiteInfo, getAISummaryReport } from "../api/getInfo.js";
import SQLInjection from "../components/SQLInjection.jsx";
import XSSInjection from "../components/XSSInjection.jsx";
import IPInfoCard from "../components/cards/IPInfoCard.jsx";
import DNSCard from "../components/cards/DNSCard.jsx";
import ServerInfoCard from "../components/cards/ServerInfoCard.jsx";
import OpenPortsCard from "../components/cards/OpenPortsCard.jsx";
import WhoisCard from "../components/cards/WhoisCard.jsx";
import GeneralInfoCard from "../components/cards/GeneralInfoCard.jsx";
import { useScanData } from "../context/ScanDataContext";

const Dashboard = () => {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const {
    reconData,
    sqlScanResult,
    xssScanResult,
    setReconData,
  } = useScanData();
  const [error, setError] = useState(null);
  const [summaryFile, setSummaryFile] = useState(null);
  const [generatingSummary, setGeneratingSummary] = useState(false);

  const handleNewScan = async (e) => {
    e.preventDefault();
    if (!url) return;

    let scanUrl = url;
    if (!url.startsWith("http://") && !url.startsWith("https://")) {
      scanUrl = `https://${url}`;
    }

    setLoading(true);
    setError(null);

    try {
      const data = await fetchSiteInfo(scanUrl);
      setReconData(data);
    } catch (err) {
      setError("Failed to fetch site info.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // this will handle the generate summary and get the summay of the scan 
  const handleGenerateSummary = async () => {
    // need all  the things then only send the response
    if (!reconData && !sqlScanResult && !xssScanResult) return;

    const fullScanReport = {
      reconData,
      sqlScanResult,
      xssScanResult,
    };

    setGeneratingSummary(true);
    try {
      const response = await getAISummaryReport(fullScanReport);

      const blob = new Blob([response.data], { type: "text/markdown" });
      const url = window.URL.createObjectURL(blob);

      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "security_summary.md");
      document.body.appendChild(link);
      link.click();
      link.remove();

    } catch (err) {
      console.error("Summary generation failed", err);
    } finally {
      setGeneratingSummary(false);
    }
  };



  return (
    <Box maxW="7xl" mx="auto" px={{ base: 4, sm: 6, lg: 8 }} py={8}>
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

      {error && (
        <Box mb={8} p={4} bg="red.100" color="red.700" borderRadius="md">
          {error}
        </Box>
      )}

      {reconData && (
        <>
          <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6} mb={8}>
            <IPInfoCard siteData={reconData} />
            <DNSCard siteData={reconData} />
            <ServerInfoCard siteData={reconData} />
            <OpenPortsCard siteData={reconData} />
            <WhoisCard siteData={reconData} />
            <GeneralInfoCard siteData={reconData} />
          </SimpleGrid>
        </>
      )}

      <SQLInjection />
      <XSSInjection />

      {(reconData && sqlScanResult && xssScanResult) && (
        <Box mb={8}>
          <VStack spacing={4} align="start">
            <Heading as="h2" size="lg">
              AI Summary Report
            </Heading>
            <Button
              colorScheme="teal"
              isLoading={generatingSummary}
              onClick={handleGenerateSummary}
              isDisabled={generatingSummary || !reconData}
            >
              Generate Summary
            </Button>
            {summaryFile && (
              <a href={summaryFile} download="security_summary.md">
                <Button variant="outline" colorScheme="green">
                  Download Summary
                </Button>
              </a>
            )}
          </VStack>
        </Box>
      )}

    </Box>
  );
};

export default Dashboard;
