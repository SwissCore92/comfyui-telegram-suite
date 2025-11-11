import io
import os
import mimetypes
import json
import subprocess
from typing import TypedDict, Any
from pathlib import Path

import torchaudio
import numpy as np
from PIL import Image

UINT64_MIN = -9223372036854775808
UINT64_MAX = 9223372036854775807

USER_DIR = Path(os.getcwd()) / "user" / "default"

_CATEGORY = "Telegram Suite 🔽/experimental"

class Config(TypedDict):
    bots: dict[str, str]
    chats: dict[str, int]

def load_config() -> Config:
    tg_dir = USER_DIR / "telegram-suite"
    if not tg_dir.exists():
        tg_dir.mkdir(parents=True)
    config_path = tg_dir / "config.json"
    if not config_path.exists():
        cfg = {
            "bots": {
                "<YourBotName>": "<YourToken>"
            }, 
            "chats": {
                "<YourChatName>": 0
            }
        }
        write_json(config_path, cfg)
        print(f"You need to add a bot to the config file at {config_path}.")
        return cfg # type: ignore
        
    return read_json(config_path) # type: ignore


def cleanup_params(params: dict[str, Any]) -> dict[str, Any]:
    if params.get("parse_mode") == "None":
        params.pop("parse_mode")

    if params.get("message_thread_id") and params["message_thread_id"] < 0:
        params.pop("message_thread_id")

    return params

def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def write_json(path: Path, data: dict, *, indent=4) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)

def guess_mimetype(file_name: str) -> str:
    return mimetypes.guess_type(file_name)[0] or "application/octet-stream"

def images_to_bytes(images, format="PNG") -> list[bytes]:
    bytes_images = [] 
    for image in images:
        i = 255. * image.cpu().numpy()
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
        buf = io.BytesIO()
        img.save(buf, format=format)
        b = buf.getvalue()
        buf.close()
        bytes_images.append(b)

    return bytes_images

def audio_to_wav_bytes(audio, format="WAV") -> bytes:
    waveform = audio['waveform'].squeeze()
    if waveform.ndim == 1:
        waveform = waveform.unsqueeze(0)

    sample_rate = audio.get("sample_rate", 44100)

    buf = io.BytesIO()
    torchaudio.save(buf, waveform, sample_rate, format="wav") # type: ignore
    buf.seek(0)
    b = buf.getvalue()
    buf.close()
    return b

def convert_wav_bytes_ffmpeg(input_bytes: bytes, output_format: str = "mp3") -> bytes:
    cmd = [
        "ffmpeg", 
        "-y",  
        "-f", "wav", 
        "-i", "pipe:0", 
        # "-f", output_format, 
        "-f", "opus" if output_format == "ogg" else output_format, #TODO: test (using libopus)
        "pipe:1"
    ]

    result = subprocess.run(
        cmd,
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg audio conversion failed: {result.stderr.decode()}")

    return result.stdout

class ParseJSON:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_string": ("STRING", {"multiline": True}),
            },
        }

    RETURN_TYPES = ("DICT",)
    RETURN_NAMES = ("DICT",)

    FUNCTION = "parse_json"
    CATEGORY = _CATEGORY
    
    def parse_json(self, json_string):
        return (json.loads(json_string),)

