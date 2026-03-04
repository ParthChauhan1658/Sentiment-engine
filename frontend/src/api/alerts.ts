import api from './client'

export const getRecentAlerts = (limit = 10) =>
  api.get('/api/alerts/recent', { params: { limit } })
