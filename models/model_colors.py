import flet as ft

class LightTheme:
    BACKGROUND_PRIMARY = "#F5F7FA"
    BACKGROUND_SECONDARY = "#FFFFFF"
    BACKGROUND_TERTIARY = "#E8EDF2"
    
    TEXT_PRIMARY = "#1A202C"
    TEXT_SECONDARY = "#4A5568"
    TEXT_TERTIARY = "#718096"
    TEXT_DISABLED = "#A0AEC0"
    
    ACCENT_PRIMARY = "#2563EB"
    ACCENT_SECONDARY = "#3B82F6"
    ACCENT_LIGHT = "#DBEAFE"
    
    SUCCESS = "#10B981"
    SUCCESS_LIGHT = "#D1FAE5"
    WARNING = "#F59E0B"
    WARNING_LIGHT = "#FEF3C7"
    ERROR = "#EF4444"
    ERROR_LIGHT = "#FEE2E2"
    INFO = "#3B82F6"
    INFO_LIGHT = "#DBEAFE"
    
    BUTTON_PRIMARY = "#2563EB"
    BUTTON_PRIMARY_HOVER = "#1D4ED8"
    BUTTON_SECONDARY = "#6B7280"
    BUTTON_SECONDARY_HOVER = "#4B5563"
    BUTTON_SUCCESS = "#10B981"
    BUTTON_DANGER = "#EF4444"
    
    BORDER_PRIMARY = "#E5E7EB"
    BORDER_SECONDARY = "#D1D5DB"
    DIVIDER = "#E5E7EB"
    
    SHADOW = "#00000010"
    
    STOCK_HIGH = "#10B981"
    STOCK_MEDIUM = "#F59E0B"
    STOCK_LOW = "#EF4444"
    STOCK_OUT = "#6B7280"


class DarkTheme:
    BACKGROUND_PRIMARY = "#0F172A"
    BACKGROUND_SECONDARY = "#1E293B"
    BACKGROUND_TERTIARY = "#334155"
    
    TEXT_PRIMARY = "#F1F5F9"
    TEXT_SECONDARY = "#CBD5E1"
    TEXT_TERTIARY = "#94A3B8"
    TEXT_DISABLED = "#64748B"
    
    ACCENT_PRIMARY = "#3B82F6"
    ACCENT_SECONDARY = "#60A5FA"
    ACCENT_LIGHT = "#1E3A8A"
    
    SUCCESS = "#22C55E"
    SUCCESS_LIGHT = "#14532D"
    WARNING = "#FBBF24"
    WARNING_LIGHT = "#451A03"
    ERROR = "#F87171"
    ERROR_LIGHT = "#450A0A"
    INFO = "#60A5FA"
    INFO_LIGHT = "#1E3A8A"
    
    BUTTON_PRIMARY = "#3B82F6"
    BUTTON_PRIMARY_HOVER = "#2563EB"
    BUTTON_SECONDARY = "#475569"
    BUTTON_SECONDARY_HOVER = "#334155"
    BUTTON_SUCCESS = "#22C55E"
    BUTTON_DANGER = "#F87171"
    
    BORDER_PRIMARY = "#334155"
    BORDER_SECONDARY = "#475569"
    DIVIDER = "#334155"
    
    SHADOW = "#00000040"
    
    STOCK_HIGH = "#22C55E"
    STOCK_MEDIUM = "#FBBF24"
    STOCK_LOW = "#F87171"
    STOCK_OUT = "#64748B"


class ThemeManager:
    @staticmethod
    def get_theme(is_dark_mode: bool):
        return DarkTheme if is_dark_mode else LightTheme
    
    @staticmethod
    def apply_theme(page, is_dark_mode: bool):
        theme = ThemeManager.get_theme(is_dark_mode)
        page.bgcolor = theme.BACKGROUND_PRIMARY
        page.update()
        return theme