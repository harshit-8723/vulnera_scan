import React, { useState } from "react";
import axios from "axios";
import {
    Box, Input, Button, VStack, Heading, Spinner,
    Text, List, ListItem, useColorModeValue,
} from "@chakra-ui/react";
import { scanXSSInjection } from "../api/getInfo";

const XSSInjection = () => {
    const [url, setUrl] = useState("");
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleScan = async () => {
        setLoading(true);
        setError("");
        setResults(null);

        try {
            const response = await scanXSSInjection(url);
            // console.log(response);
            setResults(response);
        } catch (err) {
            setError("Failed to scan the URL for XSS.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <Box p={6} marginBottom={8} bg={useColorModeValue("gray.50", "gray.700")} borderRadius="md">
            <Heading size="md" mb={4}>XSS Scanner</Heading>
            <VStack spacing={4}>
                <Input
                    placeholder="Enter target URL"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                />
                <Button onClick={handleScan} width={"full"} size={"lg"} colorScheme="blue" isDisabled={!url || loading}>
                    {loading ? <Spinner size="sm" /> : "Scan"}
                </Button>
                {error && <Text color="red.500">{error}</Text>}

                {results && (
                    <Box w="full" bg="whiteAlpha.100" p={4} borderRadius="md">
                        <Text fontWeight="bold">Target URL: {results.url}</Text>
                        <List spacing={3} mt={2}>
                            {results.results.map((r, idx) => (
                                <ListItem key={idx}>
                                    <Text><strong>Scanned URL:</strong> {r.url}</Text>
                                    <Text><strong>Payload:</strong> <code>{r.payload}</code></Text>
                                    <Text>
                                        <strong>Vulnerability:</strong> {r.vulnerability} —{" "}
                                        <Text as="span" fontWeight="bold" color={r.found ? "green.500" : "red.500"}>
                                            {r.found ? " Found" : " Not Found"}
                                        </Text>
                                    </Text>
                                </ListItem>
                            ))}
                        </List>
                    </Box>
                )}
            </VStack>
        </Box>
    );
};

export default XSSInjection;
