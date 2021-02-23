const schedule = require('node-schedule');

module.exports = {
	name: 'schedule',
	description: 'Command to schedule events',
	execute(message, args) {
        if (!args.length) {
            message.channel.send("No arguements passed");
        }
        else if (args.length === 1) {
            const job = schedule.scheduleJob(`${args[0]} * * * * *`, function() {
                message.channel.send(`pogpogpog${args[0]}`);
            });
        }

        message.channel.send(`Command name: ${message}\nArguements: ${args}`);
	},
};