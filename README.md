# ComfyUI Telegram Suite

**Implement Telegram into your ComfyUI workflows.**



## Nodes

The main nodes:  
<img src="https://github.com/SwissCore92/comfyui-telegram-suite/blob/master/screenshots/main_nodes.png" alt="screenshots/main_nodes.png">

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

The `video` input expects a `VHS_FILENAMES` type (The `Filenames` outupt of the `Video Combine` node (Video Helper Suite)).

The video can be sent as video, animation or file.
</details>

<details><summary>Send Audio
</summary>
This Node is to send an audio. 

The audio can be sent as audio, voice, or file. 
</details>

<details><summary>Send Chat Action
</summary>
This Node is to send chat actions.

Note: This is **no output node**.
</details>

There are also some nodes to edit messages, some experimental nodes and a lot of converter nodes (see [Triggers](#triggers)).

## Installation

> **Note:** Requires `ffmpeg`!

### Step 1:

Install via `ComfyUI Manager` (and skip to [Step 2](#step-2)) or execute the following commands:

>⚠️ Make sure your ComfyUI virtual environment is activated and you are in the ComfyUI/custom_nodes directory!

```sh
git clone https://github.com/SwissCore92/comfyui-telegram-suite.git
cd comfyui-telegram-suite
pip install -r requirements.txt
```

### Step 2: 
Restart ComfyUI.

### Step 3: 
Add your bot(s) and chat(s) to the config file. 

* Open the `ComfyUI/user/default/telegram-suite/config.json` file.  
* Add your *bot token(s)* to `"bots"`.  
* Add your *chat id(s)* to `"chats"`.  

The file should look something like this:
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
> You can use any String as key value for both `"bots"` and `"chats"`.  
Just use a name you can recognize. I like to use the telegram @`username`.

### Step 4:
Restart ComfyUI again. -> Have fun!

## Triggers

The optional `trigger` inputs and outputs are there to force things to happen in the order you want. 

ComfyUI works by looking for output nodes and executes backwards to ensure all input nodes have executed (and so forth). I like to imagine that node inputs kind of "pull" the needed value out of the connected output. Traversing from end to start. The trigger passthrough ensures the node to be executed in a specific point during the workflow execution proccess.

Here is an Example of a F5-TTS workflow sending the Chat Action *recoring_voice* to the chat, before the TTS Node starts to generate ("record") the audio. After the F5-TTS node is done, the Audio will be sent to the chat. 

<img src="https://github.com/SwissCore92/comfyui-telegram-suite/blob/master/screenshots/trigger_example_tts.png" alt="screenshots/trigger_example_tts.png">

> The seed is required by the F5-TTS node, so the `Send Chat Action` node **must** be executed first. 

You can use almost any type as Trigger. The downside is that the signal must be converted to `ANY` before going into the `trigger` input and back to the original type after coming out from the `trigger` output (See example above using an `INT` signal as trigger - the seed).  
*I know this is a little bit clunky but I could not figure out another way to enforce keeping things happening in the order i want. ComfyUI typecking is very strict.*  
This is why there are so many nodes in the `converter` category.

## To Do
- [ ] Improve Docs 
- [x] Add `Edit Message Video` Node
- [x] Add `Edit Message Audio` Node
- [ ] Wait for feedback to update the Todo list