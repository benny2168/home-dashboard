const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();
async function main() {
  const user = await prisma.user.findFirst({ where: { department: 'avteam' } });
  console.log("AV Team user ID:", user ? user.id : 'not found', "isAdmin:", user ? user.isAdmin : 'N/A');

  const section = await prisma.section.findFirst({
    where: { title: { contains: "helpful hints", mode: "insensitive" } },
    include: {
      owners: { select: { id: true, name: true, email: true } },
      editors: { select: { id: true, name: true, email: true } },
      departmentAccess: true
    }
  });

  if (!section) { console.log('Section not found'); return; }
  console.log("\nSection Owners:");
  console.log(section.owners);
  console.log("\nSection Editors:");
  console.log(section.editors);
  console.log("\nDepartment Access:");
  console.log(section.departmentAccess);
  
  if (user) {
     const isOwner = section.owners.some(o => o.id === user.id);
     const isEditor = section.editors.some(e => e.id === user.id);
     console.log(`\nIs AV Team an owner? ${isOwner}`);
     console.log(`Is AV Team an editor? ${isEditor}`);
  }
}
main().finally(() => prisma.$disconnect());
