interface TriggerTagsProps {
  triggers: string[]
}

export default function TriggerTags({ triggers }: TriggerTagsProps) {
  return (
    <div className="bg-gray-800/60 border border-gray-700 rounded-xl p-4 space-y-3">
      <h3 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">
        Триггеры для инфографики
      </h3>
      <div className="flex flex-wrap gap-2">
        {triggers.map((trigger) => (
          <span
            key={trigger}
            className="inline-block px-3 py-1.5 bg-gradient-to-r from-indigo-600/30 to-purple-600/30 text-indigo-300 text-sm font-medium rounded-full border border-indigo-500/30"
          >
            {trigger}
          </span>
        ))}
      </div>
    </div>
  )
}
