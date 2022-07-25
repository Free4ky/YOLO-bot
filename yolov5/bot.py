import telebot
import pathlib
import requests
import time
import os

isRunning = False

TOKEN = "5523936677:AAFvgUWkL3fvs5Rvd8IpcQcWBZPH_o4at_o"
bot = telebot.TeleBot(TOKEN)

#currentPath = pathlib.Path().resolve()
#currentPath = currentPath.parent.absolute()
#os.system(f'python detect.py --weights best.pt --img 640 --conf 0.25 --source Test\\photos\\file_0.jpg')


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    global isRunning
    if not isRunning:
        bot.send_message(message.chat.id, 'Hello! Send a photo or a link.')
        isRunning = True


@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    src = 'Test/' + file_info.file_path
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, "Let me see...")

    try:
        os.system(f'python detect.py --weights best.pt --img 640 --conf 0.25 --source {src}')
        tempPath = file_info.file_path.replace('/', '\\')
        file_name = os.path.basename(tempPath)
        #os.system(f"copy runs\\detect\\exp\\{file_name} DETECTED\\{file_name}")
        # os.remove(f'runs\\detect\\exp\\{file_name}')
        # os.rmdir('runs\\detect\\exp')
        bot.send_photo(message.chat.id, photo=open(f'runs\\detect\\exp\\{file_name}', 'rb'))
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(content_types=['text'])
def handle_link(message):
    try:
        PATH = 'Test'
        link_text = message.text
        image = requests.get(link_text)
        downloaded_name = f'{time.time()}.jpg'
        with open(os.path.join(PATH, downloaded_name), "wb") as t:
            t.write(image.content)

        bot.reply_to(message, "Let me see...")

        os.system(
            f'python detect.py --weights best.pt --img 640 --conf 0.25 --source {os.path.join(PATH,downloaded_name)}')
        #os.system(f"copy runs\\detect\\exp\\{downloaded_name} DETECTED\\{downloaded_name}")
        # os.remove(f'runs\\detect\\exp\\{downloaded_name}')
        # os.rmdir('runs\\detect\\exp')
        bot.send_photo(message.chat.id, photo=open(f'runs\\detect\\exp\\{downloaded_name}', 'rb'))
    except Exception as e:
        # os.rmdir('runs\\detect\\exp')
        bot.reply_to(message, 'Your link is broken!')


bot.polling(none_stop=True)
