export function useFormatters() {
  function formatPrice(n: number): string {
    return Math.round(n).toLocaleString('ru-RU')
  }

  function formatPercent(n: number): string {
    const pct = (n * 100).toFixed(1)
    return n > 0 ? `+${pct}%` : `${pct}%`
  }

  function coeffClass(n: number): string {
    if (n > 0) return 'positive'
    if (n < 0) return 'negative'
    return ''
  }

  return { formatPrice, formatPercent, coeffClass }
}
