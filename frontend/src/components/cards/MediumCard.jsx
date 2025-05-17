import { Card, CardHeader, CardBody, Text, useColorModeValue } from "@chakra-ui/react";

export default function MediumCard({ vulnerabilityCounts }) {
    return (
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
    );
}
