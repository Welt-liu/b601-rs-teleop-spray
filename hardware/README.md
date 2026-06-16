# 硬件说明

## 设备清单

| 设备 | 型号 | 用途 |
|---|---|---|
| leader（主手） | reBot Arm 102 | 遥操作输入端 |
| follower（从手） | Seeed B601 RS | 遥操作执行端 |

## 连接方式

### leader

- 接口：USB 串口
- 典型端口：`/dev/ttyUSB0`
- 波特率：`1000000`

### follower

- 接口：CAN 总线
- 典型端口：`can0`（SocketCAN）或 `/dev/ttyACM0`（Damiao 适配器）
- 适配器类型：`socketcan` 或 `damiao`

## 电机

默认 7 个关节：

| 序号 | 关节名 | 说明 |
|---|---|---|
| 0 | shoulder_pan | 肩部旋转 |
| 1 | shoulder_lift | 肩部抬升 |
| 2 | elbow_flex | 肘部弯曲 |
| 3 | wrist_flex | 腕部弯曲 |
| 4 | wrist_yaw | 腕部偏航 |
| 5 | wrist_roll | 腕部滚动 |
| 6 | gripper | 夹爪（喷水末端） |

> 通常只需要裁剪 `gripper`，其他关节应保留。

## 端口配置

在 [scripts/config.yaml](../scripts/config.yaml) 中修改端口参数：

```yaml
leader:
  port: /dev/ttyUSB0
  baudrate: 1000000

follower:
  port: can0
  can_adapter: socketcan  # socketcan | damiao
```
