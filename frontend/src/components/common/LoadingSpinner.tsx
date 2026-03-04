export default function LoadingSpinner({ size = 'md' }: { size?: 'sm' | 'md' | 'lg' }) {
  const sizeMap = { sm: 'w-6 h-6', md: 'w-10 h-10', lg: 'w-14 h-14' }
  const borderMap = { sm: 'border-2', md: 'border-2', lg: 'border-[3px]' }
  return (
    <div className="flex flex-col items-center justify-center py-16 gap-4">
      <div className={`${sizeMap[size]} animate-spin rounded-full ${borderMap[size]}`}
        style={{
          borderColor: 'rgba(247, 231, 206, 0.08)',
          borderTopColor: '#F7E7CE',
          filter: 'drop-shadow(0 0 8px rgba(247, 231, 206, 0.15))',
        }} />
      <p className="text-xs tracking-wide animate-pulse" style={{ color: 'rgba(247, 231, 206, 0.3)' }}>Loading...</p>
    </div>
  )
}
