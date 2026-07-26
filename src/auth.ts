import NextAuth from "next-auth";
import { PrismaAdapter } from "@auth/prisma-adapter";
import { prisma } from "@/lib/prisma";
import { authConfig } from "./auth.config";
import Credentials from "next-auth/providers/credentials";

export const { handlers, auth, signIn, signOut } = NextAuth({
  ...authConfig,
  adapter: PrismaAdapter(prisma),
  providers: [
    ...authConfig.providers,
    Credentials({
      credentials: {
        username: { label: "Username", type: "text" },
        password: { label: "Password", type: "password" }
      },
      async authorize(credentials) {
        console.log("Credentials login attempt for:", credentials?.username);
        if (credentials?.username === "admin" && credentials?.password === "admin") {
          try {
            let user = await prisma.user.findUnique({ where: { email: "admin@local.host" } });
            if (!user) {
              user = await prisma.user.create({
                data: {
                  name: "Local Admin",
                  email: "admin@local.host",
                  password: "admin", 
                  isAdmin: true,
                  department: "IT",
                }
              });
            }
            console.log("Local admin authorized successfully");
            return user;
          } catch (error) {
            console.error("Local admin authorization failed:", error);
            return null;
          }
        }
        return null;
      }
    })
  ],
  callbacks: {
    ...authConfig.callbacks,
    async jwt({ token, user, account, profile }: any) {
      if (user) {
        console.log("JWT callback - user logged in:", user.email);
        token.id = user.id;
        token.department = (user as any).department;
        token.isAdmin = (user as any).isAdmin;
        token.iconSize = (user as any).iconSize || 48;
        token.canEditContent = (user as any).canEditContent;

        // Finalize admin status for Authentik users based on groups or admin list
        if (account?.provider === "authentik" && profile) {
          const authentikGroups = (profile as any).groups || [];
          const ADMIN_GROUPS = ["authentik Admins", "Admins", "admin"];
          const isAdminGroupMember = authentikGroups.some((g: string) => ADMIN_GROUPS.includes(g));
          if (isAdminGroupMember) {
             console.log("Admin privilege granted to Authentik group member:", token.email);
             token.isAdmin = true;
          }
        }
      }
      return token;
    },
    async session({ session, token }: any) {
      if (session.user && token) {
        session.user.id = token.id;
        session.user.department = token.department;
        session.user.isAdmin = token.isAdmin;
        session.user.iconSize = token.iconSize;
        session.user.canEditContent = token.canEditContent;
        console.log("Session created for:", session.user.email, "isAdmin:", session.user.isAdmin);
      }
      return session;
    },
    async signIn({ user, account, profile }: any) {
      console.log("SignIn check for:", user.email, "Provider:", account?.provider);
      if (account?.provider === "authentik" && profile) {
        const authentikProfile = profile as any;
        const authentikGroups = authentikProfile.groups || [];
        const ADMIN_GROUPS = ["authentik Admins", "Admins", "admin"];
        const isGroupAdmin = authentikGroups.some((g: string) => ADMIN_GROUPS.includes(g));

        console.log("Authentik Sign-in - User:", user.email, "isGroupAdmin:", isGroupAdmin);

        if (user.email) {
          try {
            await prisma.user.upsert({
              where: { email: user.email },
              update: { 
                name: user.name || undefined,
                image: user.image || undefined,
                ...(isGroupAdmin ? { isAdmin: true } : {})
              },
              create: {
                email: user.email,
                name: user.name,
                image: user.image,
                department: "General",
                dashboardGroup: "General",
                isAdmin: isGroupAdmin,
              },
            });
            console.log("Authentik User upserted:", user.email);
          } catch (error) {
            console.error("Failed to upsert user during sign in:", error);
          }
        }
      }
      return true;
    },
  },
});
