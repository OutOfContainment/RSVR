import os


class Status:
    # Player can have 5 states:
    #  - idle
    #  - playing
    #  - playing [ paused ]
    #  - recording
    #  - recording [ paused ]

    # We can determine these states using booleans:
    recording = False
    playing = False
    paused = False

    # For example,
    #  !Status.recording && !Status.playing && !Status.paused
    # means that current state is 'idle'

    curTrackAmount = 0
    curTrack = 0

    def __init__(self):
        if os.path.exists("records"):
            # Look up previous records
            for i in range(1, 10000):
                if os.path.exists(f"records/recording_{i}.wav"):
                    continue
                else:
                    Status.curTrackAmount = i-1
                    Status.curTrack = i-1
                    print("Found", Status.curTrackAmount, "records in current path")
                    break
        else:
            os.mkdir("records")


    def trackRemove():
        if os.path.exists(f"records/recording_{Status.curTrack}.wav"):
            os.remove(f"records/recording_{Status.curTrack}.wav")

            for i in range(Status.curTrack, Status.curTrackAmount):
                os.rename(f"records/recording_{i+1}.wav", f"records/recording_{i}.wav")

        else:
            print("### curTrack remove error!")
