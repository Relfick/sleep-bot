from telebot import custom_filters
from telebot.types import Message

class IsAllowedUserFilter(custom_filters.AdvancedCustomFilter):
    key = 'chats_and_admins'

    def check(self, message: Message, text: ()):
        return message.chat.id in text[0] and message.from_user.id in text[1]