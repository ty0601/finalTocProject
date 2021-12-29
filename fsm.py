from transitions.extensions import GraphMachine

from utils import send_text_message


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def read(self, event):
        text = event.message.text
        return text.lower() == "study"

    def play(self, event):
        text = event.message.text
        return text.lower() == "play"

    def reset(self, event):
        text = event.message.text
        return text.lower() == "reset"

    def read1(self, event):
        print("I'm reading")

        reply_token = event.reply_token
        send_text_message(reply_token, "You are reading")

    def read2(self, event):
        print("I'm reading")

        reply_token = event.reply_token
        send_text_message(reply_token,  "You are reading")

    def read3(self, event):
        print("I'm reading")

        reply_token = event.reply_token
        send_text_message(reply_token,  "You are reading")

    def read4(self, event):
        print("I'm reading")

        reply_token = event.reply_token
        send_text_message(reply_token, "You need to take a break!")

    

    def play1(self, event):
        print("I'm playing")

        reply_token = event.reply_token
        send_text_message(reply_token, "You are playing")


    def play2(self, event):
        print("I'm playing")

        reply_token = event.reply_token
        send_text_message(reply_token,"You are playing")

    def play3(self, event):
        print("I'm playing")

        reply_token = event.reply_token
        send_text_message(reply_token,"You are playing")

    def play4(self, event):
        print("I'm playing")

        reply_token = event.reply_token
        send_text_message(reply_token, "Don't play anymore!")