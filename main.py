from khl import Bot,Message
import json
import command_bot


# 打开配置文件
def open_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        tmp = json.load(f)
    return tmp

config = open_file("./config/config.json")

bot = Bot(config["token"])  # websocket

# bot启动时调用
@bot.on_startup
async def bot_init(bot: Bot):
    command_bot.init(bot, config)


if __name__ == '__main__':
    bot.run()