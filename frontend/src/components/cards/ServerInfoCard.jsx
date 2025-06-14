import {
  Card,
  CardHeader,
  Heading,
  CardBody,
  Text,
  Box,
  useColorModeValue,
} from "@chakra-ui/react";
import KeyValueList from "../KeyValueList";

const ServerInfoCard = ({ siteData }) => {
  if (!siteData?.server_info) return null;

  const boxBg = useColorModeValue("gray.50", "gray.90");
  const textColor = useColorModeValue("black", "white");
  const borderColor = useColorModeValue("gray.300", "gray.600");

  return (
    <Card>
      <CardHeader>
        <Heading size="md">Server Info</Heading>
      </CardHeader>
      <CardBody>
        <Text mb={2}>
          <b>Status Code:</b> {siteData.server_info.status_code || "N/A"}
        </Text>
        <Box
          maxH="300px"
          overflowY="auto"
          bg={boxBg}
          color={textColor}
          p={4} 
          border="1px solid"
          borderColor={borderColor}
          borderRadius="md"
        >
          <KeyValueList data={siteData.server_info.headers || {}} />
        </Box>
      </CardBody>
    </Card>
  );
};

export default ServerInfoCard;
