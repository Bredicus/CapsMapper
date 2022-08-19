# pystray
# Copyright (C) 2016-2022 Moses Palmér
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# license: https://github.com/moses-palmer/pystray/blob/master/COPYING

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image
from pystray import MenuItem as item
import pystray
import webbrowser
import KeyboardManager as KeyboardManager
import ProfileManager
import keycodes

class CapsMapper:
    def __init__(self, icon_on, icon_off, keyboardManager: KeyboardManager, profileManager: ProfileManager, start: bool = False) -> None:
        self.icon_on = icon_on
        self.icon_off = icon_off
        self.keyboardManager = keyboardManager
        self.profileManager = profileManager

        self.root = Tk()
        self.icon = None

        self.labels_dic = {}

        self.pop_open = False
        self.pop_profile_open = False
        self.pop_activate_for_open = False
        self.activate_for_browser_open = False

        self.key_current = ""
        self.key_new = ""

        self.build_menu()
        self.build_gui()

        if True == start:
            self.run()

    def run(self):
        self.root.geometry(f'{1047}x{380}+{int(self.root.winfo_screenwidth()/2 - 1047/2)}+{int(self.root.winfo_screenheight()/2 - 380/2)}')
        self.root.resizable(False, False)
        self.root.attributes('-toolwindow', True)
        self.root.iconbitmap(default=self.icon_on)
        self.root.configure(background="light gray")

        self.set_labels()

        suppress = False
        if True == self.profileManager.active_profile["suppress"]:
            suppress = True
        self.keyboardManager.set_lock_key_hook(suppress)

        self.update_title()
        self.root.protocol('WM_DELETE_WINDOW', self.hide_window)
        self.hide_window()

        self.root.mainloop()


    def update_title(self):
        self.root.title("CapsMapper" + ("" if "default" == self.profileManager.active_profile["profile"].lower() else (": " + self.profileManager.active_profile["profile"])))


    def add_normal_key(self, btn_text, key_val, btn_width, lbl_text, loc_x, loc_y):
        Button(self.root, text=btn_text, font='san 9 bold', anchor='n', width=btn_width, height=3, command=lambda: self.set_key_mapping(key_val)).place(x=loc_x, y=loc_y)
        self.labels_dic[key_val] = Label(self.root, text=lbl_text)
        self.labels_dic[key_val].place(x=(loc_x+2), y=(loc_y+33))


    def add_lock_key(self, btn_text, btn_width, loc_x, loc_y):
        key = Button(self.root, text=btn_text, font='san 9 bold', anchor='n', width=btn_width, height=3, state=DISABLED)
        key.config(disabledforeground='red')
        key.place(x=loc_x, y=loc_y)


    def set_key_mapping(self, key):
        if True == self.pop_open:
            return

        self.pop_open = True

        self.pop = Toplevel(self.root)
        self.pop.title("Set Key: " + keycodes.cpKeyToDisplayName.get(key, key))
        self.pop.geometry(f'{275}x{150}+{int(self.root.winfo_screenwidth()/2 - 275/2)}+{int(self.root.winfo_screenheight()/2 - 150/2)}')
        self.pop.protocol("WM_DELETE_WINDOW", self.confirm_remap)
        self.pop.resizable(False, False)
        
        pop_label = Label(self.pop, text="Press a key: ")
        pop_label.pack(pady=10)

        self.pop_label_remap = Label(self.pop, text="")
        self.pop_label_remap.pack(pady=10)

        pop_frame = Frame(self.pop)
        pop_frame.pack(pady=5)

        pop_frame_accept_btn = Button(pop_frame, text="Accept", command=lambda: self.confirm_remap(1))
        pop_frame_accept_btn.grid(row=1, column=0, padx=4, pady=2)
        pop_frame_cancel_btn = Button(pop_frame, text="Cancel", command=lambda: self.confirm_remap())
        pop_frame_cancel_btn.grid(row=1, column=1, padx=4, pady=2)

        self.key_current = key

        self.keyboardManager.get_key_press(self.set_remap, True)


    def confirm_remap(self, val = 0): 
        if 1 == val:
            if "" == self.key_new:
                self.key_new = self.key_current

            if self.key_current == self.key_new and self.key_new in self.profileManager.remaps:
                self.profileManager.remaps.pop(self.key_new)

            if self.key_current != self.key_new:
                self.profileManager.remaps[self.key_current] = self.key_new

            self.keyboardManager.set_remaps(self.profileManager.get_remaps())

            self.profileManager.cp_edit = True
            self.labels_dic[self.key_current]['text'] = self.key_new

        self.pop.destroy()

        self.key_current = ""
        self.key_new = ""

        self.pop_open = False


    def set_remap(self, event):
        keyset = keycodes.GetKeySet(event)

        if False != keyset:
            self.key_new = keyset.key
            self.pop_label_remap['text'] = keycodes.cpKeyToDisplayName.get(self.key_new, self.key_new)


    def add_new_profile(self):
        if True == self.pop_profile_open:
            return

        self.pop_profile_open = True

        self.pop_profile = Toplevel(self.root)
        self.pop_profile.title("Profile Name")
        self.pop_profile.geometry(f'{275}x{150}+{int(self.root.winfo_screenwidth()/2 - 275/2)}+{int(self.root.winfo_screenheight()/2 - 150/2)}')
        self.pop_profile.protocol("WM_DELETE_WINDOW", self.save_new_profile)
        self.pop_profile.resizable(False, False)
        
        pop_label = Label(self.pop_profile, text="Make sure to save changes before you contineu.\nEnter the Profile Name")
        pop_label.pack(pady=5)

        self.pop_profile_input = Entry(self.pop_profile)
        self.pop_profile_input.pack(pady=5)

        self.pop_profile_label = Label(self.pop_profile, text="")
        self.pop_profile_label.pack(pady=5)
        self.pop_profile_label.config(fg='red')

        pop_frame = Frame(self.pop_profile)
        pop_frame.pack(pady=5)

        pop_frame_accept_btn = Button(pop_frame, text="Accept", command=lambda: self.save_new_profile(1))
        pop_frame_accept_btn.grid(row=1, column=0, padx=4, pady=2)
        pop_frame_cancel_btn = Button(pop_frame, text="Cancel", command=lambda: self.save_new_profile())
        pop_frame_cancel_btn.grid(row=1, column=1, padx=4, pady=2)


    def change_profile(self):
        self.save_changes_messagebox()

        self.profileManager.change_active_profile(self.profilemenu_select.get())

        self.keyboardManager.clear_remap()
        self.profileManager.save_active_profile_settings()

        self.update_title()
        self.set_labels()

        self.keyboardManager.set_remaps(self.profileManager.get_remaps())
        self.keyboardManager.set_activate_on_arr(self.profileManager.get_fixed_activate_on())


    def save_new_profile(self, val = 0):
        if 1 == val:
            input = self.pop_profile_input.get()
            if "" == input:
                self.pop_profile_label["text"] = "You Must Enter a Profile Name"
                return

            if "Default" == input or "default" == input:
                self.pop_profile_label["text"] = "Profile Name is Invalid"
                return

            if False != self.profileManager.all_profiles.get(input, False):
                self.pop_profile_label["text"] = "Profile Already Exists"
                return

            copy_profile = False
            MsgBox = messagebox.askquestion('New Profile', 'Carry over current settings and remaps?' + "\n" +  'Any unsaved changes will be lost if not or carried over to the new profile.', icon = 'warning')
            if MsgBox == 'yes':
                copy_profile = True


            self.profileManager.new_profile(input, copy_profile)
            self.keyboardManager.set_remaps(self.profileManager.get_remaps())
            self.keyboardManager.set_activate_on_arr(self.profileManager.get_fixed_activate_on())

            if True == copy_profile:
                self.keyboardManager.clear_remap()
                self.set_labels()

            
            self.update_title()
            self.add_profile_to_menu(input)


        self.pop_profile_label["text"] = ""
        self.pop_profile_open = False
        self.pop_profile.destroy()


    def delete_profile(self):
        if self.profileManager.active_profile["profile"] not in ["Default", "default"]:
            MsgBox = messagebox.askquestion('Delete Profile', 'Are you sure you wish to permanently delete the profile: ' + self.profileManager.active_profile["profile"], icon = 'warning')
            if MsgBox == 'yes':

                self.profileManager.delete_current_profile()
                self.keyboardManager.set_remaps(self.profileManager.get_remaps())
                self.keyboardManager.set_activate_on_arr(self.profileManager.get_fixed_activate_on())
                self.keyboardManager.clear_remap()
                self.profilemenu.delete(self.profileManager.active_profile["profile"])
                self.update_title()
                self.set_labels()


    def open_activate_for_chooser(self):
        if True == self.activate_for_browser_open:
            return

        self.activate_for_browser_open = True

        filename = filedialog.askopenfilename(title='Pick file to launch', initialdir='/')
        item_added = self.profileManager.add_activate_on_item(filename)
        self.keyboardManager.set_activate_on_arr(self.profileManager.get_fixed_activate_on())

        if True == item_added:
            self.listbox.insert(-1, filename)
            self.listbox.see(0)

        self.activate_for_browser_open = False
        self.pop_activate_for.lift()


    def remove_activate_on_path(self):
        if self.listbox.curselection():
            selected_item = self.listbox.get(self.listbox.curselection())
            item_removed = self.profileManager.remove_activate_on_item(selected_item)
            self.keyboardManager.set_activate_on_arr(self.profileManager.get_fixed_activate_on())

            if True == item_removed:
                self.listbox.delete(self.listbox.curselection()[0])


    def reset_activate_for(self):
        self.pop_activate_for_open = False
        self.listbox = None
        self.pop_activate_for.destroy()


    def launch_activate_for_window(self):
        if True == self.pop_activate_for_open:
            return

        self.pop_activate_for_open = True

        self.pop_activate_for = Toplevel(self.root)
        self.pop_activate_for.title("Activate Profile Settings")
        self.pop_activate_for.geometry(f'{550}x{200}+{int(self.root.winfo_screenwidth()/2 - 550/2)}+{int(self.root.winfo_screenheight()/2 - 200/2)}')
        self.pop_activate_for.protocol("WM_DELETE_WINDOW", self.reset_activate_for)
        self.pop_activate_for.resizable(False, False)

        Label(self.pop_activate_for, text="The current profile will only be enabled if one of the following applications is the active window:", anchor='w', font="Helvetica 8 bold").pack(fill='both', padx=5, pady=5)      

        btn_frame = Frame(self.pop_activate_for)
        Button(btn_frame, text="Browse", command=lambda: self.open_activate_for_chooser()).pack(padx=5)
        Button(btn_frame, text="Delete", command=lambda: self.remove_activate_on_path(), bg="RED", fg="WHITE").pack(padx=5, pady=(100, 1))

        list_frame = Frame(self.pop_activate_for)
        scollbar = Scrollbar(list_frame, orient=VERTICAL)
        self.listbox = Listbox(list_frame, width=(550 - 100), yscrollcommand=scollbar.set)

        btn_frame.pack(side=LEFT)
        scollbar.config(command=self.listbox.yview)
        scollbar.pack(side=RIGHT, fill=Y)
        list_frame.pack(padx=5)
        self.listbox.pack()

        if self.profileManager.activate_on.get(self.profileManager.active_profile["profile"], False):
            for key, path in self.profileManager.activate_on[self.profileManager.active_profile["profile"]].items():
                self.listbox.insert(-1, path)


    def toggle_suppress_capslock(self):
        suppress_state = self.profileManager.toggle_suppress_lock_key()
        self.keyboardManager.set_suppress_state(suppress_state)
        self.keyboardManager.clear_remap()


    def save_changes_messagebox(self):
        if True == self.profileManager.has_unsaved_changes():
            MsgBox = messagebox.askquestion('Save Changes?', 'The current profile has been modified.' + "\n" +  'Do you wish to save the current profile before continuing?', icon = 'warning')
            if MsgBox == 'yes':
                self.profileManager.save_profile()


    def exit_app(self):
        self.save_changes_messagebox()

        self.keyboardManager.unhook_all()

        try:
            self.icon.stop()
        except NameError:
            pass
        
        try:
            self.root.destroy()
        except NameError:
            pass


    def get_image(self, state = False):
        path = self.icon_on if state else self.icon_off
        return Image.open(path)
        

    def update_tray_icon(self, state = None):
        if None == state:
            state = self.keyboardManager.state
        self.icon.icon = self.get_image(state)


    def add_profile_to_menu(self, key):
        self.profilemenu.add_radiobutton(label=key, variable=self.profilemenu_select, value=key, command=lambda: self.change_profile())
        self.profilemenu_select.set(key)


    def open_webpage(self, url = "https://capsmapper.com"):
        webbrowser.open(url)


    def open_about(self):
        aboutstr = """
        Version: 0.1.1\n
        Code:    3.10.4
        \n
        CapsMapper.com
        """
        messagebox.showinfo("CapsMapper", aboutstr)


    def set_labels(self, profile = False):
        for k in self.labels_dic:
            self.labels_dic[k]['text'] = keycodes.cpKeyToDisplayName.get(k, k)

        for k, v in self.profileManager.remaps.items():
            self.labels_dic[k]['text'] = v


    def pause_remaps(self, icon, item):
        self.keyboardManager.pause_remaps(not item.checked)


    def show_window(self, icon, item):
        self.keyboardManager.clear_remap()
        icon.stop()
        self.root.deiconify()


    def quit_window(self, icon, item):
        self.profileManager.cp_edit = False
        self.exit_app()


    def hide_window(self):
        self.save_changes_messagebox()

        if True == self.pop_open:
            self.pop.destroy()
            self.pop_open = False

        if True == self.pop_profile_open:
            self.pop_profile.destroy()
            self.pop_profile_open = False

        if True == self.pop_activate_for_open:
            self.pop_activate_for.destroy()
            self.pop_activate_for_open = False

        self.keyboardManager.set_mapping()

        menu = (item('Active', self.pause_remaps, checked=lambda item: self.keyboardManager.active_state), item('Show', self.show_window), item('Quit', self.quit_window))
        img = self.get_image(self.keyboardManager.state)
        self.root.withdraw()

        self.icon = pystray.Icon("CapsMapper", img, "CapsMapper", menu)
        self.icon.run()


    def build_menu(self):
        menubar = Menu(self.root)

        filemenu = Menu(menubar, tearoff=0)

        filemenu.add_command(label="New", command=lambda: self.add_new_profile())

        self.profilemenu = Menu(menubar, tearoff=0)
        self.profilemenu_select = StringVar()

        for key in self.profileManager.all_profiles:
            self.profilemenu.add_radiobutton(label=key, variable=self.profilemenu_select, value=key, command=lambda: self.change_profile())
        filemenu.add_cascade(label="Load", menu=self.profilemenu)

        self.profilemenu_select.set(self.profileManager.active_profile["profile"])

        filemenu.add_command(label="Save", command=lambda: self.profileManager.save_profile())
        filemenu.add_command(label="Delete", command=lambda: self.delete_profile())
        filemenu.add_separator()

        filemenu.add_command(label="Activate for ...", command=lambda: self.launch_activate_for_window())
        filemenu.add_separator()        

        suppress_caps = BooleanVar()
        suppress_caps.set(self.profileManager.active_profile['suppress'])
        filemenu.add_checkbutton(label="Suppress Capslock", onvalue=True, offvalue=False, variable=suppress_caps, command=lambda: self.toggle_suppress_capslock())
        filemenu.add_separator()

        self.run_on_startup = BooleanVar()
        self.run_on_startup.set(self.profileManager.get_win_startup())
        filemenu.add_checkbutton(label="Run on Startup", onvalue=True, offvalue=False, variable=self.run_on_startup, command=lambda: self.profileManager.toggle_win_startup())
        filemenu.add_separator()
        
        filemenu.add_command(label="Exit", command=lambda: self.exit_app())

        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help", command=lambda: self.open_webpage())
        helpmenu.add_command(label="About", command=lambda: self.open_about())
        menubar.add_cascade(label="Help", menu=helpmenu)

        donatemenu = Menu(menubar, tearoff=0)
        donatemenu.add_command(label="Donate on PayPal", command=lambda: self.open_webpage('https://www.paypal.com/donate/?hosted_button_id=LGXG2KR33LGT8'))
        donatemenu.add_command(label="Buy Me a Coffee", command=lambda: self.open_webpage('https://www.buymeacoffee.com/eddyb'))
        menubar.add_cascade(label="Donate", menu=donatemenu)

        self.root.config(menu=menubar)


    def build_gui(self):
        self.add_normal_key("esc", "esc", 8, "esc", 1, 2)

        self.add_normal_key("F1", "f1", 8, "f1", 140, 2)
        self.add_normal_key("F2", "f2", 8, "f2", 210, 2)
        self.add_normal_key("F3", "f3", 8, "f3", 280, 2)
        self.add_normal_key("F4", "f4", 8, "f4", 350, 2)

        self.add_normal_key("F5", "f5", 8, "f5", 455, 2)
        self.add_normal_key("F6", "f6", 8, "f6", 525, 2)
        self.add_normal_key("F7", "f7", 8, "f7", 595, 2)
        self.add_normal_key("F8", "f8", 8, "f8", 665, 2)

        self.add_normal_key("F9", "f9", 8, "f9", 770, 2)
        self.add_normal_key("F10", "f10", 8, "f10", 840, 2)
        self.add_normal_key("F11", "f11", 8, "f11", 910, 2)
        self.add_normal_key("F12", "f12", 8, "f12", 980, 2)

        self.add_normal_key("`", "tic", 8, "`", 1, 95)

        self.add_normal_key("1", "1", 8, "1", 70, 95)
        self.add_normal_key("2", "2", 8, "2", 140, 95)
        self.add_normal_key("3", "3", 8, "3", 210, 95)
        self.add_normal_key("4", "4", 8, "4", 280, 95)
        self.add_normal_key("5", "5", 8, "5", 350, 95)
        self.add_normal_key("6", "6", 8, "6", 420, 95)
        self.add_normal_key("7", "7", 8, "7", 490, 95)
        self.add_normal_key("8", "8", 8, "8", 560, 95)
        self.add_normal_key("9", "9", 8, "9", 630, 95)
        self.add_normal_key("0", "0", 8, "0", 700, 95)

        self.add_normal_key("-", "minus", 8, "-", 770, 95)
        self.add_normal_key("=", "equal", 8, "=", 840, 95)
        self.add_normal_key("Backspace", "backspace", 18, "backspace", 910, 95)

        self.add_normal_key("Tab", "tab", 13, "tab", 1, 152)

        self.add_normal_key("Q", "q", 8, "q", 105, 152)
        self.add_normal_key("W", "w", 8, "w", 175, 152)
        self.add_normal_key("E", "e", 8, "e", 245, 152)
        self.add_normal_key("R", "r", 8, "r", 315, 152)
        self.add_normal_key("T", "t", 8, "t", 385, 152)
        self.add_normal_key("Y", "y", 8, "y", 455, 152)
        self.add_normal_key("U", "u", 8, "u", 525, 152)
        self.add_normal_key("I", "i", 8, "i", 595, 152)
        self.add_normal_key("O", "o", 8, "o", 665, 152)
        self.add_normal_key("P", "p", 8, "p", 735, 152)

        self.add_normal_key("[", "open_bracket", 8, "[", 805, 152)
        self.add_normal_key("]", "close_bracket", 8, "]", 875, 152)
        self.add_normal_key("\\", "backslash", 13, "\\", 945, 152)

        self.add_lock_key("Caps Lock", 16, 1, 209)

        self.add_normal_key("A", "a", 8, "a", 125, 209)
        self.add_normal_key("S", "s", 8, "s", 195, 209)
        self.add_normal_key("D", "d", 8, "d", 265, 209)
        self.add_normal_key("F", "f", 8, "f", 335, 209)
        self.add_normal_key("G", "g", 8, "g", 405, 209)
        self.add_normal_key("H", "h", 8, "h", 475, 209)
        self.add_normal_key("J", "j", 8, "j", 545, 209)
        self.add_normal_key("K", "k", 8, "k", 615, 209)
        self.add_normal_key("L", "l", 8, "l", 685, 209)

        self.add_normal_key(";", "semicolon", 8, ";", 755, 209)
        self.add_normal_key("'", "quote", 8, "'", 825, 209)
        self.add_normal_key("Enter", "enter", 20, "enter", 895, 209)

        self.add_normal_key("Shift", "Lshift", 21, "Lshift", 1, 266)

        self.add_normal_key("Z", "z", 8, "z", 160, 266)
        self.add_normal_key("X", "x", 8, "x", 230, 266)
        self.add_normal_key("C", "c", 8, "c", 300, 266)
        self.add_normal_key("V", "v", 8, "v", 370, 266)
        self.add_normal_key("B", "b", 8, "b", 440, 266)
        self.add_normal_key("N", "n", 8, "n", 510, 266)
        self.add_normal_key("M", "m", 8, "m", 580, 266)

        self.add_normal_key(",", "comma", 8, ",", 650, 266)
        self.add_normal_key(".", "period", 8, ".", 720, 266)
        self.add_normal_key("/", "slash", 8, "/", 790, 266)
        self.add_normal_key("Shift", "Rshift", 25, "Rshift", 860, 266)

        self.add_normal_key("Ctrl", "Lctrl", 11, "Lctrl", 1, 323)
        self.add_normal_key("Win", "Lwin", 11, "Lwin", 90, 323)
        self.add_normal_key("Alt", "Lalt", 11, "Lalt", 180, 323)
        self.add_normal_key("__________", "space", 58, "space", 270, 323)
        self.add_normal_key("Alt", "Ralt", 11, "Ralt", 688, 323)
        self.add_normal_key("Win", "Rwin", 11, "Rwin", 778, 323)
        self.add_normal_key("Menu", "menu", 11, "menu", 868, 323)
        self.add_normal_key("Ctrl", "Rctrl", 11, "Rctrl", 958, 323)
        
