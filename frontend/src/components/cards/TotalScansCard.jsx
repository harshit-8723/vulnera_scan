import { Card, CardHeader, CardBody, Text, useColorModeValue } from "@chakra-ui/react";

export default function TotalScansCard() {
    return (
        <Card>
            <CardHeader>
                <Text fontSize="sm" fontWeight="semibold" color={useColorModeValue("gray.500", "gray.400")}>
                    Total Scans
                </Text>
            </CardHeader>
            <CardBody>
                <Text fontSize="2xl" fontWeight="bold" color={useColorModeValue("gray.800", "white")}>
                    0
                </Text>
            </CardBody>
        </Card>
    );
}
