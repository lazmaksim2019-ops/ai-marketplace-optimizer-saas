import { useState, useRef } from 'react'
import { Sparkles, Upload, ImageIcon, AlertCircle } from 'lucide-react'
import { analyze } from '../api'
import type { AnalyzeResponse } from '../types'
import ResultCard from './ResultCard'
import TriggerTags from './TriggerTags'
import SkeletonLoader from './SkeletonLoader'

export default function Dashboard() {
  const [marketplace, setMarketplace] = useState<'wb' | 'ozon'>('wb')
  const [description, setDescription] = useState('')
  const [imageUrl, setImageUrl] = useState('')
  const [file, setFile] = useState<File | null>(null)
  const [filePreview, setFilePreview] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<AnalyzeResponse | null>(null)
  const fileRef = useRef<HTMLInputElement>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0] || null
    setFile(f)
    setImageUrl('')
    if (f) {
      const reader = new FileReader()
      reader.onload = () => setFilePreview(reader.result as string)
      reader.readAsDataURL(f)
    } else {
      setFilePreview(null)
    }
  }

  const handleSubmit = async () => {
    if (!description.trim()) return

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await analyze(description, marketplace, imageUrl || undefined, file)
      setResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Неизвестная ошибка')
    } finally {
      setLoading(false)
    }
  }

  const isFormValid = description.trim().length > 0

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900/80 backdrop-blur-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center gap-3">
          <div className="p-2 bg-indigo-600/20 rounded-lg">
            <Sparkles className="w-5 h-5 text-indigo-400" />
          </div>
          <div>
            <h1 className="text-lg font-bold tracking-tight">AI Оптимизатор карточек</h1>
            <p className="text-xs text-gray-500">Wildberries / Ozon — SEO оптимизация</p>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left panel: Input */}
          <div className="space-y-6">
            <div className="bg-gray-900/60 border border-gray-800 rounded-2xl p-6 space-y-5">
              <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">
                Входные данные
              </h2>

              {/* Marketplace selector */}
              <div>
                <label className="block text-sm text-gray-400 mb-1.5">Маркетплейс</label>
                <div className="flex bg-gray-800 border border-gray-700 rounded-xl p-1">
                  <button
                    onClick={() => setMarketplace('wb')}
                    className={`flex-1 py-2 text-sm font-medium rounded-lg transition cursor-pointer ${
                      marketplace === 'wb'
                        ? 'bg-indigo-600 text-white shadow-sm'
                        : 'text-gray-400 hover:text-gray-200'
                    }`}
                  >
                    Wildberries
                  </button>
                  <button
                    onClick={() => setMarketplace('ozon')}
                    className={`flex-1 py-2 text-sm font-medium rounded-lg transition cursor-pointer ${
                      marketplace === 'ozon'
                        ? 'bg-indigo-600 text-white shadow-sm'
                        : 'text-gray-400 hover:text-gray-200'
                    }`}
                  >
                    Ozon
                  </button>
                </div>
              </div>

              {/* Image URL */}
              <div>
                <label className="block text-sm text-gray-400 mb-1.5">Ссылка на изображение</label>
                <div className="relative">
                  <ImageIcon className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
                  <input
                    type="url"
                    value={imageUrl}
                    onChange={(e) => { setImageUrl(e.target.value); setFile(null); setFilePreview(null) }}
                    placeholder="https://example.com/image.jpg"
                    className="w-full bg-gray-800 border border-gray-700 rounded-xl py-2.5 pl-10 pr-4 text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500/50 transition"
                  />
                </div>
              </div>

              <div className="flex items-center gap-3">
                <div className="flex-1 border-t border-gray-800" />
                <span className="text-xs text-gray-500">или</span>
                <div className="flex-1 border-t border-gray-800" />
              </div>

              {/* File upload */}
              <div>
                <label className="block text-sm text-gray-400 mb-1.5">Загрузить файл</label>
                <button
                  onClick={() => fileRef.current?.click()}
                  className="w-full flex items-center justify-center gap-2 py-8 border-2 border-dashed border-gray-700 rounded-xl text-gray-500 hover:border-indigo-500/50 hover:text-indigo-400 transition cursor-pointer"
                >
                  <Upload className="w-5 h-5" />
                  <span className="text-sm">{file ? file.name : 'Выберите изображение'}</span>
                </button>
                <input
                  ref={fileRef}
                  type="file"
                  accept="image/*"
                  onChange={handleFileChange}
                  className="hidden"
                />
                {filePreview && (
                  <img
                    src={filePreview}
                    alt="Preview"
                    className="mt-3 w-full h-48 object-cover rounded-xl border border-gray-700"
                  />
                )}
              </div>

              {/* Description */}
              <div>
                <label className="block text-sm text-gray-400 mb-1.5">Текущее описание товара</label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  rows={5}
                  placeholder="Введите текущее описание товара..."
                  className="w-full bg-gray-800 border border-gray-700 rounded-xl py-2.5 px-4 text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500/50 transition resize-none"
                />
              </div>

              {/* Submit */}
              <button
                onClick={handleSubmit}
                disabled={!isFormValid || loading}
                className="w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-500 disabled:bg-gray-700 disabled:text-gray-500 text-white font-medium py-3 px-6 rounded-xl transition cursor-pointer disabled:cursor-not-allowed"
              >
                <Sparkles className="w-4 h-4" />
                {loading ? 'Анализируем...' : 'Запустить AI-анализ'}
              </button>

              {error && (
                <div className="flex items-start gap-2 p-3 bg-red-900/30 border border-red-800/50 rounded-xl text-sm text-red-300">
                  <AlertCircle className="w-4 h-4 mt-0.5 shrink-0" />
                  <span>{error}</span>
                </div>
              )}
            </div>
          </div>

          {/* Right panel: Results */}
          <div className="space-y-6">
            <div className="bg-gray-900/60 border border-gray-800 rounded-2xl p-6 min-h-[300px]">
              <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-5">
                Результаты анализа
              </h2>

              {loading && <SkeletonLoader />}

              {!loading && !result && !error && (
                <div className="flex flex-col items-center justify-center py-16 text-gray-600">
                  <Sparkles className="w-10 h-10 mb-3" />
                  <p className="text-sm">Заполните данные слева и запустите анализ</p>
                </div>
              )}

              {!loading && result && (
                <div className="space-y-4">
                  <ResultCard title="SEO-заголовок" content={result.seo_title} isCode />
                  <ResultCard title="SEO-описание" content={result.seo_description} />
                  <TriggerTags triggers={result.infographics_triggers} />
                  <ResultCard title="Маркетинговые советы" content={result.marketing_tips} />
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
