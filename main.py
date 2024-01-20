import os
from aiogram import Bot, Dispatcher, types, executor
from pytube import YouTube

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_message(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "Привет! Я могу скачивать видео из YouTube и на Facebook. Пожалуйста, отправь мне ссылку на видео.")

@dp.message_handler()
async def text_message(message: types.Message):
    chat_id = message.chat.id
    url = message.text

    if url.startswith(('https://youtu.be/', 'https://www.youtube.com/', 'https://youtube.com/')):
        await bot.send_message(chat_id, "Ваше видео загружается, ожидайте...")

        await download_youtube_video(url, chat_id)
    else:
        await bot.send_message(chat_id, "Пожалуйста, отправьте действительную ссылку на YouTube.")

async def download_youtube_video(url, chat_id):
    try:
        # Create a YouTube object
        yt = YouTube(url)

        # Get the stream with both video and audio components (file_extension="mp4")
        stream = yt.streams.filter(file_extension="mp4").get_highest_resolution()

        # Sanitize the title to remove invalid characters
        sanitized_title = "".join(c if c.isalnum() or c in ['_', '-', '.'] else '_' for c in yt.title)

        # Include the sanitized title in the filename
        filename = f'{sanitized_title}.mp4'

        # Download the video
        stream.download(filename=filename)

        # Check the file size
        file_size = os.path.getsize(filename)
        max_file_size =  25 * 1024 * 1024 * 1024   # 2 GB (Telegram's maximum file size for video)

        if file_size <= max_file_size:
            # Send the video as a file
            with open(filename, 'rb') as video:
                await bot.send_video(chat_id, video, caption=f"Вот ваше видео: {yt.title}")

            # Remove the downloaded file
            os.remove(filename)
        else:
            await bot.send_message(chat_id, "Извините, видео слишком длинное для отправки через Telegram. "
                                           "Попробуйте предоставить внешнюю ссылку для загрузки.")

    except Exception as e:
        print(f"An error occurred: {e}")
        await bot.send_message(chat_id, "Произошла ошибка при загрузке видео. Пожалуйста, попробуйте еще раз!!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
