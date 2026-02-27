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

<script setup lang="ts">
const activeTab = ref('apartment')

const tabs = [
  { id: 'apartment', label: 'Квартиры' },
  { id: 'storage', label: 'Кладовые' },
  { id: 'parking', label: 'Машиноместа' },
]

const { data: options } = await useFetch('/api/options')
</script>
