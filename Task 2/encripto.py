import subprocess

def encrypt_file(input_file, output_file, password):
    try:
        command = ["openssl", "enc", "-aes-256-cbc", "-salt", "-in", input_file, "-out", output_file, "-pass", "pass:{}".format(password)]
        subprocess.run(command, check=True)
        print("Файл успешно зашифрован.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения команды OpenSSL: {e}")
    return output_file

def decrypt_file(input_file, output_file, password):
    try:
        command = ["openssl", "enc", "-d", "-aes-256-cbc","-in", input_file, "-out", output_file, "-pass", "pass:{}".format(password)]
        subprocess.run(command, check=True)
        print("Файл успешно дешифрован.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения команды OpenSSL: {e}")
    return output_file


if __name__ == "__main__":
    input_file = "documents.zip"
    output_file = "documents.enc"
    password = "your_password"

    encrypt_file(input_file, output_file, password)