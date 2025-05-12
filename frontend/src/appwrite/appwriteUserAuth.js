import { Client, Account, ID } from "appwrite";

export class AuthService {
  client = new Client();
  account;

  constructor() {
    this.client
      .setEndpoint(String(import.meta.env.VITE_APPWRITE_URL))
      .setProject(String(import.meta.env.VITE_APPWRITE_PROJECT_ID));
    this.account = new Account(this.client);
  }

  // Create account
  async createAccount({ email, password, name }) {
    try {
      const userAccount = await this.account.create(
        ID.unique(),
        email,
        password,
        name
      );
      return userAccount;
    } catch (error) {
      console.log("Appwrite service :: createAccount :: error ", error);
      return { err: error, message: error };
    }
  }

  // Login user and create session
  async login({ email, password }) {
    try {
      const session = await this.account.createEmailPasswordSession(
        email,
        password
      );
      return session;
    } catch (error) {
      console.log("Appwrite service :: login :: error ", error);
      return { err: error, message: error };
    }
  }

  // Logout the user
  async logout() {
    try {
      await this.account.deleteSessions(); // Delete all sessions to logout
    } catch (error) {
      console.log("Appwrite service :: logout :: error ", error);
      return { err: error, message: error };
    }
  }

  // Get current user info
  async getCurrentUser() {
    try {
      const user = await this.account.get(); // Fetch logged-in user
      return user;
    } catch (error) {
      console.log("Appwrite service :: getCurrentUser :: error", error);
      return { err: error, message: error };
    }
  }

  // Check if the user is logged in (session exists)
  async isLoggedIn() {
    try {
      const session = await this.account.getSession(); // Get the current session
      return session;
    } catch (error) {
      console.log(error);
      return null; // No session (user not logged in)
    }
  }
}

const service = new AuthService();
export default service;
