# Mappings for raw tags to human-friendly names (extend as needed)

ID3V2_3_MAP = {
    "TIT2": "Title",
    "TPE1": "Artist",
    "TALB": "Album",
    "TCON": "Genre",
    "TRCK": "Track Number",
    "TYER": "Year",
    "TDRC": "Recording Time",
    "TPOS": "Part of Set",
    "TPE2": "Album Artist",
    "TPE3": "Conductor",
    "TPE4": "Remixed By",
    "TXXX": "User Defined Text",
    # (add more as needed)
}

def friendly_name(tag):
    return ID3V2_3_MAP.get(tag, tag)  # Default to the tag if no mapping exists
