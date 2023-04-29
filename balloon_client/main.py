import datetime
import time
import os
import requests
from requests.auth import HTTPBasicAuth
from log import get_logger
import subprocess

DOMJUDGE_ADDR = "http://192.168.1.197/domjudge/"
BALLOON_USERNAME = "admin"
BALLOON_PASSWORD = "admin123456"
CONTEST_ID = 2
ROOMS = [""]


def get_balloons():
    url = f'{DOMJUDGE_ADDR}api/v4/contests/{CONTEST_ID}/balloons/'
    response = requests.get(url, auth=HTTPBasicAuth(BALLOON_USERNAME, BALLOON_PASSWORD))
    return response.json()


def set_done(print_id):
    url = f'{DOMJUDGE_ADDR}api/v4/contests/{CONTEST_ID}/balloons/{print_id}/done'
    response = requests.post(url,auth=HTTPBasicAuth(BALLOON_USERNAME, BALLOON_PASSWORD))
    if response.status_code != 204:
        logger.error(f"设置完成出错，print_id:{print_id},http状态码:{response.status_code},信息：{response.text}")
    else:
        logger.info(f"设置打印完成成功，print_id:{print_id},http状态码:{response.status_code},信息：{response.text}")


def get_room_from_location(location: str):
    room = location.split("-")[0]
    return room


def need_print(location):
    # room = get_room_from_location(location)
    # return room in ROOMS
    return True


def send_to_printer(balloon_id,problem,team_name,location,total_list):
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{time_now}:正在打印来自:{team_name}的{problem}的气球单，打印id:{balloon_id}")
    logger.info(f"正在打印来自:{team_name}的{problem}的气球单，打印id:{balloon_id}")
    content = f"balloon id:{balloon_id}\nteam name:{team_name}\nteam location:{location}\nsolved problem:{problem}\nall solved problems:{total_list}"
    file_name = os.path.join("balloons",str(balloon_id)+".txt")
    with open (file_name,"+w") as f:
        f.write(content)
    cmd = f"enscript -f Courier9 {file_name} 2>&1"
    result = subprocess.run(cmd,cwd=os.getcwd())
    logger.info("打印执行结果：",result.stdout)


def process(print_obj):
    balloon_id = print_obj['balloonid']
    problem = print_obj['problem']
    team_name = print_obj['team']
    location = print_obj['location']
    total = print_obj['total']
    total_list = list()
    for balloon in total:
        total_list.append(balloon)
    send_to_printer(balloon_id,problem,team_name,location,total_list)


def main():
    while True:

        pending_prints = get_balloons()
        logger.info(f"获取到{len(pending_prints)}条数据")

        print_cnt = 0
        for print_obj in pending_prints:
            if need_print(print_obj['location']):
                process(print_obj)
                set_done(print_obj['balloonid'])
                print_cnt += 1
        logger.info(f"共打印了{print_cnt}个气球单")
        time.sleep(5)


if __name__ == "__main__":
    if not os.path.exists("balloons"):
        os.mkdir("balloons")
    logger = get_logger()
    main()
