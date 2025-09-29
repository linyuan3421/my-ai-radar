# AI前沿雷达

自动聚合、分析和生成每日AI行业动态简报。

## 功能特点

- 自动抓取主流科技媒体AI频道的最新资讯
- 利用大语言模型进行智能筛选、分类和点评
- 生成结构化的每日简报，便于快速了解行业动态
- 输出为MkDocs格式，可直接构建静态博客

## 安装依赖

```bash
pip install -r requirements.txt
```

或者

```bash
pip install .
```

## 配置

1. 复制 `.env.example` 为 `.env`
2. 在 `.env` 文件中设置你的 `DASHSCOPE_API_KEY`

## 运行

```bash
python scripts/run.py
```

## 项目结构

```
ai-radar-project/
├── scripts/
│   └── run.py          # 主程序
├── docs/
│   └── radar/          # 生成的日报存放目录
├── assets/             # 静态资源
├── requirements.txt    # 项目依赖
└── mkdocs.yml          # MkDocs配置
```