<template>
  <div class="app">
    <header>
      <h1>Калькулятор доходности ЖК</h1>
    </header>

    <main>
      <ProfitabilityCalc :lots-data="lotsData" />
    </main>
  </div>
</template>

<script setup lang="ts">
const { data: lotsData } = await useFetch('/api/lots')
</script>
