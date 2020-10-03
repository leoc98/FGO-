import Click_event
from Static_data import position_dictionary, wait_select, wait_effect


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
