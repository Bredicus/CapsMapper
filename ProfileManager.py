import json
import os.path

class ProfileManager:
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        
        config = self.get_config()
        self.active_profile = config["active"]
        self.all_profiles = config["profiles"]
        self.activate_on = config["activate_on"]
        self.activate_on_arr = self.get_activate_on_arr()
        self.remaps = self.all_profiles.get(self.active_profile["profile"], {})

        self.cp_edit = False

        if self.get_win_startup():
            self.set_win_startup()


    def config_file_exists(self, path: str) -> bool:
        if os.path.isfile(path):
            return True
        else:
            return False


    def get_default_config(self) -> dict:
        return {
            "active": {
                "profile": "Default", 
                "suppress": False
            },
            "profiles": {},
            "activate_on": {}
        } 


    def get_config(self) -> dict:
        if self.config_file_exists(self.file_path):
            with open(self.file_path) as f:
                try:
                    data = json.load(f)
                except ValueError as e:
                    return self.get_default_config()
                
                test_active = data.get("active", False)
                if False != test_active:
                    test_profile = test_active.get("profile", False)
                    test_profiles = data.get("profiles", False)
                    test_activate = data.get("activate_on", False)

                    test_suppress = test_active.get("suppress", False)
                    data['active']['suppress'] = test_suppress

                    if False != test_profile and False != test_profiles:
                        active_profile_exists = False
                        for key in test_profiles:
                            if test_profile == key:
                                active_profile_exists = True

                        if False == active_profile_exists:
                            data["active"]["profile"] = "Default"

                        if False == test_activate:
                            data["activate_on"] = {}
                        
                        return data
        
        return self.get_default_config()


    def json_write_to_file(self, file: str, data: dict) -> None:
        with open(file, 'w') as f:
            json.dump(data, f, indent=4)


    def save_active_profile_settings(self) -> None:
        data = self.get_config()
        data["active"] = self.active_profile
        self.json_write_to_file(self.file_path, data)

    
    def save_activate_on_profile_settings(self) -> None:
        data = self.get_config()
        data["activate_on"][self.active_profile["profile"]] = self.activate_on.get(self.active_profile["profile"], {})
        self.json_write_to_file(self.file_path, data)
        self.activate_on_arr = self.get_activate_on_arr()


    def save_profile(self) -> None:
        self.cp_edit = False
        data = self.get_config()
        data["active"] = self.active_profile
        data["profiles"][self.active_profile["profile"]] = self.remaps
        data["activate_on"][self.active_profile["profile"]] = self.activate_on.get(self.active_profile["profile"], {})
        self.json_write_to_file(self.file_path, data)


    def get_activate_on_arr(self) -> list:
        new_list = []
        if self.activate_on.get(self.active_profile["profile"], False):
            for key, path in self.activate_on[self.active_profile["profile"]].items():
                for ch in ["/", "\\"]:
                    if ch in path:
                        path = path.replace(ch, '')
                path = path.lower()
                path = path.strip()
                new_list.append(path)
        return new_list
        

    def change_active_profile(self, new_profile: str) -> None:
        self.cp_edit = False
        self.active_profile["profile"] = new_profile
        self.remaps = self.all_profiles.get(self.active_profile["profile"], {})
        self.activate_on_arr = self.get_activate_on_arr()


    def new_profile(self, new_profile_name: str, copy: bool = False) -> None:
        previous_profile = self.active_profile["profile"]
        self.active_profile["profile"] = new_profile_name

        if True == copy:
            self.all_profiles[new_profile_name] = self.remaps
            self.activate_on[new_profile_name] = self.activate_on.get(previous_profile, {})
        else:
            self.all_profiles[new_profile_name] = {}
            self.activate_on[new_profile_name] = {}
            self.remaps = {}

        self.activate_on_arr = self.get_activate_on_arr()
        self.save_profile()


    def delete_current_profile(self) -> None:
        data = self.get_config()
        data["active"]["profile"] = "Default"
        del data["profiles"][self.active_profile["profile"]]
        del data["activate_on"][self.active_profile["profile"]]
        self.activate_on_arr = self.get_activate_on_arr()

        self.json_write_to_file(self.file_path, data)

        self.activate_on.pop(self.active_profile["profile"], None)
        self.cp_edit = False
        self.active_profile["profile"] = "Default"
        self.remaps = {}


    def add_activate_on_item(self, filename: str) -> bool:
        item_added = False
        if '' != filename and filename not in self.activate_on[self.active_profile["profile"]].values():

            items = list(self.activate_on[self.active_profile["profile"]].keys())
            if 0 == len(items):
                new_key = 0
            else:
                new_key = int(items[-1]) + 1

            self.activate_on[self.active_profile["profile"]][str(new_key)] = filename
            self.save_activate_on_profile_settings() 
            item_added = True
        
        return item_added


    def remove_activate_on_item(self, file_path: str) -> bool:
        item_removed = False
        if self.activate_on.get(self.active_profile["profile"], False):
            delete_key = -1
            for key, path in self.activate_on[self.active_profile["profile"]].items():
                if file_path == path:
                    delete_key = int(key)
                    break

            if delete_key >= 0:
                del self.activate_on[self.active_profile["profile"]][str(delete_key)]
                self.save_activate_on_profile_settings()
                item_removed = True

        return item_removed


    def get_fixed_activate_on(self) -> list:
        return self.activate_on_arr


    def get_remaps(self) -> dict:
        return self.remaps


    def get_suppress_lock_state(self) -> bool:
        return self.active_profile['suppress']


    def toggle_suppress_lock_key(self) -> bool:
        self.active_profile['suppress'] = not self.active_profile['suppress']
        self.save_active_profile_settings()
        return self.active_profile['suppress']


    def has_unsaved_changes(self) -> bool:
        unsaved_changes = False
        if True == self.cp_edit and self.active_profile["profile"] not in ["Default", "default"]:
            unsaved_changes = True

        return unsaved_changes


    def get_win_startup(self) -> bool:
        path = os.path.join('C:' + os.sep, 'Users', os.getlogin(), 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup', 'capsmapper_start.bat')
        return os.path.exists(path)


    def set_win_startup(self) -> None:
        file_name = 'CapsMapper.exe'
        output = os.popen('wmic process get description, processid').read()
        output = output.splitlines()

        for line in output:
            line = ' '.join(line.split())

            if len(line) > 0 and line.startswith(file_name):
                path = os.popen('wmic process where "ProcessId=' + line.split()[1] + '" get ExecutablePath').read()
                for ch in ["b'ExecutablePath", "ExecutablePath", "\\r\\n", "\\" + file_name]:
                    if ch in path:
                        path = path.replace(ch, '')

                path = path[:-1]
                path = path.strip()
                
                file_path = os.path.join('C:' + os.sep, 'Users', os.getlogin(), 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup', 'capsmapper_start.bat')
                
                with open(file_path, 'w') as f:
                    f.write(r'cd %s' % path)
                    f.write('\n')
                    f.write(r'start "" "%s"' % file_name)
                
                break


    def toggle_win_startup(self) -> bool:
        path = os.path.join('C:' + os.sep, 'Users', os.getlogin(), 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup', 'capsmapper_start.bat')
        is_set = self.get_win_startup()
        if is_set:
            os.remove(path)
        else:  
            self.set_win_startup()
