import type { AnalyzeResponse } from './types'

const API_BASE = import.meta.env.VITE_API_URL || '/api'

export async function analyze(
  description: string,
  marketplace: 'wb' | 'ozon',
  imageUrl?: string,
  file?: File | null,
): Promise<AnalyzeResponse> {
  const form = new FormData()
  form.append('description', description)
  form.append('marketplace', marketplace)
  if (imageUrl) {
    form.append('image_url', imageUrl)
  }
  if (file) {
    form.append('file', file)
  }

  const res = await fetch(`${API_BASE}/analyze`, {
    method: 'POST',
    body: form,
  })

  if (!res.ok) {
    const err = await res.json()
    throw new Error(err.detail || 'Ошибка при анализе')
  }

  return res.json() as Promise<AnalyzeResponse>
}
