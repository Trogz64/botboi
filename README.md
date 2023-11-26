# BotBoi

Discord bot that goes by the name BotBoi.  
Invite to your server using the link below or use the code for your own bot!

[Use this link to invite to a server](https://discord.com/api/oauth2/authorize?client_id=416406487024402432&permissions=414464863296&scope=applications.commands%20bot)

---

## config.json

To create your own version of the bot you must create a config.json file in the same directory as `bot.py` with your token in the following format:

```json
{
    "token" : "your token here"
}
```

---

## Dependencies

* Requires [Python](https://www.python.org/) version 3.8 or higher
* Requires [discord.py](https://github.com/Rapptz/discord.py/) version 2.3.2 or higher

    ```sh
    # Linux/macOS
    python3 -m pip install -U discord.py

    # Windows
    py -3 -m pip install -U discord.py
    ```

---

## Features

Botboi has the following slash commands

### Greetings

* `/hellobotboi`
* `/hellothere`

### Commands

* `/wednesday`
* `/goodbot`
* `/badbot`
* `/evaluate [<numbers>]`
* `/birthday [<member>]`
* `/servercount`
* `/roll <number_of_faces>`
* `/poll <question> <option1> <option2> [<option3>] [<option4>] [<option5>] [<option6>] [<option7>] [<option8>] [<option9>]`
* `/github`
* `/invite`
* `/eightball <question>`

### Other

* BotBoi will react with emotes or messages to certain words or phrases when used in a message
