# Fate Grand Order FGO自动战斗脚本v0.1



## 简介

此项目为国服命运冠位指定脚本，使用opencv图像识别进行按钮分析。

目前实现的功能有

1. 根据图片自动选择助战角色，若角色不存在，会自动进行助战刷新，直到找到；
2. 根据设定流程进行宝具洗地；
3. 战斗结束后连续出击重复刷本，若体力不足，则默认先金后银苹果补充体力；

*仅支持单开，多开需要自行指定adb连接端口


## 环境

需要安装下列python包:

```
pip install opencv-python==3.* -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install uiautomator2 -i https://mirrors.aliyun.com/pypi/simple/
```

windows端需要adb工具，在adb文件夹，请自行手动添加到path中

若使用模拟器,则需要将模拟器设置为桥接模式.  具体参考这个项目(https://github.com/Jiahonzheng/JGM-Automator)

默认使用雷电模拟器4以下（不包含）的版本，4及以上版本的雷电模拟器可能会找不到端口

**重要：模拟器分辨率要求540*960**

## 配置方式

1. 使用文本编辑器，打开文件目录下的 ***main.py*** 进行编辑；

2. 打开模拟器在助战界面对所需的助战进行截图，并保存在 ***img/*** 目录下（不建议完整截图，建议只截取助战头像的不会闪动的部份，即加不包括加成物品的部分（参考 ***img/cba_zhuzhan.jpg***）

3. 将 ***main.py*** 中的 ***support*** 变量改为 ***"img/你刚才截图的名字.jpg"***

4. 定义战斗流程（可直接修改 ***fight_ticket_1***，也可自定义函数），具体方式见下
    1. 先实例化一个 ***Fgo_event***
        ```
        fe=Fgo_event()
        ```
    2. 对于每一面（换人面除外），调用一次 ***regular_fight_term*** ，该函数共有两个必须参数
        1. ***skill_list*** ，第一个参数，用于指定该面使用的技能
## 使用方式

1. 启动雷电模拟器，设置分辨率为540*960

2. 在任意终端（如cmd）中输入以下命令，会自动在模拟器上安装一个图标为小黄车的app（ATX）

    ```
    adb connect 127.0.0.1:7555
    python -m uiautomator2 init
    ```

3. 在模拟器上打开 ATX(小黄车) ，点击 ***启动 UIAutomator*** 选项，确保 UIAutomator 是运行的。

4. 在模拟器中启动FGO，请确保安装的是国服版本；

5. 打开需要反复战斗的副本的选人界面；

5. 然后在终端中输入

    ```
    cd main.py文件所在的目录（自己复制）
    例如：cd C:\Users\Administrator\Documents\Princess-connection-farm
    ```

5. 再输入以下命令，程序将按顺序自动完成简介中功能1-3。

    ```
    python main.py
    ```

6. 若需要停止脚本，可直接关闭终端或者模拟器（关闭模拟器终端会自动关闭）



## 额外说明

1. **本项目下zhanghao.txt为待刷账号与密码**;
   账号与密码之间用tab键作为分割，不要用空格；

   不同账号之间按行分割；

   第一行的zhanghao mima请也改成自己的账号密码。

2. **本项目下goumaimana.py为购买70次mana**，执行方法参照main.py

3. **本项目下juanzeng.py为行会捐赠装备**；

   建议每天上午跑一次main.py，8小时后请求新的装备后再跑juanzeng.py

4. 请不要用于商业用途。代码交流和bug反馈请联系qq 2785242720

