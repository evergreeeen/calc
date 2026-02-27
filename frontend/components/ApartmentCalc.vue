<template>
  <div v-if="!options" class="loading">Загрузка...</div>
  <div v-else>
    <div class="form-grid">
      <div class="form-group">
        <label>Тип квартиры</label>
        <select v-model="form.apartment_type">
          <option v-for="t in options.apartment_types" :key="t" :value="t">
            {{ typeLabels[t] || t }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label>Корпус</label>
        <select v-model="form.building">
          <option v-for="b in options.buildings" :key="b" :value="b">{{ b }}</option>
        </select>
      </div>

      <div class="form-group">
        <label>Этаж</label>
        <select v-model.number="form.floor">
          <option v-for="f in options.floors" :key="f" :value="f">{{ f }}</option>
        </select>
      </div>

      <div class="form-group">
        <label>Общая площадь, кв.м</label>
        <input v-model.number="form.area_total" type="number" step="0.01" min="0" />
      </div>

      <div class="form-group">
        <label>Площадь летних помещений, кв.м</label>
        <input v-model.number="form.area_summer" type="number" step="0.01" min="0" />
      </div>

      <div class="form-group">
        <label>Размер</label>
        <select v-model="form.size">
          <option v-for="s in options.sizes" :key="s" :value="s">
            {{ s }}{{ sizeHint(s) }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label>Тип планировки</label>
        <select v-model="form.layout">
          <option v-for="l in options.layouts" :key="l" :value="l">{{ l }}</option>
        </select>
      </div>

      <div class="form-group">
        <label>Геометрия</label>
        <select v-model="form.geometry">
          <option v-for="g in options.geometries" :key="g" :value="g">{{ g }}</option>
        </select>
      </div>

      <div class="form-group">
        <label>Удалённость от лифта</label>
        <select v-model="form.elevator_zone">
          <option v-for="z in options.elevator_zones" :key="z" :value="z">{{ z }}</option>
        </select>
      </div>

      <div class="form-group">
        <label>Вид из окон</label>
        <select v-model="form.view">
          <option v-for="v in options.views" :key="v" :value="v">{{ v }}</option>
        </select>
      </div>

      <div class="form-group">
        <label>Расположение на этаже</label>
        <select v-model="form.position">
          <option v-for="p in options.positions" :key="p" :value="p">{{ p }}</option>
        </select>
      </div>

      <div class="form-group">
        <label>Кол-во лотов на этаже</label>
        <select v-model.number="form.units_on_floor">
          <option v-for="u in options.units_on_floor" :key="u" :value="u">{{ u }}</option>
        </select>
      </div>

      <div class="form-group">
        <label>Повышение / скидка, %</label>
        <input v-model.number="form.price_adjustment_pct" type="number" step="0.1" />
      </div>
    </div>

    <button class="btn-calc" :disabled="loading" @click="calculate">
      {{ loading ? 'Расчёт...' : 'Рассчитать стоимость' }}
    </button>

    <div v-if="result" class="results">
      <div class="result-highlight">
        <div class="price-main">{{ formatPrice(result.pricing.final_budget) }} ₽</div>
        <div class="price-sub">
          {{ formatPrice(result.pricing.final_price_per_sqm) }} ₽/кв.м
          &middot; {{ result.areas.total }} кв.м
        </div>
      </div>

      <div class="result-section">
        <h3>Площади</h3>
        <div class="result-row">
          <span class="label">Общая площадь</span>
          <span class="value">{{ result.areas.total }} кв.м</span>
        </div>
        <div class="result-row">
          <span class="label">Летние помещения</span>
          <span class="value">{{ result.areas.summer }} кв.м</span>
        </div>
        <div class="result-row">
          <span class="label">Летние с коэф. 0.3</span>
          <span class="value">{{ result.areas.summer_with_coeff }} кв.м</span>
        </div>
        <div class="result-row">
          <span class="label">Без летних помещений</span>
          <span class="value">{{ result.areas.without_summer }} кв.м</span>
        </div>
        <div class="result-row">
          <span class="label">С коэффициентом</span>
          <span class="value">{{ result.areas.with_coeff }} кв.м</span>
        </div>
      </div>

      <div class="section-divider" />

      <div class="result-section">
        <h3>Коэффициенты</h3>
        <div class="result-row">
          <span class="label">Базовая цена ({{ form.apartment_type }})</span>
          <span class="value">{{ formatPrice(result.coefficients.base_price) }} ₽/кв.м</span>
        </div>
        <div v-for="(coeff, idx) in coeffRows" :key="idx" class="result-row">
          <span class="label">{{ coeff.label }}</span>
          <span class="value" :class="coeffClass(coeff.value)">
            {{ formatPercent(coeff.value) }}
          </span>
        </div>
        <div class="result-row" style="font-weight:700">
          <span class="label">Итого поправка</span>
          <span class="value" :class="coeffClass(result.coefficients.total)">
            {{ formatPercent(result.coefficients.total) }}
          </span>
        </div>
      </div>

      <div class="section-divider" />

      <div class="result-section">
        <h3>Ценообразование</h3>
        <div class="result-row">
          <span class="label">Расценка (цена за кв.м)</span>
          <span class="value">{{ formatPrice(result.pricing.price_per_sqm) }} ₽</span>
        </div>
        <div class="result-row">
          <span class="label">Бюджет</span>
          <span class="value">{{ formatPrice(result.pricing.budget) }} ₽</span>
        </div>
        <div v-if="result.pricing.adjustment !== 0" class="result-row">
          <span class="label">Повышение/скидка</span>
          <span class="value" :class="coeffClass(result.pricing.adjustment)">
            {{ formatPercent(result.pricing.adjustment) }}
          </span>
        </div>
        <div class="result-row" style="font-weight:700">
          <span class="label">Итоговая цена за кв.м</span>
          <span class="value">{{ formatPrice(result.pricing.final_price_per_sqm) }} ₽</span>
        </div>
        <div class="result-row" style="font-weight:700">
          <span class="label">Итоговый бюджет</span>
          <span class="value">{{ formatPrice(result.pricing.final_budget) }} ₽</span>
        </div>
      </div>

      <div class="section-divider" />

      <div class="result-section">
        <h3>Цены для CRM и сайта</h3>
        <div class="result-row">
          <span class="label">Цена CRM (со скидкой {{ (result.crm.max_discount * 100) }}%)</span>
          <span class="value">{{ formatPrice(result.crm.price_per_sqm) }} ₽/кв.м</span>
        </div>
        <div class="result-row">
          <span class="label">Бюджет CRM</span>
          <span class="value">{{ formatPrice(result.crm.budget) }} ₽</span>
        </div>
        <div class="result-row">
          <span class="label">Цена на сайт (+ бронь {{ formatPrice(result.site.booking_fee) }})</span>
          <span class="value">{{ formatPrice(result.site.price_per_sqm) }} ₽/кв.м</span>
        </div>
        <div class="result-row">
          <span class="label">Бюджет для сайта</span>
          <span class="value">{{ formatPrice(result.site.budget) }} ₽</span>
        </div>
      </div>
    </div>

    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ options: any }>()

const { formatPrice, formatPercent, coeffClass } = useFormatters()

const typeLabels: Record<string, string> = {
  'Ст': 'Студия',
  '1К': '1-комнатная',
  '2К': '2-комнатная',
}

const form = ref({
  apartment_type: 'Ст',
  building: 'С1',
  floor: 4,
  area_total: 32.93,
  area_summer: 8.19,
  size: 'S',
  layout: 'Линейная',
  geometry: 'Правильная',
  elevator_zone: 'Зона 1',
  view: 'Двор север',
  position: 'Стандарт',
  units_on_floor: 13,
  price_adjustment_pct: 0,
})

const result = ref<any>(null)
const error = ref<string | null>(null)
const loading = ref(false)

const coeffRows = computed(() => {
  if (!result.value) return []
  const c = result.value.coefficients
  return [
    { label: 'Этаж', value: c.floor },
    { label: 'Размер', value: c.size },
    { label: 'Тип планировки', value: c.layout },
    { label: 'Геометрия', value: c.geometry },
    { label: 'Удалённость от лифта', value: c.elevator },
    { label: 'Вид из окон', value: c.view },
    { label: 'Расположение на этаже', value: c.position },
    { label: 'Кол-во лотов на этаже', value: c.units_on_floor },
    { label: 'Корпус', value: c.building },
  ]
})

function sizeHint(s: string): string {
  if (!props.options?.size_ranges) return ''
  const ranges = props.options.size_ranges[form.value.apartment_type]
  if (!ranges || !ranges[s]) return ''
  return ` (${ranges[s]} кв.м)`
}

async function calculate() {
  loading.value = true
  error.value = null
  result.value = null
  try {
    const body: any = { ...form.value, price_adjustment: form.value.price_adjustment_pct / 100 }
    delete body.price_adjustment_pct
    const data = await $fetch('/api/calculate/apartment', {
      method: 'POST',
      body,
    })
    result.value = data
  } catch (e: any) {
    error.value = e.data?.detail || e.message || 'Ошибка расчёта'
  } finally {
    loading.value = false
  }
}
</script>
