<template>
  <div class="app">
    <header>
      <h1>Калькулятор цен ЖК</h1>
      <div class="tabs">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          :class="{ active: activeTab === tab.id }"
          @click="activeTab = tab.id"
        >
          {{ tab.label }}
        </button>
      </div>
    </header>

    <main>
      <ApartmentCalc v-if="activeTab === 'apartment'" :options="options" />
      <StorageCalc v-if="activeTab === 'storage'" />
      <ParkingCalc v-if="activeTab === 'parking'" :options="options" />
    </main>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import ApartmentCalc from './components/ApartmentCalc.vue'
import StorageCalc from './components/StorageCalc.vue'
import ParkingCalc from './components/ParkingCalc.vue'

export default {
  components: { ApartmentCalc, StorageCalc, ParkingCalc },
  setup() {
    const activeTab = ref('apartment')
    const options = ref(null)
    const tabs = [
      { id: 'apartment', label: 'Квартиры' },
      { id: 'storage', label: 'Кладовые' },
      { id: 'parking', label: 'Машиноместа' },
    ]

    onMounted(async () => {
      const res = await fetch('/api/options')
      options.value = await res.json()
    })

    return { activeTab, options, tabs }
  },
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f0f2f5;
  color: #1a1a2e;
}

.app {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

header {
  text-align: center;
  margin-bottom: 24px;
}

header h1 {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 16px;
}

.tabs {
  display: flex;
  gap: 4px;
  justify-content: center;
  background: #e2e6ea;
  border-radius: 10px;
  padding: 4px;
  display: inline-flex;
}

.tabs button {
  padding: 10px 24px;
  border: none;
  background: transparent;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  color: #666;
  transition: all 0.2s;
}

.tabs button.active {
  background: #fff;
  color: #1a1a2e;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.tabs button:hover:not(.active) {
  color: #333;
}

main {
  background: #fff;
  border-radius: 16px;
  padding: 28px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
}

/* Shared form styles */
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

@media (max-width: 600px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
  .app {
    padding: 12px;
  }
  main {
    padding: 16px;
  }
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-size: 12px;
  font-weight: 600;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 6px;
}

.form-group select,
.form-group input {
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  background: #fafafa;
  transition: border-color 0.2s;
}

.form-group select:focus,
.form-group input:focus {
  outline: none;
  border-color: #4a6cf7;
  background: #fff;
}

.btn-calc {
  display: block;
  width: 100%;
  padding: 14px;
  margin-top: 20px;
  background: #4a6cf7;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-calc:hover {
  background: #3a5ce5;
}

.btn-calc:disabled {
  background: #b0bec5;
  cursor: not-allowed;
}

/* Results */
.results {
  margin-top: 24px;
  border-top: 1px solid #eee;
  padding-top: 24px;
}

.results h2 {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 16px;
}

.result-section {
  margin-bottom: 20px;
}

.result-section h3 {
  font-size: 13px;
  font-weight: 600;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 10px;
}

.result-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #f5f5f5;
  font-size: 14px;
}

.result-row:last-child {
  border-bottom: none;
}

.result-row .label {
  color: #666;
}

.result-row .value {
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}

.result-row .value.positive {
  color: #2ecc71;
}

.result-row .value.negative {
  color: #e74c3c;
}

.result-highlight {
  background: #f0f4ff;
  border-radius: 12px;
  padding: 16px 20px;
  margin-bottom: 16px;
}

.result-highlight .price-main {
  font-size: 28px;
  font-weight: 800;
  color: #1a1a2e;
}

.result-highlight .price-sub {
  font-size: 14px;
  color: #888;
  margin-top: 4px;
}

.section-divider {
  height: 1px;
  background: #eee;
  margin: 16px 0;
}

.checkbox-group {
  display: flex;
  align-items: center;
  gap: 8px;
  padding-top: 24px;
}

.checkbox-group input[type="checkbox"] {
  width: 18px;
  height: 18px;
}

.checkbox-group label {
  font-size: 14px;
  color: #333;
}
</style>
