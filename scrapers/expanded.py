"""Additional official campus recruitment sources; fail explicitly on API errors."""
from datetime import datetime
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from .base import BaseScraper, JobItem, guess_category
import config


def date_text(value):
    if isinstance(value, (int, float)) and value > 0:
        return datetime.fromtimestamp(value / 1000).strftime('%Y-%m-%d')
    value = str(value or '')
    return '' if value.startswith('0001') else value[:10]


def names(values):
    return '、'.join(str(v.get('name') or v.get('Name') or '') if isinstance(v, dict) else str(v) for v in (values or []))


class MeituanScraper(BaseScraper):
    name = '美团'

    def fetch(self):
        jobs = {}
        for page in range(1, 101):
            payload = {'page': {'pageNo': page, 'pageSize': 100}, 'jobShareType': '1',
                       'keywords': '', 'cityList': [], 'department': [], 'jfJgList': [],
                       'jobType': [{'code': '1', 'subCode': []}], 'typeCode': [], 'specialCode': []}
            r = self.session.post('https://job.meituan.com/api/official/job/getJobList', json=payload, timeout=config.REQUEST_TIMEOUT)
            r.raise_for_status()
            result = r.json()
            if result.get('status') != 1 or not isinstance(result.get('data'), dict):
                raise RuntimeError('美团岗位接口返回异常')
            data = result['data']
            if not isinstance(data.get('list'), list):
                raise RuntimeError('美团岗位列表格式变化')
            for item in data['list']:
                if str(item.get('jobType')) != '1':
                    continue
                key = str(item['jobUnionId'])
                title = item['name']
                jobs[key] = JobItem(self.name, key, title,
                    category=guess_category(title) or item.get('jobFamilyGroup') or item.get('jobFamily') or '',
                    location=names(item.get('cityList')),
                    url=f'https://job.meituan.com/web/position/detail?jobUnionId={key}&jobShareType=1',
                    publish_time=date_text(item.get('refreshTime')),
                    tags='校招 / ' + str(item.get('projectName') or '届别以岗位要求为准'))
            if not data['list'] or page >= data['page']['totalPage']:
                return list(jobs.values())
        raise RuntimeError('美团分页超过限制，未返回不完整数据')


class SfScraper(BaseScraper):
    name = '顺丰'

    def fetch(self):
        jobs = {}
        for page in range(1, 101):
            r = self.session.get('https://campus.sf-express.com/api/web/position/query',
                params={'pageNum': page, 'pageSize': 100, 'staffGroup': 'A'}, timeout=config.REQUEST_TIMEOUT)
            r.raise_for_status()
            data = r.json()
            if not isinstance(data.get('list'), list) or 'isLastPage' not in data:
                raise RuntimeError('顺丰岗位列表格式变化')
            for item in data['list']:
                key = str(item['id'])
                title = item['positionName']
                jobs[key] = JobItem(self.name, key, title,
                    category=guess_category(title) or item.get('positionTypeName') or '',
                    location=item.get('demandCity') or '',
                    url=f'https://campus.sf-express.com/m/#/positionDetail/{key}',
                    publish_time=date_text(item.get('createDate')),
                    tags='校招 / ' + (item.get('orgSourceName') or ''))
            if data['isLastPage'] or not data['list']:
                return list(jobs.values())
        raise RuntimeError('顺丰分页超过限制，未返回不完整数据')


class MindrayScraper(BaseScraper):
    name = '迈瑞医疗'

    def fetch(self):
        jobs = {}
        for page in range(0, 100):
            r = self.session.post('https://career.mindray.com/api/Jobad/GetJobAdPageList',
                json={'PageIndex': page, 'PageSize': 10, 'Category': 2}, timeout=config.REQUEST_TIMEOUT)
            r.raise_for_status()
            data = r.json()
            if data.get('Code') != 200 or not isinstance(data.get('Data'), list):
                raise RuntimeError('迈瑞岗位接口返回异常')
            before = len(jobs)
            for item in data['Data']:
                if str(item.get('CategoryId')) != '2':
                    raise RuntimeError('迈瑞校招筛选失效')
                key = str(item['JobAdId'])
                title = item['JobAdName']
                jobs[key] = JobItem(self.name, key, title, category=guess_category(title),
                    location=names(item.get('LocNames')),
                    url=f'https://career.mindray.com/campus/detail?jobAdId={key}',
                    publish_time=date_text(item.get('ChangeDate') or item.get('PostDate')),
                    tags='校招 / 地点及届别请查看岗位详情')
            if len(jobs) >= data['Count']:
                return list(jobs.values())
            if len(jobs) == before:
                raise RuntimeError('迈瑞分页重复，未返回不完整数据')
        raise RuntimeError('迈瑞分页超过限制，未返回不完整数据')


class MideaScraper(BaseScraper):
    name = '美的'
    base = 'https://careers.midea.com/backend/'

    def fetch(self):
        r = self.session.get(self.base + 'school/position/common/project/list', timeout=config.REQUEST_TIMEOUT)
        r.raise_for_status()
        result = r.json()
        if result.get('code') != '0' or not isinstance(result.get('data'), list):
            raise RuntimeError('美的招聘项目接口返回异常')
        projects = [p for p in result['data'] if str(p.get('projectType')) == '1'
                    and str(p.get('numberOfSessions')) == '2027']
        jobs = {}
        for project in projects:
            project_id = project['projectRuleId']
            seen = set()
            for page in range(1, 101):
                body = {'keyword': '', 'superiorIds': [], 'recruitCategoryIds': [], 'workPlaceCodes': [],
                        'projectRuleId': project_id, 'pageIndex': page, 'pageSize': 20}
                r = self.session.post(self.base + 'school/position/common/position/list', json=body, timeout=config.REQUEST_TIMEOUT)
                r.raise_for_status()
                data = r.json()
                if data.get('code') != '0' or not isinstance(data.get('data'), dict):
                    raise RuntimeError('美的岗位接口返回异常')
                data = data['data']
                if not isinstance(data.get('data'), list) or 'total' not in data:
                    raise RuntimeError('美的岗位列表格式变化')
                before = len(seen)
                for item in data['data']:
                    key = str(item['projectPositionId'])
                    seen.add(key)
                    title = item['projectPositionName']
                    link = urlencode({'positionId': item['positionId'], 'projectRuleId': project_id,
                                      'recruitCategoryId': item['recruitCategoryId']})
                    jobs[key] = JobItem(self.name, key, title,
                        category=guess_category(title) or item.get('recruitCategoryName') or '',
                        location='、'.join(v.get('workPlaceName') or '' for v in item.get('workplaceDtoList', [])),
                        url='https://careers.midea.com/school-wechat/detail?' + link,
                        tags=project['projectRuleName'])
                if len(seen) >= data['total']:
                    break
                if len(seen) == before:
                    raise RuntimeError('美的分页缺失或重复')
            else:
                raise RuntimeError('美的分页超过限制')
        return list(jobs.values())


class CompanyAnnouncementScraper(BaseScraper):
    """OfferStar company-filtered announcements, explicitly not full official job coverage."""
    company_query = ''

    def fetch(self):
        from .offerstar import OfferstarScraper
        jobs = {}
        # A targeted company query avoids losing older announcements behind unrelated companies.
        previous = None
        for page in range(1, 21):
            r = self.session.get('https://www.offerstar.cn/recruitment',
                params={'company': self.company_query, 'title': '2027', 'channel': '校招', 'page': page},
                timeout=config.REQUEST_TIMEOUT)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, 'html.parser')
            if soup.find('table') is None:
                raise RuntimeError('公告平台未返回列表，可能出现验证或页面改版')
            items = OfferstarScraper(self.session)._parse_html(r.text)
            signature = tuple(j.dedup_key for j in items)
            if not items:
                break
            if signature == previous:
                raise RuntimeError('公告平台分页未生效')
            previous = signature
            for job in items:
                if self.company_query not in job.company:
                    raise RuntimeError('公告平台公司筛选未生效')
                job.company = self.name
                job.tags = 'OfferStar聚合公告；不代表官网完整岗位列表'
                jobs[job.job_id] = job
            if len(items) < 20:
                break
        else:
            raise RuntimeError('公司公告分页超过限制')
        return list(jobs.values())


class ByteAnnouncementScraper(CompanyAnnouncementScraper):
    name = '字节跳动（公告）'
    company_query = '字节跳动'


class DewuAnnouncementScraper(CompanyAnnouncementScraper):
    name = '得物（公告）'
    company_query = '得物'


class SanyAnnouncementScraper(CompanyAnnouncementScraper):
    name = '三一（公告）'
    company_query = '三一'
