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

// Props 接收数据
const props = defineProps({
  title: {
    type: String,
    default: 'Normalized Bar Chart',
  },
  xAxisData: {
    type: Array,
    required: true,
  },
  seriesData: {
    type: Array,
    required: true,
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

// 归一化数据
const normalizeSeriesData = (seriesData) => {
  const normalizedData = [];
  const totalValues = seriesData[0].data.map((_, index) =>
    seriesData.reduce((sum, series) => sum + series.data[index], 0)
  );

  seriesData.forEach((series) => {
    normalizedData.push({
      name: series.name,
      type: 'bar',
      stack: 'total', // 堆叠柱状图
      data: series.data.map((value, index) => (totalValues[index] === 0 ? 0 : (value / totalValues[index]) * 100)),
    });
  });

  return normalizedData;
};

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
      trigger: 'axis',
      axisPointer: {
        type: 'shadow',
      },
      formatter: (params) => {
        let tooltip = `${params[0].axisValue}<br/>`;
        params.forEach((item) => {
          tooltip += `${item.marker} ${item.seriesName}: ${item.value.toFixed(2)}%<br/>`;
        });
        return tooltip;
      },
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
      data: props.xAxisData,
      axisLine: {
        lineStyle: {
          color: isDarkMode.value ? '#ffffff' : '#000000',
        },
      },
      axisLabel: {
        color: isDarkMode.value ? '#ffffff' : '#000000',
      },
    },
    yAxis: {
      type: 'value',
      axisLine: {
        lineStyle: {
          color: isDarkMode.value ? '#ffffff' : '#000000',
        },
      },
      axisLabel: {
        color: isDarkMode.value ? '#ffffff' : '#000000',
        formatter: '{value}%',
      },
    },
    series: normalizeSeriesData(props.seriesData),
  };

  chartInstance.setOption(option);
};

// 监听 Props 数据变化，动态更新图表
watch(
  () => [props.xAxisData, props.seriesData, isDarkMode.value],
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