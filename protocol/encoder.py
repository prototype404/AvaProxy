import struct


def encode_value(raw_data, for_dict: bool = False):
    match raw_data:
    
        case None: return struct.pack(">b", 0)
        case  bool(value): return encode_bool(value)
        case   int(value): return encode_int(value)
        case float(value): return encode_float(value)
        case   str(value): return encode_string(value, for_dict)
            
        case dict(value):
            final_data  = struct.pack(">b", 6)
            final_data += encode_dict(raw_data)
            
        case list(value):
            final_data  = struct.pack(">b", 7)
            final_data += encode_list(raw_data)

    return final_data

def encode_bool(value: bool):
    final_data: bytes = struct.pack(">b", 1)
    final_data += struct.pack(">b", int(value))
    return final_data

def encode_int(value: int):
    if value <= 2147483647: # 4 bytes
        final_data: bytes = struct.pack(">b", 2)
        final_data += struct.pack(">i", value)
    else: # 8 bytes
        final_data: bytes = struct.pack(">b", 3)
        final_data += struct.pack(">q", value)
    return final_data

def encode_float(value: float):
    final_data: bytes = struct.pack(">b", 4)
    final_data += struct.pack(">d", value)
    return final_data

def encode_string(value: str, for_dict: bool):
    final_data: bytes = b""
    if not for_dict:
        final_data += struct.pack(">b", 5)
    length = len(value.encode().hex())//2
    while (length & 4294967168) != 0:
        final_data += struct.pack(">B", length & 127 | 128)
        length = length >> 7
    final_data += struct.pack(">h", length & 127)
    final_data += value.encode()
    return final_data

def encode_dict(obj: dict):
    final_data: bytes = struct.pack(">i", len(obj))
    for key in obj.keys():
        final_data += encode_value(key, True)
        final_data += encode_value(obj[key])
    return final_data

def encode_list(arr: list):
    final_data = struct.pack(">i", len(arr))
    for item in arr:
        final_data += encode_value(item)
    return final_data
