#!/usr/bin/env python3
"""
search_stock_data.py — 通过网络搜索获取股票数据

用法：
    python3 search_stock_data.py 贵州茅台
    python3 search_stock_data.py AAPL --market US
    python3 search_stock_data.py 600519 --market CN

参数：
    股票名称/代码   股票名称或代码
    --market       市场：CN（A股默认）、US（美股）、HK（港股）
    --period       数据周期：1y（1年）、2y（2年）、5y（5年）、max（全部）
    --output       输出文件路径（默认为_temp/stock-data.md）

依赖：
    pip install yfinance akshare pandas
"""

import sys
import os
import json
import argparse
from datetime import datetime, timedelta

def ensure_dependencies():
    """检查并提示安装依赖"""
    missing = []
    try:
        import yfinance
    except ImportError:
        missing.append('yfinance')
    try:
        import akshare
    except ImportError:
        missing.append('akshare')
    try:
        import pandas
    except ImportError:
        missing.append('pandas')
    if missing:
        print(f"缺少依赖: {', '.join(missing)}", file=sys.stderr)
        print(f"请运行: pip install {' '.join(missing)}", file=sys.stderr)
        sys.exit(1)

ensure_dependencies()

import yfinance as yf
import akshare as ak
import pandas as pd


# 股票名称到代码的映射（常用股票）
STOCK_NAME_MAP = {
    # A股
    '贵州茅台': '600519',
    '茅台': '600519',
    '五粮液': '000858',
    '格力电器': '000651',
    '美的集团': '000333',
    '比亚迪': '002594',
    '宁德时代': '300750',
    '中国平安': '601318',
    '招商银行': '600036',
    '工商银行': '601398',
    '建设银行': '601939',
    '农业银行': '601288',
    '中国石油': '601857',
    '中国石化': '600028',
    '中国建筑': '601668',
    '中国中免': '601888',
    '伊利股份': '600887',
    '恒瑞医药': '600276',
    '药明康德': '603259',
    '海康威视': '002415',
    '中兴通讯': '000063',
    '万科A': '000002',
    '保利发展': '600048',
    '中国神华': '601088',
    '长江电力': '600900',
    # 美股
    '苹果': 'AAPL',
    'Apple': 'AAPL',
    '微软': 'MSFT',
    'Microsoft': 'MSFT',
    '谷歌': 'GOOGL',
    'Google': 'GOOGL',
    '亚马逊': 'AMZN',
    'Amazon': 'AMZN',
    'Meta': 'META',
    '英伟达': 'NVDA',
    'NVIDIA': 'NVDA',
    '特斯拉': 'TSLA',
    'Tesla': 'TSLA',
    'Netflix': 'NFLX',
    '台积电': 'TSM',
    'TSMC': 'TSM',
    '伯克希尔': 'BRK-B',
    'Berkshire': 'BRK-B',
}


def resolve_stock_code(stock_input, market='CN'):
    """解析股票代码"""
    # 如果已经是数字代码，直接返回
    if stock_input.isdigit():
        if market == 'CN':
            suffix = '.SS' if len(stock_input) == 6 and stock_input.startswith(('6', '5')) else '.SZ'
            return stock_input + suffix
        return stock_input

    # 尝试从名称映射
    if stock_input in STOCK_NAME_MAP:
        code = STOCK_NAME_MAP[stock_input]
        if market == 'CN' and code.isdigit():
            suffix = '.SS' if code.startswith(('6', '5')) else '.SZ'
            return code + suffix
        return code

    # 假设直接是代码
    return stock_input


def get_stock_info_cn(code):
    """获取A股基本信息（东方财富）"""
    try:
        # 股票基本信息
        stock_info = ak.stock_individual_info_em(symbol=code)
        info_dict = dict(zip(stock_info['item'], stock_info['value']))
        return info_dict
    except Exception as e:
        print(f"获取A股信息失败: {e}", file=sys.stderr)
        return {}


def get_financial_data_cn(code):
    """获取A股财务数据"""
    data = {}
    try:
        # 季度财务数据
        df_quarter = ak.stock_financial_analysis_indicator(symbol=code, start_year='2022', end_year='2024')
        data['quarterly'] = df_quarter
    except Exception as e:
        print(f"获取季度财务数据失败: {e}", file=sys.stderr)

    try:
        # 年度财务数据
        df_yearly = ak.stock_financial_report_sina(symbol=code, indicator='资产负债表')
        data['yearly'] = df_yearly
    except Exception as e:
        print(f"获取年度财务数据失败: {e}", file=sys.stderr)

    return data


def get_stock_info_us(ticker):
    """获取美股基本信息"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            'name': info.get('longName', ticker),
            'price': info.get('currentPrice') or info.get('regularMarketPrice'),
            'marketCap': info.get('marketCap'),
            'pe': info.get('trailingPE'),
            'forwardPE': info.get('forwardPE'),
            'pb': info.get('priceToBook'),
            'dividendYield': info.get('dividendYield'),
            'eps': info.get('trailingEps'),
            'forwardEps': info.get('forwardEps'),
            'beta': info.get('beta'),
            '52wHigh': info.get('fiftyTwoWeekHigh'),
            '52wLow': info.get('fiftyTwoWeekLow'),
            'volume': info.get('averageVolume'),
            'avgVolume': info.get('averageVolume'),
            'revenue': info.get('totalRevenue'),
            'grossMargins': info.get('grossMargins'),
            'operatingMargins': info.get('operatingMargins'),
            'netMargins': info.get('profitMargins'),
            'roe': info.get('returnOnEquity'),
            'debtToEquity': info.get('debtToEquity'),
            'currentRatio': info.get('currentRatio'),
            'quickRatio': info.get('quickRatio'),
        }
    except Exception as e:
        print(f"获取美股信息失败: {e}", file=sys.stderr)
        return {}


def get_financial_data_us(ticker):
    """获取美股财务数据"""
    data = {}
    try:
        stock = yf.Ticker(ticker)
        # 季度利润表
        data['quarterly_income'] = stock.quarterly_income_stmt
        # 年度利润表
        data['yearly_income'] = stock.income_stmt
        # 季度资产负债表
        data['quarterly_balance'] = stock.quarterly_balance_sheet
        # 季度现金流量表
        data['quarterly_cashflow'] = stock.quarterly_cashflow
    except Exception as e:
        print(f"获取美股财务数据失败: {e}", file=sys.stderr)
    return data


def get_historical_prices(ticker, period='1y'):
    """获取历史价格数据"""
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)
        return df
    except Exception as e:
        print(f"获取历史价格失败: {e}", file=sys.stderr)
        return pd.DataFrame()


def calculate_technical_indicators(df):
    """计算技术指标"""
    if df.empty:
        return {}

    close = df['Close']
    high = df['High']
    low = df['Low']
    volume = df['Volume']

    # 简单移动平均
    ma5 = close.rolling(5).mean()
    ma20 = close.rolling(20).mean()
    ma60 = close.rolling(60).mean()
    ma200 = close.rolling(200).mean()

    # RSI (14日)
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    # MACD
    ema12 = close.ewm(span=12).mean()
    ema26 = close.ewm(span=26).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9).mean()
    histogram = macd - signal

    # 布林带
    bb_mid = close.rolling(20).mean()
    bb_std = close.rolling(20).std()
    bb_upper = bb_mid + 2 * bb_std
    bb_lower = bb_mid - 2 * bb_std

    # ATR (14日)
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(14).mean()

    return {
        'ma5': ma5.iloc[-1] if not ma5.empty else None,
        'ma20': ma20.iloc[-1] if not ma20.empty else None,
        'ma60': ma60.iloc[-1] if not ma60.empty else None,
        'ma200': ma200.iloc[-1] if not ma200.empty else None,
        'rsi': rsi.iloc[-1] if not rsi.empty else None,
        'macd': macd.iloc[-1] if not macd.empty else None,
        'macd_signal': signal.iloc[-1] if not signal.empty else None,
        'macd_hist': histogram.iloc[-1] if not histogram.empty else None,
        'bb_upper': bb_upper.iloc[-1] if not bb_upper.empty else None,
        'bb_mid': bb_mid.iloc[-1] if not bb_mid.empty else None,
        'bb_lower': bb_lower.iloc[-1] if not bb_lower.empty else None,
        'atr': atr.iloc[-1] if not atr.empty else None,
    }


def format_market_cap(market_cap):
    """格式化市值"""
    if market_cap is None:
        return 'N/A'
    if market_cap >= 1e12:
        return f'{market_cap/1e12:.2f}万亿'
    elif market_cap >= 1e8:
        return f'{market_cap/1e8:.2f}亿'
    else:
        return f'{market_cap:.2f}'


def output_markdown(stock_name, code, info, financial_data, prices, technical):
    """输出Markdown格式的数据"""
    output = f"""# 股票数据采集报告

## 基本信息

- **股票名称**：{stock_name}
- **股票代码**：{code}
- **采集时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""

    if info:
        output += "## 基本面数据\n\n"
        if 'name' in info:
            output += f"- **公司名称**：{info.get('name', 'N/A')}\n"
        if 'price' in info:
            output += f"- **当前股价**：{info.get('price', 'N/A')}\n"
        if 'marketCap' in info:
            output += f"- **市值**：{format_market_cap(info.get('marketCap'))}\n"
        if 'pe' in info and info.get('pe'):
            output += f"- **市盈率(PE)**：{info.get('pe', 'N/A'):.2f}\n"
        if 'forwardPE' in info and info.get('forwardPE'):
            output += f"- **滚动市盈率**：{info.get('forwardPE', 'N/A'):.2f}\n"
        if 'pb' in info and info.get('pb'):
            output += f"- **市净率(PB)**：{info.get('pb', 'N/A'):.2f}\n"
        if 'eps' in info and info.get('eps'):
            output += f"- **EPS(TTM)**：{info.get('eps', 'N/A'):.2f}\n"
        if 'forwardEps' in info and info.get('forwardEps'):
            output += f"- **Forward EPS**：{info.get('forwardEps', 'N/A'):.2f}\n"
        if 'dividendYield' in info and info.get('dividendYield'):
            output += f"- **股息率**：{info.get('dividendYield', 0)*100:.2f}%\n"
        if 'beta' in info:
            output += f"- **Beta**：{info.get('beta', 'N/A'):.2f}\n"
        if '52wHigh' in info:
            output += f"- **52周高点**：{info.get('52wHigh', 'N/A')}\n"
        if '52wLow' in info:
            output += f"- **52周低点**：{info.get('52wLow', 'N/A')}\n"

        # 盈利能力
        output += "\n### 盈利能力\n\n"
        if 'revenue' in info and info.get('revenue'):
            output += f"- **营收**：{info.get('revenue', 0)/1e8:.2f}亿\n"
        if 'grossMargins' in info:
            output += f"- **毛利率**：{info.get('grossMargins', 0)*100:.2f}%\n"
        if 'operatingMargins' in info:
            output += f"- **营业利润率**：{info.get('operatingMargins', 0)*100:.2f}%\n"
        if 'netMargins' in info:
            output += f"- **净利率**：{info.get('netMargins', 0)*100:.2f}%\n"
        if 'roe' in info:
            output += f"- **ROE**：{info.get('roe', 0)*100:.2f}%\n"

        # 财务健康
        output += "\n### 财务健康\n\n"
        if 'debtToEquity' in info:
            output += f"- **资产负债率(债务/权益)**：{info.get('debtToEquity', 'N/A'):.2f}\n"
        if 'currentRatio' in info:
            output += f"- **流动比率**：{info.get('currentRatio', 'N/A'):.2f}\n"
        if 'quickRatio' in info:
            output += f"- **速动比率**：{info.get('quickRatio', 'N/A'):.2f}\n"

    # 技术指标
    if technical:
        output += "\n## 技术指标\n\n"
        output += f"- **MA5**：{technical.get('ma5', 'N/A'):.2f}\n" if technical.get('ma5') else "- **MA5**：N/A\n"
        output += f"- **MA20**：{technical.get('ma20', 'N/A'):.2f}\n" if technical.get('ma20') else "- **MA20**：N/A\n"
        output += f"- **MA60**：{technical.get('ma60', 'N/A'):.2f}\n" if technical.get('ma60') else "- **MA60**：N/A\n"
        output += f"- **MA200**：{technical.get('ma200', 'N/A'):.2f}\n" if technical.get('ma200') else "- **MA200**：N/A\n"
        output += f"- **RSI(14)**：{technical.get('rsi', 'N/A'):.2f}\n" if technical.get('rsi') else "- **RSI(14)**：N/A\n"
        output += f"- **MACD**：{technical.get('macd', 'N/A'):.4f}\n" if technical.get('macd') else "- **MACD**：N/A\n"
        output += f"- **MACD Signal**：{technical.get('macd_signal', 'N/A'):.4f}\n" if technical.get('macd_signal') else "- **MACD Signal**：N/A\n"
        output += f"- **MACD Histogram**：{technical.get('macd_hist', 'N/A'):.4f}\n" if technical.get('macd_hist') else "- **MACD Histogram**：N/A\n"
        output += f"- **布林上轨**：{technical.get('bb_upper', 'N/A'):.2f}\n" if technical.get('bb_upper') else "- **布林上轨**：N/A\n"
        output += f"- **布林中轨**：{technical.get('bb_mid', 'N/A'):.2f}\n" if technical.get('bb_mid') else "- **布林中轨**：N/A\n"
        output += f"- **布林下轨**：{technical.get('bb_lower', 'N/A'):.2f}\n" if technical.get('bb_lower') else "- **布林下轨**：N/A\n"
        output += f"- **ATR(14)**：{technical.get('atr', 'N/A'):.2f}\n" if technical.get('atr') else "- **ATR(14)**：N/A\n"

    # 价格数据摘要
    if not prices.empty:
        output += "\n## 价格数据摘要\n\n"
        output += f"- **最新收盘价**：{prices['Close'].iloc[-1]:.2f}\n"
        output += f"- **期间最高价**：{prices['High'].max():.2f}\n"
        output += f"- **期间最低价**：{prices['Low'].min():.2f}\n"
        output += f"- **期间涨跌幅**：{((prices['Close'].iloc[-1] / prices['Close'].iloc[0]) - 1) * 100:.2f}%\n"
        output += f"- **数据区间**：{prices.index[0].strftime('%Y-%m-%d')} 至 {prices.index[-1].strftime('%Y-%m-%d')}\n"

    # 财务数据
    if financial_data:
        output += "\n## 财务数据详情\n\n"
        for key, df in financial_data.items():
            if isinstance(df, pd.DataFrame) and not df.empty:
                output += f"\n### {key}\n\n"
                output += df.head(8).to_markdown() + "\n"

    output += "\n---\n\n*数据来源：Yahoo Finance, Akshare, 东方财富*\n"
    output += f"*采集时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"

    return output


def main():
    parser = argparse.ArgumentParser(description='获取股票数据')
    parser.add_argument('stock', help='股票名称或代码')
    parser.add_argument('--market', choices=['CN', 'US', 'HK'], default='CN', help='市场')
    parser.add_argument('--period', default='1y', help='数据周期：1y, 2y, 5y, max')
    parser.add_argument('--output', help='输出文件路径')

    args = parser.parse_args()

    # 解析股票代码
    code = resolve_stock_code(args.stock, args.market)

    print(f"正在获取 {args.stock} ({code}) 的数据...")

    # 根据市场获取数据
    if args.market == 'CN':
        info = get_stock_info_cn(code.replace('.SS', '').replace('.SZ', ''))
        yf_code = code  # yfinance使用完整代码
    else:
        info = get_stock_info_us(code)
        yf_code = code

    # 获取财务数据
    if args.market == 'CN':
        financial_data = get_financial_data_cn(code.replace('.SS', '').replace('.SZ', ''))
    else:
        financial_data = get_financial_data_us(code)

    # 获取历史价格
    prices = get_historical_prices(yf_code, args.period)

    # 计算技术指标
    technical = calculate_technical_indicators(prices)

    # 输出
    output_content = output_markdown(args.stock, code, info, financial_data, prices, technical)

    if args.output:
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output_content)
        print(f"数据已保存到: {args.output}")
    else:
        # 默认输出到 _temp/stock-data.md
        temp_dir = '_temp'
        os.makedirs(temp_dir, exist_ok=True)
        output_path = os.path.join(temp_dir, 'stock-data.md')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_content)
        print(f"数据已保存到: {output_path}")

    print("\n" + output_content)


if __name__ == '__main__':
    main()