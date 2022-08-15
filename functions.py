import os


def config_replacement(directory, template, config, P20TToken, CSRFToken, APICaptchaToken, count):
    with open(f'{directory}/{template}') as pattern_file:
        program = pattern_file.read()

    replacement = {
        '<p20t>': P20TToken,
        '<csrf>': CSRFToken,
        '<captcha>': str(APICaptchaToken),
        '<count>': str(count),
    }

    for key, value in replacement.items():
        program = program.replace(key, value)

    with open(f'{directory}/{config}', 'w') as files:
        files.write(program)


def upload_file(client, directory, config, path, template):
    files = os.listdir(path)
    files.remove(template)
    with client.open_sftp() as sftp:

        for file in files:
            file = f'{directory}/{file}'
            sftp.put(file, file)

    os.remove(f'{directory}/{config}')


def exec_command(client, command):
    stdout, = client.exec_command(command)[1:2]
    return False if stdout.read().decode() else True


def application_launch_logic(client, directory, executable, requirements, path):
    tmux_installed = exec_command(client, 'apt list --installed | grep tmux')
    if tmux_installed:
        exec_command(client, 'sudo apt update')
        exec_command(client, 'sudo apt install tmux -y')

    if requirements in os.listdir(path):
        pip_installed = exec_command(client, 'apt list --installed | grep python3-pip')
        if pip_installed:
            exec_command(client, 'sudo apt install python3-pip -y')
        exec_command(client, f"pip3 install -r {directory}/{requirements}")

    exec_command(client, "tmux new -d -s test")
    exec_command(client, f"tmux send-keys -t test.0 'python3 {directory}/{executable}' ENTER")
