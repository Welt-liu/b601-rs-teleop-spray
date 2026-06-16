遥操作demo

参考lerobot-teleoperate这个demo，使用seeed_b601_rs_follower和rebot_arm_102_leader进行遥操作，要求可裁剪follower和leader上的控制电机数量。即虽然它们默认有7颗电机，但是也可以通过配置，实现只控制其中几个电机。要求你重新生成代码文件，可以依赖lerobot-teleoperator-rebot-arm-102和lerobot-robot-seeed-b601这两个包，事实上，lerobot-teleoperate这个demo已经实现了控制7颗电机，你要先把所有提供给你的demo和这lerobot-teleoperator-rebot-arm-102和lerobot-robot-seeed-b601（pip在线安装）都阅读一遍，然后在制定计划，告诉我方案，我来决定要怎么做，要不要修改。

以下是这个demo的启动命令，目前不可用，因为没有安装，你参考其中的参数，了解demo是怎样的逻辑



lerobot-teleoperate \
--robot.type=seeed_b601_rs_follower \
--robot.port=can0 \
--robot.id=follower1 \
--robot.can_adapter=socketcan \
--teleop.type=rebot_arm_102_leader \
--teleop.port=/dev/ttyUSB0 \
--teleop.id=rebot_arm_102_leader
 