"""
Helicopter Rescue Simulator - Flight Ops & Telemetry Dashboard
Main overview tab presenting real-time flight telemetry, status cards, and quick dispatch.
"""
import wx
from Assets.theme import Theme


class StatCard(wx.Panel):
    """Modern dark card with Safety Orange accent bar and key metric readout."""
    def __init__(self, parent, title: str, value: str, subvalue: str, accent_color=None):
        super().__init__(parent, style=wx.NO_BORDER)
        self.SetBackgroundColour(Theme.BG_CARD)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.SetDoubleBuffered(True)
        self.accent_color = accent_color or Theme.ACCENT_ORANGE
        
        self.Bind(wx.EVT_PAINT, self._on_paint)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(12)
        
        title_lbl = wx.StaticText(self, label=title.upper())
        title_lbl.SetForegroundColour(Theme.TEXT_MUTED)
        title_lbl.SetFont(Theme.get_font(size=8, bold=True))
        sizer.Add(title_lbl, 0, wx.LEFT | wx.RIGHT, 14)
        
        sizer.AddSpacer(6)
        
        val_lbl = wx.StaticText(self, label=value)
        val_lbl.SetForegroundColour(Theme.TEXT_PRIMARY)
        val_lbl.SetFont(Theme.get_font(size=18, bold=True))
        sizer.Add(val_lbl, 0, wx.LEFT | wx.RIGHT, 14)
        
        sizer.AddSpacer(4)
        
        sub_lbl = wx.StaticText(self, label=subvalue)
        sub_lbl.SetForegroundColour(self.accent_color)
        sub_lbl.SetFont(Theme.get_mono_font(size=8, bold=True))
        sizer.Add(sub_lbl, 0, wx.LEFT | wx.RIGHT, 14)
        
        sizer.AddSpacer(12)
        self.SetSizer(sizer)

    def _on_paint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        if not gc:
            return
        w, h = self.GetClientSize()
        
        # Border
        gc.SetPen(wx.Pen(Theme.BORDER_SUBTLE, 1))
        gc.SetBrush(wx.Brush(Theme.BG_CARD))
        gc.DrawRoundedRectangle(0, 0, w, h, 6)
        
        # Top Accent Line
        gc.SetPen(wx.NullPen)
        gc.SetBrush(wx.Brush(self.accent_color))
        gc.DrawRoundedRectangle(0, 0, w, 3, 2)


class TelemetryBar(wx.Panel):
    """Custom progress/gauge bar displaying flight instruments."""
    def __init__(self, parent, label: str, value_text: str, percent: float, bar_color=None):
        super().__init__(parent, size=(-1, 48), style=wx.NO_BORDER)
        self.SetBackgroundColour(Theme.BG_CARD)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.SetDoubleBuffered(True)
        self.label = label
        self.value_text = value_text
        self.percent = max(0.0, min(1.0, percent))
        self.bar_color = bar_color or Theme.ACCENT_ORANGE
        
        self.Bind(wx.EVT_PAINT, self._on_paint)

    def _on_paint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        if not gc:
            return
        w, h = self.GetClientSize()
        
        # Label (left) & Value (right)
        gc.SetFont(Theme.get_font(size=9, bold=True), Theme.TEXT_SECONDARY)
        gc.DrawText(self.label, 2, 2)
        
        gc.SetFont(Theme.get_mono_font(size=9, bold=True), Theme.TEXT_PRIMARY)
        val_w, _ = gc.GetTextExtent(self.value_text)
        gc.DrawText(self.value_text, w - val_w - 4, 2)
        
        # Progress track background
        track_y = 24.0
        track_h = 10.0
        track_w = w - 4.0
        
        gc.SetBrush(wx.Brush(Theme.BG_INPUT))
        gc.SetPen(wx.Pen(Theme.BORDER_SUBTLE, 1))
        gc.DrawRoundedRectangle(2, track_y, track_w, track_h, 3)
        
        # Progress fill
        fill_w = max(4.0, (track_w - 2.0) * self.percent)
        gc.SetBrush(wx.Brush(self.bar_color))
        gc.SetPen(wx.NullPen)
        gc.DrawRoundedRectangle(3, track_y + 1, fill_w, track_h - 2, 2)


class DashboardView(wx.Panel):
    """Main Flight Ops tab view."""
    def __init__(self, parent):
        super().__init__(parent, style=wx.NO_BORDER)
        self.SetBackgroundColour(Theme.BG_MAIN)
        self.SetDoubleBuffered(True)
        
        self._init_ui()

    def _init_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.AddSpacer(18)
        
        # View Title Section
        header_sizer = wx.BoxSizer(wx.VERTICAL)
        title_lbl = wx.StaticText(self, label="FLIGHT OPERATIONS & TELEMETRY")
        title_lbl.SetForegroundColour(Theme.TEXT_PRIMARY)
        title_lbl.SetFont(Theme.get_font(size=14, bold=True))
        header_sizer.Add(title_lbl, 0, wx.LEFT | wx.RIGHT, 24)
        
        sub_lbl = wx.StaticText(self, label="Real-time aircraft avionics, active search status, and hoist telemetry.")
        sub_lbl.SetForegroundColour(Theme.TEXT_MUTED)
        sub_lbl.SetFont(Theme.get_font(size=9))
        header_sizer.Add(sub_lbl, 0, wx.LEFT | wx.RIGHT | wx.TOP, 24, 4)
        
        main_sizer.Add(header_sizer, 0, wx.EXPAND)
        main_sizer.AddSpacer(16)
        
        # 1. Row of 4 Stat Cards
        cards_sizer = wx.BoxSizer(wx.HORIZONTAL)
        cards_sizer.AddSpacer(24)
        
        card1 = StatCard(self, "Active Missions", "3 INCIDENTS", "1 CRITICAL MAYDAY", Theme.STATUS_RED)
        cards_sizer.Add(card1, 1, wx.EXPAND | wx.RIGHT, 12)
        
        card2 = StatCard(self, "Aircraft State", "AIRBORNE", "ALT 1,850 FT • 135 KTS", Theme.STATUS_GREEN)
        cards_sizer.Add(card2, 1, wx.EXPAND | wx.RIGHT, 12)
        
        card3 = StatCard(self, "Fuel Capacity", "78% (1,450 L)", "ENDURANCE: 02H 45M", Theme.ACCENT_ORANGE)
        cards_sizer.Add(card3, 1, wx.EXPAND | wx.RIGHT, 12)
        
        card4 = StatCard(self, "Rescue Hoist", "DEPLOYED 42M", "TENSION: 110 KG (STABLE)", Theme.STATUS_CYAN)
        cards_sizer.Add(card4, 1, wx.EXPAND)
        
        cards_sizer.AddSpacer(24)
        main_sizer.Add(cards_sizer, 0, wx.EXPAND)
        main_sizer.AddSpacer(16)
        
        # 2. Main Body Split: Left Telemetry, Right Mission Summary & Controls
        content_sizer = wx.BoxSizer(wx.HORIZONTAL)
        content_sizer.AddSpacer(24)
        
        # Left Panel: Flight Avionics
        avionics_panel = self._create_avionics_panel()
        content_sizer.Add(avionics_panel, 1, wx.EXPAND | wx.RIGHT, 16)
        
        # Right Panel: Active SAR Target & Tactical Log
        tactical_panel = self._create_tactical_panel()
        content_sizer.Add(tactical_panel, 1, wx.EXPAND)
        
        content_sizer.AddSpacer(24)
        main_sizer.Add(content_sizer, 1, wx.EXPAND | wx.BOTTOM, 20)
        
        self.SetSizer(main_sizer)

    def _create_avionics_panel(self):
        panel = wx.Panel(self, style=wx.NO_BORDER)
        panel.SetBackgroundColour(Theme.BG_CARD)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(16)
        
        # Section Header
        hdr = wx.StaticText(panel, label="COCKPIT AVIONICS & ENGINE GAUGES")
        hdr.SetForegroundColour(Theme.ACCENT_ORANGE)
        hdr.SetFont(Theme.get_font(size=10, bold=True))
        sizer.Add(hdr, 0, wx.LEFT | wx.RIGHT, 18)
        
        sizer.AddSpacer(14)
        
        # Gauges list
        g1 = TelemetryBar(panel, "ALTITUDE (MSL)", "1,850 FT / TARGET: 2,000 FT", 0.62, Theme.STATUS_CYAN)
        sizer.Add(g1, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 18)
        sizer.AddSpacer(10)
        
        g2 = TelemetryBar(panel, "INDICATED AIRSPEED (KIAS)", "135 KNOTS / VNE: 165 KTS", 0.72, Theme.ACCENT_ORANGE)
        sizer.Add(g2, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 18)
        sizer.AddSpacer(10)
        
        g3 = TelemetryBar(panel, "MAIN ROTOR SPEED (NR)", "102% (NOMINAL)", 0.85, Theme.STATUS_GREEN)
        sizer.Add(g3, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 18)
        sizer.AddSpacer(10)
        
        g4 = TelemetryBar(panel, "TWIN TURBOSHAFT TORQUE", "ENG 1: 84% | ENG 2: 85%", 0.84, Theme.ACCENT_ORANGE)
        sizer.Add(g4, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 18)
        sizer.AddSpacer(10)
        
        g5 = TelemetryBar(panel, "RESCUE HOIST CABLE EXTENSION", "42.5 M / MAX: 90 M", 0.47, Theme.STATUS_AMBER)
        sizer.Add(g5, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 18)
        
        sizer.AddStretchSpacer(1)
        panel.SetSizer(sizer)
        return panel

    def _create_tactical_panel(self):
        panel = wx.Panel(self, style=wx.NO_BORDER)
        panel.SetBackgroundColour(Theme.BG_CARD)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(16)
        
        # Section Header
        hdr = wx.StaticText(panel, label="DISPATCH & RESCUE LOG")
        hdr.SetForegroundColour(Theme.ACCENT_ORANGE)
        hdr.SetFont(Theme.get_font(size=10, bold=True))
        sizer.Add(hdr, 0, wx.LEFT | wx.RIGHT, 18)
        
        sizer.AddSpacer(14)
        
        # Current Target Box
        target_box = wx.Panel(panel, style=wx.NO_BORDER)
        target_box.SetBackgroundColour(Theme.BG_CARD_ALT)
        tb_sizer = wx.BoxSizer(wx.VERTICAL)
        tb_sizer.AddSpacer(10)
        
        tb_title = wx.StaticText(target_box, label="PRIMARY TARGET: TRAWLER 'PACIFIC STAR'")
        tb_title.SetForegroundColour(Theme.TEXT_PRIMARY)
        tb_title.SetFont(Theme.get_font(size=9, bold=True))
        tb_sizer.Add(tb_title, 0, wx.LEFT | wx.RIGHT, 12)
        
        tb_coords = wx.StaticText(target_box, label="COORDS: 08°42'15\" S  115°10'48\" E  •  BEARING: 245°  •  DIST: 14.2 NM")
        tb_coords.SetForegroundColour(Theme.TEXT_ACCENT)
        tb_coords.SetFont(Theme.get_mono_font(size=8))
        tb_sizer.Add(tb_coords, 0, wx.LEFT | wx.RIGHT | wx.TOP, 12, 4)
        
        tb_sizer.AddSpacer(10)
        target_box.SetSizer(tb_sizer)
        sizer.Add(target_box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 18)
        
        sizer.AddSpacer(14)
        
        # SAR Log Entries
        logs = [
            ("14:32:00", "MAYDAY relayed from Maritime Distress Frequency 121.5 MHz", Theme.STATUS_RED),
            ("14:33:15", "Heli SAR-01 scrambled from Coastal Airbase Station Alfa", Theme.ACCENT_ORANGE),
            ("14:41:20", "FLIR Thermal imaging acquired vessel heat signature", Theme.STATUS_CYAN),
            ("14:45:00", "Rescue swimmer deployed via hoist, 2 survivors secured", Theme.STATUS_GREEN)
        ]
        
        log_box = wx.BoxSizer(wx.VERTICAL)
        for timestamp, text, color in logs:
            row = wx.BoxSizer(wx.HORIZONTAL)
            t_lbl = wx.StaticText(panel, label=f"[{timestamp}]")
            t_lbl.SetForegroundColour(color)
            t_lbl.SetFont(Theme.get_mono_font(size=8, bold=True))
            row.Add(t_lbl, 0, wx.ALIGN_CENTER_VERTICAL)
            
            m_lbl = wx.StaticText(panel, label=f" {text}")
            m_lbl.SetForegroundColour(Theme.TEXT_SECONDARY)
            m_lbl.SetFont(Theme.get_font(size=8))
            row.Add(m_lbl, 1, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 4)
            
            log_box.Add(row, 0, wx.EXPAND | wx.BOTTOM, 8)
            
        sizer.Add(log_box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 18)
        
        sizer.AddStretchSpacer(1)
        
        # Action Buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        scramble_btn = wx.Button(panel, label="DISPATCH BACKUP HELI")
        scramble_btn.SetBackgroundColour(Theme.ACCENT_ORANGE)
        scramble_btn.SetForegroundColour(Theme.TEXT_PRIMARY)
        scramble_btn.SetFont(Theme.get_font(size=9, bold=True))
        btn_sizer.Add(scramble_btn, 1, wx.RIGHT, 8)
        
        hoist_btn = wx.Button(panel, label="TOGGLE WINCH HOIST")
        hoist_btn.SetBackgroundColour(Theme.BG_CARD_ALT)
        hoist_btn.SetForegroundColour(Theme.TEXT_PRIMARY)
        hoist_btn.SetFont(Theme.get_font(size=9))
        btn_sizer.Add(hoist_btn, 1)
        
        sizer.Add(btn_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 18)
        
        panel.SetSizer(sizer)
        return panel
