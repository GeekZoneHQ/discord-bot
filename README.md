# discord-bot

The Geek.Zone stand-up bot

---
## Documentation

### config.json
```
{
    "role": int,                        <-- int: role id of role to message

    "start": "YYYY-MM-DD HH:MM:SS",     <-- first time the first message will be sent
    "interval": "DD HH:MM:SS",          <-- interval between each message (of each iteration)

    "msg1": " This is the first message to send."
}
```