# Cloud adder

## Description
Many tech companies have work chats that new hires must join. Spam protection in Telegram does not allow you to immediately add an employee to all chats, throttling is enabled. The script automates this process and adds the employee to all work chats. It is enough to record work chats in file once, and each new employee can spend time adapting and learning while the script does its work in the background!


## Usage for employer
In order to obtain an API id and develop your own application using the Telegram API you need to do the following:

1. Sign up for Telegram using any application
2. Log in to your Telegram core: https://my.telegram.org
3. Go to "API development tools" and fill out the form
4. You will get basic addresses as well as the api_id and api_hash parameters required for user authorization
5. Add values to variables: 
 - `api_id = <api_id>`
 - `api_hash = "api_hash"`
6. Add invite links to chats in dictionary `"chats"` in `adder.py`. (Example: `"Chat_name": "chat_id"`)
7. Share your script

## Usage for employee
1. Run commands in your home environment
 - `python -m venv .venv`
 - `. .venv/bin/activate`
 - `python -m pip install certifi asyncio functools typing tqdm Telethon pathlib ssl httpx`

If some libraries are not installed, it's okay
    
2. Copy or download adder.py from employer

4. Run  `python3 adder.py`

4. Enter your personal code that you will receive from Telegram, and press "Enter", the addition will begin. If you are already in the chat, the addition will move to the next chat. If Telegram enables throttling protection, the script will wait for the required time and continue adding.

5. After adding to all chats, go to Active Sessions in Telegram Settings and delete the Clouder user from whom the addition was performed
