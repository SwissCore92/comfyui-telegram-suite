# ComfyUI Telegram Suite

**Implement Telegram into your ComfyUI workflows.**

> Requires `ffmpeg`!

## Nodes

<img src="https://github.com/SwissCore92/comfyui-telegram-suite/blob/master/screenshots/main_nodes.png" alt="main_nodes">

<details><summary>Telegram Bot
</summary>
This Node is to load a Bot and an optional default chat.   

You can configure this in `ComfyUI/user/default/telegram-suite/config.json`.
</details>

<details><summary>Send Message
</summary>
This Node is to send a text message. 

Nothing special to say about this node.
</details>

<details><summary>Send Image(s)
</summary>
This Node is to send one or multiple Images.  

If the `IMAGE` input contains multiple images and `group` is set to True, the images are sent as media group. Else, the images are sent one by one.  

If `send_as_file` is True, the image(s) will be sent as file(s).

**Note:**  
*If multiple messages are sent, only the `message(_id)` of the **last** sent message wil be returned to the output.*
</details>

<details><summary>Send Video
</summary>
This Node is to send a video. 
</details>

<details><summary>Send Audio
</summary>
This Node is to send an audio. 
</details>

<details><summary>Send Chat Action
</summary>
This Node is to send chat actions. 
</details>

## Installation

### Step 1:
Open a terminal in you *ComfyUI* directory.  
> **⚠️ Make sure your ComfyUI virtual environment is activated**!

```sh
cd custom_nodes
git clone https://github.com/SwissCore92/comfyui-telegram-suite.git
cd comfyui-telegram-suite
pip install -r requirements.txt
```

### Step 2: 
Restart ComfyUI

### Step 3: 
Go to `ComfyUI/user/default/telegram-suite`.  
There should be a `config.json` file.  
Add your bot(s) token(s) to `"bots"`.
Add your chat id(s) to `"chats"`.
eg.
```python
{
    "bots": {
        "MyCoolBot": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
        "MyOtherCoolBot": "654321:CBA-DEF1234ghIkl-zyx57W2v1u123ew11"
    },
    "chats" {
        "MyPrivateChat": 567891234,
        "MyGroupChat": -1012345678
    }
}
```

### Step 4:
Restart ComfyUI again.  

Have fun!

## Triggers

The optional `trigger` inputs and outputs are there to force things to happen in the order you want. 

Here is an Example of a F5-TTS workflow sending the Chat Action *recoring_voice* to the chat, before the TTS Node starts to generate ("record") the audio. After the F5-TTS node is done, the Audio will be sent to the chat. 

<img src="https://github.com/SwissCore92/comfyui-telegram-suite/blob/master/screenshots/trigger_example_tts.png" alt="trigger_example_tts">

You can use almost any type as Trigger. The downside is that the signal must be converted to `ANY` before going into the `trigger` input and back to the original type after coming out from the `trigger` output (See example above using an `INT` signal as trigger - the seed).  
*I know this is a little bit clunky but I could not figure out another way to enforce kepping things in sync.*  
This is why there are so many nodes in the `converter` category.

