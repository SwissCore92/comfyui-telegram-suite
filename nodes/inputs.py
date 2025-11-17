
from .utils import UINT64_MAX


bot = ("TELEGRAM_BOT", {
    "forceInput": True,
    "tooltip": "Telegram bot instance"
})

method_name = ("STRING", {
    "default": "getMe",
    "tooltip": "The telegram bot api message to call. (case insensitive)"
})

params = ("DICT", {
    "default": {},
    "tooltip": "The method parameters."
})

chat_id = ("INT", {
    "forceInput": True,
    "tooltip": "Unique identifier for the target chat"
})

message_id = ("INT", {
    "forceInput": True,
    "tooltip": "Unique Identifier of the message to edit"
})

trigger = ("*", {
    "forceInput": True,
    "tooltip": "Optional trigger to enforce execution order"
})

text = ("STRING", {
    "multiline": True, 
    "default": "",
    "tooltip": "Text of the message to be sent, 1-4096 characters after entities parsing"
})

caption = ("STRING", {
    "multiline": True, 
    "default": "",
    "tooltip": "Media caption, 0-1024 characters after entities parsing"
})

parse_mode = (["None", "HTML", "Markdown", "MarkdownV2"], {
    "tooltip": "Mode for parsing entities in the photo caption. "
    "See https://core.telegram.org/bots/api#formatting-options for more details."
})

show_caption_above_media = ("BOOLEAN", {
    "default": False,
    "tooltip": "Pass True, if the caption must be shown above the message media"
})

disable_notification = ("BOOLEAN", {
    "default": True,
    "tooltip": "Sends the message silently. Users will receive a notification with no sound."
})

has_spoiler = ("BOOLEAN", {
    "default": False,
    "tooltip": "Pass True if the media needs to be covered with a spoiler animation"
})

protect_content = ("BOOLEAN", {
    "default": False,
    "tooltip": "Protects the contents of the sent message from forwarding and saving"
})

message_thread_id = ("INT", {
    "default": -1, 
    "min": -1, 
    "max": UINT64_MAX, 
    "tooltip": "Unique identifier for the target message thread of the forum topic (-1 = None)"
})

group = ("BOOLEAN", {
    "default": True,
    "tooltip": "Pass True to send multiple media as media group"
})

send_as_file = ("BOOLEAN", {
    "default": False,
    "tooltip": "Pass True to send the media as file without compression"
})

image_formats = (["PNG", "WEBP", "JPG"], {
    "tooltip": "image format"
})

send_video_as = (["Animation", "Video", "File"], {
    "tooltip": "How to send the video"
})

send_audio_as = (["Voice", "Audio", "File"], {
    "tooltip": "How to send the audio"
})


image = ["IMAGE", {
    "forceInput": True,
    "tooltip": "the image(s) to send"
}]

video = ("VHS_FILENAMES", {
    "forceInput": True,
    "tooltip": "the video to send (VHS)"
})

audio = ("AUDIO", {
    "forceInput": True,
    "tooltip": "the audio to send"
})

chat_action = ([
    "typing",
    "upload_photo",
    "record_video",
    "upload_video",
    "record_voice",
    "upload_voice",
    "upload_document",
    "choose_sticker",
    "find_location",
    "record_video_note",
    "upload_video_note",
], {
    "tooltip": "Type of action to broadcast. "
    "Choose one, depending on what the user is about to receive. "
})

def file_name(default: str):
    return ("STRING", {
        "default": default,
        "tooltip": "the file name for this media"
    })