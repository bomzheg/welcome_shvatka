from aiogram.utils.text_decorations import html_decoration as hd
from app.models import dto


def user_link(user: dto.User) -> str:
    if user.username:
        rez = hd.link(hd.quote(user.name_mention), f"t.me/{user.username}")
    else:
        rez = hd.link(user.name_mention, f"tg://user?id={user.tg_id}")
    return rez
