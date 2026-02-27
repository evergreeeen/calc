<template>
  <div>
    <div class="form-grid">
      <div class="form-group">
        <label>Площадь кладовой, кв.м</label>
        <input v-model.number="area" type="number" step="0.01" min="0" />
      </div>
    </div>

    <div class="checkbox-group">
      <input id="storage-discount" v-model="withDiscount" type="checkbox" />
      <label for="storage-discount">Применить скидку 5%</label>
    </div>

    <button class="btn-calc" :disabled="loading || !area" @click="calculate">
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
        <div v-if="result.discount > 0" class="result-row">
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

<script setup lang="ts">
const { formatPrice } = useFormatters()

const area = ref(3.5)
const withDiscount = ref(false)
const result = ref<any>(null)
const loading = ref(false)

async function calculate() {
  loading.value = true
  result.value = null
  try {
    result.value = await $fetch('/api/calculate/storage', {
      method: 'POST',
      body: { area: area.value, with_discount: withDiscount.value },
    })
  } finally {
    loading.value = false
  }
}
</script>
