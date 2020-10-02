import Automator
import time


class Click_event:
    def __init__(self, position=None, img=None, wait=False, wait_before=0, wait_after=0.5):
        self.wait_before = wait_before
        self.wait_after = wait_after
        self.position = position
        self.img = img
        self.wait = wait

    def click(self, handler=None):
        time.sleep(self.wait_before)
        if self.img is not None:
            screen_shot = handler.screenshot()
            if self.wait:
                while not handler.is_there_img(screen_shot, self.img):
                    time.sleep(0.3)
                    # print("wait for 0.5 second")
                    screen_shot = handler.screenshot()
            time.sleep(self.wait_before)
            if not handler.is_there_img(screen_shot, self.img):
                return False
            if self.position is None:
                handler.guochang(screen_shot, [self.img])
            else:
                handler.click(self.position)
        else:
            handler.click(self.position)
        time.sleep(self.wait_after)
        return True

    def __str__(self):
        return str(self.position) + str(self.img)

    def ping(self, msg="default message"):
        print(msg)


if __name__ == "__main__":
    ctl = Automator.Automator()
    ce = Click_event(img="img/gift.jpg")
    print(ce.click(ctl))
