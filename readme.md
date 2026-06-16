# 喷水机械臂 Demo

基于 [LeRobot](https://github.com/huggingface/lerobot) 的遥操作方案，使用 `reBot Arm 102` 作为 leader（主手），`Seeed B601 RS` 作为 follower（从手），支持通过配置裁剪电机数量。

## 环境要求

- Python 3.12
- Linux（需要 SocketCAN 或串口权限）

## 安装

### 1. 创建并激活 conda 环境

```bash
conda create -n lerobot python=3.12
conda activate lerobot
```

### 2. 安装 lerobot 核心库

克隆lerobot模块并安装：

```bash
git clone https://github.com/Seeed-Projects/lerobot.git
cd lerobot
pip install -e .
cd ..
```

### 3. 安装第三方插件包

```bash
# leader 臂（reBot Arm 102）
pip install lerobot-teleoperator-rebot-arm-102

# follower 臂（Seeed B601 RS）
pip install lerobot-robot-seeed-b601
```

### 4. 其他依赖

脚本依赖 `pyyaml` 和 `rerun-sdk`（lerobot 已自带 rerun，如缺失可手动安装）：

```bash
pip install pyyaml
```

## 使用

### 配置文件

所有参数在 [scripts/config.yaml](scripts/config.yaml) 中管理：

默认情况下裁剪了gripper，如有特殊需要请修改本配置文件。
校准文件和id绑定。



```yaml
# 启用的电机（删减此行即可裁剪电机数量）
enabled_joints:
  - shoulder_pan
  - shoulder_lift
  - elbow_flex
  - wrist_flex
  - wrist_yaw
  - wrist_roll
  - gripper

leader:
  port: /dev/ttyUSB0
  baudrate: 1000000
  id: rebot_arm_102_leader

follower:
  port: can0
  can_adapter: socketcan  # socketcan | damiao
  id: follower1

loop:
  fps: 60
  duration: null  # null = 无限运行；设数字则运行对应秒数后停止
  display_data: false
  display_ip: null
  display_port: null
```

**裁剪电机：** 注释掉不需要的电机即可。通常只裁剪 gripper（夹爪），其他关节应保留：

```yaml
enabled_joints:
  - shoulder_pan
  - shoulder_lift
  - elbow_flex
  - wrist_flex
  - wrist_yaw
  - wrist_roll
  # - gripper  # 无夹爪时注释掉
```

### 运行

```bash
# 进入脚本目录
cd scripts

# 使用 lerobot 环境的 Python 运行

# ** 首次运行时，需要设置机械臂零点，请将机械臂放置在零位，参考lerobot wiki的零位要求 **

python teleoperate.py

# 指定配置文件
python teleoperate.py --config /path/to/config.yaml
```


## 文件结构

```
.
├── readme.md              # 本文档
├── hardware/
│   └── README.md          # 硬件说明（设备清单、连接方式、电机定义）
├── scripts/
│   ├── config.yaml        # 配置文件（修改电机、端口等）
│   └── teleoperate.py     # 遥操作脚本（支持裁剪电机）
└── lerobot/               # LeRobot 核心库（子模块）
```
