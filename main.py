from playsound3 import playsound
import dearpygui.dearpygui as dpg
import threading
import yt_dlp

SELECTED_TYPE = ""
SELECTED_CODEC = ""
SELECTED_QUALITY = ""

URL = ""
TYPE = ["Audio","Video"]
CODECAUDIO = ["aac", "alac", "flac", "m4a", "mp3", "opus", "vorbis", "wav"]
CODECVIDEO = ["mp4", "mov", "m4a", "webm", "mkv", "mka"]
CODEC_TYPE = [""]
QUALITY = ['64','128','192','256','320']

# Extra
def show_notification(title, message):
    with dpg.window(label=title, modal=True, tag="notif_window", width=250, height=100):
        dpg.add_text(message)
        dpg.add_button(label="OK", width=60, callback=lambda: dpg.delete_item("notif_window"))

def play_sound_async(file):
    threading.Thread(target=playsound, args=(file,)).start() # Prevent freezing between popup and sound

# Theme
# This is not the cleanest way, I'll change this soon
'''
def apply_theme(apply_theme: bool):
    with dpg.theme() as theme:
        with dpg.theme_component(dpg.mvAll):
            if apply_theme:
                pass
            else:
                pass
'''

# all logic
def combo_callback(sender, app_data, user_data,):
    global SELECTED_QUALITY, SELECTED_CODEC, SELECTED_TYPE

    if user_data == "Type":
        SELECTED_TYPE = app_data

        if app_data == "Audio":
            CODEC_TYPE = CODECAUDIO
            SELECTED_CODEC = CODECAUDIO[0]
            dpg.configure_item("codec_combo", items=CODECAUDIO)


        elif app_data == "Video":
            CODEC_TYPE = CODECVIDEO
            SELECTED_CODEC = CODECVIDEO[0]
            dpg.configure_item("codec_combo", items=CODECVIDEO)

    elif user_data == "Codec":
        SELECTED_CODEC = app_data

    elif user_data == "Quality":
        SELECTED_QUALITY = app_data

    print(f"{user_data} selected: {app_data}")

def save_callback():
    global URL, SELECTED_QUALITY, SELECTED_CODEC, SELECTED_TYPE

    if not URL.strip():
        show_notification("Error", "Enter a valid URL!")
        return

    if SELECTED_TYPE == "Audio":
        post = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": SELECTED_CODEC,
            "preferredquality": SELECTED_QUALITY,
        }]
        yt_opts = {
            "format": "bestaudio/best",
            "postprocessors": post,
        }

    elif SELECTED_TYPE == "Video":
        yt_opts = {
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": SELECTED_CODEC,
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

# Gui
dpg.create_context()
with dpg.window(tag="Primary Window"):
    with dpg.menu_bar():
        with dpg.menu(label="Menu"):
                with dpg.menu(label="Themes"):
                    dpg.add_menu_item(label="Dark", check=True, default_value=True)

    dpg.add_combo(
        label="Type",
        items=TYPE,
        default_value=SELECTED_TYPE,
        callback=combo_callback,
        user_data='Type',
        )

    dpg.add_combo(
        label="Codec",
        items=CODEC_TYPE,
        default_value=SELECTED_CODEC,
        callback=combo_callback,
        user_data="Codec",
        tag="codec_combo"
    )

    dpg.add_combo(
        label="Quality",
        items=QUALITY,
        default_value=SELECTED_QUALITY,
        callback=combo_callback,
        user_data="Quality",
        )

    dpg.add_input_text(
        label="ytb-url",
        callback=string_callback,
        )

    dpg.add_button(
        label="Save",
        callback=save_callback,
        )

dpg.create_viewport(title='ytb-dlp-imgui', width=600, height=400, resizable=False)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()