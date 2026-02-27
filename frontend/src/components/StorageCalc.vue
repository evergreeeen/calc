<template>
  <div>
    <div class="form-grid">
      <div class="form-group">
        <label>Площадь кладовой, кв.м</label>
        <input v-model.number="area" type="number" step="0.01" min="0" />
      </div>
    </div>

    <div class="checkbox-group">
      <input id="storage-discount" type="checkbox" v-model="withDiscount" />
      <label for="storage-discount">Применить скидку 5%</label>
    </div>

    <button class="btn-calc" @click="calculate" :disabled="loading || !area">
      {{ loading ? 'Расчёт...' : 'Рассчитать стоимость' }}
    </button>

    <div v-if="result" class="results">
      <div class="result-highlight">
        <div class="price-main">{{ formatPrice(result.total) }} ₽</div>
        <div class="price-sub">
          {{ formatPrice(result.price_per_sqm) }} ₽/кв.м &middot; {{ result.area }} кв.м
        </div>
      </div>

      <div class="result-section">
        <div class="result-row">
          <span class="label">Цена за кв.м</span>
          <span class="value">{{ formatPrice(result.price_per_sqm) }} ₽</span>
        </div>
        <div class="result-row" v-if="result.discount > 0">
          <span class="label">Скидка</span>
          <span class="value negative">-{{ (result.discount * 100).toFixed(0) }}%</span>
        </div>
        <div class="result-row" style="font-weight:700">
          <span class="label">Итого</span>
          <span class="value">{{ formatPrice(result.total) }} ₽</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  setup() {
    const area = ref(3.5)
    const withDiscount = ref(false)
    const result = ref(null)
    const loading = ref(false)

    function formatPrice(n) {
      return Math.round(n).toLocaleString('ru-RU')
    }

    async function calculate() {
      loading.value = true
      result.value = null
      const res = await fetch('/api/calculate/storage', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ area: area.value, with_discount: withDiscount.value }),
      })
      result.value = await res.json()
      loading.value = false
    }

    return { area, withDiscount, result, loading, formatPrice, calculate }
  },
}
</script>
