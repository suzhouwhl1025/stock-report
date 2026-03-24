# 股票分析详细工作流

> SKILL.md 的执行层。按需查阅，不必全读。

## 数据采集工作流

### Phase 1: 数据采集

通过网络搜索获取股票相关数据。

**采集来源**：
- 财务数据：Yahoo Finance、Google Finance、东方财富网、雪球
- 技术数据：TradingView、Yahoo Finance历史价格
- 机构持仓：SEC EDGAR、各基金13F报告
- 行业数据：行业协会、宏观数据

**采集步骤**：

1. **确认股票代码**
   ```python
   # 常见对应关系
   贵州茅台 -> 600519.SS (A股) / 600519.SHI (港股)
   苹果 -> AAPL (美股)
   ```

2. **财务数据采集**
   - 近4季度季度报告数据
   - 近3年年度数据
   - 可比公司同期数据

3. **技术数据采集**
   - 至少1年历史价格（日线）
   - 成交量数据
   - 技术指标计算

4. **数据整理输出**
   - 所有数据写入 `_temp/stock-data.md`
   - 标注每个数据的来源和采集时间
   - 标注数据缺失项

---

### Phase 2: 专家选角

固定两个专家角色：

**价值投资分析师**：
- 背景：格雷厄姆+巴菲特+霍华德马克斯
- 任务：估值分析、护城河分析、周期判断

**技术分析分析师**：
- 背景：道氏理论+艾略特波浪+欧奈尔CAN SLIM
- 任务：趋势判断、波浪计数、CAN SLIM评分

---

### Phase 3: 并行深度分析

**subagent prompt模板（价值投资）**：

```
你是价值投资分析师，请对以下股票进行深度价值投资分析。

## 股票信息
- 股票名称：[股票名]
- 股票代码：[代码]
- 数据文件：_temp/stock-data.md

## 你的分析框架

### 1. 格雷厄姆安全边际估值
- 计算Graham Number
- DCF三场景估值（保守/中性/乐观）
- 与当前股价对比，计算安全边际

### 2. 巴菲特护城河分析
评估五个维度：
- 品牌护城河
- 转换成本
- 网络效应
- 成本优势
- 监管护城河

### 3. 霍华德·马克斯周期思维
- 行业周期所处阶段
- 市场情绪指标
- 信贷周期信号

## 输出要求
将分析结果写入 `_temp/analysis-01-value.md`
文件必须包含：
1. 核心发现（3-5条，带具体数字）
2. 详细分析（每个维度一节）
3. 关键数据汇总表
4. 图表建议
5. 投资结论
```

**subagent prompt模板（技术分析）**：

```
你是技术分析专家，请对以下股票进行深度技术分析。

## 股票信息
- 股票名称：[股票名]
- 股票代码：[代码]
- 数据文件：_temp/stock-data.md

## 你的分析框架

### 1. 道氏理论趋势分析
- 主要趋势判断（牛市/熊市/盘整）
- 次要趋势（回调/反弹）
- 成交量确认
- 支撑位和阻力位

### 2. 艾略特波浪分析
- 当前波浪位置
- 各浪起止点和幅度
- 目标位和支撑位
- 波浪计数置信度

### 3. 欧奈尔CAN SLIM分析
- C（季度EPS增长）
- A（年度EPS增长）
- N（新产品/创新）
- S（供需/流通股）
- L（相对强度）
- I（机构持仓）
- M（大盘方向）

### 4. 技术指标汇总
- RSI（14日）
- MACD
- 布林带
- 均线关系
- ATR

## 输出要求
将分析结果写入 `_temp/analysis-02-technical.md`
文件必须包含：
1. 核心发现（3-5条，带具体数字）
2. 详细分析（每个维度一节）
3. 关键数据汇总表
4. 图表建议
5. 技术分析结论
```

---

### Phase 4: 统一综合呈现

**整合步骤**：
1. 读取 `_temp/analysis-01-value.md` 和 `_temp/analysis-02-technical.md`
2. 提炼关键发现
3. 按主题重新组织（估值、趋势、风险等）
4. 交叉引用两种分析的发现
5. 生成HTML报告

**报告结构**：
```
1. 标题（结论式）
2. 核心摘要（5条）
3. 关键指标面板
4. 价值投资分析
5. 技术分析
6. 综合研判
7. 风险提示
8. 适合投资者类型
```

---

## 数据来源参考

### A股数据源
- 雪球：https://xueqiu.com/S/[代码]
- 东方财富：https://data.eastmoney.com
- 新浪财经：https://finance.sina.com.cn

### 美股数据源
- Yahoo Finance：https://finance.yahoo.com/quote/[代码]
- SEC EDGAR：https://www.sec.gov/cgi-bin/browse-edgar

### 技术数据源
- TradingView：https://www.tradingview.com
- StockCharts：https://stockcharts.com

---

## 依赖安装

```bash
pip install pandas openpyxl yfinance akshare
```

---

## 文件输出约定

| 类型 | 命名规范 |
|------|---------|
| 数据采集 | `_temp/stock-data.md` |
| 专家角色 | `_temp/expert-roles.md` |
| 价值分析 | `_temp/analysis-01-value.md` |
| 技术分析 | `_temp/analysis-02-technical.md` |
| 最终报告 | `_temp/report-[股票名].html` |
| 股票数据Excel | `_temp/[股票名]-data.xlsx` |
