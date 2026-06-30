# 硬件指南

## 设备清单

| 角色 | 型号 | 通信接口 |
|------|------|----------|
| Leader（主手） | reBot Arm 102 | USB 串口 `/dev/ttyUSB0` |
| Follower（从手） | Seeed B601 RS | CAN 总线 `can0` |
| CAN 适配器 | SocketCAN 兼容 | USB |

## 连接拓扑

```
reBot Arm 102 ──USB──▶ 主机 ◀──CAN Adapter──◀── Seeed B601 RS
```

## 电机定义

本系统支持 7 个关节电机：

| 电机名称 | 含义 | Leader ID | Follower CAN ID |
|----------|------|-----------|-----------------|
| `shoulder_pan` | 肩部旋转 | 0 | 0x01 |
| `shoulder_lift` | 肩部抬升 | 1 | 0x02 |
| `elbow_flex` | 肘部弯曲 | 2 | 0x03 |
| `wrist_flex` | 腕部弯曲 | 3 | 0x04 |
| `wrist_yaw` | 腕部偏航 | 4 | 0x05 |
| `wrist_roll` | 腕部旋转 | 5 | 0x06 |
| `gripper` | 夹爪 | 6 | 0x07 |

### 关节限位

| 电机 | 范围 |
|------|------|
| shoulder_pan | -150° ~ 150° |
| shoulder_lift | -1° ~ 170° |
| elbow_flex | -200° ~ 1° |
| wrist_flex | -80° ~ 90° |
| wrist_yaw | -90° ~ 90° |
| wrist_roll | -90° ~ 90° |
| gripper | 0° ~ 270° |

## 末端工具

`hardware/` 目录中提供了 3D 模型文件：

- `connector.step` — 喷头连接件，适用于 A1 Mini 0.4 喷头，使用 M5×35 螺丝固定
- `02_Gripper_Connector_B.step` — B601-RS 末端通用连接件，可基于此设计自定义末端

![喷头连接件](media/connector.png)

![安装尺寸参考](media/png1.png)

> **注意：** 螺丝安装孔位需要根据实际 3D 打印机精度微调。
