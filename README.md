# ComfyUI Telegram Suite

**Implement Telegram into your ComfyUI workflows.**

> Requires `ffmpeg`!

## Nodes

<details><summary>Telegram Bot
</summary>
This Node is to load a Bot and an optional default chat.   

You can configure this in `ComfyUI/user/default/telegram-suite/config.json`.

---
</details>

<details><summary>Send Message
</summary>
This Node is to send a text message.

---
</details>

<details><summary>Send Image(s)
</summary>
This Node is to send Images.


---
</details>

<details><summary>Send Video
</summary>
Test
</details>

<details><summary>Send Audio
</summary>
Test
</details>

<details><summary>Send Chat Action
</summary>
Test
</details>

>**Note:**  
>The optional `trigger` inputs and outputs are there to force things to happen in the order you want.  


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
<img src="https://github.com/SwissCore92/comfyui-telegram-suite/blob/master/screenshots/trigger_example_tts.png">
