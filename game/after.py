from utils.handler_cv2 import HandlerCv2


class After:
    def __init__(self, cv2: HandlerCv2):
        self.cv2 = cv2

    def marchants(self):
        print("TODO")

    def quests(self):
        def dailies():
            print("TODO")

        def weeklies():
            print("TODO")

        def campaign():
            print("TODO")

        dailies()
        weeklies()
        campaign()

    def run(self):
        self.marchants()
        self.quests()