import NextAuth, { DefaultSession } from "next-auth";

import NextAuth, { DefaultSession } from "next-auth";

declare module "next-auth" {
  interface Session {
    user: {
      id: string;
      department?: string | null;
      isAdmin?: boolean;
      canEditContent?: boolean;
    } & DefaultSession["user"];
  }

  interface User {
    id: string;
    department?: string | null;
    isAdmin?: boolean;
    canEditContent?: boolean;
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    id: string;
    department?: string | null;
    isAdmin?: boolean;
    canEditContent?: boolean;
  }
}
