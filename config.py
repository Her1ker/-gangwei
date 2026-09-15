"""
Campus Radar 配置文件
修改这里的配置来定制你的秋招监控。
"""

# ==================== 监控公司开关 ====================
# 把不想监控的公司设为 False 即可
ENABLED_COMPANIES = {
    "美团": True,
    "顺丰": True,
    "迈瑞医疗": True,
    "美的": True,
    "字节跳动（公告）": True,
    "得物（公告）": True,
    "三一（公告）": True,
    "京东": True,
    "快手": True,
    "小红书": True,
    "拼多多": True,
    "淘宝": True,
    "offerstar": True,   # 聚合平台，补充行业动态
}

# ==================== 岗位关键词 ====================
# 简报会优先按"职位类别"过滤，再用关键词对岗位标题做兜底匹配
# 想加方向直接往里加关键词即可
KEYWORDS = {
    "电商运营": [
        "电商运营",
        "平台运营",
        "商家运营",
        "商家成长",
        "商家拓展",
        "商家管理",
        "店铺运营",
        "商品运营",
        "品类运营",
        "行业运营",
        "交易运营",
        "用户增长",
        "电商活动运营",
        "直播电商",
        "直播运营",
        "内容电商",
        "跨境电商",
        "跨境运营",
        "渠道运营",
        "电商管培生",
        "采销管培生"
    ],
    "企业销售（ToB）": [
        "ToB销售",
        "B端销售",
        "企业销售",
        "企业客户",
        "企业业务",
        "政企销售",
        "政企业务",
        "大客户销售",
        "大客户经理",
        "客户经理",
        "客户代表",
        "销售代表",
        "销售工程师",
        "解决方案销售",
        "行业销售",
        "渠道销售",
        "渠道拓展",
        "渠道经理",
        "商务拓展",
        "商务开发",
        "商务合作",
        "BD",
        "商业化销售",
        "广告销售",
        "客户成功",
        "销售管培生",
        "营销管培生",
        "国际销售",
        "海外销售"
    ],
    "供应链与采购": [
        "供应链",
        "供应链管理",
        "供应链运营",
        "供应链计划",
        "供应链分析",
        "采购",
        "采购管理",
        "采购专员",
        "采购工程师",
        "战略采购",
        "品类采购",
        "采购寻源",
        "供应商管理",
        "供应商开发",
        "采销",
        "需求计划",
        "供应计划",
        "生产计划",
        "物料计划",
        "库存管理",
        "订单管理",
        "物流管理",
        "物流运营",
        "仓储管理",
        "仓储运营",
        "运输管理",
        "配送管理",
        "履约运营",
        "国际物流",
        "进出口",
        "供应链管培生",
        "物流管培生"
    ]
}

# 仅使用明确相关的类别，避免泛产品、泛运营匹配。
CATEGORY_KEYWORDS = ["电商", "商家", "采销", "企业销售", "ToB", "B端销售", "政企", "大客户", "渠道销售", "商务拓展", "客户成功", "供应链", "采购", "物流", "仓储"]

# ==================== 目标城市 ====================
# 留空 [] 表示全国都看；填了就只看这些城市
# 注意：部分公司（如小红书）按城市过滤，填这里会精确过滤
TARGET_CITIES = ["上海", "北京", "杭州", "深圳", "广州", "长沙"]

# ==================== 各公司专属参数 ====================
COMPANY_CONFIG = {
    "京东": {
        # 应届生招聘类型，type=present 表示应届生
        "type": "present",
    },
    "快手": {
        # 27届校招项目代码（从官网 URL 里提取）
        "recruit_sub_project_codes": ["20271779425607"],
    },
    "小红书": {
        # term_regular = 应届生校招
        "campus_recruit_types": ["term_regular"],
        # workplace 城市编码（4401=上海）。留空则不限城市
        "workplaces": [],  # [] = 全国
    },
    "拼多多": {
        # t=null 表示全部类别，也可填具体类别 job code
        "t": None,
    },
    "淘宝": {
        # batchId 会自动获取，这里留默认即可
        "batch_channel": "campus_group_official_site",
    },
    "offerstar": {
        # 聚合平台查询参数
        "title": "2027",
        "positions": ["电商", "运营", "销售", "商务", "供应链", "采购", "物流"],  # 搜索后按关键词细筛
        "channel": "校招",
    },
}

# ==================== 通用抓取源（零代码添加新公司）====================
# 后续添加新公司，只需在这里加一段配置即可，无需写代码！
# 配置格式见 scrapers/generic.py 文件顶部说明。
#
# 示例（取消注释并修改即可启用）：
#
# GENERIC_SOURCES = [
#     {
#         "name": "某公司",
#         "type": "api",                          # api 或 html
#         "url": "https://example.com/api/jobs",
#         "method": "POST",
#         "headers": {"Content-Type": "application/json"},
#         "body_template": {"page": "{page}", "size": 100},
#         "pagination": {"page_start": 1, "page_key": "page", "stop_when": "less_than_size"},
#         "response": {"list_path": "data.list", "total_path": "data.total"},
#         "fields": {
#             "job_id": "id", "title": "positionName", "category": "jobType",
#             "location": "workCity", "publish_time": "createTime",
#         },
#         "detail_url_template": "https://example.com/jobs/{job_id}",
#         "timestamp_field": "createTime",
#     },
# ]
GENERIC_SOURCES = []

# ==================== 运行参数 ====================
# 请求超时（秒）
REQUEST_TIMEOUT = 20
# 失败重试次数
MAX_RETRIES = 2
# 每页抓取条数（尽量大，减少翻页）
PAGE_SIZE = 100
# User-Agent
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)
