export const useToast = () => {
  const toast = useToastController();
  return {
    toast: ({ title, description, variant, ...rest }) => {
      toast({
        title,
        description,
        status: variant === "destructive" ? "error" : "info",
        duration: 5000,
        isClosable: true,
        ...rest,
      });
    },
  };
};
