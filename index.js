const Discord = require('discord.js');
const bot = new Discord.Client();
const config = require("./config.json");

bot.on('message', (message) => {
    if(message.content == 'ping') {
        message.channel.send('pog');
    }
});

bot.login(config.token);