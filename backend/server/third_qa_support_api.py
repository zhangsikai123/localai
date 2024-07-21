import datetime
import http.client
import json

from threading import Thread

import requests

from configs import logger
from server.utils import api_address
from webui_pages.utils import ApiRequest
from webui_pages.utils import check_error_msg

DEFAULT_QA_TEXT = "不理解当前的问题"
TEMPERATURE = 0.5
HISTORY_LEN = 5
WORK_TOOL_HOST = "api.worktool.ymdyes.cn"
WORK_TOOL_ROBOT_ID = "wt2i3f5s7jc8sykeii7kl7xd061al552"  # todo: 找个地方放 @sky

api = ApiRequest(base_url=api_address())


class QAResult:
    def __init__(self, code: int, message: str, data: dict):
        self.__code = code
        self.__message = message
        self.__data = data

    def to_dict(self):
        return {"code": self.__code, "message": self.__message, "data": self.__data}


def qa_handler(body: dict):
    prompt = body.get("spoken", "")
    if not prompt:
        result = QAResult(0, "success", make_response_text_data(DEFAULT_QA_TEXT))
        return result.to_dict()

    # 异步发送 llm 处理的响应
    def fn(param: dict):
        query = param.get("spoken", "")
        logger.info(f"third qa bodyparam: {param}")
        history = get_history(param.get("receivedName"))
        r = api.chat_chat(
            query,
            history=history,
            temperature=TEMPERATURE,
            stream=False,
            prompt_name="weixin",
        )
        response_text = ""
        try:
            for t in r:
                if error_msg == check_error_msg(t):
                    res = QAResult(50000, error_msg, {})
                    return res.to_dict()
                response_text += t
        except Exception as ex:
            logger.error(f"qa_handler failed: {ex}")
            response_text = "不理解当前的问题"

        group_name = param.get("groupName")  # 群名
        at_who = param.get("receivedName")  # 提问者
        # 发送消息指令
        send_work_tool_msg_by_body(group_name, response_text, at_who)

    thr = Thread(target=fn, args=(body,))
    thr.start()

    # 快速返回空文本
    result = QAResult(0, "success", make_response_text_data(""))
    return result.to_dict()


def make_response_text_data(text: str) -> dict:
    return {"type": 5000, "info": {"text": text}}  # 5000 回答类型为文本


def send_work_tool_msg_by_body(group_name: str, response_text: str, at_who: str):
    conn = http.client.HTTPSConnection(WORK_TOOL_HOST)
    logger.info(
        f"group_name: {group_name}, response_text: {response_text} at_who: {at_who}"
    )
    payload = json.dumps(
        {
            "socketType": 2,  # 通讯类型 固定值=2
            "list": [
                {
                    "type": 203,  # 消息类型 固定值=203
                    "titleList": [f"{group_name}"],
                    "receivedContent": f"{response_text}",
                    # "atList": [f"@{at_who}"],
                }
            ],
        }
    )
    headers = {
        "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
        "Content-Type": "application/json",
    }
    try:
        work_tool_send_msg_api = f"/wework/sendRawMessage?robotId={WORK_TOOL_ROBOT_ID}"
        conn.request("POST", work_tool_send_msg_api, payload, headers)
        res = conn.getresponse()
        data = res.read()
        resp_body_json_str = data.decode("utf-8")
        resp_body = json.loads(resp_body_json_str)
        if not resp_body.get("code"):
            msg = resp_body.get("message")
            raise Exception(f"request exception, code: {code}, msg: {msg}")

        logger.info(
            f"send work tool msg succeed. payload: {payload}\n response: {resp_body_json_str}".encode(
                "utf-8"
            )
        )
    except Exception as ex:
        logger.error(f"send_work_tool_msg_by_body failed: {ex}\npayload: {payload}")


def get_history(user):
    def convert_data(input_data):
        # Initialize the output list
        output_list = []
        # Iterate over the list of messages
        for msg in input_data["data"]["list"]:
            # Initialize an empty dictionary for each message
            output_dict = {}
            # Check the sender and assign the role accordingly
            if msg["sender"] == 0:
                output_dict["role"] = "user"
            elif msg["sender"] == 1:
                output_dict["role"] = "assistant"
            else:
                continue
            # Parse the itemMsgList which is a json string and get the content
            item_msg_list = json.loads(msg["itemMsgList"])
            if not item_msg_list:
                continue
            output_dict["content"] = item_msg_list[0]["text"]
            # Append the dictionary to the output list
            output_list.append(output_dict)
        return output_list

    # start of this month
    start_time = datetime.datetime.now().replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )
    # just now
    end_time = datetime.datetime.now()
    robot_id = WORK_TOOL_ROBOT_ID
    title = user
    page = 1
    size = 10
    sort = "create_time,desc"
    params = {
        "robotId": robot_id,
        "title": title,
        "page": page,
        "size": size,
        "sort": sort,
        "startTime": start_time,
        "endTime": end_time,
    }
    sort = "create_time,desc"
    res = requests.get(f"https://{WORK_TOOL_HOST}/robot/wework/message", params)
    if res.status_code != 200:
        logger.info(f"get history failed: {res.text.encode('utf-8')}")
        return []
    data = res.json()
    if data["code"] != 200:
        logger.info(f"get history failed: {data['message']}")
        return []
    history = convert_data(data)
    history.reverse()
    return history[:HISTORY_LEN]
