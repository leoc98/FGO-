import uiautomator2 as u2
import time
from cv import *
import matplotlib.pylab as plt


class Automator:
    def __init__(self, port=None, auto_task=False, auto_policy=True,
                 auto_goods=False, speedup=True):
        """
        device: 如果是 USB 连接，则为 adb devices 的返回结果；如果是模拟器，则为模拟器的控制 URL 。
        """
        self.g = False
        if port is None:
            self.d = u2.connect()
        else:
            self.d = u2.connect(port)
        self.dWidth, self.dHeight = self.d.window_size()
        self.appRunning = False
        self.last_screen_shot_hash = None
        self.last_id = None
        self.last_return_dic = None

    def get_butt_stat(self, screen_shot, template_paths, threshold=0.81):
        # 此函数输入要判断的图片path,屏幕截图, 阈值,   返回大于阈值的path,坐标字典,
        this_hash = id(screen_shot)
        this_id = id(template_paths)
        if self.last_screen_shot_hash == this_hash and this_id == self.last_id:
            return self.last_return_dic
        else:
            self.last_screen_shot_hash = this_hash
            self.last_id = this_id

            self.dWidth, self.dHeight = self.d.window_size()
            return_dic = {}
            zhongxings, max_vals = UIMatcher.findpic(screen_shot, template_paths=template_paths)

            for i, name in enumerate(template_paths):
                if max_vals[i] > threshold:
                    return_dic[name] = (zhongxings[i][0] * self.dWidth, zhongxings[i][1] * self.dHeight)

            self.last_return_dic = return_dic
        # print(return_dic)
        return return_dic

    def screenshot(self):
        return self.d.screenshot(format="opencv")

    def click(self, *args):
        if len(args) == 1:
            self.d.click(args[0][0], args[0][1])
        else:
            self.d.click(args[0], args[1])

    def guochang(self, screen_shot, template_paths, suiji=0, times=1, wait_unit=0.5):
        # suiji标号置1, 表示未找到时将点击左上角, 置0则不点击
        # 输入截图, 模板list, 得到下一次操作

        self.dWidth, self.dHeight = self.d.window_size()
        print(self.d.window_size())
        # screen_shot = screen_shot
        # template_paths = template_paths
        active_path = self.get_butt_stat(screen_shot, template_paths)
        if active_path:
            # print(active_path)
            if 'img/caidan_tiaoguo.jpg' in active_path:
                x, y = active_path['img/caidan_tiaoguo.jpg']
                self.d.click(x, y)
            else:
                for _ in range(times):
                    for _, (x, y) in active_path.items():
                        time.sleep(wait_unit)
                        # print(name)
                        self.d.click(x, y)
            time.sleep(wait_unit)
        else:
            if suiji:
                # print('未找到所需的按钮,将点击左上角')
                self.d.click(10, 400)
            else:
                # print('未找到所需的按钮,无动作')
                pass

    def is_there_img(self, screen_shot, img):
        self.dWidth, self.dHeight = self.d.window_size()
        active_path = self.get_butt_stat(screen_shot, [img])
        if img in active_path:
            return True
        else:
            return False
