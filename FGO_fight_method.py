from Static_data import ctl, wait_effect, wait_loading_fight, position_dictionary
import time
from Click_event import Click_event
import Event_flow


def select_support(support_feature):
    screen_shot = ctl.screenshot()
    if ctl.is_there_img(screen_shot, support_feature):
        Click_event(None, support_feature, True, wait_effect, 0).click(ctl)
        return True
    else:
        Click_event(None, "img/refresh.jpg", True, wait_effect, 0).click(ctl)
        if ctl.is_there_img(ctl.screenshot(), "img/refresh_cd.jpg"):
            Click_event(None, "img/refresh_cd_close.jpg", True, wait_effect, 0).click(ctl)
        else:
            Click_event(None, "img/refresh_yes.jpg", True, wait_effect, 0).click(ctl)
        return False


def wait_support(support_feature, wait_time=3):
    while not select_support(support_feature):
        time.sleep(wait_time)
    Click_event(None, "img/start.jpg", False, 2, 0).click(ctl)
    time.sleep(wait_loading_fight)


def fight_main(fight_flow):
    ef = Event_flow.Event_flow(ctl, fight_flow)
    ef.click_event_flow()


def fight_next():
    while not ctl.is_there_img(ctl.screenshot(), "img/next.jpg"):
        ctl.click(position_dictionary["return"])
    Click_event(None, "img/next.jpg", True, wait_effect, 0).click(ctl)
    Click_event(None, "img/no_apply.jpg", False, 1, 0).click(ctl)
    Click_event(None, "img/go_on.jpg", True, 1 + wait_effect, 0).click(ctl)

    # 判断是进入哪个分支
    while True:
        screen_shot = ctl.screenshot()
        if ctl.is_there_img(screen_shot, "img/golden_apple.jpg"):
            ctl.guochang(screen_shot, ["img/golden_apple.jpg"])
            Click_event(None, "img/apple_ok.jpg", True, wait_effect).click(ctl)
        elif ctl.is_there_img(screen_shot, "img/silver_apple.jpg"):
            ctl.guochang(screen_shot, ["img/silver_apple.jpg"])
            Click_event(None, "img/apple_ok.jpg", True, wait_effect).click(ctl)
        elif ctl.is_there_img(screen_shot, "img/refresh.jpg"):
            break


def fight_process(support, fight_flow):
    wait_support(support)
    fight_main(fight_flow)
    fight_next()
