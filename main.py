from Event_factory import Fgo_event
from FGO_fight_method import fight_process

support = "img/huajia_zhuzhan.jpg"


def fight_ticket_1():
    Fight_flow = Fgo_event()
    Fight_flow.regular_fight_term([1, 3, [4, 1], [7, 1]], [1], 20)
    Fight_flow.regular_fight_term([8, [9, 1]], [], change=True)
    Fight_flow.regular_fight_term([9], [1], 22)
    Fight_flow.regular_fight_term([[7, 1], [6, 1], 5], [1], 21)
    fight_flow = Fight_flow.get_event()
    return fight_flow


def fight_ticket_3():
    Fight_flow = Fgo_event()
    Fight_flow.regular_fight_term([1, 2, 3, [4, 1], [5, 1], [7, 1], [8, 1]], [], change=True)
    Fight_flow.regular_fight_term([[9, 1]], [1], 23)
    Fight_flow.regular_fight_term([], [1], 24)
    Fight_flow.regular_fight_term(["master_1"], [1], 22)
    fight_flow = Fight_flow.get_event()
    return fight_flow


if __name__ == "__main__":
    while True:
        fight_process(support, fight_ticket_3())
