import Automator
from Click_event import Click_event
import time
import Event_flow
from Event_factory import Fgo_event
from Static_data import *


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


def fight_main():
    Fight_flow = Fgo_event()
    Fight_flow.regular_fight_term([1, 3, [4, 1], [7, 1]], [1], 20)
    Fight_flow.regular_fight_term([8, [9, 1]], [], change=True)
    Fight_flow.regular_fight_term([9], [1], 20)
    Fight_flow.regular_fight_term([[7, 1], [6, 1], 5], [1], 21)

    fight_flow = Fight_flow.get_event()
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
        if ctl.is_there_img(screen_shot, "img/golden_apple.jpg") \
                or ctl.is_there_img(screen_shot, "img/silver_apple.jpg"):
            if ctl.is_there_img(screen_shot, "img/golden_apple.jpg"):
                ctl.guochang(screen_shot, ["img/golden_apple.jpg"])
            else:
                ctl.guochang(screen_shot, ["img/silver_apple.jpg"])
            Click_event(None, "img/apple_ok.jpg", True, wait_effect).click(ctl)
        elif ctl.is_there_img(screen_shot, "img/refresh.jpg"):
            break


def test_select_support():
    wait_support("img/sanxinglizhuang.jpg")


# def fight_copper():
#     Fight_flow = Fgo_event()
#     Fight_flow.regular_fight_term([1], [1], 22)
#     Fight_flow.regular_fight_term([5], [2], 23)
#     Fight_flow.regular_fight_term([8, ["master_2", 3]], [3], 30)
#
#     fight_flow = Fight_flow.get_event()
#     ef = Event_flow.Event_flow(ctl)
#     ef.click_event_flow(fight_flow)
#
#
# def fight_silver():
#     Fight_flow = Fgo_event()
#     Fight_flow.regular_fight_term([2, 3], [1], 20)
#     Fight_flow.regular_fight_term([6], [2], 20)
#     Fight_flow.regular_fight_term([7, 8, ["master_2", 3]], [3], 30)
#
#     fight_flow = Fight_flow.get_event()
#
#     ef = Event_flow.Event_flow(ctl)
#     ef.click_event_flow(fight_flow)
#
#
# def fight_golden():
#     Fight_flow = Fgo_event()
#     Fight_flow.regular_fight_term([1, 3, 4, 9], [1], 22)
#     Fight_flow.regular_fight_term([], [2], 23)
#     Fight_flow.regular_fight_term([7, ["master_2", 3]], [3], 30)
#
#     fight_flow = Fight_flow.get_event()
#
#     ef = Event_flow.Event_flow(ctl)
#     ef.click_event_flow(fight_flow)


if __name__ == "__main__":
    ctl = Automator.Automator()
    while True:
        wait_support("img/cba_zhuzhan.jpg")
        fight_main()
        fight_next()
