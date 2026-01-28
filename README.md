# CS饰品行情助手

一个基于Flask的CS:GO饰品行情查询工具，提供实时价格、涨跌幅分析和K线图展示。

## 功能特点

- 📊 **大盘指数** - 实时查看CS饰品市场整体走势
- 📈 **涨幅榜** - 查看涨幅最大的饰品，支持24h/7日/30日/90日排序
- 📉 **跌幅榜** - 查看跌幅最大的饰品
- 🔪 **匕首/手套** - 专门的匕首和手套行情
- 🔍 **搜索功能** - 快速查找特定饰品
- 📉 **K线图** - 每个饰品都有15/30/90日走势图
- 🎨 **二次元背景** - 随机二次元插画背景，可切换

## 本地运行

```bash
pip install -r requirements.txt
python web_app.py
```

访问 http://127.0.0.1:5001

## 部署

支持部署到Railway、Render等平台。

## 技术栈

- **后端**: Flask + Python
- **前端**: HTML + JavaScript + Chart.js
- **数据源**: CSQAQ API

## 截图

![主界面](screenshot.png)

## 许可

MIT License
