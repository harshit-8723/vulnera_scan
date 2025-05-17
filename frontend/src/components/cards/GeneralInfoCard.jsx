import { Card, CardHeader, Heading, CardBody, Text } from "@chakra-ui/react";

const GeneralInfoCard = ({ siteData }) => {
    if (!siteData) return null;

    return (
        <Card>
            <CardHeader>
                <Heading size="md">General Info</Heading>
            </CardHeader>
            <CardBody>
                <Text><b>Domain:</b> {siteData.domain || "N/A"}</Text>
                <Text><b>URL:</b> {siteData.url || "N/A"}</Text>
                <Text><b>IP:</b> {siteData.ip || "N/A"}</Text>
                <Text><b>Server:</b> {siteData.server_info?.server || "N/A"}</Text>
            </CardBody>
        </Card>
    );
};

export default GeneralInfoCard;
