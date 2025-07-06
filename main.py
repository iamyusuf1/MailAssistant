import pyttsx3  # ✅ TTS Engine

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from mail_reader import read_latest_email
from summarize_email import summarize_email

# ✅ Initialize TTS engine
engine = pyttsx3.init()

class MailAssistant(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.result_label = Label(
            text="Press the button to read your latest mail",
            size_hint_y=None,
            height=400,
            text_size=(300, None),
            halign='left',
            valign='top',
            markup=True
        )

        self.scroll = ScrollView(size_hint=(1, 0.8))
        self.scroll.add_widget(self.result_label)
        self.add_widget(self.scroll)

        self.button = Button(text="Read and Summarize Mail", size_hint=(1, 0.2))
        self.button.bind(on_press=self.read_and_summarize)
        self.add_widget(self.button)

    def read_and_summarize(self, instance):
        try:
            subject, body = read_latest_email()
            summary = summarize_email(subject, body)
            self.result_label.text = f"[b]Subject:[/b] {subject}\n\n[b]Summary:[/b] {summary}"

            # ✅ Speak the summary
            engine.say(f"Subject is: {subject}. Here's the summary: {summary}")
            engine.runAndWait()

        except Exception as e:
            self.result_label.text = f"[b]Error:[/b] {str(e)}"

class MailApp(App):
    def build(self):
        return MailAssistant()

if __name__ == "__main__":
    MailApp().run()
