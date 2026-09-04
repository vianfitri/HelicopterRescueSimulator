"""
Helicopter Rescue Simulator - Theme & Color Definitions
Modern Cockpit & Tactical Dark Theme with Safety Orange Accents
"""
import wx


class Theme:
    # --- Base Dark Colors ---
    BG_MAIN = wx.Colour(17, 19, 23)           # #111317: Deep carbon cockpit dark
    BG_HEADER = wx.Colour(23, 26, 32)         # #171A20: Subtle contrast for top title bar
    BG_SIDEBAR = wx.Colour(21, 24, 30)        # #15181E: Left navigation background
    BG_SIDEBAR_ACTIVE = wx.Colour(34, 39, 51) # #222733: Active item background
    BG_SIDEBAR_HOVER = wx.Colour(28, 32, 40)  # #1C2028: Item hover background
    
    BG_CARD = wx.Colour(26, 30, 38)           # #1A1E26: Content cards & panels
    BG_CARD_ALT = wx.Colour(31, 36, 46)       # #1F242E: Alternate card / sub-panel
    BG_CARD_HOVER = wx.Colour(35, 41, 52)     # #232934: Interactive card hover
    BG_INPUT = wx.Colour(19, 22, 28)          # #13161C: Input / readout background
    
    # --- Borders ---
    BORDER_SUBTLE = wx.Colour(43, 49, 61)     # #2B313D
    BORDER_LIGHT = wx.Colour(59, 67, 82)      # #3B4352
    BORDER_ACTIVE = wx.Colour(255, 94, 19)    # Safety Orange border
    
    # --- Accent Palette (SAR / High-Viz Safety Orange) ---
    ACCENT_ORANGE = wx.Colour(255, 94, 19)    # #FF5E13: International Safety Orange
    ACCENT_ORANGE_LIGHT = wx.Colour(255, 122, 56) # #FF7A38: Hover / Highlight
    ACCENT_ORANGE_DARK = wx.Colour(217, 72, 6)   # #D94806: Pressed state
    ACCENT_ORANGE_DIM = wx.Colour(255, 94, 19, 45) # Translucent glow
    
    # --- Status Indicators ---
    STATUS_GREEN = wx.Colour(32, 201, 151)    # Operational / Systems Normal
    STATUS_AMBER = wx.Colour(245, 159, 0)     # Standby / Caution
    STATUS_RED = wx.Colour(250, 82, 82)       # Mayday / Emergency / Alert
    STATUS_CYAN = wx.Colour(34, 184, 207)     # Radar / Sensors / Telemetry
    
    # --- Typography Colors ---
    TEXT_PRIMARY = wx.Colour(255, 255, 255)   # Crisp white
    TEXT_SECONDARY = wx.Colour(203, 213, 225) # Cool gray / Secondary
    TEXT_MUTED = wx.Colour(129, 142, 155)     # Dim label / Muted
    TEXT_ACCENT = wx.Colour(255, 122, 56)     # Orange text highlight

    # --- Typography Helpers ---
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
