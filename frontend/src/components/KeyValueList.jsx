import { List, ListItem, Text } from "@chakra-ui/react";

// Helper component to display key-value pairs in list format
const KeyValueList = ({ data }) => (
  <List spacing={1}>
    {Object.entries(data).map(([key, value]) => (
      <ListItem key={key}>
        <Text as="span" fontWeight="semibold" textTransform="capitalize">
          {key.replace(/_/g, " ")}:
        </Text>{" "}
        {typeof value === "object" ? JSON.stringify(value) : value?.toString()}
      </ListItem>
    ))}
  </List>
);

export default KeyValueList;