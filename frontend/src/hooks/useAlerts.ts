import { useQuery } from '@tanstack/react-query'
import { getRecentAlerts } from '../api/alerts'

export function useAlerts(limit = 20) {
  return useQuery({
    queryKey: ['alerts', limit],
    queryFn: () => getRecentAlerts(limit).then(r => r.data),
    refetchInterval: 30000,
  })
}
