from colorama import Fore

from .nodes import telegram 
from .nodes import utils
from .nodes import converters

NODE_CLASS_MAPPINGS = {
    f"TelegramSuite_{k}": v for k, v in {
        "TelegramBot": telegram.TelegramBot,
        "APIMethod": telegram.APIMethod,
        "SendMessage": telegram.SendMessage,
        "SendImage": telegram.SendImage,
        "SendVideo": telegram.SendVideo,
        "SendAudio": telegram.SendAudio,
        "SendChatAction": telegram.SendChatAction,

        "EditMessageText": telegram.EditMessageText,
        "EditMessageCaption": telegram.EditMessageCaption,
        "EditMessageImage": telegram.EditMessageImage,
        "EditMessageVideo": telegram.EditMessageVideo,
        "EditMessageAudio": telegram.EditMessageAudio,

        "ParseJSON": utils.ParseJSON,
        
        **converters.type_mapping
    }.items()
}

NODE_DISPLAY_NAME_MAPPINGS = {
    f"TelegramSuite_{k}": f"{v} 🔽" for k, v in {
        "TelegramBot": "Telegram Bot",
        "APIMethod": "API Method",
        "SendMessage": "Send Message",
        "SendImage": "Send Image(s)",
        "SendVideo": "Send Video",
        "SendAudio": "Send Audio",
        "SendChatAction": "Send Chat Action",

        "EditMessageText": "Edit Message Text",
        "EditMessageCaption": "Edit Message Caption",
        "EditMessageImage": "Edit Message Image",
        "EditMessageVideo": "Edit Message Video",
        "EditMessageAudio": "Edit Message Audio",

        "ParseJSON": "Parse JSON",

        **converters.name_mapping
    }.items()
}

CUSTOM_NODE_INPUT_TYPES = {
    "TELEGRAM_BOT": telegram.TelegramBot,
    "MESSAGES": list[dict],
    "MESSAGE_IDS": list[int],
}

__all__ = (
    "NODE_CLASS_MAPPINGS", 
    "NODE_DISPLAY_NAME_MAPPINGS", 
    "CUSTOM_NODE_INPUT_TYPES",
)

print(f"\n{Fore.LIGHTCYAN_EX}[Telegram Suite 🔽] {len(NODE_CLASS_MAPPINGS)} nodes loaded!{Fore.RESET}\n")
