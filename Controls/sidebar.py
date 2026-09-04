"""
Helicopter Rescue Simulator - Custom Modern Sidebar
Vertical tab navigation container with branding, 4 custom tab buttons, and unit status card.
"""
import wx
from Assets.theme import Theme
from Assets.icons import IconRenderer
from .tab_button import TabButton, EVT_TAB_SELECTED


class SidebarControl(wx.Panel):
    """
    Modern dark-themed sidebar hosting the custom tab controls and unit telemetry badge.
    """
    def __init__(self, parent, on_tab_changed=None):
        super().__init__(parent, id=wx.ID_ANY, style=wx.NO_BORDER)
        self.SetBackgroundColour(Theme.BG_SIDEBAR)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.SetDoubleBuffered(True)
        self.SetMinSize((250, -1))
        self.SetMaxSize((280, -1))
        
        self.on_tab_changed = on_tab_changed
        self.buttons = []
        self.active_tab_index = 0
        
        self.Bind(wx.EVT_PAINT, self._on_paint)
        
        self._init_ui()

    def _init_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 1. Header Logo & Title Area
        header_panel = wx.Panel(self, style=wx.NO_BORDER)
        header_panel.SetBackgroundColour(Theme.BG_SIDEBAR)
        header_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Top spacing
        header_sizer.AddSpacer(18)
        
        # Branding Header Box
        brand_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Tactical Badge
        badge_canvas = wx.Panel(header_panel, size=(38, 38), style=wx.NO_BORDER)
        badge_canvas.SetBackgroundColour(Theme.BG_SIDEBAR)
        badge_canvas.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        def draw_badge(evt):
            dc = wx.AutoBufferedPaintDC(badge_canvas)
            gc = wx.GraphicsContext.Create(dc)
            if gc:
                IconRenderer.draw_helicopter_badge(gc, 2, 2, 34, 34)
        badge_canvas.Bind(wx.EVT_PAINT, draw_badge)
        brand_sizer.Add(badge_canvas, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 16)
        
        # Title texts
        title_box = wx.BoxSizer(wx.VERTICAL)
        app_title = wx.StaticText(header_panel, label="SAR RESCUE")
        app_title.SetForegroundColour(Theme.TEXT_PRIMARY)
        app_title.SetFont(Theme.get_font(size=12, bold=True))
        
        app_sub = wx.StaticText(header_panel, label="AIR DIVISION • TACTICAL")
        app_sub.SetForegroundColour(Theme.ACCENT_ORANGE)
        app_sub.SetFont(Theme.get_font(size=8, bold=True))
        
        title_box.Add(app_title, 0, wx.EXPAND)
        title_box.Add(app_sub, 0, wx.EXPAND | wx.TOP, 1)
        brand_sizer.Add(title_box, 1, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 12)
        
        header_sizer.Add(brand_sizer, 0, wx.EXPAND)
        header_sizer.AddSpacer(18)
        
        # Menu Category Label
        cat_label = wx.StaticText(header_panel, label="NAVIGATION SYSTEMS")
        cat_label.SetForegroundColour(Theme.TEXT_MUTED)
        cat_label.SetFont(Theme.get_font(size=8, bold=True))
        header_sizer.Add(cat_label, 0, wx.LEFT | wx.BOTTOM, 16)
        
        header_panel.SetSizer(header_sizer)
        main_sizer.Add(header_panel, 0, wx.EXPAND)

        # 2. Tab Buttons (4 Functional Tabs)
        tab_definitions = [
            (0, "Flight Ops", "Cockpit & Telemetry", "flight"),
            (1, "Rescue Missions", "Active Distress Calls", "missions"),
            (2, "Fleet & Gear", "Hangar & Equipment", "fleet"),
            (3, "Weather & Radar", "Sensors & Storm Scan", "weather")
        ]
        
        tabs_sizer = wx.BoxSizer(wx.VERTICAL)
        for tab_id, label, subtitle, icon_type in tab_definitions:
            btn = TabButton(self, tab_id=tab_id, label=label, subtitle=subtitle, icon_type=icon_type)
            btn.Bind(EVT_TAB_SELECTED, self._on_tab_click)
            self.buttons.append(btn)
            tabs_sizer.Add(btn, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 8)
            
        main_sizer.Add(tabs_sizer, 0, wx.EXPAND)
        
        # Flexible spacer to push status box to bottom
        main_sizer.AddStretchSpacer(1)
        
        # 3. Unit Status Card at bottom
        status_card = self._create_status_card()
        main_sizer.Add(status_card, 0, wx.EXPAND | wx.ALL, 12)
        
        self.SetSizer(main_sizer)
        
        # Activate initial tab (0)
        self.select_tab(0)

    def _create_status_card(self):
        """Creates unit readiness footer card."""
        panel = wx.Panel(self, style=wx.NO_BORDER)
        panel.SetBackgroundColour(Theme.BG_CARD)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Top row: Callsign and Status dot
        top_row = wx.BoxSizer(wx.HORIZONTAL)
        unit_lbl = wx.StaticText(panel, label="RESCUE-01")
        unit_lbl.SetForegroundColour(Theme.TEXT_PRIMARY)
        unit_lbl.SetFont(Theme.get_font(size=9, bold=True))
        
        status_lbl = wx.StaticText(panel, label="● READY")
        status_lbl.SetForegroundColour(Theme.STATUS_GREEN)
        status_lbl.SetFont(Theme.get_font(size=8, bold=True))
        
        top_row.Add(unit_lbl, 1, wx.ALIGN_CENTER_VERTICAL)
        top_row.Add(status_lbl, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(top_row, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
        
        # Divider line
        sizer.AddSpacer(6)
        
        # Helicopter Model & Transponder
        heli_lbl = wx.StaticText(panel, label="SIKORSKY S-92 SAR")
        heli_lbl.SetForegroundColour(Theme.TEXT_MUTED)
        heli_lbl.SetFont(Theme.get_mono_font(size=8))
        sizer.Add(heli_lbl, 0, wx.LEFT | wx.RIGHT, 10)
        
        xpdr_lbl = wx.StaticText(panel, label="XPDR: 7700 [EMERGENCY SAR]")
        xpdr_lbl.SetForegroundColour(Theme.ACCENT_ORANGE)
        xpdr_lbl.SetFont(Theme.get_mono_font(size=8))
        sizer.Add(xpdr_lbl, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.TOP, 10)
        
        panel.SetSizer(sizer)
        return panel

    def _on_tab_click(self, event):
        tab_id = event.tab_id
        self.select_tab(tab_id)

    def select_tab(self, index: int):
        self.active_tab_index = index
        for idx, btn in enumerate(self.buttons):
            btn.set_selected(idx == index)
        if self.on_tab_changed:
            self.on_tab_changed(index)

    def _on_paint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        # Right border line separating sidebar from content
        w, h = self.GetClientSize()
        dc.SetPen(wx.Pen(Theme.BORDER_SUBTLE, 1))
        dc.DrawLine(w - 1, 0, w - 1, h)
