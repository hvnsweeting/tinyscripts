#!/bin/bash
# play a random song with duration < 10 mins in your ~/Music
# requires: ffmpeg
# tested on OSX 10.10.5
# Viet Hung Nguyen <hvn@familug.org>

for i in {1..3}; do
    music_file=$(find Music/ -name '*.mp3' | python -c "import random, sys; print(random.choice(sys.stdin.readlines()))")
    printf "Got file ${music_file}\n"
    # music file shorter than 10 mins
    file_duration=$(ffmpeg -i "${music_file}" 2>&1 | grep Duration | cut -d ' ' -f4 | tr -d ',' | tr -d ':')
    printf "Length: ${file_duration}\n"
    if [ $(echo "${file_duration} < 1000" | bc) = 1 ]; then
        printf "Playing ${music_file}\n"
        afplay "${music_file}"
        exit 0
    fi
done
echo "Oops, picked 3 long audio files. Have a good day!"
