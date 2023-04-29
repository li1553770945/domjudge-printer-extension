import datetime
import subprocess
import time
import os
import requests
from requests.auth import HTTPBasicAuth
from log import get_logger
import shlex
SERVER_ADDR = "http://localhost:8000/"
FILE_PATH = "files"
ROOMS = ["501"]
USERNAME = "printuser"
PASSWORD = "print123456"

def get_pending_prints():
    url = f'{SERVER_ADDR}print-list/?status=pending'
    response = requests.get(url,auth=HTTPBasicAuth(USERNAME,PASSWORD))
    if response.status_code != 200:
        print(f"请求打印列表错误，http状态码:{response.status_code},信息：{response.text}")
        logger.error(f"请求打印列表错误，http状态码:{response.status_code},信息：{response.text}")
        return []
    else:
        logger.info(f"请求打印列表成功，http状态码:{response.status_code},信息：{response.text}")
    data = response.json()['data']
    return data


def set_processing(print_id):
    url = f'{SERVER_ADDR}print/'
    response = requests.put(url, data={"id": print_id, "status": "processing"},auth=HTTPBasicAuth(USERNAME,PASSWORD))
    if response.status_code != 200:
        logger.error(f"设置processing出错，print_id:{print_id},http状态码:{response.status_code},信息：{response.text}")
        print(f"设置processing出错，print_id:{print_id},http状态码:{response.status_code},信息：{response.text}")


def set_done(print_id):
    url = f'{SERVER_ADDR}print/'
    response = requests.put(url, data={"id": print_id, "status": "done"},auth=HTTPBasicAuth(USERNAME,PASSWORD))
    if response.status_code != 200:
        logger.error(f"设置done出错，print_id:{print_id},http状态码:{response.status_code},信息：{response.text}")
        print(f"设置done出错，print_id:{print_id},http状态码:{response.status_code},信息：{response.text}")


def get_room_from_location(location: str):
    room = location.split("-")[0]
    return room


def need_print(location):
    room = get_room_from_location(location)
    return room in ROOMS


def send_to_printer(print_id,team_name,file_name,location):
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{time_now}:正在打印来自:{team_name}的内容，打印id:{print_id}")
    logger.info(f"正在打印来自:{team_name}的内容，打印id:{print_id}")
    header = shlex.quote(f"id:{print_id}:{team_name}:{location}")
    cmd = f"enscript -b  {header} -f Courier9 {file_name} 2>&1"
    result = subprocess.run(cmd,cwd=os.getcwd())
    logger.info("打印执行结果：", result.stdout)


def process(print_obj):
    url = f"{SERVER_ADDR}{print_obj['file']}"
    response = requests.get(url)
    file_path = os.path.join(FILE_PATH, print_obj['original_name'])
    with open(file_path, 'wb') as f:
        f.write(response.content)
    send_to_printer(print_obj['id'],print_obj['team_name'],file_path,print_obj['location'])
    return


def main():
    if not os.path.exists(FILE_PATH):
        os.makedirs(FILE_PATH)
    while True:

        pending_prints = get_pending_prints()
        logger.info(f"获取到{len(pending_prints)}条数据")

        print_cnt = 0
        for print_obj in pending_prints:
            if need_print(print_obj['location']):
                set_processing(print_obj['id'])
                process(print_obj)
                set_done(print_obj['id'])
                print_cnt += 1
        logger.info(f"共打印了{print_cnt}份文件")
        time.sleep(5)


if __name__ == "__main__":
    logger = get_logger()
    main()
