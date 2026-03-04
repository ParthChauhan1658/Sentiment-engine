import api from './client'

export const analyzeSingle = (text: string) =>
  api.post('/api/sentiment/analyze', { text })

export const analyzeBatch = (texts: string[]) =>
  api.post('/api/sentiment/analyze-batch', { texts })
