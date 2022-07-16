import paramiko
import pandas as pd
import json
import os


def upload_file(client, P20TToken, CSRFToken):
    with open('mysteryBox/config_pattern.py') as pattern_file:
        program = pattern_file.read()
    program = program.replace('<p20t>', P20TToken).replace('<csrf>', CSRFToken)

    with open(f'mysteryBox/config.py', 'w') as files:
        files.write(program)

    sftp = client.open_sftp()
    remotepath = 'mysteryBox.py'
    localpath = './mysteryBox/mysteryBox.py'
    sftp.put(localpath, remotepath)
    remotepath = 'config.py'
    localpath = './mysteryBox/config.py'
    sftp.put(localpath, remotepath)
    if sftp:
        sftp.close()
    os.remove('mysteryBox/config.py')


def exec_command(client, command):
    stdout, = client.exec_command(command)[1:2]
    data = stdout.read().decode()
    if data:
        return False
    else:
        return True


def send_command(client):
    tmux_installed = exec_command(client, 'apt list --installed | grep tmux')
    if tmux_installed:
        exec_command(client, 'sudo apt update')
        exec_command(client, 'sudo apt install tmux -y')

    exec_command(client, "tmux new -d -s test")
    exec_command(client, "tmux send-keys -t test.0 'python3 mysteryBox.py' ENTER")


def main():
    # paramiko.util.log_to_file("paramiko.log")
    df = pd.read_excel('data.xlsx')
    data_json = json.loads(df.to_json(orient='records'))

    print(f'Количество профилей: {len(data_json)}')

    for profile in data_json:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(hostname=profile['HOST'], username=profile['USER'], password=profile['PASSWORD'], port=22)

            upload_file(client, profile['P20TToken'], profile['CSRFToken'])
            send_command(client)

            if client:
                client.close()
        except TimeoutError:
            print(f'Что-то не так с сервером / данными [{profile["HOST"]}]')


if __name__ == "__main__":
    main()
