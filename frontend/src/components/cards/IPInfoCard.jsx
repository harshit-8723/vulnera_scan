import { Card, CardHeader, Heading, CardBody } from "@chakra-ui/react";
import KeyValueList from "../KeyValueList";

const IPInfoCard = ({ siteData }) => {
  if (!siteData?.ip_info) return null;

  return (
    <Card>
      <CardHeader>
        <Heading size="md">IP Info</Heading>
      </CardHeader>
      <CardBody>
        <KeyValueList data={siteData.ip_info} />
      </CardBody>
    </Card>
  );
};

export default IPInfoCard;
