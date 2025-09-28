---
title: Home
---

<!-- 
  Hero Section: A big, bold statement to capture attention.
  We use custom CSS classes for styling which you can add later.
-->
<div class="hero">
  <div class="hero-text">
    <h1>AI Frontier Pulse</h1>
    <p>Your Automated Signal in the Noise of AI.</p>
  </div>
</div>

<!-- 
  Grid Cards Section: The core of the dashboard.
  This provides quick access to the most important parts of the site.
-->
<div class="grid cards" markdown>

-   __**🚀 最新AI简报**__

    ---

    汇集每日全球AI领域最前沿的动态。所有内容均由AI自动抓取、分析和提炼，为您节省宝贵的时间。

    [:octicons-arrow-right-24: 进入雷达](radar/index.md)

-   __**📊 按分类探索**__

    ---

    深入研究特定领域的动态。从 `融资事件` 到 `技术突破`，快速定位您最关心的信息类别。

    [:octicons-arrow-right-24: 查看所有分类](categories.md)

-   __**💡 关于本项目**__

    ---

    了解 "AI Frontier Pulse" 背后的技术栈、工作原理和AI方法论。探索我是如何从0到1构建这个自动化信息流产品的。

    [:octicons-arrow-right-24: 了解更多](about.md)

</div>

---

### 今日焦点 (Today's Highlight)

> 由AI根据今日动态的重要性自动筛选出的焦点信息。

!!! quote "传闻OpenAI正在秘密开发下一代模型 "Q*""

    **摘要:** 根据多方消息源，OpenAI正在进行一个名为 "Q*" (Q-Star) 的秘密项目，该项目旨在实现通用人工智能（AGI）的重大突破，其逻辑和推理能力远超现有模型。
    
    **VC洞察:** 如果属实，这不仅会重塑当前的AI市场格局，更可能引发新一轮的技术竞赛和资本狂潮。需要密切关注其后续的官方发布和技术细节。
    
    **分类:** `技术突破`
    **标签:** `OpenAI`, `AGI`, `Q-Star`

---

### 核心能力 (Core Features)

<div class="grid" markdown>
<div class="feature-item">
    <span class="feature-icon">:material-robot-happy-outline:</span>
    <h4>全流程自动化</h4>
    <p>从数据采集、AI分析到网站发布，整个流程由GitHub Actions驱动，实现每日无人值守自动更新。</p>
</div>
<div class="feature-item">
    <span class="feature-icon">:material-brain:</span>
    <h4>LLM驱动的洞察</h4>
    <p>不仅仅是信息聚合。每一条动态都经过大语言模型的深度分析，提炼出摘要、分类和富有前瞻性的VC洞察。</p>
</div>
<div class="feature-item">
    <span class="feature-icon">:material-auto-fix:</span>
    <h4>结构化数据</h4>
    <p>所有信息都通过标签和分类进行结构化处理，方便用户进行深度检索和研究，将噪音转化为有价值的信号。</p>
</div>
</div>

<style>
  /* 
    Custom CSS for the Hero section.
    MkDocs Material allows adding custom CSS like this.
  */
  .hero {
    background: linear-gradient(90deg, #121212 0%, #1E1E1E 100%);
    padding: 4rem 2rem;
    text-align: center;
    border-radius: 0.5rem;
    margin-bottom: 2rem;
  }
  .hero-text h1 {
    font-size: 3rem;
    font-weight: 700;
    color: #00BFFF; /* Deep Sky Blue */
    margin: 0;
  }
  .hero-text p {
    font-size: 1.2rem;
    color: #E0E0E0;
    margin-top: 0.5rem;
  }
  .feature-item {
    text-align: center;
  }
  .feature-icon {
    font-size: 3rem;
    color: #00BFFF;
  }
</style>