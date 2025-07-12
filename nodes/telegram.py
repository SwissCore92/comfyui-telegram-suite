import json
import logging
import mimetypes

import httpx
from colorama import Fore

from . import utils

# prevent httpx from logging the token
logger = logging.getLogger("httpx").setLevel(logging.CRITICAL)

debug = True

_CATEGORY = "Telegram Suite 🔽"

config = utils.load_config()

class TelegramException(Exception): ...

class TelegramBot:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": (list(config["bots"].keys()), {}),
            },
            "optional": {
                "chat": (list(config["chats"].keys()), {}),
            }
        }
    
    RETURN_TYPES = ("TELEGRAM_BOT", "INT")
    RETURN_NAMES = ("bot", "chat_id")

    FUNCTION = "init_telegram_bot"
    CATEGORY = _CATEGORY

    def init_telegram_bot(self, bot: str, chat=None):
        token = config["bots"][bot]

        self.session = httpx.Client(
            base_url=f"https://api.telegram.org/bot{token}/",
        )

        return (self, 0 if chat is None else config["chats"][chat])

    def __call__(self, method_name: str, params: dict | None = None, files: dict | None = None):
        params = {
            k: json.dumps(v, ensure_ascii=False, separators=(",", ":")) 
            if isinstance(v, (dict, list)) else v 
            for k, v in params.items()
            if v # is not None
        } if params else None

        result = self.session.post(method_name, data=params or None, files=files or None).json()

        if not result["ok"]:
            if debug:
                f = {k: (v[0], "<file_bytes>", v[2]) for k, v in files.items()} if files else None
                print(f"[TELEGRAM SUITE]: {method_name}({params=}, files={f}) -> {result}")

            raise TelegramException(f"'{method_name}' was unsuccessful: ", result)
        
        print(f"[TELEGRAM SUITE]: {method_name}(...) -> OK")
        return result["result"]

class APIMethod:
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": ("TELEGRAM_BOT", {"forceInput": True}),
                "method_name": ("STRING", {"default": "sendMessage"}),
            },
            "optional": {
                "chat_id": ("INT", {"forceInput": True}),
                "params": ("DICT", {"default": {}})
            }
        }
     
    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("RESULT *",)

    FUNCTION = "call_api_method"
    CATEGORY = f"{_CATEGORY}/experimental"

    def call_api_method(self, bot: TelegramBot, method_name, chat_id=None, params=None):
        params = params if params else {}
        params["chat_id"] = chat_id
        return (bot(method_name, params=params),)


class SendGeneric:
    OUTPUT_NODE = True

    RETURN_TYPES = ("DICT", "INT", "*")
    RETURN_NAMES = ("message", "message_id", "trigger")

    CATEGORY = _CATEGORY

class SendMessage(SendGeneric):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": ("TELEGRAM_BOT", {"forceInput": True}),
                "chat_id": ("INT", {"forceInput": True}),
                "text": ("STRING", {"multiline": True, "default": ""}),
                "parse_mode": (["None", "HTML", "Markdown", "MarkdownV2"], {}),
                "disable_notification": ("BOOLEAN", {"default": True}),
                "protect_content": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "trigger": ("*", {"forceInput": True})
            }
        }

    FUNCTION = "send_message"

    def send_message(self, bot: TelegramBot, trigger=None, **params):
        if params["parse_mode"] == "None":
            params.pop("parse_mode")
        
        message = bot("sendMessage", params=params)

        return message, message["message_id"], trigger

class SendImage(SendGeneric):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": ("TELEGRAM_BOT", {"forceInput": True}),
                "chat_id": ("INT", {"forceInput": True}),
                "IMAGE": ("IMAGE", {"forceInput": True}),
                "caption": ("STRING", {"multiline": True, "default": ""}),
                "parse_mode": (["None", "HTML", "Markdown", "MarkdownV2"], {}),
                "show_caption_above_media": ("BOOLEAN", {"default": False}),
                "disable_notification": ("BOOLEAN", {"default": True}),
                "protect_content": ("BOOLEAN", {"default": False}),
                "group": ("BOOLEAN", {"default": True}),
                "send_as_file": ("BOOLEAN", {"default": False}),
                "file_name": ("STRING", {"default": "image"}),
                "format": (["PNG", "WEBP", "JPG"], {}),
            },
            "optional": {
                "trigger": ("*", {"forceInput": True})
            }
        }

    FUNCTION = "send_photo"

    def send_photo(self, bot: TelegramBot, IMAGE, group, send_as_file, file_name, format, trigger=None, **params):
        id = "document" if send_as_file else "photo"

        if params["parse_mode"] == "None":
            params.pop("parse_mode")

        images_bytes = utils.images_to_bytes(IMAGE, format)

        if len(images_bytes) == 1:
            # Single Image
            params[id] = f"attach://{id}"
            file_name = f"{file_name or "image"}.{format.lower()}"
            message = bot(
                "sendDocument" if send_as_file else "sendPhoto", 
                params=params, 
                files={id: (file_name, image_bytes, utils.guess_mimetype(file_name))}
            )
            return message, message["message_id"], trigger

        else:
            if group:
                # Multiple images - send as media group
                media = []
                files = {}
                for i, b in enumerate(images_bytes):
                    name = f"{file_name or "image"}{i}.{format.lower()}"
                    files[f"{id}{i}"] = (name, b, utils.guess_mimetype(name))

                    m = {
                        "type": "document" if send_as_file else "photo", 
                        "media": f"attach://{id}{i}",
                    }
                    if params.get("caption"):
                        m["caption"] = params.get("caption"), 
                    if params.get("parse_mode", "None") != "None":
                        m["parse_mode"] = params.get("parse_mode")
                    if id != "document":
                        m["show_caption_above_media"] = params["show_caption_above_media"] or None,

                    media.append(m)

                messages = bot(
                    "sendMediaGroup", 
                    params={
                        "chat_id": params["chat_id"], 
                        "media": media, 
                        "disable_notification": params["disable_notification"] or None,
                        "protect_content": params["protect_content"] or None,
                    },
                    files=files
                )
                return messages[-1], messages[-1]["message_id"], trigger

            else:
                # Multiple images - send individually
                messages = []
                for index, image_bytes in enumerate(images_bytes):
                    params[id] = f"attach://{id}"
                    name = f"{file_name}_{index}.{format.lower()}"

                    if id == "document":
                        params.pop("show_caption_above_media")

                    messages.append(
                        bot(
                            "sendDocument" if send_as_file else "sendPhoto", 
                            params=params, 
                            files={id: (name, image_bytes, utils.guess_mimetype(name))}
                        )
                    )
                return messages[-1], messages[-1]["message_id"], trigger

class SendVideo(SendGeneric):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": ("TELEGRAM_BOT", {"forceInput": True}),
                "chat_id": ("INT", {"forceInput": True}),
                "video": ("VHS_FILENAMES", {"forceInput": True}),
                "caption": ("STRING", {"multiline": True, "default": ""}),
                "parse_mode": (["None", "HTML", "Markdown", "MarkdownV2"], {}),
                "show_caption_above_media": ("BOOLEAN", {"default": False}),
                "disable_notification": ("BOOLEAN", {"default": True}),
                "protect_content": ("BOOLEAN", {"default": False}),
                "send_as": (["Animation", "Video", "File"], {}),
            },
            "optional": {
                "trigger": ("*", {"forceInput": True})
            }
        }

    FUNCTION = "send_video"

    def send_video(self, bot: TelegramBot, video, send_as, trigger=None, **params):
        if params["parse_mode"] == "None":
            params.pop("parse_mode")
        
        file_path = [v for v in video[1] if not v.endswith(".png")][0]

        file_name = file_path.rsplit("/", 1)[-1]
        mimetype = mimetypes.guess_type(file_name)[0] or "application/octet_stream"

        if send_as == "File":
            send_as = "Document"

        id = send_as.lower()

        params[id] = f"attach://{id}"

        with open(file_path, "rb") as f:
            message = bot(
                f"send{send_as}",
                params=params,
                files={id: (file_name, f.read(), mimetype)}
            )
        
        return message, message["message_id"], trigger

class SendAudio(SendGeneric):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": ("TELEGRAM_BOT", {"forceInput": True}),
                "chat_id": ("INT", {"forceInput": True}),
                "audio": ("AUDIO", {"forceInput": True}),
                "caption": ("STRING", {"multiline": True, "default": ""}),
                "parse_mode": (["None", "HTML", "Markdown", "MarkdownV2"], {}),
                "show_caption_above_media": ("BOOLEAN", {"default": False}),
                "disable_notification": ("BOOLEAN", {"default": True}),
                "protect_content": ("BOOLEAN", {"default": False}),
                "send_as": (["Voice", "Audio", "File"], {}),
                "file_name": ("STRING", {"default": "audio"}),
            },
            "optional": {
                "trigger": ("*", {"forceInput": True})
            }
        }

    FUNCTION = "send_audio"

    def send_audio(self, bot: TelegramBot, audio, send_as, file_name, trigger=None, **params):
        if params["parse_mode"] == "None":
            params.pop("parse_mode")
        params["caption"] = params["caption"] or None

        format = "ogg" if send_as == "Voice" else "mp3" if send_as == "Audio" else "wav"

        wav_bytes = utils.audio_to_wav_bytes(audio)

        name = f"{file_name or "audio"}.{format}"

        if send_as == "File":
            params["document"] = "attach://document"
            message = bot("sendDocument", params=params, files={"document": (name, wav_bytes, utils.guess_mimetype(name))})
            return message, message["message_id"], trigger
        
        id = "audio" if send_as == "Audio" else "voice"
        params[id] = f"attach://{id}"

        b = utils.convert_wav_bytes_ffmpeg(wav_bytes, "mp3" if send_as == "Audio" else "ogg")

        message = bot(f"send{id.capitalize()}", params=params, files={id: (name, b, utils.guess_mimetype(name))})
        
        return message, message["message_id"], trigger


class EditMessageText(SendGeneric):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": ("TELEGRAM_BOT", {"forceInput": True}),
                "chat_id": ("INT", {"forceInput": True}),
                "message_id": ("INT", {"forceInput": True}),
                "text": ("STRING", {"multiline": True, "default": ""}),
                "parse_mode": (["None", "HTML", "Markdown", "MarkdownV2"], {}),
            },
            "optional": {
                "trigger": ("*", {"forceInput": True})
            }
        }
    CATEGORY = f"{_CATEGORY}/edit"
    FUNCTION = "edit_message_text"

    def edit_message_text(self, bot: TelegramBot, trigger=None, **params):
        if params["parse_mode"] == "None":
            params.pop("parse_mode")
        
        message = bot("editMessageText", params=params)

        return message, message["message_id"], trigger

class EditMessageCaption(SendGeneric):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": ("TELEGRAM_BOT", {"forceInput": True}),
                "chat_id": ("INT", {"forceInput": True}),
                "message_id": ("INT", {"forceInput": True}),
                "caption": ("STRING", {"multiline": True, "default": ""}),
                "parse_mode": (["None", "HTML", "Markdown", "MarkdownV2"], {}),
                "show_caption_above_media": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "trigger": ("*", {"forceInput": True})
            }
        }

    CATEGORY = f"{_CATEGORY}/edit"
    FUNCTION = "edit_message_caption"

    def edit_message_caption(self, bot: TelegramBot, trigger=None, **params):
        if params["parse_mode"] == "None":
            params.pop("parse_mode")
        
        message = bot("editMessageCaption", params=params)

        return message, message["message_id"], trigger

class EditMessageImage(SendGeneric):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": ("TELEGRAM_BOT", {"forceInput": True}),
                "chat_id": ("INT", {"forceInput": True}),
                "message_id": ("INT", {"forceInput": True}),
                "IMAGE": ("IMAGE", {"forceInput": True}),
                "caption": ("STRING", {"multiline": True, "default": ""}),
                "parse_mode": (["None", "HTML", "Markdown", "MarkdownV2"], {}),
                "show_caption_above_media": ("BOOLEAN", {"default": False}),
                "file_name": ("STRING", {"default": "image"}),
                "format": (["PNG", "WEBP", "JPG"], {}),
                "as_file": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "trigger": ("*", {"forceInput": True})
            }
        }
    
    CATEGORY = f"{_CATEGORY}/edit"
    FUNCTION = "edit_message_image"

    def edit_message_image(self, bot: TelegramBot, IMAGE, file_name, format,  as_file, trigger=None, **params):
        if params["parse_mode"] == "None":
            params.pop("parse_mode")
        
        name = f"{file_name}.{format.lower()}"
        
        _params = {
            "chat_id": params["chat_id"],
            "message_id": params["message_id"],
            "media": {k: v for k, v in {
                "type": "document" if as_file else "photo",
                "media": "attach://media",
                "caption": params.get("caption"),
                "parse_mode": params.get("parse_mode"),
                "show_caption_above_media": params.get("show_caption_above_media")
            }.items() if v}
        }

        b = utils.images_to_bytes(IMAGE, format)

        files = {"media": (name, b, utils.guess_mimetype(name))}

        message = bot("editMessageMedia", params=_params, files=files)

        return message, message["message_id"], trigger

class EditMessageVideo(SendGeneric):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": ("TELEGRAM_BOT", {"forceInput": True}),
                "chat_id": ("INT", {"forceInput": True}),
                "message_id": ("INT", {"forceInput": True}),
                "video": ("VHS_FILENAMES", {"forceInput": True}),
                "caption": ("STRING", {"multiline": True, "default": ""}),
                "parse_mode": (["None", "HTML", "Markdown", "MarkdownV2"], {}),
                "show_caption_above_media": ("BOOLEAN", {"default": False}),
                "send_as": (["Animation", "Video", "File"], {}),
            },
            "optional": {
                "trigger": ("*", {"forceInput": True})
            }
        }
    
    CATEGORY = f"{_CATEGORY}/edit"
    FUNCTION = "edit_message_video"

    def edit_message_video(self, bot: TelegramBot, video, send_as, trigger=None, **params):
        if params["parse_mode"] == "None":
            params.pop("parse_mode")

        file_path = [v for v in video[1] if not v.endswith(".png")][0]
        file_name = file_path.rsplit("/", 1)[-1]

        if send_as == "File":
            send_as = "Document"

        id = send_as.lower()
        
        _params = {
            "chat_id": params["chat_id"],
            "message_id": params["message_id"],
            "media": {k: v for k, v in {
                "type": id,
                "media": "attach://media",
                "caption": params.get("caption"),
                "parse_mode": params.get("parse_mode"),
                "show_caption_above_media": params.get("show_caption_above_media")
            }.items() if v}
        }

        with open(file_path, "rb") as f:
            files = {"media": (file_name, f.read(), utils.guess_mimetype(file_name))}
            message = bot("editMessageMedia", params=_params, files=files)
            return message, message["message_id"], trigger

class EditMessageAudio(SendGeneric):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": ("TELEGRAM_BOT", {"forceInput": True}),
                "chat_id": ("INT", {"forceInput": True}),
                "message_id": ("INT", {"forceInput": True}),
                "audio": ("AUDIO", {"forceInput": True}),
                "caption": ("STRING", {"multiline": True, "default": ""}),
                "parse_mode": (["None", "HTML", "Markdown", "MarkdownV2"], {}),
                "show_caption_above_media": ("BOOLEAN", {"default": False}),
                "file_name": ("STRING", {"default": "audio"}),
                "as_file": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "trigger": ("*", {"forceInput": True})
            }
        }
    
    CATEGORY = f"{_CATEGORY}/edit"
    FUNCTION = "edit_message_audio"

    def edit_message_audio(self, bot: TelegramBot, audio, file_name, as_file, trigger=None, **params):
        if params["parse_mode"] == "None":
            params.pop("parse_mode")
        
        ext = "wav" if as_file else "mp3"
        
        name = f"{file_name}.{ext}"

        _params = {
            "chat_id": params["chat_id"],
            "message_id": params["message_id"],
            "media": {k: v for k, v in {
                "type": "document" if as_file else "audio",
                "media": "attach://media",
                "caption": params.get("caption"),
                "parse_mode": params.get("parse_mode"),
                "show_caption_above_media": params.get("show_caption_above_media")
            }.items() if v}
        }

        b = utils.audio_to_wav_bytes(audio)
        if not as_file:
            b = utils.convert_wav_bytes_ffmpeg(b)

        files = {"media": (name, b, utils.guess_mimetype(name))}

        message = bot("editMessageMedia", params=_params, files=files)

        return message, message["message_id"], trigger

class SendChatAction:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot": ("TELEGRAM_BOT", {"forceInput": True}),
                "chat_id": ("INT", {"forceInput": True}),
                "action": ([
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
                ], {}),
            },
            "optional": {
                "trigger": ("*", {"forceInput": True})
            }
        }
    
    RETURN_TYPES = ("BOOL", "*")
    RETURN_NAMES = ("True", "trigger")

    FUNCTION = "send_chat_action"
    CATEGORY = _CATEGORY

    def send_chat_action(self, bot: TelegramBot, trigger=None, **params):
        result = bot("sendChatAction", params=params)
        return result, trigger

