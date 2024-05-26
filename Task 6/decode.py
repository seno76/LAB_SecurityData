import data

def main(in_file, out_file):
    block = 89
    stream_2 = open(out_file, "wb")
    with open(in_file, "rb") as stream_1:
        while True:
            chunk = stream_1.read(block)
            if not chunk:
                break
            decrypted_chunk = decrypt(chunk, len(chunk))
            stream_2.write(bytes(decrypted_chunk))
    stream_2.close()


def decrypt(__block, __edflag):

    __block = list(__block)

    xor(__block,__edflag)
    substitute(__block,__edflag)
    xor(__block,__edflag)

    permutate(__block,__edflag)
    xor(__block,__edflag)
    substitute(__block,__edflag)

    substitute(__block,__edflag);
    permutate(__block,__edflag);
    substitute(__block,__edflag);

    substitute(__block,__edflag);
    permutate(__block,__edflag);
    substitute(__block,__edflag);

    return __block

def substitute(arr, param_2):
    for local_c in range(param_2):
        arr[local_c] = data.substitution_table.index(arr[local_c])

def xor(arr, param_2):
    local_10 = 0
    for local_c in range(param_2):
        arr[local_c] = arr[local_c] ^ data.xor_key[local_10]
        local_10 = (local_10 + 1) % 40


def permutate(arr, param_2):
    new_stack = [0] * 40
    for local_c in range(0, param_2 - 26, 27):
        for local_10 in range(27):
            new_stack[local_10] = arr[local_c + data.permutation.index(local_10)]
        for local_10 in range(27):
            arr[local_10 + local_c] = new_stack[local_10]


main("t20.txt", "decoded_text.txt")