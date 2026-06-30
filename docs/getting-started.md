---
title: 快速开始
---

# 快速开始

## 环境要求

- Python 3.12
- Linux（需要 SocketCAN 或串口权限）
- conda（推荐）或 venv

## 安装步骤

### 1. 创建虚拟环境

```bash
conda create -n lerobot python=3.12
conda activate lerobot
```

### 2. 安装 LeRobot 核心库

```bash
git clone https://github.com/Seeed-Projects/lerobot.git
cd lerobot
pip install -e .
cd ..
```

### 3. 安装第三方插件包

```bash
# Leader 臂（reBot Arm 102）
pip install lerobot-teleoperator-rebot-arm-102

# Follower 臂（Seeed B601 RS）
pip install lerobot-robot-seeed-b601
```

### 4. 安装其他依赖

```bash
pip install pyyaml
```

## 首次运行

### 连接硬件

1. 将 Leader 臂通过 USB 连接到主机
2. 将 Follower 臂通过 CAN 适配器连接到主机
3. 确认设备节点存在：
   - Leader: `/dev/ttyUSB0`
   - Follower: `can0`（SocketCAN）

### 校准零点

> **重要：** 首次运行时需要设置机械臂零点。将机械臂放置在零位姿态，参考 [LeRobot Wiki](https://github.com/huggingface/lerobot/wiki) 的零位要求。

### 启动遥操作

```bash
cd scripts
python teleoperate.py
```

默认读取同目录下的 `config.yaml`，也可以指定配置文件：

```bash
python teleoperate.py --config /path/to/custom_config.yaml
```

### 停止

按 `Ctrl+C` 安全断开连接。

## 裁剪电机

如果你的机械臂没有夹爪（gripper），在 `config.yaml` 中将 `gripper` 注释掉：

```yaml
enabled_joints:
  - shoulder_pan
  - shoulder_lift
  - elbow_flex
  - wrist_flex
  - wrist_yaw
  - wrist_roll
  # - gripper  # 注释此行
```

脚本会自动裁剪对应的配置参数，无需修改代码。
