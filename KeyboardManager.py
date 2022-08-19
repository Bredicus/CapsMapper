# keyboard
# MIT License

# Copyright (c) 2016 BoppreH

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# license: https://github.com/boppreh/keyboard/blob/8e9fc77c26638c94e2965f6554934dd1a0936f2f/LICENSE.txt

import keyboard
import ctypes
import keycodes

class KeyboardManager:
    def __init__(self, remaps: dict, activate_on_arr: list = [], suppress_state: bool = False, toggle_key_index: int = 0) -> None: 
        self.remaps = remaps
        self.activate_on_arr = activate_on_arr
        self.suppress_state = suppress_state
        self.toggle_callbacks = []
        self._callbacks = []

        vc_lock_keys = [
            0x14,   # VK_CAPITAL
            0x90,   # VK_NUMLOCK
            0x91    # VK_SCROLL
        ]

        sc_lock_keys = [
            58,   # SC_CAPITAL
            69,   # SC_NUMLOCK
            70    # SC_SCROLL
        ]

        if toggle_key_index < 0 or toggle_key_index > (len(vc_lock_keys) - 1):
            toggle_key_index = 0

        self.toggle_key_vk = vc_lock_keys[toggle_key_index]
        self.toggle_key_sc = sc_lock_keys[toggle_key_index]
        
        self.state = None
        self.active_state = True
        self.activate_on_state = True
        self.reset_lock_key_state()


    def reset_lock_key_state(self) -> None:
        hllDll = ctypes.WinDLL ("User32.dll")

        GetKeyState = hllDll.GetKeyState 
        GetKeyState.argtypes = (ctypes.c_int,)
        GetKeyState.restype = ctypes.wintypes.USHORT
        self.state = GetKeyState(self.toggle_key_vk)

        while self.state not in [0, 1]:
            self.state = GetKeyState(self.toggle_key_vk)


    def set_lock_key_hook(self, suppress: bool = False) -> None:
        keyboard.on_press_key(self.toggle_key_sc, self.toggle_mapping, suppress)


    def set_mapping(self, state: int = None) -> None:
        if None == state:
            state = self.state
        self.remap_keys() if 1 == state else self.clear_remap()


    def add_toggle_callback(self, cb) -> None:
        self.toggle_callbacks.append(cb)


    def toggle_mapping(self, event: keyboard._keyboard_event.KeyboardEvent) -> None:
        if 1 == self.state:
            self.state = 0
        else:
            self.state = 1

        self.set_mapping()

        for cb_func in self.toggle_callbacks:
            cb_func(self.state)

    
    def set_suppress_state(self, state: bool) -> None:
        self.suppress_state = state

        if False == state:
            self.reset_lock_key_state()


    def clear_remap(self) -> None:
        keyboard.unhook_all()
        suppress = False

        if True == self.suppress_state and True == self.active_state and True == self.activate_on_state:
            suppress = True
        
        self.set_lock_key_hook(suppress)


    def set_remaps(self, remaps: dict) -> None:
        self.remaps = remaps


    def remap_keys(self) -> None:
        if True == self.active_state and True == self.activate_on_state:
            for key, val in self.remaps.items():
                src = keycodes.cpKeyToCode.get(key, False)
                dst = keycodes.cpKeyToCode.get(val, False)
                if False != src and False != dst:
                    keyboard.remap_key(src, dst)


    def set_activate_on_arr(self, arr: list) -> None:
        self.activate_on_arr = arr

    
    def active_window_toggle_callback(self, act_prog_path: str) -> int:
        enable_keys = -1
        for ch in ["/", "\\"]:
            if ch in act_prog_path:
                act_prog_path = act_prog_path.replace(ch, '')
        act_prog_path = act_prog_path.lower()
        act_prog_path = act_prog_path.strip()
        if len(self.activate_on_arr) > 0:
            self.activate_on_state = False
            for path in self.activate_on_arr:
                if act_prog_path == path:
                    self.activate_on_state = True
                    break

            enable_keys = 0
            if True == self.activate_on_state and 1 == self.state:
                enable_keys = 1

            self.set_mapping(enable_keys)
        
        return enable_keys


    def get_key_press(self, callback, suppress: bool = False) -> None:
        keyboard.on_press(callback, suppress)

    
    def unhook_all(self) -> None:
        keyboard.unhook_all()

    
    def pause_remaps(self, state: int) -> None:
        self.active_state = state

        remap_state = 0
        if True == self.active_state and 1 == self.state:
            remap_state = 1
        
        self.set_mapping(remap_state)
