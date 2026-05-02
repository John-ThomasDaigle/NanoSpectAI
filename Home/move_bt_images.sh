#!/bin/bash
WATCH_DIR="$HOME/Downloads"
TARGET_DIR="$HOME/audio-transcription-using-openai-whisper/captured_images"

inotifywait -m -e close_write "$WATCH_DIR" |
while read dir event file; do
    if [[ "$file" =~ \.(jpg|jpeg|png|bmp)$ ]]; then
        mv "$WATCH_DIR/$file" "$TARGET_DIR/$file"
        echo "Moved: $file → $TARGET_DIR"
    fi
done
