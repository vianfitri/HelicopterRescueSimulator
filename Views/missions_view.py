"""
Helicopter Rescue Simulator - Search & Rescue Missions View
Manages active SAR emergency calls, victim status, dispatch operations, and mission dossiers.
"""
import wx
from Assets.theme import Theme


class MissionCard(wx.Panel):
    """Clickable incident card in the SAR missions list."""
    def __init__(self, parent, mission_data, is_selected=False, on_select=None):
        super().__init__(parent, style=wx.NO_BORDER)
        self.mission_data = mission_data
        self.is_selected = is_selected
        self.on_select = on_select
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.SetDoubleBuffered(True)
        self.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        
        self.Bind(wx.EVT_PAINT, self._on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self._on_click)
        
        self._init_ui()

    def _init_ui(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(12)
        
        # Priority row
        top_row = wx.BoxSizer(wx.HORIZONTAL)
        pri_lbl = wx.StaticText(self, label=f"● {self.mission_data['priority']}")
        pri_lbl.SetForegroundColour(self.mission_data['color'])
        pri_lbl.SetFont(Theme.get_font(size=8, bold=True))
        top_row.Add(pri_lbl, 0, wx.ALIGN_CENTER_VERTICAL)
        
        code_lbl = wx.StaticText(self, label=self.mission_data['code'])
        code_lbl.SetForegroundColour(Theme.TEXT_MUTED)
        code_lbl.SetFont(Theme.get_mono_font(size=8))
        top_row.Add(code_lbl, 1, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 8)
        
        sizer.Add(top_row, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 14)
        sizer.AddSpacer(6)
        
        # Incident Title
        title_lbl = wx.StaticText(self, label=self.mission_data['title'])
        title_lbl.SetForegroundColour(Theme.TEXT_PRIMARY)
        title_lbl.SetFont(Theme.get_font(size=10, bold=True))
        sizer.Add(title_lbl, 0, wx.LEFT | wx.RIGHT, 14)
        sizer.AddSpacer(4)
        
        # Sector & Victims
        info_lbl = wx.StaticText(self, label=f"{self.mission_data['sector']} • {self.mission_data['souls']}")
        info_lbl.SetForegroundColour(Theme.TEXT_SECONDARY)
        info_lbl.SetFont(Theme.get_font(size=8))
        sizer.Add(info_lbl, 0, wx.LEFT | wx.RIGHT, 14)
        
        sizer.AddSpacer(12)
        self.SetSizer(sizer)

    def set_selected(self, selected: bool):
        self.is_selected = selected
        self.Refresh()

    def _on_click(self, event):
        if self.on_select:
            self.on_select(self.mission_data)
        event.Skip()

    def _on_paint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        if not gc:
            return
        w, h = self.GetClientSize()
        
        bg_col = Theme.BG_CARD_ALT if self.is_selected else Theme.BG_CARD
        gc.SetBrush(wx.Brush(bg_col))
        gc.SetPen(wx.Pen(Theme.ACCENT_ORANGE if self.is_selected else Theme.BORDER_SUBTLE, 1))
        gc.DrawRoundedRectangle(0, 0, w, h, 6)
        
        if self.is_selected:
            gc.SetPen(wx.NullPen)
            gc.SetBrush(wx.Brush(Theme.ACCENT_ORANGE))
            gc.DrawRoundedRectangle(0, 0, 4, h, 2)


class MissionsView(wx.Panel):
    """View handling search and rescue incident dispatch and dossier details."""
    def __init__(self, parent):
        super().__init__(parent, style=wx.NO_BORDER)
        self.SetBackgroundColour(Theme.BG_MAIN)
        self.SetDoubleBuffered(True)
        
        self.missions = [
            {
                "code": "SAR-MAYDAY-09",
                "priority": "CRITICAL EMERGENCY",
                "color": Theme.STATUS_RED,
                "title": "Trawler 'Pacific Star' Capsized",
                "sector": "Sector Delta-9 (Offshore)",
                "souls": "4 Souls in Water",
                "coords": "08°42'15\" S, 115°10'48\" E",
                "weather": "Sea State 5, 35kt Gale, 2.8m Swells",
                "assigned": "Rescue-01 (S-92 Heavy SAR)",
                "briefing": "Commercial fishing boat reported engine compartment flooding before communications severed. Emergency Position Indicating Radiobeacon (EPIRB) actively transmitting on 406 MHz. Deploy rescue swimmer with rescue sling immediately."
            },
            {
                "code": "SAR-ALPINE-03",
                "priority": "URGENT DISPATCH",
                "color": Theme.ACCENT_ORANGE,
                "title": "Mountain Ridge Climbers Avalanche",
                "sector": "Sector Alpha-2 (Alpine Ridge)",
                "souls": "2 Injured Climbers",
                "coords": "07°32'10\" S, 110°26'34\" E",
                "weather": "Sub-zero -4°C, High Altitude Turbulence, Cloud Base 6,000 FT",
                "assigned": "Rescue-02 (Airbus H145)",
                "briefing": "Expedition party caught in snow drift at 2,400m elevation. One fractured femur. High hover out of ground effect (HOGE) winch operation required due to treacherous crags."
            },
            {
                "code": "SAR-MEDEVAC-07",
                "priority": "MEDICAL PRIORITY",
                "color": Theme.STATUS_AMBER,
                "title": "Offshore Oil Platform Trauma",
                "sector": "Sector Echo-1 (Drilling Rig)",
                "souls": "1 Severe Burn Patient",
                "coords": "06°15'55\" S, 118°45'12\" E",
                "weather": "Gusting 22kt, Visibility 8 NM, Light Rain",
                "assigned": "Rescue-03 (AW139)",
                "briefing": "Industrial pipe rupture on oil rig helideck. Helipad clear for direct landing. Flight medic on board ready with trauma stabilization unit."
            }
        ]
        
        self.active_mission = self.missions[0]
        self.card_widgets = []
        
        self._init_ui()

    def _init_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.AddSpacer(18)
        
        # Header
        header_sizer = wx.BoxSizer(wx.VERTICAL)
        title_lbl = wx.StaticText(self, label="SEARCH & RESCUE MISSION DISPATCH")
        title_lbl.SetForegroundColour(Theme.TEXT_PRIMARY)
        title_lbl.SetFont(Theme.get_font(size=14, bold=True))
        header_sizer.Add(title_lbl, 0, wx.LEFT | wx.RIGHT, 24)
        
        sub_lbl = wx.StaticText(self, label="Active emergency incidents, victim status, and tactical helicopter deployment.")
        sub_lbl.SetForegroundColour(Theme.TEXT_MUTED)
        sub_lbl.SetFont(Theme.get_font(size=9))
        header_sizer.Add(sub_lbl, 0, wx.LEFT | wx.RIGHT | wx.TOP, 24, 4)
        
        main_sizer.Add(header_sizer, 0, wx.EXPAND)
        main_sizer.AddSpacer(16)
        
        # Body split: Left incident cards (380px), Right incident dossier
        content_sizer = wx.BoxSizer(wx.HORIZONTAL)
        content_sizer.AddSpacer(24)
        
        # Left: Incidents list
        list_panel = wx.Panel(self, style=wx.NO_BORDER)
        list_panel.SetBackgroundColour(Theme.BG_MAIN)
        list_sizer = wx.BoxSizer(wx.VERTICAL)
        
        list_hdr = wx.StaticText(list_panel, label="ACTIVE DISTRESS CALLS")
        list_hdr.SetForegroundColour(Theme.ACCENT_ORANGE)
        list_hdr.SetFont(Theme.get_font(size=10, bold=True))
        list_sizer.Add(list_hdr, 0, wx.BOTTOM, 12)
        
        for idx, m in enumerate(self.missions):
            card = MissionCard(list_panel, m, is_selected=(idx == 0), on_select=self._on_select_mission)
            self.card_widgets.append(card)
            list_sizer.Add(card, 0, wx.EXPAND | wx.BOTTOM, 10)
            
        list_panel.SetSizer(list_sizer)
        content_sizer.Add(list_panel, 0, wx.EXPAND | wx.RIGHT, 18)
        list_panel.SetMinSize((380, -1))
        
        # Right: Dossier Details
        self.dossier_panel = self._create_dossier_panel()
        content_sizer.Add(self.dossier_panel, 1, wx.EXPAND)
        
        content_sizer.AddSpacer(24)
        main_sizer.Add(content_sizer, 1, wx.EXPAND | wx.BOTTOM, 20)
        
        self.SetSizer(main_sizer)

    def _create_dossier_panel(self):
        panel = wx.Panel(self, style=wx.NO_BORDER)
        panel.SetBackgroundColour(Theme.BG_CARD)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(18)
        
        # Header row
        self.dossier_title = wx.StaticText(panel, label=self.active_mission['title'].upper())
        self.dossier_title.SetForegroundColour(Theme.TEXT_PRIMARY)
        self.dossier_title.SetFont(Theme.get_font(size=13, bold=True))
        sizer.Add(self.dossier_title, 0, wx.LEFT | wx.RIGHT, 20)
        
        self.dossier_code = wx.StaticText(panel, label=f"INCIDENT CODE: {self.active_mission['code']} • {self.active_mission['priority']}")
        self.dossier_code.SetForegroundColour(self.active_mission['color'])
        self.dossier_code.SetFont(Theme.get_mono_font(size=9, bold=True))
        sizer.Add(self.dossier_code, 0, wx.LEFT | wx.RIGHT | wx.TOP, 20, 4)
        
        sizer.AddSpacer(16)
        
        # Grid Info Box
        info_box = wx.Panel(panel, style=wx.NO_BORDER)
        info_box.SetBackgroundColour(Theme.BG_CARD_ALT)
        ib_sizer = wx.FlexGridSizer(rows=2, cols=2, vgap=12, hgap=24)
        ib_sizer.AddGrowableCol(0, 1)
        ib_sizer.AddGrowableCol(1, 1)
        
        self.info_coords = self._add_field(info_box, ib_sizer, "GPS COORDINATES", self.active_mission['coords'])
        self.info_souls = self._add_field(info_box, ib_sizer, "VICTIM STATUS", self.active_mission['souls'])
        self.info_weather = self._add_field(info_box, ib_sizer, "WEATHER & CONDITIONS", self.active_mission['weather'])
        self.info_asset = self._add_field(info_box, ib_sizer, "ASSIGNED HELICOPTER", self.active_mission['assigned'])
        
        info_box.SetSizer(ib_sizer)
        sizer.Add(info_box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        
        sizer.AddSpacer(16)
        
        # Tactical Briefing description
        briefing_hdr = wx.StaticText(panel, label="TACTICAL MISSION BRIEFING")
        briefing_hdr.SetForegroundColour(Theme.ACCENT_ORANGE)
        briefing_hdr.SetFont(Theme.get_font(size=9, bold=True))
        sizer.Add(briefing_hdr, 0, wx.LEFT | wx.RIGHT, 20)
        sizer.AddSpacer(6)
        
        self.briefing_text = wx.StaticText(panel, label=self.active_mission['briefing'])
        self.briefing_text.SetForegroundColour(Theme.TEXT_SECONDARY)
        self.briefing_text.SetFont(Theme.get_font(size=9))
        self.briefing_text.Wrap(650)
        sizer.Add(self.briefing_text, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        
        sizer.AddStretchSpacer(1)
        
        # Action Buttons Row
        act_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        scramble_btn = wx.Button(panel, label="SCRAMBLE / DISPATCH NOW")
        scramble_btn.SetBackgroundColour(Theme.ACCENT_ORANGE)
        scramble_btn.SetForegroundColour(Theme.TEXT_PRIMARY)
        scramble_btn.SetFont(Theme.get_font(size=9, bold=True))
        act_sizer.Add(scramble_btn, 1, wx.RIGHT, 10)
        
        basket_btn = wx.Button(panel, label="DEPLOY RESCUE BASKET")
        basket_btn.SetBackgroundColour(Theme.BG_CARD_ALT)
        basket_btn.SetForegroundColour(Theme.TEXT_PRIMARY)
        basket_btn.SetFont(Theme.get_font(size=9))
        act_sizer.Add(basket_btn, 1, wx.RIGHT, 10)
        
        searchlight_btn = wx.Button(panel, label="NIGHTSUN 30M CANDLEPOWER")
        searchlight_btn.SetBackgroundColour(Theme.BG_CARD_ALT)
        searchlight_btn.SetForegroundColour(Theme.TEXT_PRIMARY)
        searchlight_btn.SetFont(Theme.get_font(size=9))
        act_sizer.Add(searchlight_btn, 1)
        
        sizer.Add(act_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 20)
        
        panel.SetSizer(sizer)
        return panel

    def _add_field(self, parent, sizer, label, value):
        box = wx.BoxSizer(wx.VERTICAL)
        l = wx.StaticText(parent, label=label)
        l.SetForegroundColour(Theme.TEXT_MUTED)
        l.SetFont(Theme.get_font(size=8, bold=True))
        box.Add(l, 0, wx.EXPAND)
        
        v = wx.StaticText(parent, label=value)
        v.SetForegroundColour(Theme.TEXT_PRIMARY)
        v.SetFont(Theme.get_mono_font(size=9, bold=True))
        box.Add(v, 0, wx.EXPAND | wx.TOP, 3)
        
        sizer.Add(box, 1, wx.EXPAND | wx.ALL, 8)
        return v

    def _on_select_mission(self, mission_data):
        self.active_mission = mission_data
        for c in self.card_widgets:
            c.set_selected(c.mission_data['code'] == mission_data['code'])
            
        self.dossier_title.SetLabel(mission_data['title'].upper())
        self.dossier_code.SetLabel(f"INCIDENT CODE: {mission_data['code']} • {mission_data['priority']}")
        self.dossier_code.SetForegroundColour(mission_data['color'])
        self.info_coords.SetLabel(mission_data['coords'])
        self.info_souls.SetLabel(mission_data['souls'])
        self.info_weather.SetLabel(mission_data['weather'])
        self.info_asset.SetLabel(mission_data['assigned'])
        self.briefing_text.SetLabel(mission_data['briefing'])
        self.briefing_text.Wrap(650)
        self.dossier_panel.Layout()
