import { Card, CardHeader, Heading, CardBody, List, ListItem, Text } from "@chakra-ui/react";

const OpenPortsCard = ({ siteData }) => {
    if (!siteData?.open_ports?.length) return null;

    return (
        <Card>
            <CardHeader>
                <Heading size="md">Open Ports</Heading>
            </CardHeader>
            <CardBody>
                <List spacing={2}>
                    {siteData.open_ports.map(({ port, banner }, idx) => (
                        <ListItem key={idx}>
                            <Text>
                                <b>Port:</b> {port} — <b>Banner:</b> {banner}
                            </Text>
                        </ListItem>
                    ))}
                </List>
            </CardBody>
        </Card>
    );
};

export default OpenPortsCard;
