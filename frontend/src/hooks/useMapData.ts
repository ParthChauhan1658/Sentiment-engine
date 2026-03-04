import { useQuery } from '@tanstack/react-query'
import { getConstituencies, getHeatmap } from '../api/map'

export function useConstituencies() {
  return useQuery({
    queryKey: ['map', 'constituencies'],
    queryFn: () => getConstituencies().then(r => r.data),
  })
}

export function useHeatmap(hours = 24) {
  return useQuery({
    queryKey: ['map', 'heatmap', hours],
    queryFn: () => getHeatmap(hours).then(r => r.data),
    refetchInterval: 60000,
  })
}
