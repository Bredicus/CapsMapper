from ProfileManager import ProfileManager
from KeyboardManager import KeyboardManager
from CapsMapper_gui import CapsMapper
import icons
import sys
import os
import base64
import ctypes
import ctypes.wintypes

icon_off = 'IconGray.ico'
if not os.path.isfile(icon_off): 
    icon_data = base64.b64decode(icons.APP_ICON_OFF)
    new_icon_file = open(icon_off,"wb")
    new_icon_file.write(icon_data)
    new_icon_file.close()

icon_on = 'IconBlack.ico'
if not os.path.isfile(icon_on): 
    icon_data = base64.b64decode(icons.APP_ICON_ON)
    new_icon_file = open(icon_on,"wb")
    new_icon_file.write(icon_data)
    new_icon_file.close()

del icons.APP_ICON
del icons.APP_ICON_ON
del icons.APP_ICON_OFF

def toggle_callback(state):
    global gui
    gui.update_tray_icon(state)

profileManager = ProfileManager('CapsMapper.json')
keyboardManager = KeyboardManager(profileManager.get_remaps(), profileManager.get_fixed_activate_on(), profileManager.get_suppress_lock_state())
keyboardManager.add_toggle_callback(toggle_callback)
gui = CapsMapper(icon_on, icon_off, keyboardManager, profileManager)

EVENT_SYSTEM_FOREGROUND = 0x0003
WINEVENT_OUTOFCONTEXT = 0x0000

user32 = ctypes.windll.user32
ole32 = ctypes.windll.ole32

ole32.CoInitialize(0)

WinEventProcType = ctypes.WINFUNCTYPE(
    None, 
    ctypes.wintypes.HANDLE,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.HWND,
    ctypes.wintypes.LONG,
    ctypes.wintypes.LONG,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.DWORD
)

def callback(hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
    global keyboardManager
    global gui

    pid = ctypes.wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

    path = os.popen('wmic process where "ProcessId=' + str(pid.value) + '" get ExecutablePath').read()
    for ch in ["b'ExecutablePath", "ExecutablePath", "\\r\\n"]:
        if ch in path:
            path = path.replace(ch, '')    

    path = path[:-1]
    path = path.strip()
    keyboardManager.active_window_toggle_callback(path)

WinEventProc = WinEventProcType(callback)

user32.SetWinEventHook.restype = ctypes.wintypes.HANDLE
hook = user32.SetWinEventHook(
    EVENT_SYSTEM_FOREGROUND,
    EVENT_SYSTEM_FOREGROUND,
    0,
    WinEventProc,
    0,
    0,
    WINEVENT_OUTOFCONTEXT
)
if hook == 0:
    sys.exit(1)

gui.run()

user32.UnhookWinEvent(hook)
ole32.CoUninitialize()
