"""
Helicopter Rescue Simulator - Fleet & Hangar View
Details helicopter inventory, dual hoist specifications, FLIR payload, and hangar maintenance.
"""
import wx
from Assets.theme import Theme


class FleetCard(wx.Panel):
    """Card representing an individual helicopter in the fleet."""
    def __init__(self, parent, heli_data, is_selected=False, on_select=None):
        super().__init__(parent, style=wx.NO_BORDER)
        self.heli_data = heli_data
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
        
        # Status Pill
        top_row = wx.BoxSizer(wx.HORIZONTAL)
        st_lbl = wx.StaticText(self, label=f"● {self.heli_data['status']}")
        st_lbl.SetForegroundColour(self.heli_data['status_color'])
        st_lbl.SetFont(Theme.get_font(size=8, bold=True))
        top_row.Add(st_lbl, 1, wx.ALIGN_CENTER_VERTICAL)
        
        tail_lbl = wx.StaticText(self, label=self.heli_data['tail_number'])
        tail_lbl.SetForegroundColour(Theme.TEXT_MUTED)
        tail_lbl.SetFont(Theme.get_mono_font(size=8))
        top_row.Add(tail_lbl, 0, wx.ALIGN_CENTER_VERTICAL)
        
        sizer.Add(top_row, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 14)
        sizer.AddSpacer(6)
        
        # Model Name
        name_lbl = wx.StaticText(self, label=self.heli_data['name'])
        name_lbl.SetForegroundColour(Theme.TEXT_PRIMARY)
        name_lbl.SetFont(Theme.get_font(size=10, bold=True))
        sizer.Add(name_lbl, 0, wx.LEFT | wx.RIGHT, 14)
        sizer.AddSpacer(4)
        
        # Role & Engine
        role_lbl = wx.StaticText(self, label=f"{self.heli_data['role']} • {self.heli_data['engines']}")
        role_lbl.SetForegroundColour(Theme.TEXT_SECONDARY)
        role_lbl.SetFont(Theme.get_font(size=8))
        sizer.Add(role_lbl, 0, wx.LEFT | wx.RIGHT, 14)
        
        sizer.AddSpacer(12)
        self.SetSizer(sizer)

    def set_selected(self, selected: bool):
        self.is_selected = selected
        self.Refresh()

    def _on_click(self, event):
        if self.on_select:
            self.on_select(self.heli_data)
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


class FleetView(wx.Panel):
    """View managing SAR aircraft fleet, hoist systems, and maintenance."""
    def __init__(self, parent):
        super().__init__(parent, style=wx.NO_BORDER)
        self.SetBackgroundColour(Theme.BG_MAIN)
        self.SetDoubleBuffered(True)
        
        self.helicopters = [
            {
                "id": "heli_1",
                "name": "Sikorsky S-92 SAR Helibus",
                "callsign": "RESCUE-01",
                "tail_number": "SAR-9201",
                "status": "ON PATROL (AIRBORNE)",
                "status_color": Theme.STATUS_GREEN,
                "role": "Heavy Maritime Long-Range SAR",
                "engines": "2x GE CT7-8A Turboshaft (5,040 shp)",
                "max_speed": "165 KTS (306 km/h)",
                "range": "539 NM (998 km)",
                "rotor_dia": "17.17 m (4-Blade Composite)",
                "hoist": "Dual Goodrich Electric (90m cable / 272kg rating)",
                "cabin": "Up to 21 passengers / 2 litters + medical crew",
                "flir": "FLIR UltraForce 350-HD High-Definition Gimbal",
                "searchlight": "TrakkaBeam A800 800W Xenon System",
                "maint_due": "48 Flight Hours until 100h Check"
            },
            {
                "id": "heli_2",
                "name": "Airbus Helicopters H145 D3",
                "callsign": "RESCUE-02",
                "tail_number": "SAR-1452",
                "status": "HANGAR STANDBY (READY)",
                "status_color": Theme.STATUS_CYAN,
                "role": "Alpine & High-Altitude Rescue",
                "engines": "2x Safran Arriel 2E (1,788 shp)",
                "max_speed": "140 KTS (260 km/h)",
                "range": "355 NM (657 km)",
                "rotor_dia": "11.0 m (5-Blade Bearingless)",
                "hoist": "Single Variable Speed Winch (90m / 250kg)",
                "cabin": "Modular EMS medical interior + 1 stretcher",
                "flir": "Wescam MX-10 EO/IR Multi-Sensor",
                "searchlight": "Spectrolab SX-16 Nightsun",
                "maint_due": "112 Flight Hours until Service"
            },
            {
                "id": "heli_3",
                "name": "Leonardo AW139 Maritime SAR",
                "callsign": "RESCUE-03",
                "tail_number": "SAR-1393",
                "status": "TURNAROUND / REFUELED",
                "status_color": Theme.STATUS_AMBER,
                "role": "Medium Twin Offshore SAR",
                "engines": "2x Pratt & Whitney PT6C-67C (3,358 shp)",
                "max_speed": "167 KTS (310 km/h)",
                "range": "573 NM (1,061 km)",
                "rotor_dia": "13.8 m (5-Blade High-Inertia)",
                "hoist": "Dual Hoist (High-Speed Variable 272kg)",
                "cabin": "Full Intensive Care Suite (2 stretchers)",
                "flir": "Star SAFIRE 380-HD Thermal Camera",
                "searchlight": "TrakkaBeam A800 with IR Filter",
                "maint_due": "Inspection Complete (Ready for Dispatch)"
            }
        ]
        
        self.active_heli = self.helicopters[0]
        self.card_widgets = []
        
        self._init_ui()

    def _init_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.AddSpacer(18)
        
        # Header
        header_sizer = wx.BoxSizer(wx.VERTICAL)
        title_lbl = wx.StaticText(self, label="FLEET READINESS & RESCUE EQUIPMENT")
        title_lbl.SetForegroundColour(Theme.TEXT_PRIMARY)
        title_lbl.SetFont(Theme.get_font(size=14, bold=True))
        header_sizer.Add(title_lbl, 0, wx.LEFT | wx.RIGHT, 24)
        
        sub_lbl = wx.StaticText(self, label="Aircraft maintenance logs, dual rescue hoists, thermal FLIR payloads, and avionics.")
        sub_lbl.SetForegroundColour(Theme.TEXT_MUTED)
        sub_lbl.SetFont(Theme.get_font(size=9))
        header_sizer.Add(sub_lbl, 0, wx.LEFT | wx.RIGHT | wx.TOP, 24, 4)
        
        main_sizer.Add(header_sizer, 0, wx.EXPAND)
        main_sizer.AddSpacer(16)
        
        # Split: Left Fleet Selection list, Right Detailed Aircraft Specs
        content_sizer = wx.BoxSizer(wx.HORIZONTAL)
        content_sizer.AddSpacer(24)
        
        # Left List
        left_panel = wx.Panel(self, style=wx.NO_BORDER)
        left_panel.SetBackgroundColour(Theme.BG_MAIN)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        
        hdr = wx.StaticText(left_panel, label="HANGAR INVENTORY")
        hdr.SetForegroundColour(Theme.ACCENT_ORANGE)
        hdr.SetFont(Theme.get_font(size=10, bold=True))
        left_sizer.Add(hdr, 0, wx.BOTTOM, 12)
        
        for idx, h in enumerate(self.helicopters):
            card = FleetCard(left_panel, h, is_selected=(idx == 0), on_select=self._on_select_heli)
            self.card_widgets.append(card)
            left_sizer.Add(card, 0, wx.EXPAND | wx.BOTTOM, 10)
            
        left_panel.SetSizer(left_sizer)
        content_sizer.Add(left_panel, 0, wx.EXPAND | wx.RIGHT, 18)
        left_panel.SetMinSize((380, -1))
        
        # Right Spec Panel
        self.spec_panel = self._create_spec_panel()
        content_sizer.Add(self.spec_panel, 1, wx.EXPAND)
        
        content_sizer.AddSpacer(24)
        main_sizer.Add(content_sizer, 1, wx.EXPAND | wx.BOTTOM, 20)
        
        self.SetSizer(main_sizer)

    def _create_spec_panel(self):
        panel = wx.Panel(self, style=wx.NO_BORDER)
        panel.SetBackgroundColour(Theme.BG_CARD)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(18)
        
        # Title
        self.heli_title = wx.StaticText(panel, label=self.active_heli['name'].upper())
        self.heli_title.SetForegroundColour(Theme.TEXT_PRIMARY)
        self.heli_title.SetFont(Theme.get_font(size=13, bold=True))
        sizer.Add(self.heli_title, 0, wx.LEFT | wx.RIGHT, 20)
        
        self.heli_status = wx.StaticText(panel, label=f"CALLSIGN: {self.active_heli['callsign']} • {self.active_heli['status']}")
        self.heli_status.SetForegroundColour(self.active_heli['status_color'])
        self.heli_status.SetFont(Theme.get_mono_font(size=9, bold=True))
        sizer.Add(self.heli_status, 0, wx.LEFT | wx.RIGHT | wx.TOP, 20, 4)
        
        sizer.AddSpacer(16)
        
        # Grid of Specs
        grid_box = wx.Panel(panel, style=wx.NO_BORDER)
        grid_box.SetBackgroundColour(Theme.BG_CARD_ALT)
        g_sizer = wx.FlexGridSizer(rows=3, cols=2, vgap=12, hgap=24)
        g_sizer.AddGrowableCol(0, 1)
        g_sizer.AddGrowableCol(1, 1)
        
        self.spec_engines = self._add_spec_item(grid_box, g_sizer, "POWERPLANT", self.active_heli['engines'])
        self.spec_speed = self._add_spec_item(grid_box, g_sizer, "MAX SPEED / RANGE", f"{self.active_heli['max_speed']} / {self.active_heli['range']}")
        self.spec_rotor = self._add_spec_item(grid_box, g_sizer, "ROTOR SYSTEM", self.active_heli['rotor_dia'])
        self.spec_hoist = self._add_spec_item(grid_box, g_sizer, "WINCH / HOIST", self.active_heli['hoist'])
        self.spec_flir = self._add_spec_item(grid_box, g_sizer, "THERMAL FLIR PAYLOAD", self.active_heli['flir'])
        self.spec_light = self._add_spec_item(grid_box, g_sizer, "SEARCHLIGHT", self.active_heli['searchlight'])
        
        grid_box.SetSizer(g_sizer)
        sizer.Add(grid_box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        
        sizer.AddSpacer(16)
        
        # Maintenance Box
        maint_hdr = wx.StaticText(panel, label="AIRWORTHINESS & SCHEDULED MAINTENANCE")
        maint_hdr.SetForegroundColour(Theme.ACCENT_ORANGE)
        maint_hdr.SetFont(Theme.get_font(size=9, bold=True))
        sizer.Add(maint_hdr, 0, wx.LEFT | wx.RIGHT, 20)
        sizer.AddSpacer(6)
        
        self.maint_text = wx.StaticText(panel, label=f"Avionics Diagnostic: PASS • Gearbox Oil Pressure: NOMINAL • {self.active_heli['maint_due']}")
        self.maint_text.SetForegroundColour(Theme.TEXT_SECONDARY)
        self.maint_text.SetFont(Theme.get_font(size=9))
        sizer.Add(self.maint_text, 0, wx.LEFT | wx.RIGHT, 20)
        
        sizer.AddStretchSpacer(1)
        
        # Action Buttons
        act_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        fuel_btn = wx.Button(panel, label="AUTHORIZE PRE-FLIGHT REFUEL")
        fuel_btn.SetBackgroundColour(Theme.ACCENT_ORANGE)
        fuel_btn.SetForegroundColour(Theme.TEXT_PRIMARY)
        fuel_btn.SetFont(Theme.get_font(size=9, bold=True))
        act_sizer.Add(fuel_btn, 1, wx.RIGHT, 10)
        
        inspect_btn = wx.Button(panel, label="DIAGNOSTIC RUN TEST")
        inspect_btn.SetBackgroundColour(Theme.BG_CARD_ALT)
        inspect_btn.SetForegroundColour(Theme.TEXT_PRIMARY)
        inspect_btn.SetFont(Theme.get_font(size=9))
        act_sizer.Add(inspect_btn, 1)
        
        sizer.Add(act_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 20)
        
        panel.SetSizer(sizer)
        return panel

    def _add_spec_item(self, parent, sizer, label, value):
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

    def _on_select_heli(self, heli_data):
        self.active_heli = heli_data
        for c in self.card_widgets:
            c.set_selected(c.heli_data['id'] == heli_data['id'])
            
        self.heli_title.SetLabel(heli_data['name'].upper())
        self.heli_status.SetLabel(f"CALLSIGN: {heli_data['callsign']} • {heli_data['status']}")
        self.heli_status.SetForegroundColour(heli_data['status_color'])
        self.spec_engines.SetLabel(heli_data['engines'])
        self.spec_speed.SetLabel(f"{heli_data['max_speed']} / {heli_data['range']}")
        self.spec_rotor.SetLabel(heli_data['rotor_dia'])
        self.spec_hoist.SetLabel(heli_data['hoist'])
        self.spec_flir.SetLabel(heli_data['flir'])
        self.spec_light.SetLabel(heli_data['searchlight'])
        self.maint_text.SetLabel(f"Avionics Diagnostic: PASS • Gearbox Oil Pressure: NOMINAL • {heli_data['maint_due']}")
        self.spec_panel.Layout()
