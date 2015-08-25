import lexer
import sys

# Create an environment for storing of variables and functions. 
# Essentially a dictionary
Env = dict

# Create a basic environment with basic functions 
def standard_env():
    env = Env()
    env.update({
        '+': lambda args:reduce(lambda x,y:x+y,args),
        '-': lambda args:0-args[0] if len(args)==1 else reduce(lambda x,y:x-y,args),
        '*': lambda args:reduce(lambda x,y:x*y,args),
        '/': lambda args:reduce(lambda x,y:x/y,args),
        'frac': lambda x: float(x[0]/x[1]),
    })
    return env

# Setting the created environment as the global environment.
# For easy understanding
global_env = standard_env()

# Evaluates a dynamic list of tokens as passed on from the lexer module
# Input : Dynamic List of token tuples 
# Returns : Value of the parent command in the dynamic list
def eval(token, env=global_env):
	# Base Cases: 
	# Case 1: If the token is a symbol, return the equivalent funtion as stored in the environment.
	if token[1]==lexer.SYM:
		return env[token[0]]
	# Case 2: If the token is a variable, return the respective value from the environment
	elif token[1]==lexer.VAR:
		return env[token[0]]
	# Case 3: If the token is a number, parse it into an Integer and return it
	elif token[1]==lexer.NUM:
		return float(token[0])
	# Case 4: This means that token is basically a list itself containing a function and two arguments
	else:
		# Case 4-1: If the function is a bind function, create a varible of the respective name in the environment, and return the same
		if token[0][0]=='bind':
			env[token[1][0]]=eval(token[2:][0],env)
			return env[token[1][0]]
		# Case 4-2: This means the function is an operator. In this case we obtain the respective function corresponding to 
		# the operator from the environment and store it into "process". The rest of the items in the list are individually 
		# evaluated and we store the obtained values in the list into a list called 
		# "arguments". We return the value obtained from running the process on the arguments 
		else:
			process = eval(token[0], env)
			arguments = [eval(arg, env) for arg in token[1:]]
			return process(arguments)

if __name__ == '__main__':
	# Reading the input file
    filename = sys.argv[1]
    file = open(filename)
    characters = file.read()
    file.close()
    # Cleaning the input
    tokens=lexer.segment(characters)
    result='Invalid program'
    # Try statement to bypass all exceptions raised
    try:
	    for token in lexer.superlex(tokens):
	    	result=eval(token)
    except Exception:
    	pass
    print result
