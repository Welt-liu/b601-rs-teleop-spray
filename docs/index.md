---
title: 喷水机械臂遥操作
---

# 喷水机械臂遥操作

基于 [LeRobot](https://github.com/huggingface/lerobot) 的双机械臂遥操作系统，使用 **reBot Arm 102** 作为主手（leader）控制 **Seeed B601 RS** 从手（follower），支持通过配置文件裁剪电机数量。

## 硬件架构

```
┌──────────────┐    遥操作指令     ┌──────────────┐
│ reBot Arm 102 │  ────────────▶  │ Seeed B601 RS │
│   (Leader)    │                 │  (Follower)   │
│  USB 直连      │                 │  CAN / 串口    │
└──────────────┘                 └──────────────┘
```

## 快速导航

- [快速开始](getting-started) — 环境安装与首次运行
- [硬件指南](hardware) — 设备清单、连接方式、末端模型
- [配置参考](configuration) — `config.yaml` 参数详解

## 项目文件结构

```
.
├── readme.md                # 项目说明
├── docs/                    # 在线文档（当前页面）
│   ├── index.md
│   ├── getting-started.md
│   ├── hardware.md
│   └── configuration.md
├── hardware/                # 硬件资源
│   ├── README.md
│   └── *.step               # 3D 模型文件
├── media/                   # 示意图
│   ├── connector.png
│   └── png1.png
└── scripts/
    ├── config.yaml          # 遥操作配置
    └── teleoperate.py       # 主程序
```
