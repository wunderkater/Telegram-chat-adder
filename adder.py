import certifi
import asyncio
from functools import partial
from typing import Tuple, Type
from tqdm.asyncio import tqdm, tqdm_asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon import errors as tgerrors
from telethon import functions as tgfunctions
import ssl
import httpx
from os import path
from pathlib import Path

chats = {"Chat_name": "chat_id"}
api_id = <api_id>
api_hash = "api_hash"

home = str(Path.home())
packagelocation = path.dirname(path.realpath(__file__))
context = ssl.create_default_context()
context.load_verify_locations(cafile=certifi.where())
client = httpx.AsyncClient(verify=context)


async def get_telegram_session():
    def get():
        try:
            with open(f"{home}/.telegramsession", "r") as s:
                session = s.read().strip()
                return StringSession(session)
        except:
            return StringSession(None)

    return await asyncio.to_thread(get)


async def save_telegram_session(session):
    def save(session):
        with open(f"{home}/.telegramsession", "w") as s:
            session = s.write(session)

    await asyncio.to_thread(save, session)


async def add_to_chat(client: TelegramClient, tqdm: Type[tqdm_asyncio], pbar: tqdm_asyncio, i: Tuple[str, str]):
    try:
        await client(tgfunctions.messages.ImportChatInviteRequest(i[1]))
    except tgerrors.rpcerrorlist.InviteHashExpiredError:
        tqdm.write(f"Invite link expired for chat {i[0]}")
    except (tgerrors.rpcerrorlist.InviteHashInvalidError, tgerrors.rpcerrorlist.InviteHashEmptyError):
        tqdm.write(f"Invalid link for chat {i[0]}")
    except tgerrors.rpcerrorlist.FloodWaitError as e:
        throttled = int(str(e).split(" ")[3])
        tqdm.write(f"Telegram api throttled for {throttled} seconds")
        for t in range(throttled):
            pbar.set_postfix(chat=i[0], sleep=f"{t}/{throttled} seconds")
            await asyncio.sleep(1)
        await add_to_chat(client, tqdm, pbar, i)
    except Exception as e:
        tqdm.write(f"While adding to chat {i[0]}, error: {e}")
    for t in range(10):
        pbar.set_postfix(chat=i[0], sleep=f"{t}/{10} seconds")
        await asyncio.sleep(1)


async def main():
    print(f"Recieved {len(chats)} chats")
    print("initializing telethon from $HOME/.telegramsession")
    session = await get_telegram_session()
    client = TelegramClient(retry_delay=3, request_retries=10, session=session, api_id=api_id, api_hash=api_hash)
    await client.start(code_callback=partial(asyncio.to_thread, input, "Please enter telegram code: "))
    await save_telegram_session(client.session.save())
    print("Adding you to chats")
    with tqdm(chats.items()) as pbar:
        async for i in pbar:
            i: Tuple[str, str]
            pbar.set_postfix(chat=i[0])
            await add_to_chat(client, tqdm, pbar, i)
    await client.disconnect()

    
asyncio.run(main())
