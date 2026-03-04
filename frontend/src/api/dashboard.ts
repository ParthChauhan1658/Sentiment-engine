import api from './client'

export const getDashboardSummary = (hours = 24) =>
  api.get('/api/dashboard/summary', { params: { hours } })

export const getTimeline = (hours = 24) =>
  api.get('/api/dashboard/timeline', { params: { hours } })

export const getTopics = (limit = 20, hours = 24) =>
  api.get('/api/dashboard/topics', { params: { limit, hours } })

export const getSources = (hours = 24) =>
  api.get('/api/dashboard/sources', { params: { hours } })

export const getLanguages = (hours = 24) =>
  api.get('/api/dashboard/languages', { params: { hours } })

export const getRecent = (limit = 50, page = 1) =>
  api.get('/api/dashboard/recent', { params: { limit, page } })

export const getStats = () =>
  api.get('/api/dashboard/stats')

export const scrapeAndAnalyze = (keywords = 'Modi government, development, infrastructure') =>
  api.get('/api/scrape-and-analyze', { params: { keywords }, timeout: 120000 })
