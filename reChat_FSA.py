# import relevant modules (regular expressions)
import re

# create the function to solve the reChat problem
def reChatParseCommand(message, state):
    
    # Define necessary Regex variables for what constitutes a valid Username and Channel name
    
    validUsernameRegex = r'''@[a-z]+(\.[a-z]+)*@[a-z]+(\.[a-z]+)*(\.org|\.com)'''
    validChannelRegex = r'''#([A-Za-z][A-Za-z0-9]*)'''
    
    # set of what are valid specs for the list command
    validSpec = {'channels', 'users'}
    
    # set of what are valid commands for user input, message is not included as it does not have a specific string
    commands = {'', '\\list ',  '\\quit', '\\join ', '\\dm ', '\\leave', '\\read'}
    
    # Function that is called when an input is invalid, the message and state must both be valid
    def invalidInput(message, state):
        action = {'error': 'Invalid command'}
        return action, state

    # Function that checks if the state is None meaning the program has just started, otherwise
    # determines the current state stored in the state dictionary 'mode' key, as the program has been run before
    def determineState(state):
        # Initial state is just None and is not a dictionary
        if state == None:
            return None
        # Check for the state in the mode key of the state dictionary
        mode = state.get('mode')
        if mode == 'command':
            return 'command'
        elif mode == 'channel':
            return 'channel'
        elif mode == 'direct message':
            return 'direct message'

    # Function that determines whether the input message is valid, and returns an overarching string message
    # All valid messages can be determined if it begins with a command, while a message
    # is not a specific string, and can be any input that does not start with '\\' in the correct state.
    def determineMessage(message):
        # Check if any of the messages starts with a command from commands set
        if any(message.startswith(command) for command in commands):
            # User is messaging to connect initially
            if message == '':
                return ''
            # User is messaging the list command
            elif message.startswith('\\list '):
                return determineValidSpec(message)
            # User is messaging the quit command
            elif message == '\\quit':
                return '\\quit'
            # User is messaging the join command
            elif message.startswith('\\join '):
                return determineValidChannelName(message)
            # User is messaging the dm command
            elif message.startswith("\\dm "):
                return determineValidUsername(message)
            # User is messaging the leave command
            elif message == '\\leave':
                return '\\leave'
            # User is messaging the read command
            elif message == '\\read':
                return '\\read'
        # If the message does not start with any command, then if it does not start with '\\' it is a message
        if not message.startswith('\\'):
                return '<message>'
    
    # Function that determines whether the user messaged a valid spec, with the command for list
    def determineValidSpec(message):
        # Check the spec by removing the list command portion of the message
        spec = message[len('\\list '):]
        # Check if they input one of the two valid specs 'channels' or 'users'
        if spec in validSpec:
            # if the message the user input was the valid list command from commands set
            # with string concatenation add the spec from the validSpec set
            # if the entire message is a valid string concatenation of both, it is a full valid input for the list command
            if message == ('\\list ' + spec):
                return '\\list '
    
    # Function that determines whether the user messaged a valid channel name, with the command for join
    def determineValidChannelName(message):
        # Check the channel name by removing the join command portion of the message
        channelName = message[len('\\join '):]
        # Check if a valid channel name can be found in the message using the validChannelRegex
        validChannelNameMatch = re.fullmatch(validChannelRegex, channelName)
        if validChannelNameMatch:
            # Turn the validChannelNameMatch object into a string
            validChannelName = validChannelNameMatch.group(0)
            # Check if the message the user input was the valid join command from commands set
            # with string concatenation add the validChannelName
            # if the entire message is a valid string concatenation of both, it is a full valid input for the join command
            validChannelMessage = '\\join ' + validChannelName
            if message == validChannelMessage:       
                return '\\join '
    
    # Function that determines whether the user messaged a valid username, with the command for dm
    def determineValidUsername(message):
        # Check the username by removing the join command portion of the message
        username = message[len('\\dm '):]
        # Check if a valid username can be found in the message using the validChannelRegex
        validUsernameMatch = re.fullmatch(validUsernameRegex, username)
        if validUsernameMatch:
            validUsername = validUsernameMatch.group(0)
            # Check if the message the user input was the valid dm command from commands set
            # with string concatenation add the validUsernameMatch
            # if the entire message is a valid string concatenation of both, it is a full valid input for the join command
            validUsernameMessage = '\\dm ' + validUsername
            if message == validUsernameMessage:       
                return '\\dm '
    
    # Function that checks the message and state for whether it is valid to connect the user to reChat
    def Connect(message, state):
        # Assign action and state
        action = {'action': 'greeting'}
        state = {'mode': 'command', 'validRegex': None}
        return action, state
    
    # Function that checks the message and state for whether a user can use the \list command.
    def List(message, state):
        # Identify spec portion of the message
        # Check if user input a valid <spec> for the spec language to use the \list command
        spec = message[len('\\list '):]
        action = {'action': 'list', 'param': spec}
        state = {'mode': 'command', 'validRegex': None}
        return action, state
           
    # Function that checks the message and state for whether a user can \quit
    def Quit(message, state):
        # Assign action and state for quitting from command state
        action = {'action': 'quit'}
        state = {'mode': 'command', 'validRegex': None}
        return action, state
    
    # Function that checks the message and state for whether a user can \join
    def Join(message, state):
        # Find the channel name by removing the join command portion
        channelName = message[len('\\join '):]
        # Assign action and state
        action = {'action': 'join', 'channel': channelName}
        # channelName is assigned to the validRegex portion of the state dictionary, used for further calls of reChatParseCommand
        state = {'mode': 'channel', 'validRegex': channelName}  
        return action, state
    
    # Function that checks the message and state for whether a user can \dm
    def DM(message, state):
        # Find the channel name by removing the dm command portion
        username = message[len('\\dm '):]
        # Assign action and state
        action = {'action': 'dm', 'user': username}
        # username is assigned to the validRegex portion of the state dictionary, used for further calls of reChatParseCommand
        state = {'mode': 'direct message', 'validRegex': username}
        return action, state
    
    # Function that checks the message and state for whether a user can \leave
    def Leave(message, state):
        # Leave is a command possible to be operated while in both channel and direct message states
        # Differentiate whether the state is a channel or direct message state by the validRegex key in state dictionary
        validRegex = state.get('validRegex')
        # channel state will always have a validRegex of channelName, that must start with #
        if validRegex.startswith('#'):
            channelName = validRegex
            action = {'action': 'leaveChannel', 'channel': channelName}
            # Remove the validRegex when user leaves this state
            state = {'mode': 'command', 'validRegex': None}
            return action, state
        # direct message state will always have a validRegex of username, that must start with @
        if validRegex.startswith('@'):
            username = state.get('validRegex')
            action = {'action': 'leaveDM', 'user': username}
            # Remove the validRegex when user leaves this state
            state = {'mode': 'command', 'validRegex': None}
            return action, state
    
    # Function that checks the message and state for whether a user can \read
    def Read(message, state):
        # Read is a command possible to be operated while in both channel and direct message states
        # Differentiate whether the state is a channel or direct message state by the validRegex key in state dictionary
        validRegex = state.get('validRegex')
        # channel state will always have a validRegex of channelName, that must start with #
        if validRegex.startswith('#'):
            channelName = validRegex
            action = {'action': 'readChannel', 'channel': channelName}
            state = {'mode': 'channel', 'validRegex': channelName}
            return action, state
        # direct message state will always have a validRegex of username, that must start with @
        if validRegex.startswith('@'):
            username = validRegex
            action = {'action': 'readDM', 'user': username}
            state = {'mode': 'direct message', 'validRegex': username}
            return action, state
    
    # Function that checks the message and state for whether a user can \message
    def Message(message, state):
        # Use re.finditer to check for all valid usernames with validUsernameRegex in the message
        # To be assigned as mentions, which are displayed in action
        mentions = {mention.group(0) for mention in re.finditer(validUsernameRegex, message)}
        # Message is a command possible to be operated while in both channel and direct message states
        # Differentiate whether the states is a channel or direct message state by the validRegex key in state dictionary
        validRegex = state.get('validRegex')
        # channel state will always have a validRegex of channelName, that must start with #
        if validRegex.startswith('#'):
            channelName = validRegex
            action = {'action': 'postChannel','channel': channelName,'message': message,'mentions': mentions}
            state = {'mode': 'channel', 'validRegex': channelName}
            return action, state
        # direct message state will always have a validRegex of username, that must start with @
        if validRegex.startswith('@'):
            username = validRegex
            action = {'action': 'postDM','user': username,'message': message,'mentions': mentions}
            state = {'mode': 'channel', 'validRegex': username}
            return action, state
    
    # Dispatch table that has the key (state, message): function. This means that only if
    # The assigned valid state and message is provided, that the function associated with the key
    # (state, message) is callable
    # For example, if in the command state, and a user enters a message that is valid to use the \list command
    # Then the function List can be used
    transitionTable = {
        # commands for users with no state
        (None, ''): Connect,
        # commands for users with command state
        ('command', '\\list '): List,
        ('command', '\\quit'): Quit,
        ('command', '\\join '): Join,
        ('command', '\\dm '): DM,
        # commands for users with channel state
        ('channel', '\\leave'): Leave,
        ('channel', '\\read'): Read,
        ('channel', '<message>'): Message,
        # commands for users with direct message state
        ('direct message', '\\leave'): Leave,
        ('direct message', '\\read'): Read,
        ('direct message', '<message>'): Message,
        }
    
    # Function that uses the dispatch table, taking in the message and state provided to reChatParseCommand
    # To decide whether a transition in the finite state automata is valid
    def determineTransition(message, state):
        # transition is the transition in finite state automata, if provided a state and message
        # Whether the state can transition to the next state
        # The state and message provided to reChatParseCommand is used for the determine functions
        # If a valid state is provided for determineState to assign the state to determinedState, and
        # If a valid message is provided for determineMessage to assign the message to determinedMessage
        # transitionTable.get looks through the dispatch table dictionary for a valid match
        # To the assigned state and message, if not the default value is an invalidInput meaning
        # The transition to the next state is rejected
        determinedState = determineState(state)
        determinedMessage = determineMessage(message)
        # If determinedMessage is an empty string, if the state is None this means to establish a connection
        if determinedMessage == "":
        # If the state is in channel or direct message modes
        # Empty string is a valid message
            if determinedState != None and determinedState in ('channel', 'direct message'):
                determinedMessage = '<message>'
        
        # Check if a transition is possible, must have valid state and message found in the dispatch table
        # Otherwise if valid input is not found, invalidInput is the default value
        transition = transitionTable.get((determinedState, determinedMessage), invalidInput)
        return transition(message, state)

    # The final action and state, is the returned value for the message and state from transition
    # This transition could either be valid and accepted, or invalid and rejected
    action, state = determineTransition(message, state)
    
    return action, state