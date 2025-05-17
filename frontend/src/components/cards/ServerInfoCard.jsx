import { Card, CardHeader, Heading, CardBody, Text, Box } from "@chakra-ui/react";
import KeyValueList from "../KeyValueList";

const ServerInfoCard = ({ siteData }) => {
  if (!siteData?.server_info) return null;

  return (
    <Card>
      <CardHeader>
        <Heading size="md">Server Info</Heading>
      </CardHeader>
      <CardBody>
        <Text>
          <b>Status Code:</b> {siteData.server_info.status_code || "N/A"}
        </Text>
        <Box maxH="150px" overflowY="auto" mt={2} fontSize="sm" bg="gray.50" p={2} borderRadius="md">
          <KeyValueList data={siteData.server_info.headers || {}} />
        </Box>
      </CardBody>
    </Card>
  );
};

export default ServerInfoCard;
