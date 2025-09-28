# ==============================================================================
# AI Frontier Pulse - 自动情报聚合与分析引擎 (RSS稳定版)
# ==============================================================================
import os
import datetime
import logging
import json
import random
from typing import List, Dict, Optional

# --- 依赖项检查与导入 ---
try:
    import feedparser
    import dashscope
    from dotenv import load_dotenv
    from bs4 import BeautifulSoup # 用于从HTML内容中提取纯文本
except ImportError as e:
    logging.error(f"关键模块导入失败: {e}")
    logging.error("请确保已安装所有必需的依赖项。")
    logging.error("请在终端运行: pip install feedparser dashscope python-dotenv beautifulsoup4")
    exit(1)

# --- 1. 全局配置模块 ---

# 加载环境变量 (API Key)
load_dotenv()

# 日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')

# 全球化、高质量的RSS信源配置
TARGET_FEEDS = [
    {"name": "36氪-AIGC", "url": "https://36kr.com/information/web_news/aigc/feed"},
    {"name": "TechCrunch-AI", "url": "https://techcrunch.com/category/artificial-intelligence/feed/"},
    {"name": "VentureBeat-AI", "url": "https://venturebeat.com/category/ai/feed/"},
    {"name": "Y Combinator Blog", "url": "https://www.ycombinator.com/blog/rss"},
    {"name": "InfoQ-AI", "url": "https://www.infoq.cn/topic/AI/feed"},
    {"name": "机器之心", "url": "https://www.jiqizhixin.com/rss"},
    {"name": "Google AI Blog", "url": "https://ai.googleblog.com/feeds/posts/default?alt=rss"},
]
# 每天从所有聚合文章中，随机选取分析的总数上限，以控制API成本
TOTAL_ARTICLES_TO_ANALYZE = 15

# --- AI 分析配置 ---
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
if not dashscope.api_key:
    logging.error("致命错误: 未找到 DASHSCOPE_API_KEY 环境变量。请在项目根目录的 .env 文件中设置。")
    exit(1)

AI_MODEL = "qwen-plus"  # 使用效果更好的模型
AI_PROMPT_TEMPLATE = """
# 角色
你是一名顶级的AI行业分析师，为一家全球领先的VC工作。你的任务是为合伙人筛选、提炼和点评每日的AI行业动态。你的风格必须：专业、精准、一针见血。

# 任务
请阅读以下文章的标题和摘要内容，并以严格的JSON格式提取关键信息。

# 约束与规则
1.  **分类 (category):** 必须从以下列表中选择一个最贴切的：[`融资事件`, `产品发布`, `技术突破`, `市场报告`, `人物观点`, `开源社区`]
2.  **标签 (tags):** 提取3-5个最核心的关键词作为标签，例如具体的公司名、技术术语、项目名等。
3.  **摘要 (summary):** 用不超过60个字的中文，对原文摘要进行再次精炼，总结出文章的核心内容。
4.  **洞察 (insight):** 站在VC投资人的视角，用一句话点评该事件的潜在影响、机会或风险。语言要犀利、有前瞻性。
5.  所有输出都必须是中文。
6.  如果文章内容质量过低或与AI无关，所有字段请返回 "N/A"。

# 文章信息
标题: "{title}"
摘要内容:
{content}

# 输出格式 (严格遵守此JSON结构，不要有任何多余的解释)
{{
  "category": "...",
  "tags": ["...", "...", "..."],
  "summary": "...",
  "insight": "..."
}}
"""

# --- 2. 核心功能模块 ---

def scrape_all_rss_feeds() -> List[Dict[str, str]]:
    """
    遍历所有RSS源，解析文章，并聚合成统一格式的列表。
    这是一个稳定且高效的数据获取方法。
    """
    all_articles = []
    for feed_info in TARGET_FEEDS:
        logging.info(f"--- 正在处理RSS源: {feed_info['name']} ---")
        try:
            # feedparser 会自动处理请求、解析和标准化
            parsed_feed = feedparser.parse(feed_info['url'])
            
            if parsed_feed.bozo: # bozo=1表示RSS源格式可能有问题
                logging.warning(f"警告: '{feed_info['name']}' 的RSS源可能格式不正确或无法访问。错误: {parsed_feed.bozo_exception}")
                continue

            for entry in parsed_feed.entries:
                title = entry.get('title', '无标题')
                link = entry.get('link', '#')
                
                # 优先使用 content，其次是 summary，最后是 description
                raw_content = entry.get('content', [{}])[0].get('value', entry.get('summary', entry.get('description', '')))
                
                # 使用BeautifulSoup从HTML内容中提取纯文本，去除HTML标签
                soup = BeautifulSoup(raw_content, 'html.parser')
                plain_text_content = soup.get_text(separator=' ', strip=True)

                all_articles.append({
                    "title": title,
                    "link": link,
                    "content": plain_text_content, # 现在是纯文本内容
                    "source": feed_info['name']
                })
            logging.info(f"从 {feed_info['name']} 成功聚合 {len(parsed_feed.entries)} 篇文章。")
        except Exception as e:
            logging.error(f"处理 '{feed_info['name']}' RSS源时发生未知异常: {e}")
            
    return all_articles

def analyze_article_with_ai(article: Dict[str, str]) -> Optional[Dict[str, any]]:
    """
    使用通义千问(Qwen)模型分析单篇文章。
    """
    logging.info(f"开始Qwen-AI分析文章: '{article['title']}'")
    # 为了节省token和提高效率，我们只把内容的前1000个字符发给AI
    content_snippet = (article['content'] or "")[:1000]
    prompt = AI_PROMPT_TEMPLATE.format(title=article['title'], content=content_snippet)
    
    try:
        response = dashscope.Generation.call(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": "You are a professional AI industry analyst."},
                {"role": "user", "content": prompt}
            ],
            result_format='json_object',
            temperature=0.5,
        )
        
        if response.status_code == 200:
            analysis_result = response.output.text
            # 增加一层JSON解析的错误处理，防止AI返回非标准JSON
            try:
                return json.loads(analysis_result)
            except json.JSONDecodeError:
                logging.error(f"AI返回了非JSON格式的内容: {analysis_result}")
                return None
        else:
            logging.error(f"Qwen API 调用失败: '{article['title']}'. Code: {response.status_code}, Msg: {response.message}")
            return None

    except Exception as e:
        logging.error(f"Qwen-AI分析过程中发生异常: '{article['title']}'. 错误: {e}")
        return None

def create_daily_report_markdown(analyzed_articles: List[Dict[str, any]]):
    """
    将分析结果生成为符合MkDocs博客规范的Markdown文件。
    """
    if not analyzed_articles:
        logging.warning("没有可供生成的分析结果，已跳过文件创建。")
        return

    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")
    
    output_dir = os.path.join("docs", "radar")
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{today_str}.md")
    
    logging.info(f"开始生成日报Markdown文件: {filepath}")

    all_tags = set()
    for article in analyzed_articles:
        if isinstance(article.get("tags"), list):
            all_tags.update(article["tags"])

    frontmatter = f"---\ndate: {today_str}\ncategories:\n  - Daily Brief\ntags:\n"
    for tag in sorted(list(all_tags)):
        frontmatter += f"  - {tag}\n"
    frontmatter += "---\n\n"

    main_content = f"# AI前沿脉搏日报: {today.strftime('%Y年%m月%d日')}\n\n"
    main_content += "由AI自动聚合、分析和生成的每日AI行业动态简报。\n\n---\n\n"

    for article in analyzed_articles:
        main_content += f"## {article.get('original_title', '未知标题')}\n\n"
        main_content += f"**来源:** [{article.get('source', 'N/A')}]({article.get('link', '#')})  \n"
        main_content += f"**摘要:** {article.get('summary', 'N/A')}  \n"
        main_content += f"> **VC洞察:** {article.get('insight', 'N/A')}  \n\n"
        main_content += f"**分类:** `{article.get('category', 'N/A')}`  \n"
        
        tags = article.get('tags', [])
        if isinstance(tags, list):
            tags_str = ", ".join([f"`{tag}`" for tag in tags])
            main_content += f"**标签:** {tags_str}\n\n"
        
        main_content += "---\n\n"

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(frontmatter + main_content)
        logging.info(f"日报文件已成功生成: {filepath}")
    except IOError as e:
        logging.error(f"写入文件失败: {e}")

# --- 3. 主流程控制 ---

def main():
    """
    主执行函数，协调整个情报聚合与分析流程。
    """
    logging.info("==========================================================")
    logging.info("===== 开始执行RSS聚合AI雷达任务 (由Qwen驱动) =====")
    logging.info("==========================================================")
    
    # Step 1: 从所有RSS源稳定、高效地聚合文章
    all_raw_articles = scrape_all_rss_feeds()
    
    if not all_raw_articles:
        logging.warning("所有信源均未能聚合到任何文章，任务结束。")
        return

    logging.info(f"成功从所有源聚合了 {len(all_raw_articles)} 篇文章。")

    # Step 2: 随机打乱并截取部分文章进行分析，以控制成本和时间
    random.shuffle(all_raw_articles)
    articles_to_analyze = all_raw_articles[:TOTAL_ARTICLES_TO_ANALYZE]
    logging.info(f"将从聚合结果中随机选取 {len(articles_to_analyze)} 篇进行AI分析。")

    # Step 3: 对筛选后的文章进行AI分析
    analyzed_articles = []
    for article in articles_to_analyze:
        analysis_data = analyze_article_with_ai(article)
        if analysis_data and analysis_data.get("summary") != "N/A":
            # 将原始信息和分析结果合并
            combined_data = {**article, **analysis_data, "original_title": article["title"]}
            analyzed_articles.append(combined_data)

    # Step 4: 生成最终的Markdown报告
    create_daily_report_markdown(analyzed_articles)
    
    logging.info("==========================================================")
    logging.info("===== 每日AI雷达任务执行完毕 =====")
    logging.info("==========================================================")

if __name__ == "__main__":
    main()