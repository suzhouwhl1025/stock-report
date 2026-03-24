# 股票分析图表模板

> 股票分析HTML报告中常用的ECharts图表模板。

---

## 1. 估值仪表盘

展示当前估值与内在价值的对比。

```javascript
// 格雷厄姆估值仪表盘
option = {
  series: [
    {
      type: 'gauge',
      startAngle: 180,
      endAngle: 0,
      min: 0,
      max: 最高估值,
      splitNumber: 4,
      axisLine: {
        lineStyle: {
          width: 30,
          color: [
            [0.4, '#09823A'],  // 安全边际 > 40%
            [0.7, '#F5A623'], // 40% > 安全边际 > 20%
            [1, '#CC0000']    // 安全边际 < 20%
          ]
        }
      },
      pointer: {
        itemStyle: { color: '#33302E' },
        width: 5,
        length: '60%'
      },
      axisTick: { distance: -20, length: 8 },
      splitLine: { distance: -20, length: 20 },
      axisLabel: {
        formatter: function(value) {
          if (value === 0) return '低';
          if (value === 最高估值 * 0.5) return '中';
          if (value === 最高估值) return '高';
        },
        distance: 15
      },
      detail: {
        formatter: '{value}%',
        fontSize: 32,
        offsetCenter: [0, '70%']
      },
      data: [{ value: 安全边际百分比, name: '安全边际' }]
    }
  ]
};
```

---

## 2. 股价走势图（均线系统）

展示股价与均线的趋势关系。

```javascript
option = {
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'cross' }
  },
  legend: {
    data: ['股价', 'MA5', 'MA20', 'MA60', 'MA200'],
    bottom: 10
  },
  grid: { left: '5%', right: '5%', top: '10%', bottom: '15%' },
  xAxis: {
    type: 'category',
    data: 日期数组,
    boundaryGap: false
  },
  yAxis: {
    type: 'value',
    scale: true,
    splitLine: { lineStyle: { color: '#E0D3C3', type: 'dashed' } }
  },
  series: [
    {
      name: '股价',
      type: 'line',
      data: 股价数组,
      smooth: true,
      lineStyle: { width: 2, color: '#0F5499' },
      itemStyle: { color: '#0F5499' },
      markArea: {
        data: [
          [
            { yAxis: 支撑位, itemStyle: { color: 'rgba(9,130,58,0.1)' } },
            { yAxis: 阻力位 }
          ]
        ]
      }
    },
    {
      name: 'MA20',
      type: 'line',
      data: MA20数组,
      smooth: true,
      lineStyle: { width: 1, color: '#F5A623' },
      showSymbol: false
    },
    {
      name: 'MA60',
      type: 'line',
      data: MA60数组,
      smooth: true,
      lineStyle: { width: 1, color: '#E3120B' },
      showSymbol: false
    },
    {
      name: 'MA200',
      type: 'line',
      data: MA200数组,
      smooth: true,
      lineStyle: { width: 2, color: '#00338D' },
      showSymbol: false
    }
  ]
};
```

---

## 3. 波浪标注图

在价格走势图上标注艾略特波浪计数。

```javascript
option = {
  // 在股价走势图基础上添加标注
  series: [
    {
      name: '股价',
      type: 'line',
      data: 股价数组,
      markPoint: {
        symbol: 'circle',
        symbolSize: 8,
        label: { show: true, position: 'top', formatter: '{c}' },
        data: [
          { coord: [浪1位置, 浪1价格], name: '1浪' },
          { coord: [浪2位置, 浪2价格], name: '2浪' },
          { coord: [浪3位置, 浪3价格], name: '3浪' },
          { coord: [浪4位置, 浪4价格], name: '4浪' },
          { coord: [浪5位置, 浪5价格], name: '5浪' }
        ]
      },
      markLine: {
        lineStyle: { color: '#0F5499', type: 'dashed', width: 1 },
        data: [
          { yAxis: 目标位1, name: '目标1' },
          { yAxis: 目标位2, name: '目标2' },
          { yAxis: 支撑位1, name: '支撑1' }
        ]
      }
    }
  ]
};
```

---

## 4. CAN SLIM雷达图

展示CAN SLIM七维度评分。

```javascript
option = {
  tooltip: {},
  legend: {
    data: ['CAN SLIM评分', '满分基准'],
    bottom: 10
  },
  radar: {
    indicator: [
      { name: 'C 季度EPS', max: 10 },
      { name: 'A 年度EPS', max: 10 },
      { name: 'N 新产品', max: 10 },
      { name: 'S 供需', max: 10 },
      { name: 'L 相对强度', max: 10 },
      { name: 'I 机构持仓', max: 10 },
      { name: 'M 大盘方向', max: 10 }
    ],
    center: ['50%', '50%'],
    radius: '65%',
    splitNumber: 5,
    axisName: { color: '#33302E', fontSize: 12 }
  },
  series: [
    {
      type: 'radar',
      data: [
        {
          value: [C分, A分, N分, S分, L分, I分, M分],
          name: 'CAN SLIM评分',
          lineStyle: { color: '#0F5499', width: 2 },
          areaStyle: { color: 'rgba(15,84,153,0.2)' },
          itemStyle: { color: '#0F5499' }
        },
        {
          value: [10, 10, 10, 10, 10, 10, 10],
          name: '满分基准',
          lineStyle: { color: '#CCCCCC', width: 1, type: 'dashed' },
          areaStyle: { color: 'rgba(200,200,200,0.05)' },
          itemStyle: { color: '#CCCCCC' }
        }
      ]
    }
  ]
};
```

---

## 5. 财务数据柱状图

展示营收、净利润等财务数据对比。

```javascript
option = {
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'shadow' }
  },
  legend: {
    data: ['营收', '净利润', '毛利率', '净利率'],
    bottom: 10
  },
  grid: { left: '3%', right: '4%', bottom: '15%', top: '10%' },
  xAxis: {
    type: 'category',
    data: ['Q1', 'Q2', 'Q3', 'Q4', 'FY2023', 'FY2024']
  },
  yAxis: [
    {
      type: 'value',
      name: '金额(亿)',
      splitLine: { lineStyle: { color: '#E0D3C3', type: 'dashed' } }
    },
    {
      type: 'value',
      name: '比率(%)',
      max: 100,
      splitLine: { show: false }
    }
  ],
  series: [
    {
      name: '营收',
      type: 'bar',
      data: 营收数组,
      itemStyle: { color: '#0F5499', borderRadius: [4, 4, 0, 0] }
    },
    {
      name: '净利润',
      type: 'bar',
      data: 净利润数组,
      itemStyle: { color: '#09823A', borderRadius: [4, 4, 0, 0] }
    },
    {
      name: '毛利率',
      type: 'line',
      yAxisIndex: 1,
      data: 毛利率数组,
      lineStyle: { width: 2 },
      itemStyle: { color: '#F5A623' },
      smooth: true
    },
    {
      name: '净利率',
      type: 'line',
      yAxisIndex: 1,
      data: 净利率数组,
      lineStyle: { width: 2 },
      itemStyle: { color: '#CC0000' },
      smooth: true
    }
  ]
};
```

---

## 6. 护城河评级图

展示五维度护城河评估结果。

```javascript
option = {
  tooltip: {
    trigger: 'item',
    formatter: '{b}: {c}'
  },
  series: [
    {
      type: 'pie',
      radius: ['35%', '65%'],
      center: ['50%', '50%'],
      roseType: 'radius',
      itemStyle: {
        borderRadius: 5
      },
      label: {
        show: true,
        formatter: '{b}\n{c}分',
        fontSize: 12
      },
      data: [
        { value: 品牌得分, name: '品牌护城河', itemStyle: { color: '#0F5499' } },
        { value: 转换成本得分, name: '转换成本', itemStyle: { color: '#09823A' } },
        { value: 网络效应得分, name: '网络效应', itemStyle: { color: '#F5A623' } },
        { value: 成本优势得分, name: '成本优势', itemStyle: { color: '#E3120B' } },
        { value: 监管护城河得分, name: '监管护城河', itemStyle: { color: '#8B7355' } }
      ]
    }
  ]
};
```

---

## 7. RSI/MACD副图

展示技术指标副图组合。

```javascript
option = {
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'cross' },
    formatter: function(params) {
      let result = params[0].axisValue + '<br/>';
      params.forEach(p => {
        result += p.marker + p.seriesName + ': ' + p.value + '<br/>';
      });
      return result;
    }
  },
  legend: {
    data: ['RSI', 'MACD', '信号线', '柱状图'],
    bottom: 10
  },
  grid: [
    { left: '5%', right: '5%', top: '5%', height: '35%' },
    { left: '5%', right: '5%', top: '45%', height: '35%' }
  ],
  xAxis: [
    {
      type: 'category',
      data: 日期数组,
      gridIndex: 0,
      boundaryGap: false
    },
    {
      type: 'category',
      data: 日期数组,
      gridIndex: 1,
      boundaryGap: false
    }
  ],
  yAxis: [
    { type: 'value', min: 0, max: 100, gridIndex: 0, splitLine: { lineStyle: { type: 'dashed' } } },
    { gridIndex: 1, splitLine: { lineStyle: { type: 'dashed' } } }
  ],
  series: [
    {
      name: 'RSI',
      type: 'line',
      xAxisIndex: 0,
      yAxisIndex: 0,
      data: RSI数组,
      lineStyle: { width: 1, color: '#CC0000' },
      markLine: {
        silent: true,
        lineStyle: { color: '#CC0000', type: 'dashed' },
        data: [{ yAxis: 70 }, { yAxis: 30 }],
        label: { show: false }
      }
    },
    {
      name: 'MACD',
      type: 'line',
      xAxisIndex: 1,
      yAxisIndex: 1,
      data: MACD数组,
      lineStyle: { width: 1, color: '#0F5499' }
    },
    {
      name: '信号线',
      type: 'line',
      xAxisIndex: 1,
      yAxisIndex: 1,
      data: SIGNAL数组,
      lineStyle: { width: 1, color: '#F5A623' }
    },
    {
      name: '柱状图',
      type: 'bar',
      xAxisIndex: 1,
      yAxisIndex: 1,
      data: HISTOGRAM数组,
      itemStyle: {
        color: function(params) {
          return params.value >= 0 ? '#09823A' : '#CC0000';
        }
      }
    }
  ]
};
```

---

## 8. DCF敏感性分析表

展示DCF估值对关键假设的敏感性。

```javascript
option = {
  tooltip: {
    formatter: function(params) {
      const cell = params.data;
      return `WACC: ${cell[0]}%<br/>永续增长率: ${cell[1]}%<br/>DCF估值: ¥${cell[2]}`;
    }
  },
  grid: { left: '3%', right: '4%', bottom: '3%', top: '3%' },
  xAxis: {
    type: 'category',
    data: ['WACC 7%', 'WACC 8%', 'WACC 9%', 'WACC 10%', 'WACC 11%'],
    axisLabel: { fontSize: 10 },
    axisLine: { lineStyle: { color: '#333' } }
  },
  yAxis: {
    type: 'category',
    data: ['g=5%', 'g=4%', 'g=3%', 'g=2%', 'g=1%'],
    axisLabel: { fontSize: 10 },
    axisLine: { lineStyle: { color: '#333' } }
  },
  series: [
    {
      type: 'heatmap',
      data: [
        [0, 0, DCF_7_5], [1, 0, DCF_8_5], [2, 0, DCF_9_5], [3, 0, DCF_10_5], [4, 0, DCF_11_5],
        [0, 1, DCF_7_4], [1, 1, DCF_8_4], [2, 1, DCF_9_4], [3, 1, DCF_10_4], [4, 1, DCF_11_4],
        // ... 其他组合
      ],
      label: {
        show: true,
        formatter: function(params) {
          const val = params.data[2];
          return val.toFixed(0);
        },
        fontSize: 10
      },
      itemStyle: {
        color: function(params) {
          const val = params.data[2];
          if (val > 当前股价 * 1.5) return '#09823A';
          if (val > 当前股价) return '#90EE90';
          if (val > 当前股价 * 0.8) return '#F5A623';
          return '#CC0000';
        }
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
};
```

---

## 图表配色参考

### Financial Times 风格
```javascript
['#0F5499', '#09823A', '#CC0000', '#F5A623', '#996600', '#6B6B6B']
```

### McKinsey 风格
```javascript
['#003366', '#4472C4', '#70AD47', '#ED7D31', '#A5B4C8']
```

### Economist 风格
```javascript
['#E3120B', '#0A5E87', '#3B7A57', '#B8B8B8']
```

### Goldman Sachs 风格
```javascript
['#00338D', '#5B9BD5', '#A5A5A5', '#C62828', '#D4AF37']
```
