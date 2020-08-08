import discord
from discord.ext import commands
import requests
import datetime
import time
from functools import reduce


def ddc_fetcher(day: int = 7, *, fix: datetime.date = None, id: str = None):
    if day > 15:
        return '为避免刷屏，最大值为15'
    overflow = False
    today = datetime.date.today() if not fix else fix  # today
    next_month = datetime.date(today.year, today.month+1, 1)
    offset = (next_month-today).days

    if day > offset:
        delta = day-offset
        overflow = True

    date = today.day

    url = 'https://api.live.bilibili.com/xlive/web-ucenter/v2/calendar/GetProgramList?type=1&year_month={}'.format(
        today.strftime("%Y-%m"))
    '''
    type=1 推荐查找
    type=2 我关注的主播（怎么可能会关注啦）
    type=3 精确查找（按uid）
    '''

    if id:
        url = 'https://api.live.bilibili.com/xlive/web-ucenter/v2/calendar/GetProgramList?type=3&year_month={}&ruids={}'.format(
            today.strftime("%Y-%m"), id)

    data = requests.get(url).json()
    name_list = data['data']['user_infos']

    def info(p): return map(lambda x: {'name': name_list[str(x['ruid'])]['uname'],
                                       'title': x['title'], 'id': x['room_id'], 'time_h': time.localtime(x['start_time'])[3],
                                       'time_min': time.localtime(x['start_time'])[4], 'Brecommand': x['is_recommend']}, p)

    def output(p): return reduce(lambda m, n: m+n, list(map(lambda x: '{5}[[{0}](https://live.bilibili.com/{4})]{5}{1}({2}:{3})\n'.format(x['name'],
                                                                                                                                          x['title'], x['time_h'], x['time_min'] if x[
        'time_min'] != 0 else '00',
        x['id'], '**' if x['Brecommand'] == 1 else ''), info(p))))

    program_list = list(filter(lambda k: k != None, map(lambda x: f'**{today.month}月' + x +
                                                        '日:**\n' + output(data['data']['program_infos'][x]['program_list']) if int(
                                                            x) in range(date, date+day) else None,
                                                        data['data']['program_infos'])))

    if fix:
        return (''.join(program_list), len(program_list))
    elif not overflow:
        length = len(program_list)
        if length != 0:
            return ['共{}日结果:'.format(length), ''.join(program_list)]
        else:
            return '无结果，估计你的单推是懒狗'
    else:
        fixed = ddc_fetcher(delta, fix=next_month, id=id)
        length = len(program_list)+fixed[1]
        if length != 0:
            return ['近{}日结果:'.format(len(program_list)+fixed[1]), ''.join(program_list) + fixed[0]]
        else:
            return '无结果，估计你的单推是懒狗'


vtb_info_list = requests.get('https://api.vtbs.moe/v1/info').json()
vtb_aliases_list = [['月ノ美兎', '月之美兔', '委员长'],
                    ['湊あくあ', '湊-阿库娅', 'aqua', '阿夸'],
                    ['京华', 'Overidea', '张京华'],
                    ['大神ミオ', '大神澪', '三才', '二哈', '老干部'],
                    ['YuNi', '太子'],
                    ['もちひよこ', 'Mochi', 'Hiyoko', '饼叽'],
                    ['瀬戸あさひ', '濑户旭', '眼镜', '臭眼镜'],
                    ['宗谷いちか', '黄豆', '黄豆一花'],
                    ['叶', 'にじさんじゲームズ', '叶师', '叶神父'],
                    ['椎名唯华', '大福', '三下', '草莓大福', '断头台', '麻将王'],
                    ['笹木咲', '熊猫人'],
                    ['织田信姬', '家主', '大头'],
                    ['宇森ひなこ', '蝙蝠妹'],
                    ['本间ひまわり', '本间向日葵', '傻葵', '阿葵', '葵天使'],
                    ['白上フブキ', '白上吹雪', '狐狸', '猫', '工具人', '玉米人'],
                    ['Kizuna', 'AI', 'キズナアイ', '绊爱', '爱酱', '亲分'],
                    ['田中ヒメ', '田中姬', '猴子'],
                    ['Mirai', 'Akari', '未来明', '6000w之女', '金发渣男', '满星光', '阿满'],
                    ['斗和キセキ', '红异端', '高达', '泉家三妹'],
                    ['夏色まつり', '夏色祭', '夏哥', '祭妹', '马自立', '打桩祭'],
                    ['时乃空', 'ときのそら', 'Tokino', 'Sora', '空妈'],
                    ['神楽七奈', '狗妈'],
                    ['KMNZ', 'LIZ', 'リズ', 'LITA', 'リタ', '阿猫阿狗'],
                    ['ロボ子さん', '萝卜子', '高性能', '大根子'],
                    ['さくらみこ', '樱巫女', '35', '樱火龙'],
                    ['夜空メル', '夜空梅露', '摸鱼怪'],
                    ['赤井はあと', '赤井心', '心豚'],
                    ['アキ・ローゼンタール', '亚绮·罗森塔尔', '亚绮·罗森'],
                    ['紫咲シオン', '紫咲诗音', '傻紫', '小学生'],
                    ['百鬼あやめ', '百鬼绫目', '狗狗','苦压西'],
                    ['癒月', 'ちょこ', '愈月巧可', '老师'],
                    ['大空', 'スバル', '大空昴', '486', '古神'],
                    ['猫又おかゆ', '猫又小粥', '阿汤哥'],
                    ['戌神ころね', '戌神沁音', '面包狗']]


def check_name(name):
    for vtb_aliases in vtb_aliases_list:
        if name in vtb_aliases:
            return vtb_aliases
    return name


def use_uid(uid_list):
    for vtb_info in vtb_info_list:
        for uid in uid_list:
            if uid['mid'] == vtb_info['mid']:
                return vtb_info
    return False


@commands.command(aliases=('DD日历', 'dd_calendar'))
async def ddc(ctx, *args):
    '''
    原则上是 ddc [数字] [主播名]
    可以直接ddc [主播名]，默认搜索7天的内容
    移植过来的神奇产物，kni修改版本
    '''
    digit = None
    sstr = None

    for i in args:
        if digit != None and sstr != None:
            break
        if i.isdigit():
            digit = i
        else:
            sstr = i

    if digit == None and sstr == None:
        digit=3

    if sstr:
        name = check_name(str(sstr))
        header = {'Referer': 'https://search.bilibili.com/'}
        if type(name) == list:
            for i in name:
                uid_list = requests.get(f'https://api.bilibili.com/x/web-interface/search/type?search_type=bili_user&page=1&order=fans&keyword={i}&order_sort=0&changing=mid',
                                        headers=header).json()['data']['result']
                info_data = use_uid(uid_list)
                if info_data != False:
                    break
        else:
            uid_list = requests.get(f'https://api.bilibili.com/x/web-interface/search/type?search_type=bili_user&page=1&order=fans&keyword={name}&order_sort=0&changing=mid',
                                    headers=header).json()['data']['result']
            info_data = use_uid(uid_list)
        if info_data == False:
            await ctx.send('未找到相应VTB')
            return
        title = '{}'.format(info_data['uname'])
        uurl = f'https://space.bilibili.com/{info_data["mid"]}'
        desc = info_data['sign']
        photo = info_data['face'].replace('http://', 'https://')
        top = info_data['topPhoto'].replace('http://', 'https://')

        if digit:
            msg = ddc_fetcher(int(digit), id=info_data['mid'])
        else:
            msg = ddc_fetcher(id=info_data['mid'])
    else:
        msg = ddc_fetcher(int(digit))
        if msg != '无结果，估计你的单推是懒狗' and msg != '为避免刷屏，最大值为15':
            await ctx.send(embed=discord.Embed(title=msg[0], description=msg[1], url='https://live.bilibili.com/p/html/live-web-calendar/index.html'))
        elif msg == '为避免刷屏，最大值为15':
            await ctx.send(msg)
        return
    if msg != '无结果，估计你的单推是懒狗' and msg != '为避免刷屏，最大值为15':
        desc = f'{desc}\n[{msg[0]}](https://live.bilibili.com/p/html/live-web-calendar/index.html)\n{msg[1]}'
    elif msg == '为避免刷屏，最大值为15':
        await ctx.send(msg)
    emb = discord.Embed(title=title, description=desc, url=uurl)
    emb.set_thumbnail(url=photo)
    emb.set_image(url=top)
    await ctx.send(embed=emb)

    return


def setup(bot):
    bot.add_command(ddc)
