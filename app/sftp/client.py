"""Simple SFTP polling example."""
import paramiko
from pathlib import Path


def download_files(host: str, username: str, password: str, remote_dir: str, local_dir: str):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password)
    sftp = client.open_sftp()
    Path(local_dir).mkdir(parents=True, exist_ok=True)
    for filename in sftp.listdir(remote_dir):
        remote_path = f"{remote_dir}/{filename}"
        local_path = Path(local_dir) / filename
        sftp.get(remote_path, str(local_path))
    sftp.close()
    client.close()
