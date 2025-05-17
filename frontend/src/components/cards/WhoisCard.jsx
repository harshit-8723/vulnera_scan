import { Card, CardHeader, Heading, CardBody } from "@chakra-ui/react";
import KeyValueList from "../KeyValueList";

const WhoisCard = ({ siteData }) => {
  if (!siteData?.whois) return null;

  return (
    <Card>
      <CardHeader>
        <Heading size="md">Whois Info</Heading>
      </CardHeader>
      <CardBody>
        <KeyValueList data={siteData.whois} />
      </CardBody>
    </Card>
  );
};

export default WhoisCard;
