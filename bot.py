import asyncio
from pyrogram import Client
from pyrogram.errors import FloodWait, RPCError

# --- НАСТРОЙКИ ---
API_ID = 31728423 
API_HASH = "f8b413b25cf8a3eafbbfdf9977135f68"
CHANNEL_SOURCE = "richesttraderever" 

# Список чатов: 
# Если это ветка: ("юзернейм", ID_ветки)
# Если обычный чат: ("юзернейм", None)
CHATS = [
    ("SafeBaseList", 829273),
    ("testrassilka101", None)
]

INTERVAL = 300 

async def main():
    app = Client("my_account", api_id=API_ID, api_hash=API_HASH, no_updates=True)
    
    async with app:
        print("🚀 Скрипт запущен. Исправлена работа с ветками.")
        
        while True:
            print("\n--- Начало круга рассылки ---")
            try:
                # Получаем последний пост из канала
                last_post = None
                async for message in app.get_chat_history(CHANNEL_SOURCE, limit=5):
                    if message.service: continue
                    last_post = message
                    break
                
                if not last_post:
                    print("❌ Пост не найден.")
                    await asyncio.sleep(60)
                    continue

                for chat_username, thread_id in CHATS:
                    try:
                        # 1. Получаем ID чата по юзернейму
                        chat = await app.get_chat(chat_username)
                        
                        # 2. Копируем сообщение
                        # thread_id передается в reply_to_message_id
                        await app.copy_message(
                            chat_id=chat.id,
                            from_chat_id=CHANNEL_SOURCE,
                            message_id=last_post.id,
                            reply_to_message_id=thread_id
                        )
                        
                        print(f"✅ Отправлено в {chat_username} (Ветка: {thread_id})")
                        await asyncio.sleep(5) 

                    except FloodWait as e:
                        print(f"⚠️ Ждем {e.value} сек...")
                        await asyncio.sleep(e.value)
                    except Exception as e:
                        print(f"❌ Ошибка в чате {chat_username}: {e}")

            except Exception as e:
                print(f"🚨 Ошибка: {e}")

            print(f"😴 Ждем {INTERVAL} секунд...")
            await asyncio.sleep(INTERVAL)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Остановка.")
