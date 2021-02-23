module.exports = {
	name: 'args-info',
	description: 'Command to test arguements',
	execute(message, args) {
		if (!args.length) {
            return message.channel.send(`No arguements provided, ${message.author}`);
        }
        else if (args[0] === 'foo') {
            return message.channel.send('bar');
        }
        
        message.channel.send(`Command name: ${message}\nArguements: ${args}`);
	},
};