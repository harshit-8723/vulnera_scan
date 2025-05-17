import { Card, CardHeader, CardBody, Text, useColorModeValue } from "@chakra-ui/react";

export default function LowCard({ vulnerabilityCounts }) {
    return (
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
    );
}
