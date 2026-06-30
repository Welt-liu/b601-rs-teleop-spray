---
title: 配置参考
---

# 配置参考

所有参数在 `scripts/config.yaml` 中管理。以下是完整的配置项说明。

## 完整配置示例

```yaml
enabled_joints:
  - shoulder_pan
  - shoulder_lift
  - elbow_flex
  - wrist_flex
  - wrist_yaw
  - wrist_roll
  # - gripper

leader:
  port: /dev/ttyUSB0
  baudrate: 1000000
  id: leader1

follower:
  port: can0
  can_adapter: socketcan
  id: follower1

loop:
  fps: 60
  duration: null
  display_data: false
  display_ip: null
  display_port: null
```

## 配置项详解

### `enabled_joints`

启用的电机列表。可选值：

```
shoulder_pan, shoulder_lift, elbow_flex, wrist_flex, wrist_yaw, wrist_roll, gripper
```

- 注释掉不需要的电机即可裁剪
- 通常只裁剪 `gripper`（无夹爪时），其他关节应保留
- 修改后无需修改代码，脚本自动适配

### `leader` — 主手配置

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `port` | string | `/dev/ttyUSB0` | 串口设备路径 |
| `baudrate` | int | `1000000` | 波特率 |
| `id` | string | `leader1` | 设备标识符 |

### `follower` — 从手配置

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `port` | string | `can0` | CAN 接口名称 |
| `can_adapter` | string | `socketcan` | CAN 适配器类型：`socketcan` 或 `damiao` |
| `id` | string | `follower1` | 设备标识符 |

### `loop` — 遥操作循环配置

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `fps` | int | `60` | 控制循环频率 |
| `duration` | float or null | `null` | 运行时长（秒），`null` 为无限运行 |
| `display_data` | bool | `false` | 是否启动 Rerun 可视化 |
| `display_ip` | string or null | `null` | Rerun 可视化 IP |
| `display_port` | int or null | `null` | Rerun 可视化端口 |

## 常见场景

### 无夹爪

```yaml
enabled_joints:
  - shoulder_pan
  - shoulder_lift
  - elbow_flex
  - wrist_flex
  - wrist_yaw
  - wrist_roll
  # - gripper
```

### 定时运行 10 秒

```yaml
loop:
  fps: 60
  duration: 10
```

### 启用 Rerun 可视化

```yaml
loop:
  fps: 60
  duration: null
  display_data: true
  display_ip: "127.0.0.1"
  display_port: 9876
```

### 使用大淼 CAN 适配器

```yaml
follower:
  port: /dev/ttyUSB1
  can_adapter: damiao
  id: follower1
```
