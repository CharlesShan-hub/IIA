<script>
/**
 * Chartist line-area chart
 */
export default {
  name: 'WidgetChart',
  data() {
    return {
      data: {
        labels: [1, 2, 3, 4, 5, 6, 7, 8],
        series: [[5, 9, 7, 8, 5, 3, 5, 4]]
      },
      options: {
        low: 0,
        showArea: true,
        height: 300
      }
    }
  }
}
</script>
<template>
  <chartist
    ratio="ct-chart"
    :data="data"
    :options="options"
    type="Line"
  ></chartist>
</template>