import os, sys, select, ctypes

### source: https://stackoverflow.com/questions/9488560/capturing-print-output-from-shared-library-called-from-python-with-ctypes-module #

def setup_pipe():
    global pipe_out, pipe_in, stdout
    sys.stdout.write(' \b')
    pipe_out, pipe_in = os.pipe()
    stdout = os.dup(1)
    os.dup2(pipe_in, 1)

def more_data():
    r, _, _ = select.select([pipe_out], [], [], 0)
    return bool(r)

def read_pipe():
    out = ''
    while more_data():
        out += os.read(pipe_out, 1024)

    return out
###

# Init shared library
_zenroom = ctypes.CDLL('zenroom/_zenroom.so')

# Get script
with open('zenroom/encrypt_message.lua', 'r') as input:
    script = input.read()
 
def encrypt_data(data, keys):
    setup_pipe()
    _zenroom.zenroom_exec(script, None, keys, data, 1) # params: script, conf, keys, data, verbosity
    os.dup2(stdout, 1)
    return read_pipe()

# Will come from PWA
with open('zenroom/pub_key.keys', 'r') as input:
    public_key = input.read()

# Personal data from user
testData = "Whatever"

# output = encrypt_data(testData, public_key)
# print(output)