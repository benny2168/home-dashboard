import Authentik from "next-auth/providers/authentik";
import type { NextAuthConfig } from "next-auth";

export const authConfig = {
  session: { strategy: "jwt" },
  trustHost: true,
  secret: process.env.AUTH_SECRET || process.env.NEXTAUTH_SECRET,
  pages: {
    signIn: "/login",
  },
  callbacks: {
    authorized({ auth, request: { nextUrl } }) {
      const isLoggedIn = !!auth?.user;
      const isAdmin = (auth?.user as any)?.isAdmin;
      const isLoginPage = nextUrl.pathname.startsWith("/login");
      const isPublicApi = nextUrl.pathname.startsWith("/api/auth");
      const isPublicAsset =
        nextUrl.pathname.startsWith("/_next") ||
        nextUrl.pathname.startsWith("/favicon.ico") ||
        nextUrl.pathname.startsWith("/uploads");

      // 🛡️ Master Exclusion Governance
      if (isLoginPage || isPublicApi || isPublicAsset) {
        if (isLoginPage && isLoggedIn) {
          // If already authenticated, manifest the dashboard manifestation layer
          return Response.redirect(new URL("/", nextUrl));
        }
        return true;
      }

      // 🔐 Global protection signal
      if (!isLoggedIn) return false;

      // 🛡️ Admin protection signal
      if (nextUrl.pathname.startsWith("/admin")) {
        const ADMIN_EMAILS = ["tech@mtcd.org", "pastor@mtcd.org", "admin@mtcd.org", "admin@local.host"];
        const email = auth?.user?.email;
        const isEmailAdmin = !!email && ADMIN_EMAILS.includes(email);
        return isAdmin || isEmailAdmin;
      }

      return true;
    },
  },
  providers: [
    Authentik({
      clientId: process.env.AUTH_AUTHENTIK_ID ?? "3j3HshFL3BRmraagBvkxLQuOBQuGIuehNp6j9rxd",
      clientSecret: process.env.AUTH_AUTHENTIK_SECRET ?? "BsHdkuYnAXjz2dxT9gER5fkRlBVtMirMN2YCOBzTVkm3fm8X5uKDejzQ99JKBxEzlmAbUP6nAzNuV3kBpFJfueMjUNrBkqavh6qVs1TdMtyxFik3iCiUmnW2N1sa17hK",
      issuer: process.env.AUTH_AUTHENTIK_ISSUER ?? "https://auth.abraham16.com/application/o/dashboard/",
      allowDangerousEmailAccountLinking: true,
      profile(profile: any) {
        return {
          id: profile.sub,
          name: profile.name || profile.preferred_username || "",
          email: profile.email || profile.preferred_username,
          image: profile.picture || null,
        };
      },
    }),
  ],
} satisfies NextAuthConfig;
