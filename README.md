This is an inference plugin for Atlas IDS.
It subscribes to get nfstream flows from the related extension, piles up a batch of flows, then provide a prediction to the reporting extension through Redis.

Installation
------------

Clone this repository or add it using Atlas command

    atlas feature https://github.com/sooualil/atlas-ml-inference-extension.git ml_inference
