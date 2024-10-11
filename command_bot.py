from datetime import datetime
from datetime import timedelta
from function_bot import count_down
from khl.card import Card, CardMessage, Module, Types, Element, Struct
from khl import Bot,Message


def init(bot: Bot, config: dict):
    # /lotto <str : item> <int : number> <int : time>
    #          抽奖奖品          数量          时间(小时)
    @bot.command(name='lotto')
    async def lotto_command(msg: Message, text: str, number: int, time: int):

        try:
            # 获取频道ID
            ch = await bot.client.fetch_public_channel(config["channel"])

            card = Card(Module.Header('抽奖'))  # 标题
            card.append(Module.Divider())  # 分割线
            card.append(Module.Section(Element.Text(f'奖品为:  **{text}**,  数量为: **{number}**')))  # 正文
            card.append(Module.Context("在这条卡片下方用✋回应来参与抽奖"))  # 小字提示
            card.append(
                Module.Countdown(
                    datetime.now() + timedelta(seconds=(time * 3600)), mode=Types.CountdownMode.DAY  # 倒计时
                ))
            card.append(Module.Countdown(
                datetime.now() + timedelta(seconds=(time * 3600)), mode=Types.CountdownMode.HOUR  # 倒计时
            ))

            ret = await ch.send(CardMessage(card))  # 向指定频道发送发片

            config["msg_id"] = ret["msg_id"]  # 记录抽奖消息ID(获取该条消息的回应)

            winner_userid = count_down(time, config["msg_id"], config["token"], number)
            for userid in winner_userid:
                await ch.send(f"恭喜 (met){userid}(met)  获得了 {text} !")  # @中奖用户
                user = await bot.client.fetch_user(userid)
                card = Card(Module.Header(f"恭喜你获得了 {text} "))
                card.append(Module.Section(Element.Text(f'快去开票频道开票联系管理员吧 !')))
                await user.send(CardMessage(card))
        except:
            card = Card(Module.Header('发生错误,检查下有没有设置频道ID,或者没有足够的用户参加抽奖'))
            await msg.reply(CardMessage(card))

    # /help
    @bot.command(name='help')
    async def help(msg: Message):

        card = Card(Module.Header('指令'))  # 标题
        card.append(Module.Divider())  # 分割线
        card.append(Module.Section(
            Element.Text('抽奖指令: `/lotto <str:物品> <int:数量> <int:时间(小时)>`')))
        card.append(Module.Section(
            Element.Text('设置频道: `/channel <str:频道ID>`')))
        card.append(Module.Section(
            Element.Text('向频道发送初始消息: `/msg `')))
        await msg.reply(CardMessage(card))

    # /channel <channel_id : int> 设置频道ID
    @bot.command(name='ch')
    async def channel(msg: Message, channel_id: int):

        # 记录频道ID
        config["channel"] = channel_id
        card = Card(Module.Header('频道设置成功'))  # 标题
        await msg.reply(CardMessage(card))

    # /msg 向指定频道发送消息
    @bot.command(name='msg')
    async def msg(msg: Message):
        ch = await bot.client.fetch_public_channel(config["channel"])

        card = Card(Module.Header('该频道为抽奖频道'))  # 标题
        card.append(Module.Divider())  # 分割线
        card.append(Module.Section(Element.Text('请在**抽奖消息中**使用**✋表情包回应**来参与抽奖')))
        card.append(Module.Section(Element.Text('**中奖用户**请在**开票频道开票**')))
        card.append(Module.Section(Element.Text('示例如下:')))
        await ch.send(CardMessage(card))