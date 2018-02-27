#encoding: utf-8
import scrapy
import re
import uuid
import datetime
from scrapy.selector import Selector
from news.items import GenericItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

class LeadersSpider(CrawlSpider):
    name='leaders'
    source = "新华网——领导人活动"
    allowed_domains = ["xinhuanet.com"]
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday1 = yesterday.strftime('%Y-%m/%d')
    yesterday2=yesterday.strftime('%Y%m%d')
    reg='('+yesterday1+')|('+yesterday2+')'
    start_urls = [
        'http://www.bj.xinhuanet.com/bjzw/swsj/zyjh.htm',
        'http://www.bj.xinhuanet.com/bjzw/swsj/zxhd.htm',
        'http://www.bj.xinhuanet.com/bjzw/rdzr/zyjh.htm',
        'http://www.bj.xinhuanet.com/bjzw/rdzr/zxhd.htm',
        'http://www.bj.xinhuanet.com/bjzw/zxzx/zyjh.htm',
        'http://www.bj.xinhuanet.com/bjzw/zxzx/zxhd.htm',  # 北京
        'http://www.sh.xinhuanet.com/leaders/hz/zyjh.htm',
        'http://www.sh.xinhuanet.com/leaders/hz/zxhd.htm',
        'http://www.sh.xinhuanet.com/leaders/yyc/zyjh.htm',
        'http://www.sh.xinhuanet.com/leaders/yyc/zxhd.htm',
        'http://www.sh.xinhuanet.com/leaders/yy/zyjh.htm',
        'http://www.sh.xinhuanet.com/leaders/yy/zxhd.htm',
        'http://www.sh.xinhuanet.com/leaders/wzm/zyjh.htm',
        'http://www.sh.xinhuanet.com/leaders/wzm/zxhd.htm',  # 上海
        # 天津特殊
        'http://www.cq.xinhuanet.com/cq/szc_more.htm',
        'http://www.cq.xinhuanet.com/cq/szc_more1.htm',
        'http://www.cq.xinhuanet.com/cq/zx_more.htm',
        'http://www.cq.xinhuanet.com/cq/zgq_more.htm',
        'http://www.cq.xinhuanet.com/cq/zgq_more1.htm',
        'http://www.cq.xinhuanet.com/cq/xjy_more.htm',  # 重庆
        # 河北特殊
        'http://www.sx.xinhuanet.com/sxzw/leaders/luohn/zyjh.htm',
        'http://www.sx.xinhuanet.com/sxzw/leaders/luohn/zxbd.htm',
        'http://www.sx.xinhuanet.com/sxzw/leaders/louys/zyjh.htm',
        'http://www.sx.xinhuanet.com/sxzw/leaders/louys/zxhd.htm',
        'http://www.sx.xinhuanet.com/sxzw/leaders/xyz/zyjh.htm',
        'http://www.sx.xinhuanet.com/sxzw/leaders/xyz/zxbd.htm', # 山西
        'http://www.nmg.xinhuanet.com/ldhd/dwwjlibrary/zyjh.htm',
        'http://www.nmg.xinhuanet.com/ldhd/dwwjlibrary/zxhd.htm',
        'http://www.nmg.xinhuanet.com/ldhd/zfzxlibrary/zyjh.htm',
        'http://www.nmg.xinhuanet.com/ldhd/zfzxlibrary/zxbd.htm',
        'http://www.nmg.xinhuanet.com/ldhd/zxzxlibrary/zxhd.htm',
        'http://www.nmg.xinhuanet.com/ldhd/zxzxlibrary/zyjh.htm',  # 内蒙
        # 辽宁特殊
        'http://www.jl.xinhuanet.com/jlld/11zxhd.htm',
        'http://www.jl.xinhuanet.com/jlld/11zyjh.htm',
        'http://www.jl.xinhuanet.com/jlld/33zyjh.htm',
        'http://www.jl.xinhuanet.com/jlld/33zxhd.htm',  # 吉林
        'http://hlj.xinhuanet.com/ldhd/zyjh1.htm',
        'http://hlj.xinhuanet.com/ldhd/zxhd1.htm',
        'http://hlj.xinhuanet.com/ldhd/zyjh1.htm',
        'http://hlj.xinhuanet.com/ldhd/zxhd1.htm',
        'http://hlj.xinhuanet.com/ldhd/zyjh3.htm',
        'http://hlj.xinhuanet.com/ldhd/zxhd3.htm',
        'http://hlj.xinhuanet.com/ldhd/zyjh4.htm',
        'http://hlj.xinhuanet.com/ldhd/zxhd4.htm',  # 黑龙江
        'http://www.js.xinhuanet.com/zhengwu/zhengwu/zyjh_lq.htm',
        'http://www.js.xinhuanet.com/zhengwu/zhengwu/zxhd_lq.htm',
        'http://www.js.xinhuanet.com/zhengwu/zwpd/zhengwu/stfjh.htm',
        'http://www.js.xinhuanet.com/zhengwu/zwpd/zhengwu/stfhd.htm',
        'http://www.js.xinhuanet.com/zhengwu/zwpd/zhengwu/szxzyjh.htm',
        'http://www.js.xinhuanet.com/zhengwu/zwpd/zhengwu/szxzxhd.htm',  # 江苏
        # 浙江特殊
        'http://www.ah.xinhuanet.com/ahzw2006/swsjjh.htm',
        'http://www.ah.xinhuanet.com/ahzw2006/swsjhd.htm',
        'http://www.ah.xinhuanet.com/ahzw2006/szjh.htm',
        'http://www.ah.xinhuanet.com/ahzw2006/szhd.htm',
        'http://www.ah.xinhuanet.com/ahzw2006/szjh.htm',
        'http://www.ah.xinhuanet.com/ahzw2006/szhd.htm',
        'http://www.ah.xinhuanet.com/ahzw2006/szxzxjh.htm',
        'http://www.ah.xinhuanet.com/ahzw2006/szxzxhd.htm',# 安徽
        'http://www.fj.xinhuanet.com/sldhd/sjzyjh.htm',
        'http://www.fj.xinhuanet.com/sldhd/sjzxhd.htm',
        'http://www.fj.xinhuanet.com/sldhd/dszzyjh.htm',
        'http://www.fj.xinhuanet.com/sldhd/dszzxhd.htm',
        'http://www.fj.xinhuanet.com/sldhd/zxzyjh.htm',
        'http://www.fj.xinhuanet.com/sldhd/zxzxhd.htm',  # 福建
        'http://www.jx.xinhuanet.com/lingdao/sz01.htm',
        'http://www.jx.xinhuanet.com/lingdao/sz02.htm',
        'http://www.jx.xinhuanet.com/2016sz01/',
        'http://www.jx.xinhuanet.com/2016sz02',
        'http://www.jx.xinhuanet.com/lingdao/szxzx01.htm',
        'http://www.jx.xinhuanet.com/lingdao/szxzx02.htm',#  江西
        'http://www.sd.xinhuanet.com/ldhd/sw/zyjh.htm',
        'http://www.sd.xinhuanet.com/ldhd/sw/zxhd.htm',
        'http://www.sd.xinhuanet.com/ldhd/zx/zyjh.htm',
        'http://www.sd.xinhuanet.com/ldhd/zx/zxhd.htm',  # 山东
        # 河南特殊
        'http://www.hb.xinhuanet.com/ldbd/swsj/zyjh.html',
        'http://www.hb.xinhuanet.com/ldbd/swsj/zxhd.html',
        'http://www.hb.xinhuanet.com/ldbd/sz/zyjh.html',
        'http://www.hb.xinhuanet.com/ldbd/sz/zxhd.html',
        'http://www.hb.xinhuanet.com/ldbd/zxzx/zyjh.html',
        'http://www.hb.xinhuanet.com/ldbd/zxzx/zxhd.html',  # 湖北
        'http://www.hn.xinhuanet.com/hnpd_plc_hnldhd_djh_jh.htm',
        'http://www.hn.xinhuanet.com/hnpd_plc_hnldhd_djh_hd.htm',
        'http://www.hn.xinhuanet.com/hnpd_plc_hnldhd_lww.htm#',  # 湖南
        'http://gd.xinhuanet.com/sungov/leader/hchjh.htm',
        'http://gd.xinhuanet.com/sungov/leader/hchhd.htm',
        'http://gd.xinhuanet.com/sungov/leader/zxzxjh.htm',
        'http://gd.xinhuanet.com/sungov/leader/zxzxhd.htm',
        'http://gd.xinhuanet.com/sungov/leader/szjh.htm',
        'http://gd.xinhuanet.com/sungov/leader/szhd.htm',
        'http://gd.xinhuanet.com/sungov/leader/wrjh.htm',
        'http://gd.xinhuanet.com/sungov/leader/wrhd.htm',  # 广东
        'http://www.gx.xinhuanet.com/gxzw/ld/dwjh.htm',
        'http://www.gx.xinhuanet.com/gxzw/ld/dwhd.htm',
        'http://www.gx.xinhuanet.com/gxzw/ld/zfjh.htm',
        'http://www.gx.xinhuanet.com/gxzw/ld/zfhd.htm',
        'http://www.gx.xinhuanet.com/gxzw/ld/zxjh.htm',
        'http://www.gx.xinhuanet.com/gxzw/ld/zxhd.htm',  # 广西
        'http://www.hq.xinhuanet.com/hngov/hnld/sj_zyjh.htm',
        'http://www.hq.xinhuanet.com/hngov/hnld/sj_zxhd.htm',
        'http://www.hq.xinhuanet.com/hngov/hnld/sz_zyjh.htm',
        'http://www.hq.xinhuanet.com/hngov/hnld/sz_zxhd.htm',
        'http://www.hq.xinhuanet.com/hngov/hnld/zx_zyjh.htm',
        'http://www.hq.xinhuanet.com/hngov/hnld/zx_zxhd.htm',  # 海南
        'http://www.sc.xinhuanet.com/scld/sc_wdm_jh.htm',
        'http://www.sc.xinhuanet.com/scld/sc_wdm_hd.htm',
        'http://www.sc.xinhuanet.com/scld/sc_yl_jh.htm',
        'http://www.sc.xinhuanet.com/scld/sc_yl_hd.htm',
        'http://sc.news.cn/scld/sc_kzp_jh.htm',
        'http://sc.news.cn/scld/sc_kzp_hd.htm',  # 四川
        'http://www.gz.xinhuanet.com/xwzx/gzld/zyjh4.htm',
        'http://www.gz.xinhuanet.com/xwzx/gzld/zxhd4.htm',
        'http://www.gz.xinhuanet.com/xwzx/gzld/zyjh5.htm',
        'http://www.gz.xinhuanet.com/xwzx/gzld/zxhd5.htm',
        'http://www.gz.xinhuanet.com/xwzx/gzld/zyjh3.htm',
        'http://www.gz.xinhuanet.com/xwzx/gzld/zxhd3.htm',  # 贵州
        # 云南特殊
        # 西藏特殊
        'http://www.sn.xinhuanet.com/201205mon/lingdaoma.htm',
        'http://www.sn.xinhuanet.com/201205mon/lingdaomc.htm',
        'http://www.sn.xinhuanet.com/201205mon/lingdaomd.htm',  # 陕西
        'http://www.gs.xinhuanet.com/lingdao/shengzhang/zyjh.htm',
        'http://www.gs.xinhuanet.com/lingdao/shengzhang/zyhd.htm',
        'http://www.gs.xinhuanet.com/lingdao/shuji/zyjh.htm',
        'http://www.gs.xinhuanet.com/lingdao/shuji/zyhd.htm',
        'http://www.gs.xinhuanet.com/lingdao/shengzhang/zyjh.htm',
        'http://www.gs.xinhuanet.com/lingdao/shengzhang/zyhd.htm',
        'http://www.gs.xinhuanet.com/lingdao/zhengxie/zyjh.htm',
        'http://www.gs.xinhuanet.com/lingdao/zhengxie/zyhd.htm',  # 甘肃
        # 青海特殊
        'http://www.nx.xinhuanet.com/leader/dwsj-jh.htm',
        'http://www.nx.xinhuanet.com/leader/dwsj-hd.htm',
        'http://www.nx.xinhuanet.com/leader/zx-jh.htm',
        'http://www.nx.xinhuanet.com/leader/zx-hd.htm',
        'http://www.nx.xinhuanet.com/leader/zxzx-jh.htm',
        'http://www.nx.xinhuanet.com/leader/zxzx-hd.htm',  # 宁夏
        'http://www.xj.xinhuanet.com/ldbdj/dwsj/zyjh.htm',
        'http://www.xj.xinhuanet.com/ldbdj/dwsj/zxhd.htm',
        'http://www.xj.xinhuanet.com/ldbdj/rdzr/zyjh.htm',
        'http://www.xj.xinhuanet.com/ldbdj/rdzr/zxhd.htm',
        'http://www.xj.xinhuanet.com/ldbdj/zhuxi/zyjh.htm',
        'http://www.xj.xinhuanet.com/ldbdj/zhuxi/zxhd.htm',
        'http://www.xj.xinhuanet.com/ldbdj/zxzx/zyjh.htm',
        'http://www.xj.xinhuanet.com/ldbdj/zxzx/zxhd.htm',  # 新疆
    ]

    centers=(
        'xijinping','likeqiang','zhangdejiang','yuzhengsheng','liuyunshan','wangqishan','zhanggaoli',#常委
    )
    for center in centers:
        start_urls.append('http://www.xinhuanet.com/politics/leaders/'+center+'/zyhd.htm')
        start_urls.append('http://www.xinhuanet.com/politics/leaders/' + center + '/zyjh.htm')
        start_urls.append('http://www.xinhuanet.com/politics/leaders/' + center + '/cgkc.htm')
        start_urls.append('http://www.xinhuanet.com/politics/leaders/' + center + '/hjjj.htm')
        start_urls.append('http://www.xinhuanet.com/politics/leaders/' + center + '/cf.htm')
        start_urls.append('http://www.xinhuanet.com/politics/leaders/' + center + '/zdzx.htm')
        start_urls.append('http://www.xinhuanet.com/politics/leaders/' + center + '/qt.htm')


    leaders=(
        'makai','wanghuning','liuyandong','liuqibao','xuqiliang','sunchunlan','sunzhengcai','lijianguo',
        'liyuanchao','wangyang','zhangchunxian','zhanggaoli','fanchanglong','mengjianzhu','zhaoleji','huchunhua',
        'yuzhengsheng','lizhanshu','guojinlong','hanzheng',#中央政治局
        'duqinglin','zhaohongzhu','yangjing',#中央书记处
    )

    for leader in leaders:
        start_urls.append('http://www.xinhuanet.com/politics/leaders/'+leader+'/zyjh.htm')
        start_urls.append('http://www.xinhuanet.com/politics/leaders/' + leader + '/zyhd.htm')


    rules=(
        Rule(LinkExtractor(allow=reg), callback="parse_news", follow=True),
    )
    def printcn(uni):
        for i in uni:
            print uni.encode('utf-8')
    def parse_news(self,response):
        item = GenericItem()
        self.get_id(response,item)
        self.get_url(response,item)
        self.get_source(response,item)
        self.get_title(response,item)
        self.get_date(response,item)
        self.get_body(response,item)
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!remenber to Retrun Item after parse
        if item['body']:
            return item

    def get_id(self,response,item):
        id=uuid.uuid4()
        if id:
            item['id']=id
    def get_url(self,response,item):
        news_url=response.url
        if news_url:
            item['url']=news_url
    def get_source(self,response,item):
        source=self.source
        if source:
            item['source']=source
    def get_title(self,response,item):
        title=response.xpath('//title/text()').extract()
        if title:
            item['title']=''.join(title).strip()
    def get_date(self, response, item):
        date = self.yesterday2+'000000'
        item['date'] = date
    def get_body(self,response,item):
        paras = response.xpath('//p')
        news_body = ''
        for p in paras:
            data = p.xpath('string(.)').extract()
            if data:
                body = ''
                for line in ''.join(data).splitlines():
                    #   print entry.encode('utf-8')
                    body += line.strip()
                news_body += body + '_|_'
        item['body'] = news_body.replace('_|__|_', '_|_')
