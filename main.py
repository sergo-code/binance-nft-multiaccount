import paramiko
import pandas as pd
import json
from errors import *

from functions import *
from config import *


def main():
    path = os.getcwd() + '/' + directory

    paramiko.util.log_to_file("paramiko.log", 'INFO')
    # Loading profiles
    df = pd.read_excel(io=f'{exel_file}', sheet_name=0)
    profiles = json.loads(df.to_json(orient='records'))
    print(f'Number of profiles: {len(profiles)}')
    # Launching all profiles
    for profile in profiles:
        with paramiko.SSHClient() as client:
            try:
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(hostname=profile['HOST'],
                               username=profile['USER'],
                               password=profile['PASSWORD'],
                               port=22)
                # File processing
                config_replacement(directory,
                                   template,
                                   config,
                                   profile['P20TToken'],
                                   profile['CSRFToken'],
                                   profile['APICaptchaToken'],
                                   profile['Count'])
                # Сreating a directory for files
                exec_command(client, f"mkdir {directory}")
                # Uploading files to the server
                upload_file(client, directory, config, path, template)
                # Installing dependencies and running the program
                application_launch_logic(client, directory, executable, requirements, path)
            except TimeoutError:
                print(ERROR_TIMEOUT, profile["HOST"])


if __name__ == "__main__":
    main()
