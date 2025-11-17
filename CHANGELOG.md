## Changelog

### Version 1.0.4
* Added a changelog
* Local Telegram Bot API server support  
You can add your local bot api url to config.json `"api_url": <url>`
Just select the url to use in the `Telegram Bot` node
* No more `trigger` input converter node required  
The `<Type> To Any` nodes are still included for backward compatibility
* Added `has_spoiler` option to some nodes
* Added `message_thread_id` option to some nodes
* Telegram Bot now uses one-time sessions
* Added tooltips to all node inputs 