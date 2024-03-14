import threading
import time
import wave
import tkinter as tk
from tkinter import ttk

from status import Status
from audio import Sound


class GUI:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("RSDE [python]")
        self.win.resizable(False, False)

        self.screen = ttk.Frame(self.win)

        self.timer = tk.Label(self.screen,
                              text="😴",
                              font=("Roboto", 16))
        self.trackDisplay = tk.Label(self.screen,
                                     text=f"{Status.curTrack}/{Status.curTrackAmount}",
                                     font=("Roboto", 16))

        self.buttonsTop = ttk.Frame(self.win)

        self.stopButton = tk.Button(self.buttonsTop, text="⏹", state="disabled",
                                    font=("Roboto", 24, "bold"),
                                    command=self.stopClick)
        self.playButton = tk.Button(self.buttonsTop, text="⏵", state="disabled",
                                    font=("Roboto", 24, "bold"),
                                    command=self.playClick)
        self.recButton = tk.Button(self.buttonsTop, text="⏺",
                                   font=("Roboto", 24, "bold"),
                                   command=self.recClick)
        self.pauseButton = tk.Button(self.buttonsTop, text="⏸", state="disabled",
                                     font=("Roboto", 24, "bold"),
                                     command=self.pauseClick)

        self.buttonsLow = ttk.Frame(self.win)
        self.prevButton = tk.Button(self.buttonsLow, text='⏮', state="disabled",
                                    font=("Roboto", 16, "bold"),
                                    command=self.prevClick)
        self.removeButton = tk.Button(self.buttonsLow, text='🗑️', state="disabled",
                                      font=("Roboto", 16, "bold"),
                                      command=self.removeClick)
        self.nextButton = tk.Button(self.buttonsLow, text='⏭', state="disabled",
                                    font=("Roboto", 16, "bold"),
                                    command=self.nextClick)

        # Button status init
        if Status.curTrackAmount != 0:
            self.playButton["state"] = "normal"
            self.removeButton["state"] = "normal"
        if Status.curTrack >= 2:
            self.prevButton["state"] = "normal"

        # Layout
        self.screen.pack(side="top", expand=True, fill='x')
        self.buttonsLow.pack(side="bottom")
        self.buttonsTop.pack(side="bottom")

        self.timer.pack(side="left", expand=True)
        self.trackDisplay.pack(side="right", expand=False)

        self.stopButton.grid(row=0, column=1)
        self.playButton.grid(row=0, column=2)
        self.recButton.grid(row=0, column=3)
        self.pauseButton.grid(row=0, column=4)

        self.prevButton.grid(row=0, column=0)
        self.removeButton.grid(row=0, column=1)
        self.nextButton.grid(row=0, column=2)

        self.win.mainloop()

    def displayUpdate(self):
        self.trackDisplay.config(text=f"{Status.curTrack}/{Status.curTrackAmount}")

    def timerDisplay(self):
        startTS = time.time()
        timePaused = 0
        while Status.recording:
            while Status.paused:
                self.timer.config(fg="gray")
                timePaused += 0.01
                time.sleep(0.01)
            timePassed = time.time() - startTS - timePaused
            sec = timePassed % 60
            min = timePassed // 60
            hours = min // 60

            self.timer.config(fg="red",
                 text=f"⏺ {int(hours):02d}:{int(min):02d}:{int(sec):02d}")

        if Status.playing:
            with wave.open(f"records/recording_{Status.curTrack}.wav", 'rb') as wf:
                while Status.playing:
                    while Status.paused:
                        self.timer.config(fg="gray")
                        timePaused += 0.01
                        time.sleep(0.01)

                    frames = wf.getnframes()
                    recTime = frames / Sound.RATE

                    timeToPass = recTime - (time.time() - startTS - timePaused)
                    sec = timeToPass % 60
                    min = timeToPass // 60
                    hours = min // 60
                    self.timer.config(fg="green",
                         text=f"⏵ {int(hours):02d}:{int(min):02d}:{int(sec):02d}")

            self.stopButton["state"] = "disabled"
            self.playButton["state"] = "normal"
            self.recButton["state"] = "normal"
            self.pauseButton["state"] = "disabled"

        self.timer.config(text="😴", fg="black")

    # Buttons func
    def stopClick(self):
        print("GUI: stopClick")
        if Status.recording and not Status.playing:
            Status.recording = False
            Status.paused = False
            print("Status: recording -> idle")
            Status.curTrack += 1
            Status.curTrackAmount += 1

            self.stopButton["state"] = "disabled"
            self.playButton["state"] = "normal"
            self.recButton["state"] = "normal"
            self.pauseButton["state"] = "disabled"
            self.removeButton["state"] = "normal"

            if Status.curTrack > 1:
                self.prevButton["state"] = "normal"

            self.displayUpdate()

        elif not Status.recording and Status.playing:
            Status.playing = False
            Status.paused = False
            print("Status: playing -> idle")
            self.stopButton["state"] = "disabled"
            self.playButton["state"] = "normal"
            self.pauseButton["state"] = "disabled"
        else:
            print("### Stop button error! ###")

    def playClick(self):
        print("GUI: playClick")
        if not Status.recording and not Status.playing and not Status.paused:
            Status.playing = True
            print("Status: idle -> playing")
            self.stopButton["state"] = "normal"
            self.playButton["state"] = "disabled"
            self.recButton["state"] = "disabled"
            self.pauseButton["state"] = "normal"
            threading.Thread(target=self.timerDisplay).start()
            threading.Thread(target=Sound.play).start()
        else:
            print("### Play button error! ###")

    def recClick(self):
        print("GUI: recClick")
        if not Status.recording and not Status.playing and not Status.paused:
            Status.recording = True
            print("Status: idle -> recording")
            self.stopButton["state"] = "normal"
            self.playButton["state"] = "disabled"
            self.recButton["state"] = "disabled"
            self.pauseButton["state"] = "normal"

            threading.Thread(target=self.timerDisplay).start()
            threading.Thread(target=Sound.record).start()
        else:
            print("### Record button error! ###")

    def pauseClick(self):
        print("GUI: pauseClick")
        if Status.paused:
            print("Status: unpaused -> paused")
            Status.paused = False
        elif not Status.paused:
            Status.paused = True
            print("Status: paused -> unpaused")
        else:
            print("### Pause button error! ###")

    def prevClick(self):
        print("GUI: prevClick")
        Status.curTrack -= 1
        self.displayUpdate()
        if Status.curTrack == 1:
            self.prevButton["state"] = "disabled"
        if self.nextButton["state"] == "disabled":
            self.nextButton["state"] = "normal"

    def removeClick(self):
        Status.trackRemove()
        Status.curTrackAmount -= 1
        if Status.curTrack > 1 or Status.curTrackAmount == 0:
            Status.curTrack -= 1
            if Status.curTrackAmount == 0:
                self.playButton["state"] = "disabled"
                self.removeButton["state"] = "disabled"
            elif Status.curTrack == 1:
                self.prevButton["state"] = "disabled"
        elif Status.curTrack == Status.curTrackAmount:
            self.nextButton["state"] = "disabled"
            self.prevButton["state"] = "disabled"
        else:
            print("### Remove button error! ###")
        self.displayUpdate()

    def nextClick(self):
        print("GUI: nextClick")
        Status.curTrack += 1
        self.displayUpdate()
        if Status.curTrack == Status.curTrackAmount:
            self.nextButton["state"] = "disabled"
        if self.prevButton["state"] == "disabled":
            self.prevButton["state"] = "normal"
