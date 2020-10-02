import Automator
import Click_event
import time
import Event_flow

position_dictionary = {
    "skill_1": (54, 432),
    "skill_2": (123, 432),
    "skill_3": (192, 432),
    "skill_4": (291, 432),
    "skill_5": (362, 432),
    "skill_6": (432, 432),
    "skill_7": (530, 432),
    "skill_8": (600, 432),
    "skill_9": (672, 432),
    "master_skill_option": (896, 273),
    "skill_master_1": (680, 230),
    "skill_master_2": (747, 230),
    "skill_master_3": (813, 230),
    "change_3": (400, 400),
    "change_4": (550, 400),
    "change_confirm": (482, 473),
    "skill_select_1": (240, 350),
    "skill_select_2": (480, 350),
    "skill_select_3": (710, 350),
    "noble_fantasy_1": (300, 150),
    "noble_fantasy_2": (480, 150),
    "noble_fantasy_3": (660, 150),
    "arbitrary_command_card_1": (300, 380),
    "arbitrary_command_card_2": (490, 380),
    "return": (10, 10),
    "attack": (850, 450),

}
wait_select = 0.6
wait_effect = 0.4
ctl = None


class Event_factory:
    def __init__(self):
        self.event_list = []

    def get_event(self):
        return [
            Click_event.Click_event(parameter[0], parameter[1], parameter[2], parameter[3], parameter[4])
            for parameter in self.event_list
        ]


class Fgo_event(Event_factory):
    def use_skill(self, which):
        if type(which) is str:
            if "master" in which:
                self.event_list.append(
                    [position_dictionary["master_skill_option"], "img/my_term.jpg", True, wait_effect, 0],
                )
        self.event_list.append(
            [position_dictionary[f"skill_{which}"], "img/my_term.jpg", True, wait_effect, 0]
        )

    def use_skill_to(self, which, who):
        if type(which) is str:
            if "master" in which:
                self.event_list.append(
                    [position_dictionary["master_skill_option"], "img/my_term.jpg", True, wait_effect, 0],
                )
        self.event_list.append(
            [position_dictionary[f"skill_{which}"], "img/my_term.jpg", True, wait_effect, 0]
        )
        self.event_list.append(
            [position_dictionary[f"skill_select_{who}"], None, False, wait_select, 0]
        )

    def use_noble_fantasy(self, who_list):
        self.event_list.append(
            [position_dictionary["attack"], "img/my_term.jpg", True, wait_effect, 1]
        )

        for who in who_list:
            self.event_list.append(
                [position_dictionary[f"noble_fantasy_{who}"], None, False, wait_select, 0]
            )

        rest_card = 3 - len(who_list)
        for i in range(rest_card):
            self.event_list.append(
                [position_dictionary[f"arbitrary_command_card_{i + 1}"], None, False, wait_select, 0],
            )

    def regular_fight_term(self, skill_list, noble_fantasy_list, wait_cg=0, change=False):
        for skill in skill_list:
            if type(skill) is str:
                if "master" in skill:
                    self.event_list.append(
                        [position_dictionary["master_skill_option"], "img/my_term.jpg", True, wait_effect, 0],
                    )
            if type(skill) != list:
                self.use_skill(skill)
            else:
                self.use_skill_to(skill[0], skill[1])

        if change:
            self.change()
            return

        self.use_noble_fantasy(noble_fantasy_list)

        self.event_list.append(
            [[0, 0], None, False, 0, wait_cg]
        )

    def change(self):
        append_list = [
            [position_dictionary["master_skill_option"], "img/my_term.jpg", True, wait_effect, 0],
            [position_dictionary["skill_master_3"], None, False, wait_select, 0],
            [position_dictionary["change_3"], None, False, wait_select, 0],
            [position_dictionary["change_4"], None, False, wait_select, 0],
            [position_dictionary["change_confirm"], None, False, wait_select, 0],
        ]
        for append_item in append_list:
            self.event_list.append(
                append_item
            )





def select_support(support_feature):
    screen_shot = ctl.screenshot()
    if ctl.is_there_img(screen_shot, support_feature):
        Click_event.Click_event(None, support_feature, True, wait_effect, 0).click(ctl)
        return True
    else:
        Click_event.Click_event(None, "img/refresh.jpg", True, wait_effect, 0).click(ctl)
        if ctl.is_there_img(ctl.screenshot(), "img/refresh_cd.jpg"):
            Click_event.Click_event(None, "img/refresh_cd_close.jpg", True, wait_effect, 0).click(ctl)
        else:
            Click_event.Click_event(None, "img/refresh_yes.jpg", True, wait_effect, 0).click(ctl)
        return False


def wait_support(support_feature, wait_time=3):
    while not select_support(support_feature):
        time.sleep(wait_time)
    Click_event.Click_event(None, "img/start.jpg", False, 2, 0).click(ctl)


def fight_main():
    Fight_flow = Fgo_event()
    Fight_flow.regular_fight_term([1, 3, [4, 1], [7, 1]], [1], 20)
    Fight_flow.regular_fight_term([8, [9, 1]], [], change=True)
    Fight_flow.regular_fight_term([9], [1], 20)
    Fight_flow.regular_fight_term([[7, 1], [6, 1], 5], [1], 21)

    fight_flow = Fight_flow.get_event()
    ef = Event_flow.Event_flow(ctl,fight_flow)
    ef.click_event_flow()


def fight_next():
    while not ctl.is_there_img(ctl.screenshot(), "img/next.jpg"):
        ctl.click(position_dictionary["return"])
    Click_event.Click_event(None, "img/next.jpg", True, wait_effect, 0).click(ctl)
    Click_event.Click_event(None, "img/no_apply.jpg", False, 1, 0).click(ctl)
    Click_event.Click_event(None, "img/go_on.jpg", True, 1 + wait_effect, 0).click(ctl)

    # 判断是进入哪个分支
    while True:
        screen_shot = ctl.screenshot()
        if ctl.is_there_img(screen_shot, "img/golden_apple.jpg") \
                or ctl.is_there_img(screen_shot, "img/silver_apple.jpg"):
            if ctl.is_there_img(screen_shot, "img/golden_apple.jpg"):
                ctl.guochang(screen_shot, ["img/golden_apple.jpg"])
            else:
                ctl.guochang(screen_shot, ["img/silver_apple.jpg"])
            Click_event.Click_event(None, "img/apple_ok.jpg", True, wait_effect).click(ctl)
        elif ctl.is_there_img(screen_shot, "img/refresh.jpg"):
            break


def some_main():
    ef = Event_flow.Event_flow(ctl)
    flow_parameter_list = [
        [None, "img/cba_zhuzhan.jpg", True, 0, 0],
        [None, "img/start.jpg", True, 0, 0],
        [position_dictionary["skill_1"], "img/my_term.jpg", True, wait_effect, 0],
        [position_dictionary["skill_3"], "img/my_term.jpg", True, wait_effect, 0],
        [position_dictionary["skill_4"], "img/my_term.jpg", True, wait_effect, 0],
        [position_dictionary["skill_select_1"], None, False, wait_select, 0],
        [position_dictionary["skill_7"], "img/my_term.jpg", True, wait_effect, 0],
        [position_dictionary["skill_select_1"], None, False, wait_select, 0],
        [position_dictionary["attack"], "img/my_term.jpg", True, wait_effect, 1],
        [position_dictionary["noble_fantasy_1"], None, False, wait_select, 0],
        [position_dictionary["arbitrary_command_card_1"], None, False, wait_select, 0],
        [position_dictionary["arbitrary_command_card_2"], None, False, wait_select, 0],

        [position_dictionary["skill_9"], "img/my_term.jpg", True, wait_effect, 0],
        [position_dictionary["skill_select_1"], None, False, wait_select, 0],
        [position_dictionary["skill_8"], "img/my_term.jpg", True, wait_effect, 0],
        [position_dictionary["master_skill_option"], "img/my_term.jpg", True, wait_effect, 0],
        [position_dictionary["master_skill_3"], None, False, wait_select, 0],
        [position_dictionary["change_3"], None, False, wait_select, 0],
        [position_dictionary["change_4"], None, False, wait_select, 0],
        [position_dictionary["change_confirm"], None, False, wait_select, 0],
        [position_dictionary["skill_9"], "img/my_term.jpg", True, wait_effect, 0],
        [position_dictionary["attack"], "img/my_term.jpg", True, wait_effect, 1],
        [position_dictionary["noble_fantasy_1"], None, False, wait_select, 0],
        [position_dictionary["arbitrary_command_card_1"], None, False, wait_select, 0],
        [position_dictionary["arbitrary_command_card_2"], None, False, wait_select, 0],

        [position_dictionary["skill_6"], "img/my_term.jpg", True, wait_effect, 0],
        [position_dictionary["skill_select_1"], None, False, wait_select, 0],
        [position_dictionary["skill_5"], "img/my_term.jpg", True, wait_effect, 0],
        [position_dictionary["skill_7"], "img/my_term.jpg", True, wait_effect, 0],
        [position_dictionary["skill_select_1"], None, False, wait_select, 0],
        [position_dictionary["master_skill_option"], "img/my_term.jpg", True, wait_effect, 0],
        [position_dictionary["master_skill_1"], None, False, wait_select, 0],
        [position_dictionary["attack"], "img/my_term.jpg", True, wait_effect, 1],
        [position_dictionary["noble_fantasy_1"], None, False, wait_select, 0],
        [position_dictionary["arbitrary_command_card_1"], None, False, wait_select, 0],
        [position_dictionary["arbitrary_command_card_2"], None, False, wait_select, 0],

    ]
    flow = [
        Click_event.Click_event(parameter[0], parameter[1], parameter[2], parameter[3], parameter[4])
        for parameter in flow_parameter_list
    ]
    # ef.click_event_flow(flow)

    Click_event.Click_event(None, "img/go_on.jpg", True, wait_effect, 0).click(ctl)
    # Click_event.Click_event(position_dictionary["return"],"img/next.jpg", True, wait_effect, 0).click(ctl)


def test_select_support():
    wait_support("img/sanxinglizhuang.jpg")


def fight_copper():
    Fight_flow = Fgo_event()
    Fight_flow.regular_fight_term([1], [1], 22)
    Fight_flow.regular_fight_term([5], [2], 23)
    Fight_flow.regular_fight_term([8, ["master_2", 3]], [3], 30)

    fight_flow = Fight_flow.get_event()
    ef = Event_flow.Event_flow(ctl)
    ef.click_event_flow(fight_flow)


def fight_silver():
    Fight_flow = Fgo_event()
    Fight_flow.regular_fight_term([2, 3], [1], 20)
    Fight_flow.regular_fight_term([6], [2], 20)
    Fight_flow.regular_fight_term([7, 8, ["master_2", 3]], [3], 30)

    fight_flow = Fight_flow.get_event()

    ef = Event_flow.Event_flow(ctl)
    ef.click_event_flow(fight_flow)


def fight_golden():
    Fight_flow = Fgo_event()
    Fight_flow.regular_fight_term([1, 3, 4, 9], [1], 22)
    Fight_flow.regular_fight_term([], [2], 23)
    Fight_flow.regular_fight_term([7, ["master_2", 3]], [3], 30)

    fight_flow = Fight_flow.get_event()

    ef = Event_flow.Event_flow(ctl)
    ef.click_event_flow(fight_flow)


if __name__ == "__main__":
    ctl = Automator.Automator()
    while True:
        wait_support("img/cba_zhuzhan.jpg")
        fight_main()
        fight_next()
