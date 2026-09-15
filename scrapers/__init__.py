"""scrapers 包"""
from .jd import JdScraper
from .kuaishou import KuaishouScraper
from .xiaohongshu import XiaohongshuScraper
from .pdd import PddScraper
from .taotian import TaotianScraper
from .offerstar import OfferstarScraper
from .generic import GenericScraper

# 内置抓取器（每个公司一个专用类）
SCRAPERS = {
    "京东": JdScraper,
    "快手": KuaishouScraper,
    "小红书": XiaohongshuScraper,
    "拼多多": PddScraper,
    "淘宝": TaotianScraper,
    "offerstar": OfferstarScraper,
}

from .expanded import (MeituanScraper, SfScraper, MindrayScraper, MideaScraper,
                       ByteAnnouncementScraper, DewuAnnouncementScraper, SanyAnnouncementScraper)

SCRAPERS.update({
    "美团": MeituanScraper, "顺丰": SfScraper, "迈瑞医疗": MindrayScraper, "美的": MideaScraper,
    "字节跳动（公告）": ByteAnnouncementScraper, "得物（公告）": DewuAnnouncementScraper,
    "三一（公告）": SanyAnnouncementScraper,
})
