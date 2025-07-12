# ComfyUI Telegram Suite

**Implement Telegram into your ComfyUI workflows.**



## Nodes

The main nodes:  
<img src="https://github.com/SwissCore92/comfyui-telegram-suite/blob/master/screenshots/main_nodes.png" alt="screenshots/main_nodes.png">

<details><summary>Telegram Bot
</summary>
This node loads your Telegram bot and (optionally) sets a default chat.  

You can configure it via: `ComfyUI/user/default/telegram-suite/config.json`
</details>

<details><summary>Send Message
</summary>
This node just sends a simple text message.
</details>

<details><summary>Send Image(s)
</summary>
This node sends one or more (up to 10) images.  

* If the `IMAGE` input contains multiple images and `group` is set to `True`, they’ll be sent as a media group.
* If `group` is False, the images will be sent individually.
* If `send_as_file` is `True`, the images will be sent as files instead of inline media.

> Note:  
> Only the `message(_id)` of the last sent image will be returned to the output.
</details>

<details><summary>Send Video
</summary>
This node sends a video file.

* The video input must be of type `VHS_FILENAMES` (e.g., from the `Filenames` output of the ***Video Combine*** node in the ***Video Helper Suite***).

The video can be sent as a regular video, an animation, or a file.
</details>

<details><summary>Send Audio
</summary>
This node sends an audio file.

* Can be sent as an audio message, voice message, or file.
</details>

<details><summary>Send Chat Action
</summary>
This node sends chat actions like “typing...”, “uploading X...”, or “recording X...”.  

⚠️ This is not an output node, so the trigger passthrough **is required** for this node to work.
</details>

Additional nodes include message editing, experimental features, and various type converters (see [Triggers](#triggers)).

## Installation

> **Note:** Requires `ffmpeg`!

### Step 1:

Install via `ComfyUI Manager` (and skip to [Step 2](#step-2)) or execute the following commands:

>⚠️ Ensure your ComfyUI virtual environment is activated and you're in the `ComfyUI/custom_nodes` directory.

```sh
git clone https://github.com/SwissCore92/comfyui-telegram-suite.git
cd comfyui-telegram-suite
pip install -r requirements.txt
```

### Step 2: 
Restart ComfyUI.

### Step 3: 
Add your bot(s) and chat(s) to the config file. 

* Open: `ComfyUI/user/default/telegram-suite/config.json`.  
* Add your *bot token(s)* under `"bots"`.  
* Add your *chat ID(s)* under `"chats"`.  

Example:
```json
{
    "bots": {
        "MyCoolBot": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
        "MyOtherCoolBot": "654321:CBA-DEF1234ghIkl-zyx57W2v1u123ew11"
    },
    "chats": {
        "MyPrivateChat": 567891234,
        "MyGroupChat": -1012345678
    }
}
```
> Use any string as the key for `"bots"` and "`chats"` — I like to use the Telegram @`username` for clarity.

### Step 4:
Restart ComfyUI again — and you're good to go!

## Triggers

The optional `trigger` inputs/outputs are used to enforce execution order in your workflow.

ComfyUI runs by evaluating output nodes and working backward to resolve dependencies. I like to think of it as the inputs "pulling" the values they need from connected outputs.

The trigger passthrough ensures a node executes at a specific point during the workflow. Here's an example using F5-TTS:

<img src="https://github.com/SwissCore92/comfyui-telegram-suite/blob/master/screenshots/trigger_example_tts.png" alt="screenshots/trigger_example_tts.png">

This flow sends the `recording_voice` chat action before generating the audio with the F5-TTS node. Once audio is generated, it's sent to the chat.

> The seed is required by the `F5-TTS Audio` node, so the `Send Chat Action` node ***must*** execute first.

You can use almost any type as a trigger. However, since ComfyUI has strict type checking, you'll need to:

* Convert the signal to ANY before feeding it into the trigger input.
* Convert it back to the original type after the trigger output.

*Yes, it's a bit clunky — but it’s the only reliable way I’ve found to control execution order. That’s also why the `converter` category has so many nodes.*

## To Do
- [ ] Improve documentation 
- [x] Add `Edit Message Video` node
- [x] Add `Edit Message Audio` node
- [ ] Wait for feedback to refine this list