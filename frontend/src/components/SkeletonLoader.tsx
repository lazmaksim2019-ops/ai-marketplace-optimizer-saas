export default function SkeletonLoader() {
  return (
    <div className="space-y-4 animate-pulse">
      <div className="h-4 bg-gray-700 rounded w-3/4" />
      <div className="space-y-2">
        <div className="h-3 bg-gray-700 rounded w-full" />
        <div className="h-3 bg-gray-700 rounded w-5/6" />
        <div className="h-3 bg-gray-700 rounded w-4/5" />
      </div>
      <div className="flex gap-2 flex-wrap">
        <div className="h-7 bg-gray-700 rounded-full w-28" />
        <div className="h-7 bg-gray-700 rounded-full w-24" />
        <div className="h-7 bg-gray-700 rounded-full w-32" />
      </div>
      <div className="h-20 bg-gray-700 rounded w-full" />
    </div>
  )
}
