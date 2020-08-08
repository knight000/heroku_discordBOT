import discord
from discord.ext import commands
from random import randint


class test_command(commands.Cog):
    '''
    测试中的指令或者正在测试的指令
    '''
    @commands.command(name="math", aliases=("计算", "eval",), help='计算模块，其实就是个eval')
    async def math(self, ctx, a):
        await ctx.send(eval(a))

    @commands.command(name="ra", help='跑团检定指令，格式是[技能名][数值]')
    async def ra(self, ctx, skill, value=0):
        if value == 0:
            try:
                value = int(skill)
                skill = ''
            except:
                await ctx.send('请输入技能数值')
                return
        if value >= 100:
            await ctx.send('技能数值过大无需检定')
        else:
            check = randint(1, 100)
            if check <= value:
                if check <= 5:
                    roll_type = '大成功'
                elif check <= value/5:
                    roll_type = '极难成功'
                elif check <= value/2:
                    roll_type = '困难成功'
                else:
                    roll_type = '成功'
            else:
                if check > 95:
                    roll_type = '大失败'
                else:
                    roll_type = '失败'
            name = str(ctx.author)
            name = name[:name.find('#')]
            await ctx.send(f'{name}进行{skill}检定：1D100={check}/{value} {roll_type}')


def setup(bot):
    bot.add_cog(test_command())
