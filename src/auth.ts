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

        // Finalize admin status for Microsoft Entra ID users based on group ID
        if (account?.provider === "microsoft-entra-id" && profile) {
          const entraGroups = (profile as any).groups || [];
          const ADMIN_GROUP_ID = "f2b5c042-85d0-489b-b343-b103a4ab64dd";
          if (entraGroups.includes(ADMIN_GROUP_ID)) {
             console.log("Admin privilege granted to group member:", token.email);
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
      if (account?.provider === "microsoft-entra-id" && profile) {
        const entraProfile = profile as any;
        const ADMIN_GROUP_ID = "f2b5c042-85d0-489b-b343-b103a4ab64dd";
        const isGroupAdmin = (entraProfile.groups || []).includes(ADMIN_GROUP_ID);

        console.log("Entra ID Sign-in - User:", user.email, "isGroupAdmin:", isGroupAdmin);
        console.log("Entra profile keys:", Object.keys(entraProfile));

        // Fetch department from Graph API — it's not in the ID token
        let department = entraProfile.department || "";
        if (account?.access_token) {
          try {
            const ctrl2 = new AbortController();
            const t2 = setTimeout(() => ctrl2.abort(), 5000);
            const graphResp = await fetch(
              "https://graph.microsoft.com/v1.0/me?$select=department,jobTitle",
              { headers: { Authorization: `Bearer ${account.access_token}` }, signal: ctrl2.signal }
            );
            clearTimeout(t2);
            if (graphResp.ok) {
              const graphData = await graphResp.json();
              department = graphData.department || "";
              console.log("Graph API fetched department:", department, "jobTitle:", graphData.jobTitle);
            }
          } catch (err) {
            console.error("Graph API error in signIn:", err);
          }
        }

        (user as any).department = department;

        if (user.email) {
          try {
            await prisma.user.upsert({
              where: { email: user.email },
              update: { 
                department,
                // Auto-sync dashboard group to Entra department
                ...(department ? { dashboardGroup: department } : {}),
                ...(isGroupAdmin ? { isAdmin: true } : {})
              },
              create: {
                email: user.email,
                name: user.name,
                image: user.image,
                department,
                dashboardGroup: department || "General",
                isAdmin: isGroupAdmin,
              },
            });
            console.log("User upserted — department:", department, "dashboardGroup:", department || "General");
          } catch (error) {
            console.error("Failed to upsert user during sign in:", error);
          }
        }
      }
      return true;
    },
  },
});
