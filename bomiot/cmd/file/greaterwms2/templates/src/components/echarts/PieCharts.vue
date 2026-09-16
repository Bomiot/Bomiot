<template>
    <div ref="chart" :style="{ width: '100%', height: `${chartHeight}px` }"></div>
</template>
  
<script setup>
import { ref, watch, onMounted, onBeforeUnmount, computed } from 'vue';
import { useQuasar } from 'quasar';
import * as echarts from 'echarts/core';
import { PieChart } from 'echarts/charts';
import { TooltipComponent, TitleComponent, LegendComponent } from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';

echarts.use([PieChart, TooltipComponent, TitleComponent, LegendComponent, CanvasRenderer]);

const props = defineProps({
  title: {
    type: String,
    default: 'Pie Chart',
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
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)',
    },
    legend: {
      top: '10%',
      left: 'center',
      textStyle: {
        color: isDarkMode.value ? '#ffffff' : '#000000',
      },
    },
    series: [
      {
        name: props.title,
        type: 'pie',
        radius: '50%',
        data: props.seriesData,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
          },
        },
        label: {
          color: isDarkMode.value ? '#ffffff' : '#000000',
        },
      },
    ],
  };

  chartInstance.setOption(option);
};

watch(
  () => [props.seriesData, isDarkMode.value],
  () => {
    initChart();
  },
  { deep: true }
);

onMounted(() => {
  initChart();
  window.addEventListener('resize', resizeChart);
});

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.dispose();
    chartInstance = null;
  }
  window.removeEventListener('resize', resizeChart);
});

const resizeChart = () => {
  if (chartInstance) {
    chartInstance.resize();
  }
};
</script>

<style scoped>
  .full-height {
    height: 100%;
    width: 100%;
  }
</style>