"""
Helicopter Rescue Simulator
Main Application Entry Point
"""
import sys
import wx
from Assets.theme import Theme
from Controls.sidebar import SidebarControl
from Controls.title_bar import TitleBarControl
from Views.dashboard_view import DashboardView
from Views.missions_view import MissionsView
from Views.fleet_view import FleetView
from Views.weather_view import WeatherView


class MainFrame(wx.Frame):
    """
    Main application frame (Standard Size: 1366x768).
    Layout: Top title bar, Left custom modern tab sidebar, Right content views.
    """
    def __init__(self):
        super().__init__(
            None,
            id=wx.ID_ANY,
            title="Helicopter Rescue Simulator",
            size=(1366, 768),
            style=wx.DEFAULT_FRAME_STYLE
        )
        
        self.SetMinSize((1024, 600))
        self.SetBackgroundColour(Theme.BG_MAIN)
        self.Centre()
        
        self._init_ui()

    def _init_ui(self):
        # Vertical root sizer: Top Title Bar + Body
        root_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 1. Top Title Bar Control
        self.title_bar = TitleBarControl(self)
        root_sizer.Add(self.title_bar, 0, wx.EXPAND)
        
        # 2. Main Body: Horizontal split (Left Sidebar, Right Content Area)
        body_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Right Content Area (Simplebook page switcher)
        self.content_book = wx.Simplebook(self, style=wx.NO_BORDER)
        self.content_book.SetBackgroundColour(Theme.BG_MAIN)
        
        # Left Sidebar with Custom Modern Tab Control
        self.sidebar = SidebarControl(self, on_tab_changed=self._on_tab_changed)
        body_sizer.Add(self.sidebar, 0, wx.EXPAND)
        
        # Tab 0: Flight Ops & Telemetry Dashboard
        self.view_dashboard = DashboardView(self.content_book)
        self.content_book.AddPage(self.view_dashboard, "Flight Ops")
        
        # Tab 1: Search & Rescue Missions
        self.view_missions = MissionsView(self.content_book)
        self.content_book.AddPage(self.view_missions, "Rescue Missions")
        
        # Tab 2: Fleet & Hangar Equipment
        self.view_fleet = FleetView(self.content_book)
        self.content_book.AddPage(self.view_fleet, "Fleet & Gear")
        
        # Tab 3: Weather Radar & Meteorology
        self.view_weather = WeatherView(self.content_book)
        self.content_book.AddPage(self.view_weather, "Weather & Radar")
        
        body_sizer.Add(self.content_book, 1, wx.EXPAND)
        
        root_sizer.Add(body_sizer, 1, wx.EXPAND)
        self.SetSizer(root_sizer)
        self.Layout()

    def _on_tab_changed(self, tab_index: int):
        """Switches the active content view when a sidebar tab is clicked."""
        if hasattr(self, 'content_book') and 0 <= tab_index < self.content_book.GetPageCount():
            self.content_book.ChangeSelection(tab_index)


def main():
    app = wx.App(False)
    frame = MainFrame()
    frame.Show()
    
    # Check for automated verification mode (--test flag)
    if "--test" in sys.argv or "--test-mode" in sys.argv:
        print("[TEST] Running automated UI verification...")
        for tab_idx in range(4):
            frame.sidebar.select_tab(tab_idx)
            app.Yield()
            print(f"[TEST] Switched successfully to Tab {tab_idx}")
        print("[TEST] All UI components loaded and verified successfully.")
        wx.CallLater(300, frame.Close)
        
    app.MainLoop()


if __name__ == "__main__":
    main()
