import { PrismaClient } from "@prisma/client";
import { PrismaPg } from "@prisma/adapter-pg";
const adapter = new PrismaPg({ connectionString: process.env.DATABASE_URL || "postgresql://user:password@db:5432/dashboard?schema=public" });
const prisma = new PrismaClient({ adapter });

async function main() {
  console.log("Starting data migration for TabSection mapping...");

  const allSections = await prisma.section.findMany();
  const sections = allSections.filter((s: any) => s.tabId != null);

  console.log(`Found ${sections.length} sections to migrate.`);

  let migratedCount = 0;
  for (const section of sections) {
    if (!section.tabId) continue;
    
    // Check if it already exists to be safe
    const ex = await prisma.tabSection.findFirst({
      where: { tabId: section.tabId, sectionId: section.id }
    });

    if (!ex) {
      await prisma.tabSection.create({
        data: {
          tabId: section.tabId,
          sectionId: section.id,
          order: section.order || 0
        }
      });
      migratedCount++;
    }
  }

  console.log(`Successfully migrated ${migratedCount} sections.`);
}

main()
  .then(async () => {
    await prisma.$disconnect()
  })
  .catch(async (e) => {
    console.error(e)
    await prisma.$disconnect()
    process.exit(1)
  });
