import { Card, CardHeader, CardBody, Text, VStack, useColorModeValue } from "@chakra-ui/react";
import { AlertTriangle, AlertCircle } from "lucide-react";

export default function CriticalHighCard({ vulnerabilityCounts }) {
    const { critical, high } = vulnerabilityCounts || {};
    return (
        <Card>
            <CardHeader>
                <Text fontSize="sm" fontWeight="semibold" color={useColorModeValue("gray.500", "gray.400")}>
                    Critical/High Vulnerabilities
                </Text>
            </CardHeader>
            <CardBody>
                <Text fontSize="2xl" fontWeight="bold" color={useColorModeValue("red.500", "red.300")}>
                    {critical + high}
                </Text>
                <VStack spacing={1} align="start" mt={2} fontSize="sm" color={useColorModeValue("gray.600", "gray.400")}>
                    <Text><AlertTriangle size={16} color="red" /> {critical} Critical</Text>
                    <Text><AlertCircle size={16} color="orange" /> {high} High</Text>
                </VStack>
            </CardBody>
        </Card>
    );
}
