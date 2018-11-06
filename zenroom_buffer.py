import ctypes

_zenroom = ctypes.CDLL('./zenroom/_zenroom_1.8.1.so')

def execute(script, keys, data, verbosity=1, conf=None):
    stdout_buf = ctypes.create_string_buffer("x" * 10000)
    stdout_len = ctypes.c_size_t(10000)
    stderr_buf = ctypes.create_string_buffer("x" * 1024)
    stderr_len = ctypes.c_size_t(1024)

    _zenroom.zenroom_exec_tobuf(
      script, conf, keys, data, verbosity,
      stdout_buf, stdout_len, stderr_buf, stderr_len)
    
    # if(stderr_buf.value is not None):
    #     return stderr_buf.value
    
    return stdout_buf.value
