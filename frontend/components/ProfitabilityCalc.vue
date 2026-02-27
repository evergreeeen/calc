<template>
  <div>
    <div class="form-grid">
      <div class="form-group">
        <label>Корпус</label>
        <select v-model="building" @change="onBuildingChange">
          <option v-for="b in buildings" :key="b" :value="b">{{ b }}</option>
        </select>
      </div>

      <div class="form-group">
        <label>Номер лота</label>
        <select v-model.number="lotNumber">
          <option v-for="lot in filteredLots" :key="lot.number" :value="lot.number">
            {{ lot.number }} — {{ lot.rooms }}, {{ lot.area }} кв.м, эт.{{ lot.floor }}, {{ lot.size }}
          </option>
        </select>
      </div>
    </div>

    <div class="checkbox-group">
      <input id="installment" v-model="installment" type="checkbox" />
      <label for="installment">Покупка в рассрочку</label>
    </div>

    <button class="btn-calc" :disabled="loading || !lotNumber" @click="calculate">
      {{ loading ? 'Расчёт...' : 'Рассчитать доходность' }}
    </button>

    <div v-if="result" class="results">
      <!-- Lot info -->
      <div class="result-highlight">
        <div class="price-main">{{ fp(result.payment.purchase_price) }} ₽</div>
        <div class="price-sub">
          Лот {{ result.lot.code }} &middot; {{ result.lot.area }} кв.м &middot;
          {{ result.lot.rooms }} &middot; {{ result.lot.size }} &middot;
          эт. {{ result.lot.floor }} &middot; {{ result.lot.view }}
        </div>
      </div>

      <!-- Payment -->
      <div class="result-section">
        <h3>Стоимость</h3>
        <div class="result-row">
          <span class="label">Цена кв.м на сайте</span>
          <span class="value">{{ fp(result.payment.site_price_sqm) }} ₽</span>
        </div>
        <div class="result-row">
          <span class="label">При 100% оплате</span>
          <span class="value">{{ fp(result.payment.full_payment_price) }} ₽</span>
        </div>
        <div class="result-row">
          <span class="label">В рассрочку</span>
          <span class="value">{{ fp(result.payment.installment_price) }} ₽</span>
        </div>
      </div>

      <div class="section-divider" />

      <!-- Price growth -->
      <div class="result-section">
        <h3>Рост цены</h3>
        <div class="result-row">
          <span class="label">Дата передачи ключей</span>
          <span class="value">{{ formatDate(result.price_projection.key_delivery_date) }}</span>
        </div>
        <div class="result-row">
          <span class="label">Рост к передаче ключей</span>
          <span class="value positive">+{{ (result.price_projection.growth_to_delivery * 100).toFixed(1) }}%</span>
        </div>
        <div class="result-row">
          <span class="label">Цена к передаче ключей</span>
          <span class="value">{{ fp(result.price_projection.price_at_delivery) }} ₽</span>
        </div>
        <div class="result-row">
          <span class="label">Цена кв.м к передаче ключей</span>
          <span class="value">{{ fp(result.price_projection.price_sqm_at_delivery) }} ₽</span>
        </div>
        <div class="result-row">
          <span class="label">Доход от роста к передаче</span>
          <span class="value positive">+{{ fp(result.price_projection.profit_at_delivery) }} ₽</span>
        </div>

        <div class="section-divider" />

        <div class="result-row">
          <span class="label">Цена к 2039 году</span>
          <span class="value">{{ fp(result.price_projection.price_at_2039) }} ₽</span>
        </div>
        <div class="result-row">
          <span class="label">Доход от роста к 2039</span>
          <span class="value positive">+{{ fp(result.price_projection.profit_at_2039) }} ₽</span>
        </div>
      </div>

      <div class="section-divider" />

      <!-- Price chart -->
      <div class="result-section">
        <h3>Прогноз цены лота</h3>
        <div class="chart-container">
          <div class="bar-chart">
            <div
              v-for="(price, idx) in result.price_projection.prices"
              :key="idx"
              class="bar-item"
            >
              <div class="bar-value">{{ shortPrice(price) }}</div>
              <div
                class="bar"
                :style="{ height: barHeight(price, result.price_projection.prices) }"
                :class="{ highlight: result.price_projection.years[idx] === 2029 }"
              />
              <div class="bar-label">{{ result.price_projection.years[idx] }}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="section-divider" />

      <!-- Hotel income -->
      <div class="result-section">
        <h3>Доход от отеля (10 лет)</h3>
        <div class="result-row">
          <span class="label">Совокупный доход от отеля</span>
          <span class="value">{{ fp(result.hotel_income.total_income_10y) }} ₽</span>
        </div>
        <div class="result-row">
          <span class="label">Средний годовой доход</span>
          <span class="value">{{ fp(result.hotel_income.avg_annual_income) }} ₽</span>
        </div>
        <div class="result-row">
          <span class="label">Среднегодовая доходность</span>
          <span class="value positive">{{ (result.hotel_income.avg_annual_yield * 100).toFixed(1) }}%</span>
        </div>
      </div>

      <div class="section-divider" />

      <!-- Hotel income table -->
      <div class="result-section">
        <h3>Доход по годам</h3>
        <div class="table-scroll">
          <table class="data-table">
            <thead>
              <tr>
                <th>Год</th>
                <th>Загрузка</th>
                <th>ADR</th>
                <th>Доход в год</th>
                <th>Доход в мес.</th>
                <th>Доходность</th>
                <th>Накопленный</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="yr in result.hotel_income.years" :key="yr.year">
                <td>{{ yr.year }}</td>
                <td>{{ (yr.occupancy * 100).toFixed(0) }}%</td>
                <td>{{ fp(yr.adr) }}</td>
                <td>{{ fp(yr.owner_income) }}</td>
                <td>{{ fp(yr.monthly_income) }}</td>
                <td class="positive">{{ (yr.annual_yield * 100).toFixed(1) }}%</td>
                <td>{{ fp(yr.cumulative_income) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="section-divider" />

      <!-- Hotel income chart -->
      <div class="result-section">
        <h3>Годовой доход от отеля</h3>
        <div class="chart-container">
          <div class="bar-chart">
            <div
              v-for="yr in result.hotel_income.years"
              :key="yr.year"
              class="bar-item"
            >
              <div class="bar-value">{{ shortPrice(yr.owner_income) }}</div>
              <div
                class="bar bar-green"
                :style="{ height: barHeight(yr.owner_income, result.hotel_income.years.map(y => y.owner_income)) }"
              />
              <div class="bar-label">{{ yr.year }}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="section-divider" />

      <!-- Summary -->
      <div class="result-section">
        <h3>Итоги за 10 лет</h3>
        <div class="result-highlight" style="background: #eafbef">
          <div class="price-main" style="color: #2ecc71">{{ fp(result.summary.total_return_10y) }} ₽</div>
          <div class="price-sub">Совокупный доход (аренда + рост цены)</div>
        </div>
        <div class="result-row">
          <span class="label">Средний годовой доход общий</span>
          <span class="value">{{ fp(result.summary.avg_annual_total) }} ₽</span>
        </div>
        <div class="result-row">
          <span class="label">Среднегодовая доходность общая</span>
          <span class="value positive">{{ (result.summary.avg_annual_total_yield * 100).toFixed(1) }}%</span>
        </div>
        <div class="result-row">
          <span class="label">Окупаемость (отель + продажа)</span>
          <span class="value">{{ result.summary.payback_total_years ?? '> 10' }} лет</span>
        </div>
        <div class="result-row">
          <span class="label">Окупаемость (только отель)</span>
          <span class="value">{{ result.summary.payback_hotel_years ?? '> 10' }} лет</span>
        </div>
      </div>
    </div>

    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ lotsData: any }>()

const { formatPrice } = useFormatters()
const fp = formatPrice

const buildings = computed(() => props.lotsData?.buildings ?? [])
const building = ref(props.lotsData?.buildings?.[0] ?? 'С2')
const lotNumber = ref<number | null>(null)
const installment = ref(false)
const result = ref<any>(null)
const error = ref<string | null>(null)
const loading = ref(false)

const filteredLots = computed(() => {
  if (!props.lotsData?.lots) return []
  return props.lotsData.lots[building.value] ?? []
})

function onBuildingChange() {
  lotNumber.value = filteredLots.value[0]?.number ?? null
  result.value = null
}

watch(() => props.lotsData, () => {
  if (filteredLots.value.length && !lotNumber.value) {
    lotNumber.value = filteredLots.value[0]?.number ?? null
  }
}, { immediate: true })

function formatDate(iso: string): string {
  const d = new Date(iso)
  return d.toLocaleDateString('ru-RU', { year: 'numeric', month: 'long', day: 'numeric' })
}

function shortPrice(n: number): string {
  if (n >= 1_000_000) return (n / 1_000_000).toFixed(1) + 'М'
  if (n >= 1_000) return (n / 1_000).toFixed(0) + 'К'
  return n.toFixed(0)
}

function barHeight(value: number, all: number[]): string {
  const max = Math.max(...all)
  return Math.max(10, (value / max) * 140) + 'px'
}

async function calculate() {
  loading.value = true
  error.value = null
  result.value = null
  try {
    result.value = await $fetch('/api/calculate/profitability', {
      method: 'POST',
      body: {
        building: building.value,
        number: lotNumber.value,
        installment: installment.value,
      },
    })
  } catch (e: any) {
    error.value = e.data?.detail || e.message || 'Ошибка расчёта'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.chart-container {
  overflow-x: auto;
  padding: 8px 0;
}

.bar-chart {
  display: flex;
  gap: 4px;
  align-items: flex-end;
  min-width: 500px;
  padding-top: 20px;
}

.bar-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 40px;
}

.bar-value {
  font-size: 10px;
  color: #888;
  margin-bottom: 4px;
  white-space: nowrap;
}

.bar {
  width: 100%;
  max-width: 50px;
  background: #4a6cf7;
  border-radius: 4px 4px 0 0;
  transition: height 0.3s;
}

.bar.highlight {
  background: #e74c3c;
}

.bar.bar-green {
  background: #2ecc71;
}

.bar-label {
  font-size: 10px;
  color: #888;
  margin-top: 4px;
  transform: rotate(-45deg);
  white-space: nowrap;
}

.table-scroll {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.data-table th,
.data-table td {
  padding: 8px 10px;
  text-align: right;
  border-bottom: 1px solid #f0f0f0;
  white-space: nowrap;
}

.data-table th {
  font-size: 11px;
  font-weight: 600;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.data-table td:first-child,
.data-table th:first-child {
  text-align: left;
}

.data-table .positive {
  color: #2ecc71;
  font-weight: 600;
}
</style>
