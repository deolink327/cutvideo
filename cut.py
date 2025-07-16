from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from plyer import filechooser
from moviepy.editor import VideoFileClip
import os

class CutterUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.label = Label(text="🎬 Cắt video thành từng phần tùy chỉnh", size_hint=(1, 0.2))
        self.add_widget(self.label)

        self.minute_input = TextInput(hint_text="Phút", input_filter='int', multiline=False, size_hint=(1, 0.1))
        self.second_input = TextInput(hint_text="Giây", input_filter='int', multiline=False, size_hint=(1, 0.1))
        self.add_widget(self.minute_input)
        self.add_widget(self.second_input)

        self.choose_btn = Button(text="📁 Chọn video", on_press=self.choose_video, size_hint=(1, 0.2))
        self.add_widget(self.choose_btn)

        self.result = Label(text="", size_hint=(1, 0.2))
        self.add_widget(self.result)

    def choose_video(self, instance):
        filechooser.open_file(on_selection=self.cut_video)

    def cut_video(self, selection):
        if not selection:
            self.result.text = "⛔ Không có file được chọn."
            return

        filepath = selection[0]
        mins = int(self.minute_input.text) if self.minute_input.text else 0
        secs = int(self.second_input.text) if self.second_input.text else 0
        chunk_length = mins * 60 + secs

        if chunk_length <= 0:
            self.result.text = "⛔ Vui lòng nhập thời gian > 0."
            return

        try:
            video = VideoFileClip(filepath)
            duration = video.duration
            base_name = os.path.splitext(os.path.basename(filepath))[0]
            output_dir = f"/sdcard/{base_name}_splits"
            os.makedirs(output_dir, exist_ok=True)

            i = 0
            for start in range(0, int(duration), chunk_length):
                end = min(start + chunk_length, duration)
                clip = video.subclip(start, end)
                output_path = os.path.join(output_dir, f"{base_name}_part{i+1}.mp4")
                clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
                i += 1

            self.result.text = f"✅ Đã cắt {i} phần tại: {output_dir}"

        except Exception as e:
            self.result.text = f"❌ Lỗi: {e}"

class CutterApp(App):
    def build(self):
        return CutterUI()

if __name__ == '__main__':
    CutterApp().run()