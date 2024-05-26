import data

def main(in_file, out_file):
    block = 89
    stream_2 = open(out_file, "wb")
    with open(in_file, "rb") as stream_1:
        while True:
            chunk = stream_1.read(block)
            if not chunk:
                break
            encrypted_chunk = encrypt(chunk, len(chunk))
            stream_2.write(bytes(encrypted_chunk))
    stream_2.close()

def encrypt(__block, __edflag):

    __block = list(__block)

    substitute(__block,__edflag)
    permutate(__block,__edflag)
    substitute(__block,__edflag)

    substitute(__block,__edflag)
    permutate(__block,__edflag)
    substitute(__block,__edflag)

    substitute(__block,__edflag)
    xor(__block,__edflag)
    permutate(__block,__edflag)
    
    xor(__block,__edflag)
    substitute(__block,__edflag)
    xor(__block,__edflag)

    return __block

def substitute(arr, param_2):
    for local_c in range(param_2):
        arr[local_c] = data.substitution_table[arr[local_c]]

def permutate(arr, param_2):
    new_stack = [0] * 40
    for local_c in range(0, param_2 - 26, 27):
        for local_10 in range(27):
            new_stack[local_10] = arr[local_c + int(data.permutation[local_10])]
        for local_10 in range(27):
            arr[local_10 + local_c] = new_stack[local_10]

def xor(arr, param_2):
    local_10 = 0
    for local_c in range(param_2):
        arr[local_c] = arr[local_c] ^ data.xor_key[local_10]
        local_10 = (local_10 + 1) % 40

print(main("text.txt", "encode.txt"))