# __init__.py

import os
import subprocess
import logging
import re

_logger = logging.getLogger(__name__)


def is_docker():
    """
    判断是否在 Docker 环境中运行，检查多个条件以增加准确性
    """
    try:
        with open("/proc/1/cgroup", "r") as f:
            if 'docker' in f.read():
                return True
    except Exception:
        pass
    if os.path.exists("/run/containerd/containerd.sock"):
        return True
    hostname = os.environ.get("HOSTNAME", "")
    if re.match(r'^[a-f0-9]{12}$', hostname):
        return True
    try:
        with open("/proc/self/status", "r") as f:
            status = f.read()
            if "Name:\t" in status and "docker" in status.lower():
                return True
    except Exception:
        pass
    return False


def install_alipay_sdk():
    """
    根据环境判断并安装 python-alipay-sdk 包
    """
    try:
        import alipay
        _logger.info("python-alipay-sdk 已安装，无需重复安装。")
    except ImportError:
        _logger.info("python-alipay-sdk 未安装，开始安装...")

        if is_docker():
            _logger.info("在 Docker 环境中，安装 python-alipay-sdk...")
            install_command = ["pip3", "install", "python-alipay-sdk", "--break-system-packages"]
        else:
            _logger.info("在非 Docker 环境中，安装 python-alipay-sdk...")
            install_command = ["pip3", "install", "python-alipay-sdk"]

        try:
            subprocess.check_call(install_command)
            _logger.info("python-alipay-sdk 安装成功！")
        except subprocess.CalledProcessError as e:
            _logger.error(f"安装 python-alipay-sdk 失败：{e}")
        except Exception as e:
            _logger.error(f"未知错误：{e}")


# 在模块初始化时调用安装 SDK 的函数
install_alipay_sdk()
from . import controllers
from . import models
