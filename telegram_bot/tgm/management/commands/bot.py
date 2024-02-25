from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Min


from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from tgm.functions import (marketplace_buttoms, score_buttoms,
                           filter_marketplase, filter_score,
                           check_user, check_product,
                           get_mid_score, get_min_score, check_comment)
from tgm.models import TelegramUser
from product.models import Score, CommentProduct, Product

class Command(BaseCommand):
    help = 'Запускает телеграм бота'

    def handle(self, *args, **options):
        bot()

def bot():
    """Телеграм бот"""
    BOT = Updater(token=settings.T_BOT_TOKEN)

    market_buttoms = marketplace_buttoms
    scores_buttoms = score_buttoms
    market_filter = filter_marketplase
    score_filter = filter_score

    min_score = get_min_score
    mid_score = get_mid_score()

    DATA = {}  # article, magazin, score, comment, user


    def choice_marketplace(update, context):
        """Начало работы бота.
        Выбор маркетплейса в котором ыл куплен товар."""

        user = update.effective_chat
        check_user(user)

        if len(context.args) == 1:
            if check_product(context.args[0]):
                DATA['article'] = context.args[0]
                button = ReplyKeyboardMarkup(market_buttoms)
                context.bot.send_message(
                    chat_id=user.id,
                    text=f'где вы купили товар?',
                    reply_markup=button
                )


    def choice_score(update, context):
        """Выбор оценки товара."""

        DATA['magazin'] = update.message.text
        button = ReplyKeyboardMarkup(scores_buttoms)
        chat = update.effective_chat
        context.bot.send_message(
            chat_id=chat.id,
            text='Оцените товар',
            reply_markup=button
        )

    def product_evaluation(update, context):
        """Сравнение оценки пользователя.
        Комментарий пользователя о товаре"""

        score = int(update.message.text)
        DATA['score'] = score
        chat = update.effective_chat
        if min_score  <= score <= mid_score:
            context.bot.send_message(
                chat_id=chat.id,
                text='Напишите отзыв',
            )
        else:
            create_comment(update, context)

    def feedback(update, context):
        """Функция для ввода отзыва."""

        chat = update.effective_chat
        context.bot.send_message(
            chat_id=chat.id,
            text='Отзыв принят',)
        

    def create_comment(update, context):
        """Создание отзыва"""

        chat = update.effective_chat
        if DATA.get('article') is not None:
            if DATA.get('score') == 4 or DATA.get('score') == 5:
                DATA['comment'] = ''
            else:
                DATA['comment'] = update.message.text
            DATA['user'] = chat.id
            
            t_user = TelegramUser.objects.get(telegram_id=DATA['user'])
            if check_product(DATA['article']):
                product = Product.objects.get(id=DATA['article'])

                if not check_comment(product, t_user):
                    CommentProduct.objects.create(
                        product=product,
                        user_telegram=t_user,
                        comment=DATA['comment'],
                        user_score=DATA['score']
                    )
                    context.bot.send_message(
                        chat_id=chat.id,
                        text=f'{DATA}',
                    )
        DATA.clear()


    # Диспетчеры для обработки комманд и ввода текта пользователя
    BOT.dispatcher.add_handler(
        CommandHandler('start', choice_marketplace)
    )
    BOT.dispatcher.add_handler(
        MessageHandler(Filters.regex(market_filter), choice_score)
    )
    BOT.dispatcher.add_handler(
        MessageHandler(Filters.regex(score_filter), product_evaluation)
    )
    BOT.dispatcher.add_handler(
        MessageHandler(Filters.regex('Напишите отзыв'), feedback)
    )
    BOT.dispatcher.add_handler(
        MessageHandler(Filters.text, create_comment)
    )

    BOT.start_polling()
    BOT.idle()



