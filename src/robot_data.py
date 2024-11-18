import json

DEFAULT_ROBOT_CONFIG = { "paired_status": "paired" }
DEFAULT_MODULES = {}
DEFAULT_MBH = []
DEFAULT_SCHEDULE = {}

class RobotData:
    def __init__(self):
        global DEFAULT_MODULES
        global DEFAULT_SCHEDULE
        self._robot_map = {}
        with open('default_data_modules.json') as f:
            DEFAULT_MODULES = json.load(f)
        with open('default_data_schedule.json') as f:
            DEFAULT_SCHEDULE = json.load(f)
        with open('default_data_settings.json') as f:
            DEFAULT_ROBOT_CONFIG['settings'] = json.load(f)

    def get_config(self, robot_id):
        robot_rec = self._robot_map.get(robot_id, {})
        return robot_rec.get("config", DEFAULT_ROBOT_CONFIG)

    def get_modules(self, robot_id):
        robot_rec = self._robot_map.get(robot_id, {})
        return robot_rec.get("modules", DEFAULT_MODULES)

    def get_mbh(self, robot_id):
        robot_rec = self._robot_map.get(robot_id, {})
        return robot_rec.get("mentor_behaviors", DEFAULT_MBH)

    def get_schedule(self, robot_id):
        robot_rec = self._robot_map.get(robot_id, {})
        return robot_rec.get("schedule", DEFAULT_SCHEDULE)


if __name__ == "__main__":
    data = RobotData()
    print(f"Default rb config: {data.get_config('fakedevice')}")
    print(f"Default modules  {data.get_modules('fakedevice')}")
    print(f"Default schedule  {data.get_schedule('fakedevice')}")
