import sys
import os
import socket
import encripto
import df
import random

def send_file(server_address, file_path):

    if not os.path.exists(file_path):
        sys.stderr.write("Ошибка: Файл '{}' не существует!\n".format(file_path))
        return

    address_parts = server_address.split(':')
    server_host = address_parts[0]
    server_port = int(address_parts[1])

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_host, server_port))
        g = df.G
        a = random.randint(10000000000, 100000000000000000000000)
        p = df.P
        A = pow(g, a, p)
        str_ = str(g) + ':' + str(A) + ':' + str(p)
        client_socket.send(str_.encode('utf-8'))
        data = client_socket.recv(4096)
        B = data.decode('utf-8')
        K = pow(int(B), a, p)
        file_path = encripto.encrypt_file(file_path, "start.txt", K)
        with open(file_path, 'rb') as file:
            file_data = file.read()
            client_socket.sendall(file_data)
            print("Файл успешно отправлен на сервер.")

    except Exception as e:
        sys.stderr.write("Ошибка при отправке файла: {}\n".format(str(e)))
    finally:
        client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.stderr.write("Использование: {} address:port file-path\n".format(sys.argv[0]))
        sys.exit(1)

    server_address = sys.argv[1]
    file_path = sys.argv[2]
    send_file(server_address, file_path)