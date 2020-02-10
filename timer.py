import wx
import time 
import threading 

class TimerApp():

    start = 0
    timer = 0
    substract = 0
    default_time = "00:00:00.00"

    def __init__(self):
        
        start_thread = threading.Thread(target=self.start_timer, daemon=True)
        start_thread.start()

        self.frame = wx.Frame(parent=None, title="Timer", size=(300, 300),
            style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        panel = wx.Panel(self.frame)
        
        run_button = wx.Button(panel, label="Run", pos=(160, 50))
        run_button.Bind(wx.EVT_BUTTON, self.run)

        stop_button = wx.Button(panel, label="Pause", pos=(160, 90))
        stop_button.Bind(wx.EVT_BUTTON, self.pause)

        lap_button = wx.Button(panel, label="Lap", pos=(160, 130))
        lap_button.Bind(wx.EVT_BUTTON, self.lap)

        reset_button = wx.Button(panel, label="Reset", pos=(160, 170))
        reset_button.Bind(wx.EVT_BUTTON, self.reset)

        clear_button = wx.Button(panel, label="Clear", pos=(160, 210))
        clear_button.Bind(wx.EVT_BUTTON, self.clear)

        self.timer_box = wx.ListBox(panel, pos=(40, 50), size=(100, 190)) 

        self.timer_text = wx.StaticText(panel, label=self.default_time, pos=(85, 15))
        self.timer_text.SetFont(wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL))

        self.frame.Show()

    def run(self, event):
        if not self.start:
            self.start = 1
            if self.substract: 
                self.timer += time.perf_counter()-self.substract
            else:
                self.timer = time.perf_counter()

    def pause(self, event):
        if self.start: 
            self.start = 0
            self.substract = time.perf_counter()

    def lap(self, event): 
        self.timer_box.Append(self.timer_text.GetLabel())

    def reset(self, event):
        self.start = 0
        self.timer = 0
        self.substract = 0
        self.timer_text.SetLabel(self.default_time)

    def clear(self, event):
        self.timer_box.Clear()

    def get_time(self): 
        final = time.perf_counter()-self.timer
        hours, remaining = divmod(final, 3600)
        minutes, seconds = divmod(remaining, 60)
        return f"{int(hours):02}:{int(minutes):02}:{seconds:05.2f}"

    def start_timer(self):
        while True:
            time.sleep(0.01)
            while self.start:
                self.timer_text.SetLabel(self.get_time())
                time.sleep(0.01)

if __name__ == "__main__":
    app = wx.App()
    t = TimerApp()
    app.MainLoop()
