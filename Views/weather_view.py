"""
Helicopter Rescue Simulator - Weather & Radar View
Simulated Doppler weather radar scope with dynamic sweep animation, METAR, and sea state analysis.
"""
import math
import wx
from Assets.theme import Theme


class RadarScopePanel(wx.Panel):
    """Owner-drawn circular Doppler radar display with rotating sweep line and targets."""
    def __init__(self, parent):
        super().__init__(parent, size=(380, 380), style=wx.NO_BORDER)
        self.SetBackgroundColour(Theme.BG_CARD)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.SetDoubleBuffered(True)
        
        self.sweep_angle = 0.0
        
        # Radar sweep animation timer (30 FPS)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self._on_timer, self.timer)
        self.timer.Start(33)
        
        self.Bind(wx.EVT_PAINT, self._on_paint)
        self.Bind(wx.EVT_WINDOW_DESTROY, self._on_destroy)

    def _on_destroy(self, event):
        if hasattr(self, 'timer') and self.timer.IsRunning():
            self.timer.Stop()
        event.Skip()

    def _on_timer(self, event):
        self.sweep_angle = (self.sweep_angle + 2.5) % 360.0
        self.Refresh()

    def _on_paint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        if not gc:
            return
            
        w, h = self.GetClientSize()
        cx, cy = w / 2.0, h / 2.0
        max_r = min(w, h) / 2.0 - 20.0
        
        # Background dark circular display
        gc.SetBrush(wx.Brush(wx.Colour(12, 16, 20)))
        gc.SetPen(wx.Pen(Theme.BORDER_SUBTLE, 1))
        gc.DrawEllipse(cx - max_r, cy - max_r, max_r * 2, max_r * 2)
        
        # Concentric Range Rings (10NM, 20NM, 30NM)
        gc.SetBrush(wx.NullBrush)
        gc.SetPen(wx.Pen(wx.Colour(30, 60, 70, 180), 1, wx.PENSTYLE_SHORT_DASH))
        for ring_fraction in [0.33, 0.66, 1.0]:
            r = max_r * ring_fraction
            gc.DrawEllipse(cx - r, cy - r, r * 2, r * 2)
            
        # Crosshair Azimuth lines
        gc.SetPen(wx.Pen(wx.Colour(30, 60, 70, 140), 1))
        gc.StrokeLine(cx - max_r, cy, cx + max_r, cy)
        gc.StrokeLine(cx, cy - max_r, cx, cy + max_r)
        
        # Cardinal direction labels
        gc.SetFont(Theme.get_mono_font(size=8, bold=True), Theme.STATUS_CYAN)
        gc.DrawText("N 360°", cx - 16, cy - max_r + 4)
        gc.DrawText("S 180°", cx - 16, cy + max_r - 18)
        gc.DrawText("E 090°", cx + max_r - 38, cy - 6)
        gc.DrawText("W 270°", cx - max_r + 6, cy - 6)
        
        # Simulated Storm Cells / Precipitation echoes (Translucent radar clusters)
        gc.SetPen(wx.NullPen)
        storm_brush = wx.Brush(wx.Colour(255, 94, 19, 90)) # Orange rain band
        gc.SetBrush(storm_brush)
        gc.DrawEllipse(cx - max_r * 0.7, cy - max_r * 0.4, 55, 38)
        
        storm_inner = wx.Brush(wx.Colour(250, 82, 82, 120)) # Red core
        gc.SetBrush(storm_inner)
        gc.DrawEllipse(cx - max_r * 0.62, cy - max_r * 0.35, 26, 18)
        
        # Active SAR Emergency Target Blip (Blinking / Glowing)
        target_x = cx + max_r * 0.45
        target_y = cy + max_r * 0.35
        gc.SetBrush(wx.Brush(Theme.STATUS_RED))
        gc.DrawEllipse(target_x - 4, target_y - 4, 8, 8)
        gc.SetPen(wx.Pen(Theme.STATUS_RED, 1))
        gc.SetBrush(wx.NullBrush)
        gc.DrawEllipse(target_x - 9, target_y - 9, 18, 18)
        gc.SetFont(Theme.get_mono_font(size=7, bold=True), Theme.STATUS_RED)
        gc.DrawText("MAYDAY [DISTRESS]", target_x + 12, target_y - 6)
        
        # Sweeping Radar Beam
        rad = math.radians(self.sweep_angle)
        sweep_end_x = cx + max_r * math.cos(rad)
        sweep_end_y = cy + max_r * math.sin(rad)
        
        sweep_pen = wx.Pen(Theme.STATUS_CYAN, 2)
        gc.SetPen(sweep_pen)
        gc.StrokeLine(cx, cy, sweep_end_x, sweep_end_y)
        
        # Center Helicopter position (White delta icon)
        gc.SetBrush(wx.Brush(Theme.TEXT_PRIMARY))
        gc.SetPen(wx.NullPen)
        heli_marker = gc.CreatePath()
        heli_marker.MoveToPoint(cx, cy - 7)
        heli_marker.AddLineToPoint(cx + 6, cy + 6)
        heli_marker.AddLineToPoint(cx, cy + 3)
        heli_marker.AddLineToPoint(cx - 6, cy + 6)
        heli_marker.CloseSubpath()
        gc.DrawPath(heli_marker)


class WeatherView(wx.Panel):
    """View presenting the real-time weather radar, sea conditions, and flight hazards."""
    def __init__(self, parent):
        super().__init__(parent, style=wx.NO_BORDER)
        self.SetBackgroundColour(Theme.BG_MAIN)
        self.SetDoubleBuffered(True)
        
        self._init_ui()

    def _init_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.AddSpacer(18)
        
        # Header
        header_sizer = wx.BoxSizer(wx.VERTICAL)
        title_lbl = wx.StaticText(self, label="DOPPLER WEATHER RADAR & METEOROLOGY")
        title_lbl.SetForegroundColour(Theme.TEXT_PRIMARY)
        title_lbl.SetFont(Theme.get_font(size=14, bold=True))
        header_sizer.Add(title_lbl, 0, wx.LEFT | wx.RIGHT, 24)
        
        sub_lbl = wx.StaticText(self, label="Live storm scanner, offshore maritime sea state, cloud ceilings, and METAR data.")
        sub_lbl.SetForegroundColour(Theme.TEXT_MUTED)
        sub_lbl.SetFont(Theme.get_font(size=9))
        header_sizer.Add(sub_lbl, 0, wx.LEFT | wx.RIGHT | wx.TOP, 24, 4)
        
        main_sizer.Add(header_sizer, 0, wx.EXPAND)
        main_sizer.AddSpacer(16)
        
        # Split: Left Radar Display (420px), Right Weather Readouts
        content_sizer = wx.BoxSizer(wx.HORIZONTAL)
        content_sizer.AddSpacer(24)
        
        # Left: Radar Panel Container
        radar_box = wx.Panel(self, style=wx.NO_BORDER)
        radar_box.SetBackgroundColour(Theme.BG_CARD)
        r_sizer = wx.BoxSizer(wx.VERTICAL)
        r_sizer.AddSpacer(14)
        
        r_hdr = wx.StaticText(radar_box, label="TACTICAL RADAR SWEEP (RANGE: 30 NM)")
        r_hdr.SetForegroundColour(Theme.ACCENT_ORANGE)
        r_hdr.SetFont(Theme.get_font(size=9, bold=True))
        r_sizer.Add(r_hdr, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, 10)
        
        self.radar_scope = RadarScopePanel(radar_box)
        r_sizer.Add(self.radar_scope, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 8)
        
        r_status = wx.StaticText(radar_box, label="SWEEP MODE: CONTINUOUS • TILT: -1.5° • GAIN: AUTO")
        r_status.SetForegroundColour(Theme.TEXT_MUTED)
        r_status.SetFont(Theme.get_mono_font(size=8))
        r_sizer.Add(r_status, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM | wx.TOP, 10)
        
        radar_box.SetSizer(r_sizer)
        content_sizer.Add(radar_box, 0, wx.EXPAND | wx.RIGHT, 18)
        radar_box.SetMinSize((420, -1))
        
        # Right: Meteorological Data & Flight Advisory
        weather_info = self._create_weather_info()
        content_sizer.Add(weather_info, 1, wx.EXPAND)
        
        content_sizer.AddSpacer(24)
        main_sizer.Add(content_sizer, 1, wx.EXPAND | wx.BOTTOM, 20)
        
        self.SetSizer(main_sizer)

    def _create_weather_info(self):
        panel = wx.Panel(self, style=wx.NO_BORDER)
        panel.SetBackgroundColour(Theme.BG_CARD)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(18)
        
        # Section Title
        hdr = wx.StaticText(panel, label="ATMOSPHERIC & MARITIME CONDITIONS")
        hdr.SetForegroundColour(Theme.ACCENT_ORANGE)
        hdr.SetFont(Theme.get_font(size=10, bold=True))
        sizer.Add(hdr, 0, wx.LEFT | wx.RIGHT, 20)
        
        sizer.AddSpacer(14)
        
        # METAR Raw Feed Box
        metar_box = wx.Panel(panel, style=wx.NO_BORDER)
        metar_box.SetBackgroundColour(Theme.BG_CARD_ALT)
        mb_sizer = wx.BoxSizer(wx.VERTICAL)
        mb_sizer.AddSpacer(10)
        
        m_lbl = wx.StaticText(metar_box, label="OFFICIAL METAR OBSERVATION (SAR BASE ALFA)")
        m_lbl.SetForegroundColour(Theme.TEXT_MUTED)
        m_lbl.SetFont(Theme.get_font(size=8, bold=True))
        mb_sizer.Add(m_lbl, 0, wx.LEFT | wx.RIGHT, 12)
        
        raw_text = wx.StaticText(metar_box, label="WARQ 040900Z 24022G35KT 4000 TSRA SCT012CB BKN030 26/24 Q1008 NOSIG")
        raw_text.SetForegroundColour(Theme.STATUS_CYAN)
        raw_text.SetFont(Theme.get_mono_font(size=9, bold=True))
        mb_sizer.Add(raw_text, 0, wx.LEFT | wx.RIGHT | wx.TOP, 12, 4)
        
        mb_sizer.AddSpacer(10)
        metar_box.SetSizer(mb_sizer)
        sizer.Add(metar_box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        
        sizer.AddSpacer(16)
        
        # Meteorological Parameters Grid
        grid_box = wx.Panel(panel, style=wx.NO_BORDER)
        grid_box.SetBackgroundColour(Theme.BG_CARD_ALT)
        g_sizer = wx.FlexGridSizer(rows=2, cols=2, vgap=12, hgap=24)
        g_sizer.AddGrowableCol(0, 1)
        g_sizer.AddGrowableCol(1, 1)
        
        self._add_metric(grid_box, g_sizer, "SURFACE WIND", "240° AT 22 KTS (GUSTS 35 KTS)", Theme.STATUS_AMBER)
        self._add_metric(grid_box, g_sizer, "SEA STATE (SWELLS)", "STATE 5 (ROUGH) • 2.8 - 3.5 M", Theme.STATUS_RED)
        self._add_metric(grid_box, g_sizer, "CLOUD CEILING & VIS", "BKN 3,000 FT • VIS: 4.2 NM IN RAIN", Theme.TEXT_PRIMARY)
        self._add_metric(grid_box, g_sizer, "BAROMETER & TEMP", "1008 HPA (FALLING) • +26°C", Theme.TEXT_PRIMARY)
        
        grid_box.SetSizer(g_sizer)
        sizer.Add(grid_box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        
        sizer.AddSpacer(16)
        
        # SAR Operational Hazard Warnings Box
        hazards_hdr = wx.StaticText(panel, label="OPERATIONAL SAR FLIGHT HAZARDS")
        hazards_hdr.SetForegroundColour(Theme.ACCENT_ORANGE)
        hazards_hdr.SetFont(Theme.get_font(size=9, bold=True))
        sizer.Add(hazards_hdr, 0, wx.LEFT | wx.RIGHT, 20)
        sizer.AddSpacer(8)
        
        hazards = [
            ("CAUTION", "High crosswind gusts (35kt) exceed standard hover hoist threshold by 5kt. Pilot discretion advised.", Theme.STATUS_AMBER),
            ("WARNING", "Severe wave crest spray over vessel superstructure requires minimum 40ft hoist hovering clearance.", Theme.STATUS_RED),
            ("ADVISORY", "Squall line moving East-Southeast at 18 knots. Expected overhead sector in 25 minutes.", Theme.STATUS_CYAN)
        ]
        
        for level, desc, col in hazards:
            row = wx.BoxSizer(wx.HORIZONTAL)
            tag = wx.StaticText(panel, label=f"[{level}]")
            tag.SetForegroundColour(col)
            tag.SetFont(Theme.get_mono_font(size=8, bold=True))
            row.Add(tag, 0, wx.ALIGN_TOP)
            
            d = wx.StaticText(panel, label=f" {desc}")
            d.SetForegroundColour(Theme.TEXT_SECONDARY)
            d.SetFont(Theme.get_font(size=8))
            d.Wrap(500)
            row.Add(d, 1, wx.EXPAND | wx.LEFT, 4)
            
            sizer.Add(row, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 8)
            
        sizer.AddStretchSpacer(1)
        
        # Action Buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        rad_btn = wx.Button(panel, label="RECALIBRATE RADAR SCAN")
        rad_btn.SetBackgroundColour(Theme.ACCENT_ORANGE)
        rad_btn.SetForegroundColour(Theme.TEXT_PRIMARY)
        rad_btn.SetFont(Theme.get_font(size=9, bold=True))
        btn_sizer.Add(rad_btn, 1, wx.RIGHT, 10)
        
        atis_btn = wx.Button(panel, label="REQUEST UPDATED ATIS")
        atis_btn.SetBackgroundColour(Theme.BG_CARD_ALT)
        atis_btn.SetForegroundColour(Theme.TEXT_PRIMARY)
        atis_btn.SetFont(Theme.get_font(size=9))
        btn_sizer.Add(atis_btn, 1)
        
        sizer.Add(btn_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 20)
        
        panel.SetSizer(sizer)
        return panel

    def _add_metric(self, parent, sizer, label, value, val_color):
        box = wx.BoxSizer(wx.VERTICAL)
        l = wx.StaticText(parent, label=label)
        l.SetForegroundColour(Theme.TEXT_MUTED)
        l.SetFont(Theme.get_font(size=8, bold=True))
        box.Add(l, 0, wx.EXPAND)
        
        v = wx.StaticText(parent, label=value)
        v.SetForegroundColour(val_color)
        v.SetFont(Theme.get_mono_font(size=9, bold=True))
        box.Add(v, 0, wx.EXPAND | wx.TOP, 3)
        
        sizer.Add(box, 1, wx.EXPAND | wx.ALL, 8)
