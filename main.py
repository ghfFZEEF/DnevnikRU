from bot.tg_bot import BasicTgBot, TgBot

from bin.parser import BasicParser, SeleniumParser
from bin.HTML_reader import BasicHTML, HTML
from bin.JSON import BasicJSON, JSON
from bin.db_work import BasicDb, Db
from bin.table import BasicTable, Table

from bin.data_work import BasicData, Data
from bin.markups import BasicMarkups, Markups


def main():
    parser: BasicParser = SeleniumParser
    html: BasicHTML = HTML
    json: BasicJSON = JSON
    db: BasicDb = Db
    table: BasicTable = Table()

    data_path = "data"

    data: BasicData = Data(data_path, parser, html, json, db)
    db: BasicDb = db(data_path)
    markups: BasicMarkups = Markups()
    token = json(data_path).get_token()

    tg_bot: BasicTgBot = TgBot(token, data, db, markups, table)
    tg_bot.run()


if __name__ == "__main__":
    main()
