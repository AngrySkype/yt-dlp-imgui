from playsound3 import playsound
import dearpygui.dearpygui as dpg
import threading
import yt_dlp


SELECTED_TYPE = "FFmpegExtractAudio"
SELECTED_CODEC = ""
SELECTED_QUALITY = ""

URL = ""
TYPE = ['FFmpegExtractAudio']
CODEC = ["aac","alac","flac","m4a","mp3","opus","vorbis","wav"]
QUALITY = ['64','128','192','256','320']

def show_notification(title, message):
    with dpg.window(label=title, modal=True, tag="notif_window", width=250, height=100):
        dpg.add_text(message)
        dpg.add_button(label="OK", width=60, callback=lambda: dpg.delete_item("notif_window"))

def play_sound_async(file):
    threading.Thread(target=playsound, args=(file,)).start()

def combo_callback(sender, data, user_data):
    global SELECTED_QUALITY, SELECTED_CODEC, SELECTED_TYPE

    if user_data == "Type":
        SELECTED_TYPE = data
    elif user_data == "Codec":
        SELECTED_CODEC = data
    elif user_data == "Quality":
        SELECTED_QUALITY = data

    print(f"{user_data} selected: {data}")

def save_callback():
    global URL, SELECTED_QUALITY, SELECTED_CODEC, SELECTED_TYPE

    if not URL:
        show_notification("Error", "enter a valid URL!")
        return

    yt_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": SELECTED_TYPE,
            "preferredcodec": SELECTED_CODEC,
            "preferredquality": SELECTED_QUALITY,
        }]
    }
    with yt_dlp.YoutubeDL(yt_opts) as ydl:
        error_code = ydl.download([URL])
        print(error_code)
        show_notification("Done", "Download completed successfully!")
        play_sound_async("sounds/finish.mp3")


def string_callback(sender, data):
    global URL
    URL = data
    print("Current URL :", URL)

dpg.create_context()
with dpg.window(tag="Primary Window"):
    dpg.add_combo(label="Type",
                  items=TYPE,
                  default_value=SELECTED_TYPE,
                  callback=combo_callback,
                  user_data="Type",
                  )

    dpg.add_combo(label="Codec",
                  items=CODEC,
                  default_value=SELECTED_CODEC,
                  callback=combo_callback,
                  user_data="Codec"
                  )

    dpg.add_combo(label="Quality",
                  items=QUALITY,
                  default_value=SELECTED_QUALITY,
                  callback=combo_callback,
                  user_data="Quality",
                  )

    dpg.add_input_text(label="ytb-url",
                       callback=string_callback,
                       )

    dpg.add_button(label="Save",
                   callback=save_callback,
                   )

dpg.create_viewport(title='ytb-dlp-imgui', width=600, height=400, resizable=False)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()