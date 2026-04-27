import MicrosoftEntraID from "next-auth/providers/microsoft-entra-id";
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
    MicrosoftEntraID({
      clientId: process.env.AUTH_MICROSOFT_ENTRA_ID_ID ?? "missing_id",
      clientSecret: process.env.AUTH_MICROSOFT_ENTRA_ID_SECRET ?? "missing_secret",
      issuer: `https://login.microsoftonline.com/${process.env.AUTH_MICROSOFT_ENTRA_ID_TENANT_ID || "common"}/v2.0`,
      authorization: {
        params: {
          scope: "openid profile email offline_access https://graph.microsoft.com/User.Read",
          prompt: "select_account",
        },
      },
      allowDangerousEmailAccountLinking: true,
      profile(profile: any) {
        return {
          id: profile.sub,
          name: profile.displayName || profile.name || "",
          email: profile.email || profile.preferred_username,
          image: null,
          department: profile.department || "",
          isAdmin: false, // Default to false, handled in signIn/jwt callbacks
        };
      },
    }),
  ],
} satisfies NextAuthConfig;
