from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

cb_oo = CallbackData("oo", "id", "name")
cb_services = CallbackData("service", "id", "name")

def kb_generator(objects, cb):
    # debt: must be optimize
    # It creates list of nested list per 2 dicts in each it: [ [{}, {}], [{}, {}], ... ]
    list_lines = []
    line_buttons = []
    for elm in objects:
        button = InlineKeyboardButton(text=elm[1], callback_data=cb.new(id=elm[0], name=elm[1]))
        if len(line_buttons) < 2:
            line_buttons.append(button)
        else:
            list_lines.append(line_buttons)
            line_buttons = []
            line_buttons.append(button)
    list_lines.append(line_buttons)

    return InlineKeyboardMarkup(row_width=2, inline_keyboard=list_lines)
