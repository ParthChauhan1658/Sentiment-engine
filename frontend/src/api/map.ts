import api from './client'

export const getConstituencies = () =>
  api.get('/api/map/constituencies')

export const getHeatmap = (hours = 24) =>
  api.get('/api/map/heatmap', { params: { hours } })

export const getConstituencyDetail = (name: string, hours = 24) =>
  api.get(`/api/map/constituency/${name}`, { params: { hours } })
