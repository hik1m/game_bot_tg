import random

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart



BOT_TOKEN = "6880467854:AAHmLV7X6KXv3LGzw1ZIrO6iD1RLzBv2uVY"

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

ATTEMPTS = 5

users = {}

def get_random_number() -> int:
    return random.randint(1,100)

@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer('Привет!\nЯ бот от hikim\nСо мной можно играть в угадай число!'
                         'Чтобы получить правила игры и список доступных команд - /help')
    if message.from_user.id not in users:
        users[message.from_user.id]= {
            'in_game': False,
            'secret_number': None,
            'attempts': None,
            'total_games': 0,
            'wins': 0
        }

@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer('Правила игры очень простые\nУ тебя есть 5 попыток отгадать моё число от 1 до 100'
                         '\n/stat показывает, сколько игр у тебя сыграно и выиграно'
                         '\n/cancel буквально выход из игры, если вы играете'
                         '\n А теперь давай играть!')

@dp.message(Command(commands = 'stat'))
async def process_stat_command(message: Message):
    await message.answer(f'Всего игр сыграно:{users[message.from_user.id]["total_games"]}\n'
                         f'Игр выиграно: {users[message.from_user.id]["wins"]}'
                         )
    
@dp.message(Command(commands='cancel'))
async def procces_cancel_command(message: Message):
    if users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = False
        await message.answer(
            'Ты вышел из игры( Если захочешь сыграть снова, то напиши'
        )
    else:
        await message.answer(
            'А, мы итак с вами не играли...'
            'Может, сыграем?'
        )

@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра', 'играть', 'хочу играть']))
async def process_positive_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id] ['in_game'] = True
        users[message.from_user.id] ['secret_number'] = get_random_number()
        users[message.from_user.id] ['attempts'] = ATTEMPTS
        await message.answer(
            'ИЗИ!\n\nЯ загадал число от 1 до 100,'
            'Угадай!'
        )
    else:
        await message.answer(
            'Пока мы играем, я могу реагировать только на числа от 1 до 100'
            'Ну и на команды /cancel и /stat'
        )
@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer(
          'Ну и соси!\n\nЕсли надумаешь, то пиши'  
        )  
    else:
        await message.answer(
            'Мы же вообще-то играем!Присылайте числа от 1 до 100!'
        )

@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
            await message.answer(
                'ПОБЕДА! ТЫ УГАДАЛ!'
                '\nДавай сыграем ещё?'
            )
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -=1
            await message.answer('Моё число меньше!')
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -=1
            await message.answer('Моё число больше!')
        
        if users[message.from_user.id]['attempts'] == 0:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            await message.answer(
                f'К сожалению, у вас нету больше попыток'
                f'\nВы проиграли\n\nМоё число было {users[message.from_user.id]["secret_number"]}\n\nДавай сыграем ещё?'
            )
    else:
        await message.answer('Мы ещё не играем. Хотите поиграть?')

@dp.message()
async def process_other_answers(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer(
            'Мы сейчас играем!'
            'Присылайте числа от 1 до 100!'
        )
    else:
        await message.answer(
            'У меня недостаточно команд. Давайте просто сыграем в игру?'
        )

if __name__== '__main__':
    dp.run_polling(bot)