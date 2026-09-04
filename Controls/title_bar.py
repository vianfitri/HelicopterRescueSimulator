"""
Helicopter Rescue Simulator - Custom Top Title Bar
Sleek tactical top bar displaying mission status, UTC Zulu time, and theme toggle controls.
"""
import datetime
import wx
from Assets.theme import Theme


class TitleBarControl(wx.Panel):
    """
    Compact modern title bar providing global status, clock, and theme mode toggle.
    """
    def __init__(self, parent, on_toggle_theme=None):
        super().__init__(parent, id=wx.ID_ANY, size=(-1, 46), style=wx.NO_BORDER)
        self.on_toggle_theme = on_toggle_theme
        self.SetBackgroundColour(Theme.BG_HEADER)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.SetDoubleBuffered(True)
        
        self.Bind(wx.EVT_PAINT, self._on_paint)
        self.Bind(wx.EVT_WINDOW_DESTROY, self._on_destroy)
        
        # Clock timer (updates UTC clock every second)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self._on_timer, self.timer)
        self.timer.Start(1000)
        
        self._init_ui()

    def _on_destroy(self, event):
        if hasattr(self, 'timer') and self.timer.IsRunning():
            self.timer.Stop()
        event.Skip()

    def _init_ui(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Left Safety Orange Accent Pip
        accent_pip = wx.Panel(self, size=(4, 24), style=wx.NO_BORDER)
        accent_pip.SetBackgroundColour(Theme.ACCENT_ORANGE)
        sizer.Add(accent_pip, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 16)
        
        # Title Label
        title_lbl = wx.StaticText(self, label="HELICOPTER RESCUE SIMULATOR")
        title_lbl.SetForegroundColour(Theme.TEXT_PRIMARY)
        title_lbl.SetFont(Theme.get_font(size=10, bold=True))
        sizer.Add(title_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        
        # Mode Tag
        tag_lbl = wx.StaticText(self, label="TACTICAL COMMAND DISPATCH")
        tag_lbl.SetForegroundColour(Theme.TEXT_MUTED)
        tag_lbl.SetFont(Theme.get_mono_font(size=8))
        sizer.Add(tag_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 12)
        
        # Stretch spacer pushing status indicators to the right
        sizer.AddStretchSpacer(1)
        
        # SATCOM Status
        sat_lbl = wx.StaticText(self, label="SATCOM: LINKED [99.8%]")
        sat_lbl.SetForegroundColour(Theme.STATUS_CYAN)
        sat_lbl.SetFont(Theme.get_mono_font(size=8, bold=True))
        sizer.Add(sat_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 18)
        
        # Alert Badge Panel
        alert_badge = wx.Panel(self, style=wx.NO_BORDER)
        alert_badge.SetBackgroundColour(Theme.BG_CARD)
        alert_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        dot = wx.StaticText(alert_badge, label="●")
        dot.SetForegroundColour(Theme.ACCENT_ORANGE)
        dot.SetFont(Theme.get_font(size=9, bold=True))
        alert_sizer.Add(dot, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 8)
        
        alert_text = wx.StaticText(alert_badge, label="SAR ALERT: LEVEL 1 ACTIVE")
        alert_text.SetForegroundColour(Theme.TEXT_PRIMARY)
        alert_text.SetFont(Theme.get_font(size=8, bold=True))
        alert_sizer.Add(alert_text, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 8)
        
        alert_badge.SetSizer(alert_sizer)
        sizer.Add(alert_badge, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 16)
        
        # Theme Toggle Button
        theme_btn_label = "☀️ LIGHT" if Theme.is_dark else "🌙 DARK"
        self.theme_btn = wx.Button(self, label=theme_btn_label, size=(78, 28))
        self.theme_btn.SetBackgroundColour(Theme.BG_CARD)
        self.theme_btn.SetForegroundColour(Theme.TEXT_PRIMARY)
        self.theme_btn.SetFont(Theme.get_font(size=8, bold=True))
        self.theme_btn.Bind(wx.EVT_BUTTON, self._on_theme_btn_click)
        sizer.Add(self.theme_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 16)
        
        # Zulu Time Display
        self.time_lbl = wx.StaticText(self, label=self._get_zulu_time())
        self.time_lbl.SetForegroundColour(Theme.TEXT_PRIMARY)
        self.time_lbl.SetFont(Theme.get_mono_font(size=9, bold=True))
        sizer.Add(self.time_lbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 18)
        
        self.SetSizer(sizer)

    def _on_theme_btn_click(self, event):
        if self.on_toggle_theme:
            self.on_toggle_theme()

    def _get_zulu_time(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        return now.strftime("%H:%M:%S UTC")

    def _on_timer(self, event):
        self.time_lbl.SetLabel(self._get_zulu_time())
        self.Layout()

    def _on_paint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        w, h = self.GetClientSize()
        # Bottom border
        dc.SetPen(wx.Pen(Theme.BORDER_SUBTLE, 1))
        dc.DrawLine(0, h - 1, w, h - 1)
