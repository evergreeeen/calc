<template>
  <div v-if="!options" class="loading">Загрузка...</div>
  <div v-else>
    <div class="form-grid">
      <div class="form-group">
        <label>Тип парковочного места</label>
        <select v-model="parkingType">
          <option v-for="p in options.parking_types" :key="p" :value="p">{{ p }}</option>
        </select>
      </div>
    </div>

    <div class="checkbox-group">
      <input id="parking-discount" v-model="withDiscount" type="checkbox" />
      <label for="parking-discount">Применить скидку 5%</label>
    </div>

    <button class="btn-calc" :disabled="loading" @click="calculate">
      {{ loading ? 'Расчёт...' : 'Рассчитать стоимость' }}
    </button>

    <div v-if="result" class="results">
      <div class="result-highlight">
        <div class="price-main">{{ formatPrice(result.price) }} ₽</div>
        <div class="price-sub">{{ result.parking_type }}</div>
      </div>

      <div class="result-section">
        <div class="result-row">
          <span class="label">Базовая цена</span>
          <span class="value">{{ formatPrice(result.base_price) }} ₽</span>
        </div>
        <div v-if="result.discount > 0" class="result-row">
          <span class="label">Скидка</span>
          <span class="value negative">-{{ (result.discount * 100).toFixed(0) }}%</span>
        </div>
        <div class="result-row" style="font-weight:700">
          <span class="label">Итого</span>
          <span class="value">{{ formatPrice(result.price) }} ₽</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ options: any }>()

const { formatPrice } = useFormatters()

const parkingType = ref('Стандартное место')
const withDiscount = ref(false)
const result = ref<any>(null)
const loading = ref(false)

async function calculate() {
  loading.value = true
  result.value = null
  try {
    result.value = await $fetch('/api/calculate/parking', {
      method: 'POST',
      body: { parking_type: parkingType.value, with_discount: withDiscount.value },
    })
  } finally {
    loading.value = false
  }
}
</script>
