class Lightbulb:
    def __init__(self):
        self.state = "off"

    def change_state(self):
        if self.state == "off":
            self.state = "on"
        else:
            self.state = "off"
        print("Turning the light", self.state)
