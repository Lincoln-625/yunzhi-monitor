"""Generate the README's SVG and PNG diagrams with identical geometry.

Requires Pillow. Run from any directory; outputs go to docs/assets/.
Override DIAGRAM_FONT and DIAGRAM_FONT_BOLD when using a non-Windows host.
"""
from pathlib import Path
from html import escape
import math
import os
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[1] / 'assets'
OUT.mkdir(parents=True, exist_ok=True)
FONT = os.environ.get('DIAGRAM_FONT', 'C:/Windows/Fonts/msyh.ttc')
BOLD = os.environ.get('DIAGRAM_FONT_BOLD', 'C:/Windows/Fonts/msyhbd.ttc')
INK, MUTED, BLUE, TEAL = '#172B4D', '#586A81', '#356AE6', '#138A82'


class Diagram:
    def __init__(self, width, height, title, description):
        self.width, self.height = width, height
        self.im = Image.new('RGB', (width, height), '#F5F7FB')
        self.draw = ImageDraw.Draw(self.im)
        self.svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">',
                    f'<title>{escape(title)}</title><desc>{escape(description)}</desc>',
                    f'<rect width="{width}" height="{height}" fill="#F5F7FB"/>']

    def box(self, x, y, w, h, fill='#FFFFFF', border='#DFE6F0', radius=18):
        self.draw.rounded_rectangle((x, y, x+w, y+h), radius, fill, border, 2)
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{border}" stroke-width="2"/>')

    def text(self, x, y, text, size=26, color=INK, bold=False):
        font = ImageFont.truetype(BOLD if bold else FONT, size)
        self.draw.text((x, y), text, font=font, fill=color, anchor='lt')
        self.svg.append(f'<text x="{x}" y="{y+size*.86}" font-family="Microsoft YaHei,Noto Sans CJK SC,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{escape(text)}</text>')

    def line(self, points, color='#93A4BE', arrow=False):
        self.draw.line(points, fill=color, width=3)
        coords = ' '.join(f'{x},{y}' for x, y in points)
        self.svg.append(f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="3"/>')
        if arrow:
            (x0,y0),(x,y) = points[-2:]
            angle = math.atan2(y-y0,x-x0)
            head = [(x,y), (x-13*math.cos(angle-.5),y-13*math.sin(angle-.5)), (x-13*math.cos(angle+.5),y-13*math.sin(angle+.5))]
            self.draw.polygon(head, fill=color)
            coords = ' '.join(f'{a},{b}' for a,b in head)
            self.svg.append(f'<polygon points="{coords}" fill="{color}"/>')

    def save(self, stem):
        self.im.save(OUT / f'{stem}.png', optimize=True)
        (OUT / f'{stem}.svg').write_text('\n'.join(self.svg + ['</svg>']), encoding='utf-8')


def architecture():
    d = Diagram(1600, 1320, '云知 · AI 资讯监测助手：项目架构', '前端交互层、后端应用层、采集与模型及数据服务，以及监控处理流程。')
    d.text(64, 45, '云知 · AI 资讯监测助手', 43, bold=True)
    d.text(65, 109, '项目架构  /  从关键词配置到信息分析与分级通知', 26, MUTED)

    d.box(64, 175, 1472, 178)
    d.text(94, 198, '前端交互层', 30, bold=True)
    d.text(340, 202, 'React 19 · TypeScript · Vite · Tailwind CSS', 26, BLUE)
    for x, title in [(96,'资讯仪表盘'),(454,'关键词管理'),(812,'即时搜索'),(1170,'通知中心')]:
        d.box(x, 263, 332, 62, '#EFF4FF', '#E0E8FC', 12)
        d.text(x+25, 281, title, 25)

    d.line([(550,353),(550,446)], BLUE, True)
    d.text(260, 383, 'HTTP / REST API', 25, BLUE)
    d.line([(1030,446),(1030,353)], TEAL, True)
    d.text(1060, 383, 'Socket.io 事件推送', 25, TEAL)

    d.box(64, 446, 1472, 253)
    d.text(94, 472, '后端应用层', 30, bold=True)
    d.text(340, 475, 'Node.js · Express 5 · TypeScript', 26, BLUE)
    cards = [(96,'业务接口','关键词 / 资讯 / 通知 / 设置'),
             (581,'监控任务','node-cron 每 30 分钟 / 手动触发'),
             (1066,'结果与通知','持久化 / 订阅事件 / 邮件触发')]
    for x, title, desc in cards:
        d.box(x, 536, 438, 132, '#F7F9FD', '#E4EAF3', 12)
        d.text(x+22, 556, title, 27, bold=True)
        d.text(x+22, 608, desc, 22, MUTED)

    d.line([(800,699),(800,743)])
    d.line([(237,743),(1365,743)])
    xs = [64,440,816,1192]
    for x in xs:
        d.line([(x+172,743),(x+172,786)], arrow=True)
    services = [
        ('多源采集', 'Axios · Cheerio · API', ['Bing / 搜狗 / Hacker News', 'B站 / 微博 / Twitter/X'], BLUE),
        ('AI 模型服务', 'OpenRouter → DeepSeek', ['关键词扩展 / 内容预匹配', '相关性 / 重要性 / 摘要'], '#7856BF'),
        ('数据持久化', 'Prisma → SQLite', ['Keyword / Hotspot', 'Notification / Setting'], TEAL),
        ('邮件服务', 'Nodemailer → SMTP', ['high / urgent 级别触发', '发送至配置的收件邮箱'], '#BD7830'),
    ]
    for x, (title, tech, lines, accent) in zip(xs, services):
        d.box(x, 786, 344, 224)
        d.text(x+22, 811, title, 28, accent, True)
        d.text(x+22, 864, tech, 22, INK)
        for j, line in enumerate(lines): d.text(x+22, 922+j*37, line, 21, MUTED)

    d.box(64, 1057, 1472, 192, '#EDF3FD', '#DDE6F8')
    d.text(94, 1083, '监控处理流程', 28, bold=True)
    steps = ['激活关键词','多源采集','去重与时效过滤','AI 分析筛选','保存与通知']
    for i, title in enumerate(steps):
        x = 96 + i*288
        d.box(x, 1144, 248, 66, '#FFFFFF', '#DAE3F3', 12)
        d.text(x+18, 1164, title, 24)
        if i<4: d.line([(x+252,1177),(x+280,1177)], BLUE, True)
    d.text(66, 1273, '独立扩展：Agent Skills + Python 脚本，可单独执行检索与报告生成。', 23, MUTED)
    d.save('architecture')


def modules():
    d = Diagram(1600, 1030, '云知 · AI 资讯监测助手：功能模块', '关键词管理、多源信息采集、AI 分析、资讯仪表盘、即时搜索、分级通知六个功能模块。')
    d.text(64, 45, '围绕关键词，持续发现值得关注的信息', 39, bold=True)
    d.text(64, 106, '云知 · AI 资讯监测助手  /  功能模块', 25, MUTED)
    cards = [
        ('01','关键词管理','定义你的关注主题',['新增关键词与分类','激活、暂停与删除','手动触发监控检查']),
        ('02','多源信息采集','汇集不同平台的信息',['六类来源并行采集','URL 去重与时效过滤','保留来源和原文链接']),
        ('03','AI 内容分析','辅助判断内容与主题的关系',['关键词扩展与预匹配','相关性评分与分析理由','四级重要性与内容摘要']),
        ('04','资讯仪表盘','按需要组织与查看结果',['来源、关键词、时间筛选','热度、相关性等多维排序','概览统计与内容详情']),
        ('05','即时搜索','按需发起一次信息检索',['输入临时查询关键词','Twitter/X 与 Bing 搜索','返回结果附带 AI 分析']),
        ('06','分级通知','及时关注新结果与重点信息',['Socket.io 推送新结果','通知已读与未读管理','重要内容发送邮件提醒']),
    ]
    for i, (num,title,subtitle,lines) in enumerate(cards):
        x, y = 64+(i%3)*504, 178+(i//3)*361
        d.box(x,y,464,327)
        d.box(x+24,y+25,55,45,'#EDF3FF','#EDF3FF',10)
        d.text(x+35,y+34,num,23,BLUE,True)
        d.text(x+95,y+31,title,29,bold=True)
        d.text(x+26,y+98,subtitle,23,MUTED)
        for j,line in enumerate(lines):
            d.text(x+27,y+165+j*43,'· '+line,23)
    d.box(64,931,1472,59,'#EAF5F2','#DBEEE9',12)
    d.text(91,949,'适用场景：秋招资讯与职位发布 / AI 产品更新 / 技术动态 / 品牌与行业观察',25,TEAL)
    d.save('features')


if __name__ == '__main__':
    architecture()
    modules()
    print(f'Generated architecture and feature diagrams in {OUT}')
