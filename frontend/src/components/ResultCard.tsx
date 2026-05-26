import { Copy, Check } from 'lucide-react'
import { useState } from 'react'

interface ResultCardProps {
  title: string
  content: string
  isCode?: boolean
}

export default function ResultCard({ title, content, isCode }: ResultCardProps) {
  const [copied, setCopied] = useState(false)

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(content)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch {
      // Clipboard API may fail in non-secure contexts
    }
  }

  return (
    <div className="bg-gray-800/60 border border-gray-700 rounded-xl p-4 space-y-2">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">
          {title}
        </h3>
        <button
          onClick={handleCopy}
          className="flex items-center gap-1 text-xs text-indigo-400 hover:text-indigo-300 transition-colors"
        >
          {copied ? (
            <><Check size="sm" className="w-3.5 h-3.5" /> Скопировано</>
          ) : (
            <><Copy size="sm" className="w-3.5 h-3.5" /> Копировать</>
          )}
        </button>
      </div>
      <p className={`text-gray-100 ${isCode ? 'font-mono text-sm' : 'text-sm leading-relaxed'}`}>
        {content}
      </p>
    </div>
  )
}
