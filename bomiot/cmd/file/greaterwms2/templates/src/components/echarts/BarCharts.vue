<template>
    <div ref="chart" :style="{ width: '100%', height: `${chartHeight}px` }"></div>
</template>
  
<script setup>
import { ref, watch, onMounted, onBeforeUnmount, computed } from 'vue';
import { useQuasar } from 'quasar';
import * as echarts from 'echarts/core';
import { BarChart } from 'echarts/charts';
import { GridComponent, TooltipComponent, TitleComponent, LegendComponent } from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';

echarts.use([BarChart, GridComponent, TooltipComponent, TitleComponent, LegendComponent, CanvasRenderer]);
 
  const props = defineProps({
    title: {
      type: String,
      default: 'Bar Chart',
    },
    xAxisData: {
      type: Array,
      required: true,
    },
    seriesData: {
      type: Array,
      required: true,
    },
    chartWidth: {
      type: Number,
      required: true,
    },
    chartHeight: {
      type: Number,
      required: true,
    },
  });
  
const $q = useQuasar();
const isDarkMode = computed(() => $q.dark.isActive);
const chart = ref(null);
let chartInstance = null;
  
const initChart = () => {
if (!chart.value) return;

if (!chartInstance) {
    chartInstance = echarts.init(chart.value);
}

const option = {
    title: {
    text: props.title,
    left: 'center',
    textStyle: {
        color: isDarkMode.value ? '#ffffff' : '#000000',
    },
    },
    tooltip: {
    trigger: 'axis',
    },
    legend: {
    top: '10%',
    textStyle: {
        color: isDarkMode.value ? '#ffffff' : '#000000',
    },
    },
    grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true,
    },
    xAxis: {
    type: 'category',
    boundaryGap: false,
    data: props.xAxisData,
    axisLine: {
    lineStyle: {
        color: isDarkMode.value ? '#ffffff' : '#000000',
    },
    axisLabel: {
        color: isDarkMode.value ? '#ffffff' : '#000000',
    },
    },
    },
    yAxis: {
    type: 'value',
    },
    series: props.seriesData.map((series) => ({
    name: series.name,
    type: 'bar',
    data: series.data,
    axisLine: {
        lineStyle: {
        color: isDarkMode.value ? '#ffffff' : '#000000',
        },
    },
    axisLabel: {
        color: isDarkMode.value ? '#ffffff' : '#000000',
    },
    
    })),
};

chartInstance.setOption(option);
};
  
watch(
  () => [props.chartWidth, props.chartHeight],
  () => {
  if (chartInstance) {
    chartInstance.resize();
  }
  }
);
  
watch(
  () => [props.xAxisData, props.seriesData, isDarkMode.value],
  () => {
    initChart();
  },
  { deep: true }
)

onMounted(() => {
    initChart();
});
onBeforeUnmount(() => {
    if (chartInstance) {
        chartInstance.dispose();
        chartInstance = null;
    }
});
</script>
  
<style scoped>
  .full-height {
    height: 100%;
    width: 100%;
  }
</style>