import asyncio

# from aiogram.types import BotCommand
# from loguru import logger
#
# from src.config import dp, bot, settings
# from src.telegram.midlewares import DependanciesMiddleware
# from src.telegram.handlers import routers
#
#
# async def setup_bot_commands():
#     await bot.set_my_commands(
#         [
#             BotCommand(command="/help", description="Информация о боте"),
#             BotCommand(command="/cancel", description="Отмена действия"),
#         ]
#     )
#
#
# async def startup():
#     dm = DependanciesMiddleware()
#     dp.message.outer_middleware(dm)
#     dp.callback_query.outer_middleware(dm)
#     dp.include_routers(*routers)
#
#     await setup_bot_commands()
#     logger.info(f"Bot started: {await bot.get_me()}")
#     asyncio.create_task(dp.start_polling(bot))
#
#
# async def shutdown():
#     await bot.delete_webhook()
#     await bot.close()
#     logger.info("Bot stoped")
#
#
# async def main():
#     try:
#         await startup()
#     finally:
#         await shutdown()
#
#
# if __name__ == "__main__":
#     asyncio.run(main())

from src.google import GoogleSheetsAsync
from src.utils import to_date_dict
from time import perf_counter
gs = GoogleSheetsAsync()

SPREADSHEET_IDS = [
    "1n67MpONuq8BxSCZRBJyg2gwzbk-ljf8i_ND9cM7hvEk",
    "18DyoUi_UVYn1NBrYepseYKxHpaM4CeNtyrocLmPRs1M",
    "1EYHPAzsAPqZEq8dfHoWPxgnMMEbCfO0CgQqtXD1wjXA",
    "1X99Ruk8NWlvEhREBPO-AEhGAQ0bqA2i8dJdEPaVCa8Y",
    "1zoAoJyU38QzGKmgfuT9q3srB8aUjKpKc_WtaLgUPv0Y",
    "1aO8cd6B_cpdfTf3Xfb9IppgUM2_Isa29nzMbVnIus74",
    "1WyLg3CpX0qaryrOImEAjEycPBeIMcgjhVoGhdKCObv4",
    "108KTrh7yCG6tNem7oghLIwDy-LV2Lfaf2rGMe43pEHM",
    "1p6c2FpV4n77WjPeMOUl2cQe3Cf7gTuPwRFYJQyByLaY",
    "1Sj3gBcbufGtIfQThg8PXjeYcd8XHgrDVYD5p8V5-Ipo",
    "1w4G-TLgClcadfL5_Jv2dfYQsxc_gQYLKPnFxfBzF_K8",
    "183ZD9ZU43vNVUEBcIcNULEzZUgPfeN-4I_CjRag5ZaQ",
    "1LLQ62a1V6A3xgGl-NFd5UO4muIm3b193dmt20TkDf88",
    "1tSJ7XLnzBa6dY418eZUnkglvxh1A1FgAJiGUHYziBZE",
    "1F0fVgX9J5mQtIIgpDFimUPwNi0jz7qgS0GfsMBqlwdY",
    "19It8SphKWz-EixYKlbkNUZnixBABi_l6QVI3XfM9X14",
    "1LkvIibyQYYIv9s5MT2ko_2mwsuDWTIYmzxSyCiMK33k",
    "1g4shqQEF2R6Z5mkxfQWMmkw1LwfjzHQTYwC8wXCSJT0",
    "162vNcy3mPhY3Wu9ixDjFcoMD6sKRy6qfQxKLWqbhlvE",
    "1wFTs_6kkfVLCBS9vPKQVhyvY_eP4naTmFnZ3KyZCWLY",
    "155vDYX60BcXlvwxTGPx8DG4u6CxZRVVCLZl3NkH9Pwo",
    "1I6TMtjuKkiFeaZxTSHBGqRtWDpAaHnkEJ1OVylKRpAc",
    "1szDjiB5iVcuEyUbDn92tycaivzo29jqjuxA9YrEMoD8",
    "1R3WEZa8q_gy_fcUl5tDKC7rasTTbLxAiW-brbUk9ctI",
]


async def main():
    start_time = perf_counter()  # стартуем таймер

    for sheet_id in SPREADSHEET_IDS:
        data = await gs.get_statistic(sheet_id, "Декабрь")
        print(to_date_dict(data))

    end_time = perf_counter()  # остановка таймера
    print(f"Время выполнения: {end_time - start_time:.2f} секунд")



if __name__ == "__main__":
    asyncio.run(main())
