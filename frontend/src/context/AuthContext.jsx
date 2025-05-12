import { createContext, useContext, useState } from "react";
import { useToast } from "@chakra-ui/react";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const toast = useToast();

  const login = async (email, password) => {
    try {
      if (email === "test@example.com" && password === "password") {
        setUser({ email, name: "Test User" });
        setIsAuthenticated(true);
        toast({ title: "Login successful", status: "success" });
        return true;
      } else {
        throw new Error("Invalid credentials");
      }
    } catch (error) {
      toast({
        title: "Login failed",
        description: error.message,
        status: "error",
      });
      return false;
    }
  };

  const signup = async (email, password, name) => {
    try {
      setUser({ email, name });
      setIsAuthenticated(true);
      toast({ title: "Signup successful", status: "success" });
      return true;
    } catch (error) {
      toast({
        title: "Signup failed",
        description: error.message,
        status: "error",
      });
      return false;
    }
  };

  const logout = () => {
    setUser(null);
    setIsAuthenticated(false);
    toast({ title: "Logged out", status: "info" });
  };

  const value = { user, isAuthenticated, login, signup, logout };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => useContext(AuthContext);
