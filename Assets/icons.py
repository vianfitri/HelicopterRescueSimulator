"""
Helicopter Rescue Simulator - Vector Icon Renderer
Draws modern, crisp vector icons using wx.GraphicsContext.
"""
import math
import wx
from .theme import Theme


class IconRenderer:
    @staticmethod
    def draw_flight_ops(gc: wx.GraphicsContext, x: float, y: float, size: float, color: wx.Colour):
        """Draws Flight Operations / Horizon & Wings icon."""
        gc.SetPen(wx.Pen(color, 2))
        gc.SetBrush(wx.NullBrush)
        
        # Outer ring or horizon arc
        r = size * 0.45
        cx, cy = x + size / 2.0, y + size / 2.0
        gc.DrawEllipse(cx - r, cy - r, r * 2, r * 2)
        
        # Center pitch dot
        gc.SetBrush(wx.Brush(color))
        gc.DrawEllipse(cx - 2, cy - 2, 4, 4)
        gc.SetBrush(wx.NullBrush)
        
        # Horizon / Aircraft symbol (Wings & Center Pip)
        path = gc.CreatePath()
        path.MoveToPoint(cx - r * 0.7, cy)
        path.AddLineToPoint(cx - r * 0.25, cy)
        path.AddLineToPoint(cx - r * 0.25, cy + 3)
        
        path.MoveToPoint(cx + r * 0.25, cy + 3)
        path.AddLineToPoint(cx + r * 0.25, cy)
        path.AddLineToPoint(cx + r * 0.7, cy)
        gc.StrokePath(path)

    @staticmethod
    def draw_missions(gc: wx.GraphicsContext, x: float, y: float, size: float, color: wx.Colour):
        """Draws Search & Rescue / Target Crosshair icon."""
        gc.SetPen(wx.Pen(color, 2))
        gc.SetBrush(wx.NullBrush)
        
        cx, cy = x + size / 2.0, y + size / 2.0
        r = size * 0.42
        
        # Target circle
        gc.DrawEllipse(cx - r, cy - r, r * 2, r * 2)
        
        # Inner rescue beacon cross
        gc.SetPen(wx.Pen(color, 2))
        path = gc.CreatePath()
        # Crosshair ticks
        path.MoveToPoint(cx, cy - r - 2)
        path.AddLineToPoint(cx, cy - r * 0.4)
        
        path.MoveToPoint(cx, cy + r * 0.4)
        path.AddLineToPoint(cx, cy + r + 2)
        
        path.MoveToPoint(cx - r - 2, cy)
        path.AddLineToPoint(cx - r * 0.4, cy)
        
        path.MoveToPoint(cx + r * 0.4, cy)
        path.AddLineToPoint(cx + r + 2, cy)
        gc.StrokePath(path)
        
        # Center target dot
        gc.SetBrush(wx.Brush(color))
        gc.DrawEllipse(cx - 2.5, cy - 2.5, 5, 5)

    @staticmethod
    def draw_fleet(gc: wx.GraphicsContext, x: float, y: float, size: float, color: wx.Colour):
        """Draws Helicopter Silhouette & Rotor icon."""
        gc.SetPen(wx.Pen(color, 2))
        gc.SetBrush(wx.NullBrush)
        
        cx, cy = x + size / 2.0, y + size / 2.0
        
        # Main rotor line (horizontal)
        path = gc.CreatePath()
        path.MoveToPoint(cx - size * 0.45, cy - size * 0.28)
        path.AddLineToPoint(cx + size * 0.45, cy - size * 0.28)
        
        # Rotor mast
        path.MoveToPoint(cx, cy - size * 0.28)
        path.AddLineToPoint(cx, cy - size * 0.12)
        
        # Fuselage (Cabin & Tail Boom)
        # Cabin oval / shape
        path.MoveToPoint(cx - size * 0.25, cy - size * 0.05)
        path.AddQuadCurveToPoint(cx - size * 0.35, cy + size * 0.15, cx - size * 0.1, cy + size * 0.22)
        path.AddLineToPoint(cx + size * 0.15, cy + size * 0.20)
        # Tail boom
        path.AddLineToPoint(cx + size * 0.42, cy + size * 0.05)
        path.AddLineToPoint(cx + size * 0.42, cy - size * 0.1)
        path.AddLineToPoint(cx + size * 0.15, cy - size * 0.1)
        path.CloseSubpath()
        
        # Tail rotor
        path.MoveToPoint(cx + size * 0.42, cy - size * 0.18)
        path.AddLineToPoint(cx + size * 0.42, cy + size * 0.02)
        
        # Landing skids
        path.MoveToPoint(cx - size * 0.28, cy + size * 0.32)
        path.AddLineToPoint(cx + size * 0.18, cy + size * 0.32)
        # Skid struts
        path.MoveToPoint(cx - size * 0.15, cy + size * 0.22)
        path.AddLineToPoint(cx - size * 0.15, cy + size * 0.32)
        path.MoveToPoint(cx + size * 0.05, cy + size * 0.21)
        path.AddLineToPoint(cx + size * 0.05, cy + size * 0.32)
        
        gc.StrokePath(path)

    @staticmethod
    def draw_weather(gc: wx.GraphicsContext, x: float, y: float, size: float, color: wx.Colour):
        """Draws Weather Radar Sweep / Storm Scanner icon."""
        gc.SetPen(wx.Pen(color, 2))
        gc.SetBrush(wx.NullBrush)
        
        cx, cy = x + size / 2.0, y + size / 2.0
        r = size * 0.42
        
        # Radar circles
        gc.DrawEllipse(cx - r, cy - r, r * 2, r * 2)
        gc.DrawEllipse(cx - r * 0.55, cy - r * 0.55, r * 1.1, r * 1.1)
        
        # Radar sweep beam
        path = gc.CreatePath()
        path.MoveToPoint(cx, cy)
        angle = -40 * (math.pi / 180)
        sweep_x = cx + r * math.cos(angle)
        sweep_y = cy + r * math.sin(angle)
        path.AddLineToPoint(sweep_x, sweep_y)
        gc.StrokePath(path)
        
        # Center hub
        gc.SetBrush(wx.Brush(color))
        gc.DrawEllipse(cx - 2, cy - 2, 4, 4)

    @staticmethod
    def draw_helicopter_badge(gc: wx.GraphicsContext, x: float, y: float, width: float, height: float):
        """Draws the SAR Tactical Header Emblem with Safety Orange accent."""
        cx, cy = x + width / 2.0, y + height / 2.0
        
        # Hexagonal / Shield background
        shield_h = height * 0.85
        shield_w = width * 0.85
        
        # Shield Path
        path = gc.CreatePath()
        path.MoveToPoint(cx - shield_w * 0.45, cy - shield_h * 0.4)
        path.AddLineToPoint(cx + shield_w * 0.45, cy - shield_h * 0.4)
        path.AddLineToPoint(cx + shield_w * 0.45, cy + shield_h * 0.1)
        path.AddLineToPoint(cx, cy + shield_h * 0.48)
        path.AddLineToPoint(cx - shield_w * 0.45, cy + shield_h * 0.1)
        path.CloseSubpath()
        
        # Fill shield subtle dark
        gc.SetBrush(wx.Brush(Theme.BG_CARD_ALT))
        gc.SetPen(wx.Pen(Theme.ACCENT_ORANGE, 2))
        gc.DrawPath(path)
        
        # Draw stylized rescue star / cross
        cross_pen = wx.Pen(Theme.ACCENT_ORANGE, 3)
        gc.SetPen(cross_pen)
        cross_path = gc.CreatePath()
        c_size = min(shield_w, shield_h) * 0.28
        
        # Vertical bar
        cross_path.MoveToPoint(cx, cy - c_size)
        cross_path.AddLineToPoint(cx, cy + c_size * 0.6)
        # Horizontal bar
        cross_path.MoveToPoint(cx - c_size * 0.8, cy - c_size * 0.2)
        cross_path.AddLineToPoint(cx + c_size * 0.8, cy - c_size * 0.2)
        gc.StrokePath(cross_path)
