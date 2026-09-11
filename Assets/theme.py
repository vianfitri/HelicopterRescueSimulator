"""
Helicopter Rescue Simulator - Theme & Color Definitions
Supports Dynamic Cockpit Dark Mode and Clean Tactical Light Mode with Safety Orange Accents.
"""
import wx


class Theme:
    is_dark: bool = True

    # Current Active Colors (Default Dark)
    BG_MAIN: wx.Colour = wx.Colour(17, 19, 23)
    BG_HEADER: wx.Colour = wx.Colour(23, 26, 32)
    BG_SIDEBAR: wx.Colour = wx.Colour(21, 24, 30)
    BG_SIDEBAR_ACTIVE: wx.Colour = wx.Colour(34, 39, 51)
    BG_SIDEBAR_HOVER: wx.Colour = wx.Colour(28, 32, 40)
    
    BG_CARD: wx.Colour = wx.Colour(26, 30, 38)
    BG_CARD_ALT: wx.Colour = wx.Colour(31, 36, 46)
    BG_CARD_HOVER: wx.Colour = wx.Colour(35, 41, 52)
    BG_INPUT: wx.Colour = wx.Colour(19, 22, 28)
    
    BORDER_SUBTLE: wx.Colour = wx.Colour(43, 49, 61)
    BORDER_LIGHT: wx.Colour = wx.Colour(59, 67, 82)
    BORDER_ACTIVE: wx.Colour = wx.Colour(255, 94, 19)
    
    ACCENT_ORANGE: wx.Colour = wx.Colour(255, 94, 19)
    ACCENT_ORANGE_LIGHT: wx.Colour = wx.Colour(255, 122, 56)
    ACCENT_ORANGE_DARK: wx.Colour = wx.Colour(217, 72, 6)
    ACCENT_ORANGE_DIM: wx.Colour = wx.Colour(255, 94, 19, 45)
    
    STATUS_GREEN: wx.Colour = wx.Colour(32, 201, 151)
    STATUS_AMBER: wx.Colour = wx.Colour(245, 159, 0)
    STATUS_RED: wx.Colour = wx.Colour(250, 82, 82)
    STATUS_CYAN: wx.Colour = wx.Colour(34, 184, 207)
    
    TEXT_PRIMARY: wx.Colour = wx.Colour(255, 255, 255)
    TEXT_SECONDARY: wx.Colour = wx.Colour(203, 213, 225)
    TEXT_MUTED: wx.Colour = wx.Colour(129, 142, 155)
    TEXT_ACCENT: wx.Colour = wx.Colour(255, 122, 56)

    @classmethod
    def set_dark_mode(cls, is_dark: bool):
        """Switches between Dark Cockpit theme and Clean Tactical Light theme."""
        cls.is_dark = is_dark
        if is_dark:
            # --- Dark Cockpit Palette ---
            cls.BG_MAIN = wx.Colour(17, 19, 23)
            cls.BG_HEADER = wx.Colour(23, 26, 32)
            cls.BG_SIDEBAR = wx.Colour(21, 24, 30)
            cls.BG_SIDEBAR_ACTIVE = wx.Colour(34, 39, 51)
            cls.BG_SIDEBAR_HOVER = wx.Colour(28, 32, 40)
            
            cls.BG_CARD = wx.Colour(26, 30, 38)
            cls.BG_CARD_ALT = wx.Colour(31, 36, 46)
            cls.BG_CARD_HOVER = wx.Colour(35, 41, 52)
            cls.BG_INPUT = wx.Colour(19, 22, 28)
            
            cls.BORDER_SUBTLE = wx.Colour(43, 49, 61)
            cls.BORDER_LIGHT = wx.Colour(59, 67, 82)
            cls.BORDER_ACTIVE = wx.Colour(255, 94, 19)
            
            cls.ACCENT_ORANGE = wx.Colour(255, 94, 19)
            cls.ACCENT_ORANGE_LIGHT = wx.Colour(255, 122, 56)
            cls.ACCENT_ORANGE_DARK = wx.Colour(217, 72, 6)
            cls.ACCENT_ORANGE_DIM = wx.Colour(255, 94, 19, 45)
            
            cls.STATUS_GREEN = wx.Colour(32, 201, 151)
            cls.STATUS_AMBER = wx.Colour(245, 159, 0)
            cls.STATUS_RED = wx.Colour(250, 82, 82)
            cls.STATUS_CYAN = wx.Colour(34, 184, 207)
            
            cls.TEXT_PRIMARY = wx.Colour(255, 255, 255)
            cls.TEXT_SECONDARY = wx.Colour(203, 213, 225)
            cls.TEXT_MUTED = wx.Colour(129, 142, 155)
            cls.TEXT_ACCENT = wx.Colour(255, 122, 56)
        else:
            # --- Clean Tactical Light Palette ---
            cls.BG_MAIN = wx.Colour(241, 245, 249)        # #F1F5F9
            cls.BG_HEADER = wx.Colour(255, 255, 255)      # #FFFFFF
            cls.BG_SIDEBAR = wx.Colour(248, 250, 252)     # #F8FAFC
            cls.BG_SIDEBAR_ACTIVE = wx.Colour(254, 237, 222) # Soft orange tint
            cls.BG_SIDEBAR_HOVER = wx.Colour(237, 242, 247)
            
            cls.BG_CARD = wx.Colour(255, 255, 255)        # #FFFFFF
            cls.BG_CARD_ALT = wx.Colour(241, 245, 249)    # #F1F5F9
            cls.BG_CARD_HOVER = wx.Colour(237, 242, 247)
            cls.BG_INPUT = wx.Colour(241, 245, 249)
            
            cls.BORDER_SUBTLE = wx.Colour(226, 232, 240)  # #E2E8F0
            cls.BORDER_LIGHT = wx.Colour(203, 213, 225)   # #CBD5E1
            cls.BORDER_ACTIVE = wx.Colour(234, 88, 12)
            
            # High-visibility Safety Orange on light backgrounds
            cls.ACCENT_ORANGE = wx.Colour(234, 88, 12)    # #EA580C
            cls.ACCENT_ORANGE_LIGHT = wx.Colour(249, 115, 22)
            cls.ACCENT_ORANGE_DARK = wx.Colour(194, 65, 12)
            cls.ACCENT_ORANGE_DIM = wx.Colour(234, 88, 12, 45)
            
            cls.STATUS_GREEN = wx.Colour(13, 148, 136)    # #0D9488
            cls.STATUS_AMBER = wx.Colour(217, 119, 6)     # #D97706
            cls.STATUS_RED = wx.Colour(225, 29, 72)       # #E11D48
            cls.STATUS_CYAN = wx.Colour(8, 145, 178)      # #0891B2
            
            cls.TEXT_PRIMARY = wx.Colour(15, 23, 42)      # #0F172A (Deep Slate)
            cls.TEXT_SECONDARY = wx.Colour(51, 65, 85)    # #334155
            cls.TEXT_MUTED = wx.Colour(100, 116, 139)     # #64748B
            cls.TEXT_ACCENT = wx.Colour(234, 88, 12)

    @classmethod
    def toggle_theme(cls):
        """Toggles between Dark and Light mode."""
        cls.set_dark_mode(not cls.is_dark)
        return cls.is_dark

    @staticmethod
    def get_font(size=10, weight=wx.FONTWEIGHT_NORMAL, family=wx.FONTFAMILY_SWISS, bold=False):
        """Creates a modern Segoe UI font or system fallback."""
        w = wx.FONTWEIGHT_BOLD if bold else weight
        font = wx.Font(
            size,
            family,
            wx.FONTSTYLE_NORMAL,
            w,
            False,
            "Segoe UI"
        )
        return font

    @staticmethod
    def get_mono_font(size=10, bold=False):
        """Monospaced font for telemetry, coordinates, and timestamps."""
        w = wx.FONTWEIGHT_BOLD if bold else wx.FONTWEIGHT_NORMAL
        font = wx.Font(
            size,
            wx.FONTFAMILY_TELETYPE,
            wx.FONTSTYLE_NORMAL,
            w,
            False,
            "Consolas"
        )
        return font
