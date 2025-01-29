def byPage(commands, j, page=1):
    message = f"╭─── :bold[COMMANDS] ──⟢\n"
    for cmd in commands[page - 1]:
        message += f"│ {'○' if not j[cmd] else '⌬'} {cmd}\n"
    message += f"╰───{'─' * len('COMMANDS')}─⟢\n"
    message += f"📖 Page: ({page}/{len(commands)})\n"
    return message


def getAll(commands, j):
    message = f"╭─── :bold[COMMANDS] ──⟢\n"
    dal = list()
    for cmd in commands:
        if j[cmd]:
            dal.insert(0, cmd)
        else:
            dal.append(cmd)
    for cmd in dal:
        message += f"│ {'○' if not j[cmd] else '⌬'} {cmd}\n"
    message += f"╰───{'─' * len('COMMANDS')}─⟢\n"
    return message


async def function(bot, event):
    # Extract commands and adminOnly flags
    xzxc = {key: udo['adminOnly'] for key, udo in bot.commands.items()}
    commands = list(bot.commands.keys())
    chunk = 15  # Number of commands per page
    COMMANDS = [commands[i:i + chunk] for i in range(0, len(commands), chunk)]
    
    # Parse input arguments
    sub, *_ = event.args.split(' ', 1) if event.args else [event.args, '']
    args = ' '.join(_)

    if args:
        return await event.sendReply("ⓘ Invalid command usage, type 'help help' to see how to use this command.")

    # Display all commands
    if sub.lower() == 'all':
        message = getAll(commands, xzxc)
        message += f"╭──── :bold[EVENTS] ────⟢\n"
        for ib in bot.events:
            message += f"│ ○ {ib['fileName']}\n"
        message += f"╰────{'─' * len('EVENTS')}──⟢\n\n"
        message += f"📦 Total commands: {len(commands)}\n"
        message += f"ⓘ If you have any questions or need assistance, please contact the developer."
        return await event.sendReply(message, True)

    # Display command info
    if sub.lower() in commands:
        cmd = bot.commands.get(sub.lower())
        message = f"╭─── :bold[{sub.lower()}] ───\n"
        message += f":bold[author]: {cmd.get('author', 'Unknown')}\n"
        message += f":bold[adminOnly]: {cmd.get('adminOnly', False)}\n"
        message += f":bold[usage]: {cmd.get('usage')}\n"
        message += f":bold[description]: {cmd.get('description')}\n"
        message += f"╰────{'─' * len(sub.lower())}───\n"
        return await event.sendReply(message, True)
    elif sub:
        try:
            __nothing__ = int(sub)  # Check if sub is a number
        except ValueError:
            return await event.sendReply(f"ⓘ Command '{sub.lower()}' not found, type 'help all' to see all the commands.")

    # Paginated view of commands
    if sub:
        page = int(sub)
        if page < 1 or page > len(COMMANDS):
            return await event.sendReply(f"Page {sub} is not defined, total command pages: {len(COMMANDS)}")
    else:
        page = 1

    message = byPage(COMMANDS, xzxc, page=page)
    message += f"📦 Total commands: {len(commands)}\n"
    message += f"ⓘ If you have any questions or need assistance, please contact the developer."
    return await event.sendReply(message, True)


config = {
    "name": 'help',
    "def": function,
    "author": 'Muhammad Greeg',
    "usePrefix": False,
    "adminOnly": False,
    "description": "Show the bot available commands",
    "usage": '{p}help [<None>|<page>|<cmd name>|all]'
}
