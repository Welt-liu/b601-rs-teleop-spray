"""
遥操作脚本 — 支持裁剪 follower / leader 的电机数量。

依赖:
    pip install lerobot-teleoperator-rebot-arm-102 lerobot-robot-seeed-b601

用法:
    # 默认读取同目录下的 config.yaml
    python teleoperate.py

    # 指定配置文件
    python teleoperate.py --config /path/to/config.yaml
"""

import argparse
import logging
import time
from pathlib import Path

import rerun as rr
import yaml

from lerobot.processor import make_default_processors
from lerobot.utils.import_utils import register_third_party_plugins
from lerobot.utils.robot_utils import precise_sleep
from lerobot.utils.utils import init_logging, move_cursor_up
from lerobot.utils.visualization_utils import init_rerun, log_rerun_data

from lerobot_teleoperator_rebot_arm_102.config_rebot_arm_102_leader import (
    RebotArm102LeaderConfig,
)
from lerobot_teleoperator_rebot_arm_102.rebot_arm_102_leader import (
    RebotArm102Leader,
)
from lerobot_robot_seeed_b601.config_seeed_b601_rs_follower import (
    SeeedB601RSFollowerConfig,
)
from lerobot_robot_seeed_b601.seeed_b601_rs_follower import (
    SeeedB601RSFollower,
)

# ---------------------------------------------------------------------------
# 全部7个电机的定义（与第三方包默认值一致）
# ---------------------------------------------------------------------------
ALL_JOINTS = [
    "shoulder_pan",
    "shoulder_lift",
    "elbow_flex",
    "wrist_flex",
    "wrist_yaw",
    "wrist_roll",
    "gripper",
]

# ---------------------------------------------------------------------------
# 裁剪工具函数
# ---------------------------------------------------------------------------

def _filter_dict(d: dict, keys: set[str]) -> dict:
    return {k: v for k, v in d.items() if k in keys}


def build_leader_config(enabled_joints: list[str], port: str, id: str, baudrate: int = 1_000_000):
    """从全量配置中裁剪出 leader 配置。"""
    joint_set = set(enabled_joints)

    full_joint_ids = {
        "shoulder_pan": 0, "shoulder_lift": 1, "elbow_flex": 2,
        "wrist_flex": 3, "wrist_yaw": 4, "wrist_roll": 5, "gripper": 6,
    }
    full_joint_ranges = {
        "shoulder_pan":  (-150.0, 150.0), "shoulder_lift": (-1.0, 170.0),
        "elbow_flex":    (-200.0, 1.0),   "wrist_flex":    (-80.0, 90.0),
        "wrist_yaw":     (-90.0, 90.0),   "wrist_roll":    (-90.0, 90.0),
        "gripper":       (-0.0, 270.0),
    }

    return RebotArm102LeaderConfig(
        id=id,
        port=port,
        baudrate=baudrate,
        joint_ids=_filter_dict(full_joint_ids, joint_set),
        joint_ranges=_filter_dict(full_joint_ranges, joint_set),
    )


def build_follower_config(enabled_joints: list[str], port: str, id: str, can_adapter: str = "socketcan"):
    """从全量配置中裁剪出 follower 配置。"""
    joint_set = set(enabled_joints)

    full_motor_can_ids = {
        "shoulder_pan":  (0x01, 0xFD), "shoulder_lift": (0x02, 0xFD),
        "elbow_flex":    (0x03, 0xFD), "wrist_flex":    (0x04, 0xFD),
        "wrist_yaw":     (0x05, 0xFD), "wrist_roll":    (0x06, 0xFD),
        "gripper":       (0x07, 0xFD),
    }
    full_joint_limits = {
        "shoulder_pan":  (-145.0, 145.0), "shoulder_lift": (-0.0, 170.0),
        "elbow_flex":    (-0.0, 200.0),   "wrist_flex":    (-80.0, 90.0),
        "wrist_yaw":     (-90.0, 90.0),   "wrist_roll":    (-90.0, 90.0),
        "gripper":       (-0.0, 270.0),
    }
    full_joint_directions = {
        "shoulder_pan": 1.0, "shoulder_lift": 1.0, "elbow_flex": -1.0,
        "wrist_flex": -1.0, "wrist_yaw": -1.0,   "wrist_roll": 1.0,
        "gripper": 6.0,
    }
    full_mit_kp = {
        "shoulder_pan": 50.0, "shoulder_lift": 150.0, "elbow_flex": 150.0,
        "wrist_flex": 50.0, "wrist_yaw": 50.0, "wrist_roll": 50.0,
    }
    full_mit_kd = {
        "shoulder_pan": 3.0, "shoulder_lift": 10.0, "elbow_flex": 10.0,
        "wrist_flex": 5.0, "wrist_yaw": 4.0, "wrist_roll": 4.0,
    }

    return SeeedB601RSFollowerConfig(
        id=id,
        port=port,
        can_adapter=can_adapter,
        motor_can_ids=_filter_dict(full_motor_can_ids, joint_set),
        joint_limits=_filter_dict(full_joint_limits, joint_set),
        joint_directions=_filter_dict(full_joint_directions, joint_set),
        mit_kp=_filter_dict(full_mit_kp, joint_set),
        mit_kd=_filter_dict(full_mit_kd, joint_set),
    )


# ---------------------------------------------------------------------------
# Teleop loop（直接从 lerobot_teleoperate.py 搬过来，不依赖 draccus 装饰器）
# ---------------------------------------------------------------------------

def teleop_loop(
    teleop,
    robot,
    fps: int = 60,
    display_data: bool = False,
    duration: float | None = None,
    display_compressed_images: bool = False,
):
    display_len = max(len(key) for key in robot.action_features) if robot.action_features else 10
    teleop_action_processor, robot_action_processor, robot_observation_processor = make_default_processors()

    start = time.perf_counter()

    while True:
        loop_start = time.perf_counter()

        obs = robot.get_observation()
        raw_action = teleop.get_action()

        teleop_action = teleop_action_processor((raw_action, obs))
        robot_action_to_send = robot_action_processor((teleop_action, obs))
        _ = robot.send_action(robot_action_to_send)

        if display_data:
            obs_transition = robot_observation_processor(obs)
            log_rerun_data(
                observation=obs_transition,
                action=teleop_action,
                compress_images=display_compressed_images,
            )
            print("\n" + "-" * (display_len + 10))
            print(f"{'NAME':<{display_len}} | {'NORM':>7}")
            for motor, value in robot_action_to_send.items():
                print(f"{motor:<{display_len}} | {value:>7.2f}")
            move_cursor_up(len(robot_action_to_send) + 3)

        dt_s = time.perf_counter() - loop_start
        precise_sleep(max(1 / fps - dt_s, 0.0))
        loop_s = time.perf_counter() - loop_start
        print(f"Teleop loop time: {loop_s * 1e3:.2f}ms ({1 / loop_s:.0f} Hz)")
        move_cursor_up(1)

        if duration is not None and time.perf_counter() - start >= duration:
            return


# ---------------------------------------------------------------------------
# 配置加载
# ---------------------------------------------------------------------------

def load_config(config_path: str) -> dict:
    p = Path(config_path)
    if not p.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_path}")
    with open(p) as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="遥操作 — 可裁剪电机数量")
    parser.add_argument("--config", type=str, default="config.yaml", help="配置文件路径")
    args = parser.parse_args()

    cfg = load_config(args.config)

    enabled_joints = cfg["enabled_joints"]
    for j in enabled_joints:
        if j not in ALL_JOINTS:
            raise ValueError(f"未知电机: {j}，可选: {ALL_JOINTS}")

    init_logging()
    logging.info(f"启用电机: {enabled_joints} (共 {len(enabled_joints)} 个)")

    # 构建裁剪后的配置
    leader_config = build_leader_config(
        enabled_joints,
        cfg["leader"]["port"],
        cfg["leader"].get("id", "rebot_arm_102_leader"),
        cfg["leader"].get("baudrate", 1_000_000),
    )
    follower_config = build_follower_config(
        enabled_joints,
        cfg["follower"]["port"],
        cfg["follower"].get("id", "follower1"),
        cfg["follower"].get("can_adapter", "socketcan"),
    )

    # 直接实例化设备类
    teleop = RebotArm102Leader(leader_config)
    robot = SeeedB601RSFollower(follower_config)

    # 连接
    teleop.connect()
    robot.connect()

    loop_cfg = cfg.get("loop", {})
    display_data = loop_cfg.get("display_data", False)
    if display_data:
        init_rerun(session_name="teleoperation", ip=loop_cfg.get("display_ip"), port=loop_cfg.get("display_port"))
    display_compressed_images = (
        display_data and loop_cfg.get("display_ip") is not None and loop_cfg.get("display_port") is not None
    )

    try:
        teleop_loop(
            teleop=teleop,
            robot=robot,
            fps=loop_cfg.get("fps", 60),
            display_data=display_data,
            duration=loop_cfg.get("duration"),
            display_compressed_images=display_compressed_images,
        )
    except KeyboardInterrupt:
        pass
    finally:
        if display_data:
            rr.rerun_shutdown()
        teleop.disconnect()
        robot.disconnect()


if __name__ == "__main__":
    register_third_party_plugins()
    main()
