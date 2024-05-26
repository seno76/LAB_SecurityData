import sys
import os
import socket
import encripto
import random

def receive_file(server_port, save_file_path):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind(('0.0.0.0', server_port))
        server_socket.listen(5)
        print("Сервер запущен. Ожидание подключений...")
        while True:
            client_socket, _ = server_socket.accept()
            data = client_socket.recv(4096)
            message = data.decode('utf-8')
            g, A, p = message.split(":")
            b = random.randint(100000000000, 100000000000000000000000)
            B = pow(int(g), int(b), int(p))
            client_socket.send(str(B).encode("utf-8")) 
            K = pow(int(A), b, int(p))
            try:
                if os.path.exists(save_file_path):
                    sys.stderr.write("Файл '{}' уже существует. Новые данные не будут записаны.\n".format(save_file_path))
                else:
                    with open("file.enc", 'wb+') as file:
                            while True:
                                file_data = client_socket.recv(4096)
                                file.write(file_data)
                                if not file_data:
                                    break
                            print("Файл успешно сохранен как '{}'.".format(save_file_path))
                    encripto.decrypt_file("file.enc", save_file_path, K)
            except Exception as e:
                sys.stderr.write("Ошибка при получении файла: {}\n".format(str(e)))
            finally:
                client_socket.close()
                break
    except Exception as e:
        sys.stderr.write("Ошибка при запуске сервера: {}\n".format(str(e)))
    finally:
        server_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.stderr.write("Использование: {} port save-file-path\n".format(sys.argv[0]))
        sys.exit(1)

    server_port = int(sys.argv[1])
    save_file_path = sys.argv[2]
    receive_file(server_port, save_file_path)