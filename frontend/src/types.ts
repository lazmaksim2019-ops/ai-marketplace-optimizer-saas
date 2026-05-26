export interface AnalyzeResponse {
  seo_title: string
  seo_description: string
  infographics_triggers: string[]
  marketing_tips: string
}

export interface AnalyzeError {
  detail: string
}
