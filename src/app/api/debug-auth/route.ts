import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { auth } from '@/auth';

export const dynamic = 'force-dynamic';

export async function GET() {
  const session = await auth();
  const avTeamUsers = await prisma.user.findMany({ where: { department: { contains: 'av team', mode: 'insensitive' } } });
  
  const section = await prisma.section.findFirst({
    where: { title: { contains: 'helpful hints', mode: 'insensitive' } },
    include: {
      owners: true,
      editors: true,
      departmentAccess: true
    }
  });

  return NextResponse.json({
    session,
    avTeamUsers,
    section
  });
}
