<template>
  <div class="app">
    <header>
      <h1>Калькулятор ЖК</h1>
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
      <ProfitabilityCalc v-if="activeTab === 'profitability'" :lots-data="lotsData" />
      <ApartmentCalc v-if="activeTab === 'apartment'" :options="options" />
      <StorageCalc v-if="activeTab === 'storage'" />
      <ParkingCalc v-if="activeTab === 'parking'" :options="options" />
    </main>
  </div>
</template>

<script setup lang="ts">
const activeTab = ref('profitability')

const tabs = [
  { id: 'profitability', label: 'Доходность' },
  { id: 'apartment', label: 'Квартиры' },
  { id: 'storage', label: 'Кладовые' },
  { id: 'parking', label: 'Машиноместа' },
]

const { data: options } = await useFetch('/api/options')
const { data: lotsData } = await useFetch('/api/lots')
</script>
