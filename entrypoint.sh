#!/bin/sh
set -e

echo "Synchronizing database schema..."
npx prisma generate
./node_modules/.bin/prisma db push --schema=prisma/schema.prisma --accept-data-loss

# Use "$@" to preserve arguments, fallback to npm run dev if none
if [ $# -eq 0 ]; then
  echo "Starting application with: npm run dev"
  exec npm run dev
else
  echo "Starting application with: $@"
  exec "$@"
fi
