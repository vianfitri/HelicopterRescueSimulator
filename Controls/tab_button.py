"""
Helicopter Rescue Simulator - Custom Modern Tab Button
Double-buffered owner-drawn button with Safety Orange active indicator and hover feedback.
"""
import wx
import wx.lib.newevent
from Assets.theme import Theme
from Assets.icons import IconRenderer

# Define custom tab event
TabSelectEvent, EVT_TAB_SELECTED = wx.lib.newevent.NewCommandEvent()


class TabButton(wx.Panel):
    """
    Modern tactical tab button control for wxPython.
    Displays an icon, primary title, subtitle, and an active Safety Orange indicator bar.
    """
    def __init__(self, parent, tab_id: int, label: str, subtitle: str, icon_type: str):
        super().__init__(parent, id=wx.ID_ANY, style=wx.NO_BORDER)
        self.tab_id = tab_id
        self.label = label
        self.subtitle = subtitle
        self.icon_type = icon_type
        
        self.is_selected = False
        self.is_hovered = False
        
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.SetDoubleBuffered(True)
        self.SetMinSize((220, 60))
        self.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        
        # Event bindings
        self.Bind(wx.EVT_PAINT, self._on_paint)
        self.Bind(wx.EVT_ENTER_WINDOW, self._on_enter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self._on_leave)
        self.Bind(wx.EVT_LEFT_DOWN, self._on_click)

    def set_selected(self, selected: bool):
        if self.is_selected != selected:
            self.is_selected = selected
            self.Refresh()

    def _on_enter(self, event):
        self.is_hovered = True
        self.Refresh()
        event.Skip()

    def _on_leave(self, event):
        self.is_hovered = False
        self.Refresh()
        event.Skip()

    def _on_click(self, event):
        # Fire custom event to parent
        evt = TabSelectEvent(self.GetId(), tab_id=self.tab_id)
        evt.SetEventObject(self)
        self.GetEventHandler().ProcessEvent(evt)
        event.Skip()

    def _on_paint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        if not gc:
            return

        w, h = self.GetClientSize()

        # 1. Background color determination
        if self.is_selected:
            bg_color = Theme.BG_SIDEBAR_ACTIVE
        elif self.is_hovered:
            bg_color = Theme.BG_SIDEBAR_HOVER
        else:
            bg_color = Theme.BG_SIDEBAR

        # Fill background with slightly rounded rect if hovered/selected
        gc.SetBrush(wx.Brush(bg_color))
        gc.SetPen(wx.NullPen)
        gc.DrawRoundedRectangle(4, 2, w - 8, h - 4, 6)

        # 2. Left Active Indicator (Safety Orange Bar)
        if self.is_selected:
            indicator_pen = wx.NullPen
            indicator_brush = wx.Brush(Theme.ACCENT_ORANGE)
            gc.SetPen(indicator_pen)
            gc.SetBrush(indicator_brush)
            # Rounded indicator strip on left
            bar_w = 4
            bar_h = h - 16
            bar_y = 8
            gc.DrawRoundedRectangle(6, bar_y, bar_w, bar_h, 2)
        elif self.is_hovered:
            # Subtle accent indicator on hover
            gc.SetPen(wx.NullPen)
            gc.SetBrush(wx.Brush(wx.Colour(Theme.ACCENT_ORANGE.Red(),
                                          Theme.ACCENT_ORANGE.Green(),
                                          Theme.ACCENT_ORANGE.Blue(), 120)))
            gc.DrawRoundedRectangle(6, 12, 3, h - 24, 1.5)

        # 3. Draw Vector Icon
        icon_size = 24.0
        icon_x = 22.0
        icon_y = (h - icon_size) / 2.0

        if self.is_selected:
            icon_color = Theme.ACCENT_ORANGE
        elif self.is_hovered:
            icon_color = Theme.TEXT_PRIMARY
        else:
            icon_color = Theme.TEXT_MUTED

        if self.icon_type == 'flight':
            IconRenderer.draw_flight_ops(gc, icon_x, icon_y, icon_size, icon_color)
        elif self.icon_type == 'missions':
            IconRenderer.draw_missions(gc, icon_x, icon_y, icon_size, icon_color)
        elif self.icon_type == 'fleet':
            IconRenderer.draw_fleet(gc, icon_x, icon_y, icon_size, icon_color)
        elif self.icon_type == 'weather':
            IconRenderer.draw_weather(gc, icon_x, icon_y, icon_size, icon_color)

        # 4. Text Labels (Title & Subtitle)
        text_x = 58.0
        
        # Primary Title
        if self.is_selected:
            title_font = Theme.get_font(size=10, bold=True)
            title_color = Theme.TEXT_PRIMARY
        elif self.is_hovered:
            title_font = Theme.get_font(size=10, bold=True)
            title_color = Theme.TEXT_PRIMARY
        else:
            title_font = Theme.get_font(size=10, bold=False)
            title_color = Theme.TEXT_SECONDARY

        gc.SetFont(title_font, title_color)
        gc.DrawText(self.label, text_x, h / 2.0 - 16)

        # Subtitle
        sub_font = Theme.get_font(size=8, bold=False)
        sub_color = Theme.TEXT_MUTED if not self.is_selected else Theme.TEXT_SECONDARY
        gc.SetFont(sub_font, sub_color)
        gc.DrawText(self.subtitle, text_x, h / 2.0 + 3)

        # 5. Selected Right Arrow Indicator (Subtle Chevron)
        if self.is_selected:
            gc.SetPen(wx.Pen(Theme.ACCENT_ORANGE, 2))
            arrow_x = w - 18
            arrow_y = h / 2.0
            arrow_path = gc.CreatePath()
            arrow_path.MoveToPoint(arrow_x - 3, arrow_y - 4)
            arrow_path.AddLineToPoint(arrow_x + 1, arrow_y)
            arrow_path.AddLineToPoint(arrow_x - 3, arrow_y + 4)
            gc.StrokePath(arrow_path)
