from src.tg_bot.conversations.utils.replies.stepper import Stepper


class Replier:
    def __init__(self, replies: dict, steps: list):
        self.stepper = Stepper(steps)
        self.replies = replies

    def restart(self, steps: list, step=None):
        self.stepper.reinit(steps, 0 if step is None else step)

    def current_reply(self, **kwargs):
        step = self.stepper.current_step()

        return self.replies[step](**kwargs)

    def next_reply(self, **kwargs):
        step = self.stepper.next_step()

        return self.replies[step](**kwargs)

    def previous_reply(self, **kwargs):
        step = self.stepper.previous_step()

        return self.replies[step](**kwargs)
