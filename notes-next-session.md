# Notes for Next Session

## Immediate Next Steps & Follow-ups
1. **Curated Icon Allow-list for Lucide**: Replace wildcard `LucideIcons` import in `IconPicker.tsx` / `Dashboard.tsx` with a curated allow-list or map to enable tree-shaking for icons.
2. **Modal Lazy Loading**: Lazy-load heavy modals (`ThemeModal`, `TabModal`, `SectionModal`, `BookmarkModal`) using `next/dynamic` to reduce initial client bundle size.
3. **Prisma Permission Filtering**: Push per-user permission filtering into Prisma `where` queries directly rather than filtering in JavaScript post-fetch.
4. **Tab Tree Caching**: Evaluate `unstable_cache` or Redis/React cache for tab tree queries if permission model permits.
5. Verify live deployment with Authentik container service and test end-to-end OAuth flow.
