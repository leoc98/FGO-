import Click_event


class Event_flow:
    def __init__(self, handler, flow):
        self.handler = handler
        self.flow = flow
        pass

    """
        输入一个点击流程，按照预设时间进行点击
        flow中每个元素都是一个Click_event
    """

    def click_event_flow(self):
        for item in self.flow:
            # if event.position is not None:
            print(item)
            if type(item) == Click_event.Click_event:
                item.click(self.handler)
                # item.ping(str(self.flow))
            elif type(item) in Event_flow.__subclasses__() or type(item) is Event_flow:
                # If_flow.
                # print("hey")
                item.click_event_flow()


class If_flow(Event_flow):
    def __init__(self, handler, flow, if_condition=False):
        super().__init__(handler, flow)
        self.if_condition = if_condition

    def click_event_flow(self):
        execute = self.if_condition(self.handler) if callable(self.if_condition) else self.if_condition
        if execute:
            super().click_event_flow()


if __name__ == "__main__":
    ce = Click_event.Click_event()


    def return_false(*args):
        return True


    ief = If_flow(None, [ce], return_false)
    ef = Event_flow(None, [ce, ief])
    ef.click_event_flow()
