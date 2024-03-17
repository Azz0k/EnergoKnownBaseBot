import pandas as pd
import os
import logging
import sys
from typing import Any
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from imports.utils import *
from imports.config import *
from imports.Trie import Trie
from imports.TwoWayDict import TwoWayDict
from imports.Users_mssql import Users
from imports.Content import ContentsElement


class Support:

    def __init__(self):
        self.find_trie = Trie()
        self.name_vs_id = TwoWayDict()
        self.users = Users()
        self.data_frame = None
        self.update_data_frame()

    def update_data_frame(self):
        file_name = r'dataframe.txt'
        df = []
        parent_element = None
        try:
            file = open(file_name, 'r', encoding="utf8")
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line[0] == '.':
                    if parent_element is not None:
                        df.append(parent_element)

                    temp = line[1:].split('.')
                    parent_element = ContentsElement(element_id=temp[0], name=temp[1])
                else:
                    temp = line.split('.')
                    parent_element.add_child(temp[0], line, link='')
        finally:
            file.close()
            df.append(parent_element)
        self.data_frame = df

    def default_data_frame(self):
        return None

    def get_children(self, query: str):
        return []

    def create_repeat_markup(self, data: str) -> Any:
        """Return an inline keyboard markup with one button"""
        reply_markup = InlineKeyboardMarkup()
        button = InlineKeyboardButton(text='Повторить последний запрос', callback_data=f'{BUTTON_PREFIX}{data}')
        reply_markup.add(button)
        return reply_markup

    def create_contact_markup(self) -> Any:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = KeyboardButton('Отправить контакт', request_contact=True)
        markup.add(button)
        return markup

    def create_standard_markup(self, query: str) -> Any:
        markup = InlineKeyboardMarkup(row_width=1)
        if query == '':
            for el in self.data_frame:
                button = InlineKeyboardButton(text=el.name,
                                              callback_data=f'{BUTTON_PREFIX}{query}_{el.id}')
                markup.add(button)
        return markup

    def get_answer(self, query: str) -> str:
        return NOT_FOUND_ANSWER

    def get_message_from_b24(self, telegram_id: int) -> str:
        return self.users.get_link_by_telegram_id(telegram_id)

    def replace_ids_with_names(self, query: str):
        return self.name_vs_id.replace_ids_with_names(query)


def import_from_file():
    merch = pd.read_excel(r'C:\temp\Мерчи.xlsx')
    users = Users()
    for c in merch['Phone'].values:
        c = str(c)
        c = c.replace(' ', '')
        c = c.replace('(', '')
        c = c.replace(')', '')
        c = c.replace('-', '')
        if c.startswith('8'):
            c = '+7' + c[1:]
        if c.startswith('9'):
            c = '+7' + c
        if c.startswith('7'):
            c = '+' + c
        if not users.is_phone_number_exists(c):
            users.insert_number(c)
            print(f'{c} - добавлено')
        else:
            print(f'{c} - уже есть в базе')


if __name__ == '__main__':
    import_from_file()
