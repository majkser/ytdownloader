from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock
import yt_dlp
import os
from pathlib import Path
import threading

class Downloader(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.window.spacing = 20

        self.progress_text = Label(text="", size_hint=(1, 0.3), font_size=20)
        self.window.add_widget(self.progress_text)

        self.format = "audio"
        self.download_path = os.path.join(Path.home(), "Downloads", "yt_downloads")
        os.makedirs(self.download_path, exist_ok=True)

        self.common_opts = {
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
            'encoding': 'utf-8',
            'progress_hooks': [self.progress_hook],
        }
        
        self.vid_and_sound_opts = {
            **self.common_opts,
            'format': 'best',
        }
        
        self.vid_opts = {
            **self.common_opts,
            'format': 'bv*[ext=mp4]',
        }

        self.sound_opts = {
            **self.common_opts,
            'format': 'bestaudio',
        }

        self.ydl_opts = self.sound_opts

        self.window.add_widget(Image(source='download.jpeg'))
        self.url_text = Label(text="Enter the URL: ", font_size=28)
        self.window.add_widget(self.url_text)

        self.url = TextInput(multiline=False, font_size=16, padding_y=(10, 10), size_hint=(1, 0.5))
        self.window.add_widget(self.url)

        format_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.5))

        self.radio_video = CheckBox(group="format")
        self.radio_audio = CheckBox(group="format", active=True)
        self.radio_video_and_audio = CheckBox(group="format")

        self.radio_audio.bind(active=self.on_checkbox_change)
        self.radio_video.bind(active=self.on_checkbox_change)
        self.radio_video_and_audio.bind(active=self.on_checkbox_change)

        format_layout.add_widget(Label(text="Audio", font_size=16))
        format_layout.add_widget(self.radio_audio)
        format_layout.add_widget(Label(text="Video", font_size=16))
        format_layout.add_widget(self.radio_video)
        format_layout.add_widget(Label(text="Video + Audio", font_size=16))
        format_layout.add_widget(self.radio_video_and_audio)

        self.window.add_widget(format_layout)

        self.button = Button(text="Download", font_size=32, size_hint=(1, 0.5), bold=True, background_color=(0, 1, 1, 1))
        self.button.bind(on_press=self.download)
        self.window.add_widget(self.button)

        return self.window

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_progress = ""

    def update_progress(self, dt):
        self.progress_text.text = self.current_progress

    def progress_hook(self, d):
        if d['status'] == 'finished':
            self.current_progress = "Download completed"
            Clock.schedule_once(self.update_progress)
        elif d['status'] == 'downloading':
            self.current_progress = f"Downloading: {d.get('_percent_str', '0%')}"
            Clock.schedule_once(self.update_progress)

    def on_checkbox_change(self, checkbox, value):
        if value:
            if checkbox == self.radio_audio:
                self.format = "audio"
                self.ydl_opts = self.sound_opts
            elif checkbox == self.radio_video:
                self.format = "video"
                self.ydl_opts = self.vid_opts
            else:
                self.format = "audio_video"
                self.ydl_opts = self.vid_and_sound_opts

    def download(self, instance):
        if not self.url.text:
            self.url_text.text = "Please enter a URL"
            return

        self.current_percent = 0
        self.progress_text.text = ""
        self.button.disabled = True

        def download_thread():
            try:
                with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                    ydl.download([self.url.text])
                    Clock.schedule_once(lambda dt: setattr(self.url_text, 'text', f"Saved to: {self.download_path}"))
            except Exception as e:
                Clock.schedule_once(lambda dt: setattr(self.url_text, 'text', f"Error: {str(e)}"))
            finally:
                Clock.schedule_once(lambda dt: setattr(self.button, 'disabled', False))
        
        threading.Thread(target=download_thread, daemon=True).start()

if __name__ == "__main__":
    Downloader().run()