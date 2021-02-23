const schedule = require('node-schedule');

module.exports = {
	name: 'schedule',
	description: 'Command to schedule events',
	execute(message, args) {
        const job = schedule.scheduleJob('25 * * * * *', function() {
            message.channel.send('pogpogpog');
        });
        
        message.channel.send(`Command name: ${message}\nArguements: ${args}`);
	},
};