import { useQuery } from '@tanstack/react-query'
import { getDashboardSummary, getTimeline, getTopics, getSources, getLanguages, getRecent } from '../api/dashboard'

export function useDashboardSummary(hours = 24) {
  return useQuery({
    queryKey: ['dashboard', 'summary', hours],
    queryFn: () => getDashboardSummary(hours).then(r => r.data),
    refetchInterval: 30000,
  })
}

export function useTimeline(hours = 24) {
  return useQuery({
    queryKey: ['dashboard', 'timeline', hours],
    queryFn: () => getTimeline(hours).then(r => r.data),
    refetchInterval: 60000,
  })
}

export function useTopics(limit = 20, hours = 24) {
  return useQuery({
    queryKey: ['dashboard', 'topics', limit, hours],
    queryFn: () => getTopics(limit, hours).then(r => r.data),
    refetchInterval: 60000,
  })
}

export function useSources(hours = 24) {
  return useQuery({
    queryKey: ['dashboard', 'sources', hours],
    queryFn: () => getSources(hours).then(r => r.data),
    refetchInterval: 60000,
  })
}

export function useLanguages(hours = 24) {
  return useQuery({
    queryKey: ['dashboard', 'languages', hours],
    queryFn: () => getLanguages(hours).then(r => r.data),
    refetchInterval: 60000,
  })
}

export function useRecent(limit = 50) {
  return useQuery({
    queryKey: ['dashboard', 'recent', limit],
    queryFn: () => getRecent(limit).then(r => r.data),
    refetchInterval: 30000,
  })
}
