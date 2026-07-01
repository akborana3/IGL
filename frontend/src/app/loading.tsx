/** Premium skeleton loading page. */

import { SkeletonRow } from "@/components/ui/Skeleton";

export default function Loading() {
  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 py-6">
      <div className="w-full h-[60vh] min-h-[400px] skeleton rounded-3xl mb-8" />
      <div className="mb-8">
        <div className="h-6 w-40 skeleton rounded mb-4" />
        <SkeletonRow />
      </div>
      <div className="mb-8">
        <div className="h-6 w-40 skeleton rounded mb-4" />
        <SkeletonRow />
      </div>
    </div>
  );
}
