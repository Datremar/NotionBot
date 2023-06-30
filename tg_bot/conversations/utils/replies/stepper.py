from telegram.ext import ConversationHandler


class Stepper:
    def __init__(self, steps: list):
        self.step = 0
        self.steps = steps

    def reinit(self, steps: list, step: int):
        self.steps = steps
        self.step = step

    def current_step(self):
        return self.steps[self.step]

    def next_step(self):
        self.step += 1

        if self.step >= len(self.steps):
            self.step -= 1
            return ConversationHandler.END

        if self.steps[self.step] is None:
            return self.next_step()

        return self.steps[self.step]

    def previous_step(self):
        self.step -= 1

        if self.step < 0:
            self.step = 0

        if self.steps[self.step] is None:
            return self.previous_step()

        return self.steps[self.step]
