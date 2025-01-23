from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
import yt_dlp

class Downloader(App):
    def build(self):
        self.window = GridLayout()
        #add widgets to window
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.window.spacing = 20
        self.format = "audio"
        
        self.vid_opts = {
            'format': "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b",
            'outtmpl': '%(title)s.%(ext)s',
        }

        self.sound_opts = {
            'format': 'ba[ext=m4a]',
            'outtmpl': '%(title)s.%(ext)s',
        }
        
        self.ydl_opts = self.sound_opts
        
        self.window.add_widget(Image(source='download.jpeg'))
        self.url_text = Label(text="Enter the URL: ", font_size=28)
        self.window.add_widget(self.url_text)
        
        self.url = TextInput(multiline=False, font_size=16, padding_y=(10,10), size_hint=(1, 0.5)) 
        self.window.add_widget(self.url)
        
        format_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.5))
        
        self.radio_video = CheckBox(group="format")
        self.radio_audio = CheckBox(group="format", active=True)
        
        self.radio_audio.bind(active=self.on_checkbox_change)
        self.radio_video.bind(active=self.on_checkbox_change)
        
        format_layout.add_widget(Label(text="Audio", font_size=16))
        format_layout.add_widget(self.radio_audio)
        format_layout.add_widget(Label(text="Video", font_size=16))
        format_layout.add_widget(self.radio_video)
        
        self.window.add_widget(format_layout)       

        self.button = Button(text="Download", font_size=32, size_hint=(1, 0.5), bold=True, background_color=(0, 1, 1, 1))
        self.button.bind(on_press=self.download)
        self.window.add_widget(self.button)

        return self.window
    
    
    def on_checkbox_change(self, checkbox, value):
        if value:
            if checkbox == self.radio_audio:
                self.format = "audio"
                self.ydl_opts = self.sound_opts
            else:
                self.format = "video"
                self.ydl_opts = self.vid_opts
    
    def download(self, instance):
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([self.url.text])
            
        self.url_text.text = f"Downloading ..."
        
if __name__ == "__main__":
    Downloader().run()
