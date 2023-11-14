import subprocess

def get_docker_buildx_ls():
    try:
        result = subprocess.run(["docker", "buildx", "ls"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None

# 調用函數並打印結果
output = get_docker_buildx_ls()
if output is not None:
    print(output)