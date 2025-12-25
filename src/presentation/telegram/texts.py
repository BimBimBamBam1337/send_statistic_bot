msg_add_excel_tabel = "Отправте ссылку на таблицу"
msg_send_channel_id = "Сначала проверте есть ли бот в канале, если он там есть, то отправте id канала, который связан с таблицей, иначе сначала добавте бота, а потом отправляйте id"


def channel_added(name: str | None, channel_id: int | None):
    return f"""
Название группы: {name}
Id группы: {channel_id}
    """
