# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import os

from alibabacloud_dm20151123 import models as dm_20151123_models
from alibabacloud_dm20151123.client import Client as Dm20151123Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class MailSender:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> Dm20151123Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=access_key_secret,
        )
        # Endpoint 请参考 https://api.aliyun.com/product/Dm
        config.endpoint = f"dm.aliyuncs.com"
        return Dm20151123Client(config)

    @staticmethod
    def send(
        to_address,
        subject,
        text_body,
    ) -> None:
        # 请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID 和 ALIBABA_CLOUD_ACCESS_KEY_SECRET。
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例使用环境变量获取 AccessKey 的方式进行调用，仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = MailSender.create_client(
            os.environ["ALIBABA_CLOUD_ACCESS_KEY_ID"],
            os.environ["ALIBABA_CLOUD_ACCESS_KEY_SECRET"],
        )
        single_send_mail_request = dm_20151123_models.SingleSendMailRequest(
            account_name="noreply@xiaobaoz.com",
            address_type=1,
            reply_to_address=False,
            to_address=to_address,
            subject=subject,
            text_body=text_body,
            from_alias="Baozi",
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            client.single_send_mail_with_options(single_send_mail_request, runtime)
        except Exception as error:
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)

    @staticmethod
    async def main_async(
        to_address,
        subject,
        text_body,
    ) -> None:
        # 请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID 和 ALIBABA_CLOUD_ACCESS_KEY_SECRET。
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例使用环境变量获取 AccessKey 的方式进行调用，仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = MailSender.create_client(
            os.environ["ALIBABA_CLOUD_ACCESS_KEY_ID"],
            os.environ["ALIBABA_CLOUD_ACCESS_KEY_SECRET"],
        )
        single_send_mail_request = dm_20151123_models.SingleSendMailRequest(
            account_name="noreply@xiaobaoz.com",
            address_type=1,
            reply_to_address=False,
            to_address=to_address,
            subject=subject,
            text_body=text_body,
            from_alias="Baozi",
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            await client.single_send_mail_with_options_async(
                single_send_mail_request, runtime
            )
        except Exception as error:
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)

    @staticmethod
    def send_activation_mail(
        email,
        activation_code,
    ) -> None:
        stage = os.getenv("STAGE", "prod")
        subject = "Welcome to Baozi!"
        if stage == "dev":
            text_body = f"Your activation link is: http://localhost:5173/activation?activation_code={activation_code}"
        else:
            text_body = f"Your activation link is: https://xiaobaoz.com/activation?activation_code={activation_code}"
        MailSender.send(email, subject, text_body)
