<template>
  <div ref="chart" :style="{ width: '100%', height: `${chartHeight}px` }"></div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount, computed } from 'vue';
import { useQuasar } from 'quasar';
import * as echarts from 'echarts/core';
import { TreemapChart } from 'echarts/charts';
import { TooltipComponent, TitleComponent } from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';

// 注册 ECharts 模块
echarts.use([TreemapChart, TooltipComponent, TitleComponent, CanvasRenderer]);

// Props 接收数据
const props = defineProps({
  title: {
    type: String,
    default: 'Treemap Chart',
  },
  seriesData: {
    type: Array,
    required: true, // Treemap 数据格式
  },
  chartHeight: {
    type: Number,
    required: true,
  },
});

// Quasar 暗黑模式支持
const $q = useQuasar();
const isDarkMode = computed(() => $q.dark.isActive);

// 图表实例
const chart = ref(null);
let chartInstance = null;

// 初始化图表
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
      formatter: (info) => {
        const value = info.value || 0;
        return `${info.name}: ${value}`;
      },
    },
    series: [
      {
        type: 'treemap',
        data: props.seriesData,
        label: {
          show: true,
          formatter: '{b}',
          color: isDarkMode.value ? '#ffffff' : '#000000',
        },
        itemStyle: {
          borderColor: isDarkMode.value ? '#ffffff' : '#000000',
          borderWidth: 1,
        },
      },
    ],
  };

  chartInstance.setOption(option);
};

// 监听 Props 数据变化，动态更新图表
watch(
  () => [props.seriesData, isDarkMode.value],
  () => {
    initChart();
  },
  { deep: true }
);

// 在组件挂载时初始化图表
onMounted(() => {
  initChart();
  window.addEventListener('resize', resizeChart);
});

// 在组件销毁时清理资源
onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.dispose();
    chartInstance = null;
  }
  window.removeEventListener('resize', resizeChart);
});

// 自适应窗口大小
const resizeChart = () => {
  if (chartInstance) {
    chartInstance.resize();
  }
};
</script>

<style scoped>
/* 确保图表容器占满父容器 */
</style>