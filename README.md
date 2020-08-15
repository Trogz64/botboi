# BotBoi

## Work In Progress

Discord bot that goes by the name BotBoi.  
Invite to your server using the link below, or use the code for your own bot!

[Use this link to invite to a server](https://discordapp.com/api/oauth2/authorize?client_id=416406487024402432&permissions=523328&redirect_uri=https%3A%2F%2Fdiscordapp.com%2Fapi%2Foauth2%2Fauthorize%3Fclient_id%3D416406487024402432%26permissions%3D518208%26redirect_uri%3Dhttps%253A%252F%252Fdiscordapp.com%252Fapi%252Foauth2%252Fauthorize%253Fclient_&scope=bot)

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

* Requires [Python](https://www.python.org/) version 3.5.3 or higher
* Requires [discord.py](https://github.com/Rapptz/discord.py/) version 1.0 or higher

    ```sh
    # Linux/macOS
    python3 -m pip install -U discord.py

    # Windows
    py -3 -m pip install -U discord.py
    ```

---

## Features

* --help

### Greetings

* --hellobotboi
* --hellothere
* --heyyy

### Commands

* --chaostime
* --wednesday
* --goodbot
* --badbot
* --evaluate \<numbers\>
* --birthday [@mention/multiple @mentions]
* --servercount
* --roll d[Number of faces]
* --poll [Question]|[Option1]|[Option2]|...|[Option9]
* --github
* --invite

### Other

* BotBoi will reply with emotes or messages to certain words or phrases when used in a message
