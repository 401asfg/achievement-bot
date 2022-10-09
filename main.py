
def main():
    print("Initializing...")
    from src.ui.bot import bot, TOKEN
    print("Bot is starting up...")
    bot.run(TOKEN)
    input("Bot has ended its execution; press Enter to exit")


if __name__ == "__main__":
    main()
