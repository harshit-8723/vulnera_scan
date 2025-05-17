import { Card, CardHeader, Heading, CardBody, Box, Text, List, ListItem } from "@chakra-ui/react";

const DNSCard = ({ siteData }) => {
  if (!siteData?.dns) return null;

  return (
    <Card>
      <CardHeader>
        <Heading size="md">DNS</Heading>
      </CardHeader>
      <CardBody>
        {Object.entries(siteData.dns).map(([recordType, values]) => (
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
        ))}
      </CardBody>
    </Card>
  );
};

export default DNSCard;
