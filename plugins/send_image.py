import discord
from discord.ext import commands
import requests
import os


def OutputTags(TagList):
    url = 'https://www.pixiv.net/tags/'
    msg = ''
    for i in TagList:
        if i.count(' ') == 0:
            md_format = f'[#{i}](https://www.pixiv.net/tags/{i}) '
            msg += md_format
        else:
            msg += f'#{i} '
    return msg


class 色图相关(commands.Cog):
    '''
    注意身体，另外pixiv那个api每日请求最多300次，不过应该够了
    '''
    @commands.command(name='rand_pic', aliases=('随机图片',))
    async def rand_pic(self, ctx, count=1, mode='SAFE'):
        '''
        随机P站图片
        格式是[数量][SAFE|R18|ALL]
        但只能出全年龄
        '''
        image_type = ".tmp"
        if count > 5:
            count = 5
        elif count < 1:
            count = 1
        if mode == "r18" or mode == "R18":
            mode = "R18"
        elif mode == "all" or mode == "ALL":
            mode = "ALL"
        else:
            mode = "SAFE"
        params = {
            'count': count,
            'mode': mode,
        }
        web = requests.get(
            'http://193.112.67.15/setuapi/discovery', params=params).json()
        for i in range(0, count):
            url = web[str(i)]['url_big'].replace("pximg.net", "pixiv.cat")
            embed_box = discord.Embed(title=web[str(i)]['title'], description=OutputTags(
                web[str(i)]['tags']), url=web[str(i)]['meta']['canonical'])
            embed_box.set_image(url=url)
            await ctx.send(embed=embed_box)
        return

    @commands.command(name='pixiv', aliases=('P站图片',))
    async def pixiv(self, ctx, num=1, r18='', keyword=''):
        '''
        P站图片,支持关键词
        格式是[数量][*|R18|ALL][关键词]
        有时候全年龄会出有R18标签的作品
        '''
        if num > 5:
            num = 5
        elif num < 1:
            num = 1
        if r18 == 'r18' or r18 == 'R18':
            r18 = 1
        elif r18 == 'all' or r18 == 'ALL':
            r18 = 2
        else:
            r18 = 0
        try:
            apikey = os.environ["loliconAPI_key"]
        except:
            apikey = ''
        params = {
            "apikey": apikey,
            "r18": r18,
            "size1200": False,
            "num": num,
            "keyword": keyword
        }
        image_type = ".tmp"
        web = requests.get('https://api.lolicon.app/setu/',
                           params=params).json()
        if web['code'] != 0:
            await ctx.send(web['msg'])
        else:
            for i in range(0, num):
                url = web['data'][i]['url']
                if url.find(".jpg") != -1:
                    image_type = ".jpg"
                elif url.find(".png") != -1:
                    image_type = ".png"
                embed_box = discord.Embed(title=f"{web['data'][i]['title']}-{web['data'][i]['author']}", description=OutputTags(
                    web['data'][i]['tags']), url=f"https://www.pixiv.net/artworks/{str(web['data'][i]['pid'])}")
                embed_box.set_image(url=url)
                await ctx.send(embed=embed_box)
        return

    @commands.command(name='fluxpoint')
    async def fluxpoint(self, ctx, *args):
        '''
        使用了fluxpoint.dev的API
        格式是fluxpoint [随机|壁纸|碧蓝|nekopara|色图]* ([色图]*)
        带*的为可选，另壁纸无色图，只看色图可以直接//fluxpoint 色图
        以下是可选别名：
        ['色图', 'nsfw']['随机','random','anime']['碧蓝','azurlane']['nekopara']['壁纸','wallpaper']
        '''
        try:
            headers = {'Authorization': os.environ['fluxpointAPI_key']}
        except:
            await ctx.send('无APIkey')
            return
        url = 'https://gallery.fluxpoint.dev/api'
        tag = '/sfw'
        if len(args) >= 2:
            if args[1] in ['色图', 'nsfw']:
                tag = '/nsfw'
        if len(args) == 0:
            tag = '/sfw/anime'
        else:
            if args[0] in ['色图', 'nsfw']:
                tag = '/nsfw/lewd'
            elif args[0] in ['随机', 'random', 'anime']:
                tag += '/anime'
            elif args[0] in ['碧蓝', 'azurlane']:
                tag += '/azurlane'
            elif args[0] in ['nekopara']:
                tag += '/nekopara'
            elif args[0] in ['壁纸', 'wallpaper']:
                tag = '/sfw/wallpaper'
            else:
                await ctx.send('参数错误')
                return
        embed_box = discord.Embed()
        embed_box.set_image(url=requests.get(
            f'{url}{tag}', headers=headers).json()['file'])
        await ctx.send(embed=embed_box)
        return


def setup(bot):
    bot.add_cog(色图相关())
