const schedule = require('node-schedule');
fs = require('fs');

module.exports = {
	name: 'jobs-schedule',
	description: 'Command to schedule repeating events at a certain datetime.',
	execute(message, args) {
        if (!args.length) {
            message.channel.send(`Command name: ${module.exports.name}\nUse cron format: second minute hour day-of-month month day-of-week`);
        }
        else if (args.length !== 5) {
            // todo: check if each arguement is valid
            const job = schedule.scheduleJob(`${args[0]} ${args[1]} ${args[2]} ${args[3]} ${args[4]} ${args[5]}`, function() {
                message.channel.send("pogpogpog");
            });
        }
    }
};