import { createContext, useContext, useEffect, useState } from "react";
import { useToast } from "@chakra-ui/react";
import service from "../appwrite/appwriteUserAuth";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [sessionCookie, setSessionCookie] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const toast = useToast();

  const login = async ({ email, password }) => {
    try {
      const session = await service.login({ email, password });
      if (session?.$id) {
        const userData = await service.getCurrentUser();
        setUser(userData);
        setSessionCookie(session);
        setIsAuthenticated(true);
        toast({ title: "Login successful", status: "success" });
        return { success: true };
      } else {
        throw new Error(session?.message || "Login failed");
      }
    } catch (err) {
      toast({ title: "Login failed", description: err.message, status: "error" });
      return { success: false, error: err.message, userId: session.$id};
    }
  };

  const signup = async ({ name, email, password }) => {
    try {
      const account = await service.createAccount({ name, email, password });
      if (account?.$id) {
        await login({ email, password }); // Automatically log in
        return { success: true };
      } else {
        throw new Error(account?.message || "Signup failed");
      }
    } catch (err) {
      toast({ title: "Signup failed", description: err.message, status: "error" });
      return { success: false, error: err.message, userId: account.$id};
    }
  };

  const logout = async () => {
    try {
      await service.logout();
    } catch (e) {
      console.error("Logout failed", e);
    }
    setUser(null);
    setSessionCookie(null);
    setIsAuthenticated(false);
    toast({ title: "Logged out", status: "info" });
  };

  const getUserSession = async () => {
    try {
      const currentSession = await service.getSession();
      if (currentSession) {
        const userData = await service.getCurrentUser();
        setUser(userData);
        setSessionCookie(currentSession);
        setIsAuthenticated(true);
      }
    } catch (err) {
      console.error("Session error:", err);
    }
  };

  useEffect(() => {
    getUserSession();
  }, []);

  return (
    <AuthContext.Provider value={{ user, sessionCookie, isAuthenticated, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
