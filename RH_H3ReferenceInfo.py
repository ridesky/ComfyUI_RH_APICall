"""Build nodeInfoList entries for the supplied MiniMax H3 RunningHub graph.

Media uploads are performed by the existing ComfyUI_RH_APICall uploader
nodes. This node only maps the resulting RunningHub filenames to the cloud
workflow's fixed node IDs and skips every empty optional slot.
"""


class RH_H3ReferenceInfo:
    IMAGE_NODE_IDS = (452, 453, 454, 467, 468, 469, 470, 471, 472)
    # The H3 graph maps ref_video_0 to LoadVideo node 630 and ref_video_1 to 623.
    VIDEO_NODE_IDS = (630, 623)
    AUDIO_NODE_IDS = (475, 476, 477)

    @classmethod
    def INPUT_TYPES(cls):
        optional = {}
        for i in range(1, len(cls.IMAGE_NODE_IDS) + 1):
            optional[f"image_{i}"] = ("STRING", {"default": ""})
        for i in range(1, len(cls.VIDEO_NODE_IDS) + 1):
            optional[f"video_{i}"] = ("STRING", {"default": ""})
        for i in range(1, len(cls.AUDIO_NODE_IDS) + 1):
            optional[f"audio_{i}"] = ("STRING", {"default": ""})

        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
            },
            "optional": optional,
        }

    RETURN_TYPES = ("ARRAY",)
    RETURN_NAMES = ("nodeInfoList",)
    FUNCTION = "build"
    CATEGORY = "RunningHub"

    def build(self, prompt="", **media):
        entries = [{
            "nodeId": 138,
            "fieldName": "value",
            "fieldValue": str(prompt or ""),
        }]

        for kind, node_ids, field_name in (
            ("image", self.IMAGE_NODE_IDS, "image"),
            ("video", self.VIDEO_NODE_IDS, "file"),
            ("audio", self.AUDIO_NODE_IDS, "audio"),
        ):
            for index, node_id in enumerate(node_ids, start=1):
                filename = media.get(f"{kind}_{index}")
                if filename is None:
                    continue
                filename = str(filename).strip()
                if not filename:
                    continue
                entries.append({
                    "nodeId": node_id,
                    "fieldName": field_name,
                    "fieldValue": filename,
                })

        return (entries,)
