import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.messages import GetHistoryRequest

api_id = 27977689
api_hash = 'ccc6a9f87c64d9657183392af5355ddc'
phone_number = '+88809612473'
session_string = '1ApWapzMBu4nvev5A6dByTHcrxe2nI9qIhXFqOpiWPn_c10gRHLhpjunESIa3oWWPbNAELsAgjpQeMZG2HLvkTioXlZv1bhmn1yAXeaV6kzvpCLYlVPGWceV2B9I-x4R1tCgvQjucBhT6zFcOas8kUnLWdI3Jsg9eSd8mPnsTai6-UvZ3KrpHjIgeOXBLI6bxvX1-5UZ8iHz0ba908b2ep4cppvuRet6bq5GKQa5EGQqFrlorbGcYKM5skdW-AEltj5Vo60qGhtg80GUbI8o5rnuDt2nFEw1eL0SxAIPtazaEXRu_qjb9X3ytU0k9NwW6AmkcKn7KVK2v8LpFqinL97kdycA921M='  # Замените на вашу строку сессии

source_group_id = -1001729585806  # Замените на свою
destination_group = 'https://t.me/+Kv5_h7cuMYYzZDZi'

async def main():
    async with TelegramClient(StringSession(session_string), api_id, api_hash) as client:
        source_group = await client.get_entity(source_group_id)

        last_processed_message_id = 0

        while True:
            messages = await client(GetHistoryRequest(
                peer=source_group,
                limit=10,
                offset_id=last_processed_message_id,
                offset_date=None,
                add_offset=0,
                max_id=0,
                min_id=0,
                hash=0
            ))

            new_messages = [msg for msg in reversed(messages.messages) if msg.id > last_processed_message_id]

            for message in new_messages:
                if message.to_id:
                    if message.video:
                        media = message.video
                        await client.send_file(destination_group, media)

                        last_processed_message_id = message.id
                        await asyncio.sleep(10)  # Задержка между отправкой сообщений (10 секунд)
                    else:
                        print(f"Skipped message {message.id} because it's not a video")
                else:
                    print(f"Skipped message {message.id} because 'to_id' is None")

            await asyncio.sleep(30)  # Задержка между запросами (30 секунд)

asyncio.run(main())

