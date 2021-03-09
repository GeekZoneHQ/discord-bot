# discord-bot

The Geek.Zone stand-up bot

---
## Documentation

### config.json
```
{
    "role": int,                            <-- int: role id of role to message
    "msg": {
        "start": "YYYY-MM-DD HH:MM:SS",     <-- first time the message will be sent
        "interval": "DD HH:MM:SS",          <-- interval for sending this message
    }
}
```