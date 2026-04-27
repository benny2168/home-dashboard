const { PrismaClient } = require("@prisma/client");

const prisma = new PrismaClient();

async function main() {
  // Clear existing data
  await prisma.bookmark.deleteMany();
  await prisma.section.deleteMany();
  await prisma.tab.deleteMany();
  await prisma.theme.deleteMany();

  // Create default theme
  await prisma.theme.create({
    data: {
      name: "Default Dark",
      isActive: true,
      primaryColor: "#6366f1",
      darkMode: true,
      glassEffect: true,
    },
  });

  // Create Tabs
  const workTab = await prisma.tab.create({
    data: {
      title: "Work",
      order: 1,
    },
  });

  const devTab = await prisma.tab.create({
    data: {
      title: "Development",
      order: 2,
    },
  });

  // Create Sections & Bookmarks for Work Tab
  const generalSection = await prisma.section.create({
    data: {
      title: "General Tools",
      order: 1,
      tabId: workTab.id,
    },
  });

  await prisma.bookmark.createMany({
    data: [
      {
        title: "Outlook",
        url: "https://outlook.office.com",
        description: "Company Email",
        icon: "Mail",
        order: 1,
        sectionId: generalSection.id,
      },
      {
        title: "Microsoft Teams",
        url: "https://teams.microsoft.com",
        description: "Collaboration",
        icon: "MessageSquare",
        order: 2,
        sectionId: generalSection.id,
      },
    ],
  });

  // Admin Section (only for IT department)
  const itSection = await prisma.section.create({
    data: {
      title: "IT Admin",
      order: 2,
      tabId: workTab.id,
      organization: "IT", // Only visible to users with Department: IT
    },
  });

  await prisma.bookmark.create({
    data: {
      title: "Azure Portal",
      url: "https://portal.azure.com",
      description: "Cloud Management",
      icon: "Cloud",
      sectionId: itSection.id,
    },
  });

  // Create Sections & Bookmarks for Dev Tab
  const devTools = await prisma.section.create({
    data: {
      title: "Developer Tools",
      order: 1,
      tabId: devTab.id,
    },
  });

  await prisma.bookmark.createMany({
    data: [
      {
        title: "GitHub",
        url: "https://github.com",
        description: "Source Control",
        icon: "Github",
        order: 1,
        sectionId: devTools.id,
      },
      {
        title: "Stack Overflow",
        url: "https://stackoverflow.com",
        description: "Knowledge Base",
        icon: "Code2",
        order: 2,
        sectionId: devTools.id,
      },
    ],
  });

  console.log("Seed data created successfully!");
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
