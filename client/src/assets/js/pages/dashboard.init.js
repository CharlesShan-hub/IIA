// // 导入所需库
// import jQuery from 'jquery';
// import Chartist from 'chartist';
// import 'chartist-plugin-tooltip';

// const $ = jQuery;

// // 初始化所有图表
// function initAllCharts() {
//   // 折线图初始化
//   new Chartist.Line("#chart-with-area", {
//     labels: [1, 2, 3, 4, 5, 6, 7, 8],
//     series: [[5, 9, 7, 8, 5, 3, 5, 4]]
//   }, {
//     low: 0,
//     showArea: true,
//     plugins: [Chartist.plugins.tooltip()]
//   });

//   // 饼图初始化
//   new Chartist.Pie("#ct-donut", {
//     series: [54, 28, 17],
//     labels: [1, 2, 3]
//   }, {
//     donut: true,
//     showLabel: false, 
//     plugins: [Chartist.plugins.tooltip()]
//   });

//   // Peity图表初始化
//   $(".peity-donut").peity("donut");
//   $(".peity-line").peity("line");
// }

// // 使用jQuery的ready方法确保DOM加载完成
// $(function() {
//   initAllCharts();
// });