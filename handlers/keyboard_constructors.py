from telebot import types


def create_keyboard(btn_type='callback', **kwargs):
    '''
    Creates callback buttons for telegram bot using telebot.types
    :param kwargs: dictionary in format {callback_data/url: text}
    :param btn_type: callback or url button
    :return: keyboard
    '''
    keyboard = types.InlineKeyboardMarkup()
    for data, text in kwargs.items():
        if btn_type == 'callback':
            keyboard.add(
                types.InlineKeyboardButton(text=kwargs[data],
                                           callback_data=data))
        else:
            keyboard.add(
                types.InlineKeyboardButton(text=kwargs[data],
                                           url=data))
    return keyboard


def add_back_button(keyboard):
    if keyboard:
        keyboard.add(
            types.InlineKeyboardButton(text='Назад',
                                       callback_data='back'))
    else:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(text='Назад',
                                       callback_data='back'))
    return keyboard
