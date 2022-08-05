import os
import json
import subprocess

class Config:
    def __init__(self):
        with open('config.json') as f:
            config = json.load(f)
        
        self.host = config['host']
        self.password = config['password']
        self.port = str(config['port'])

class Obs:
    def __init__(self, config):
        self.config = config
        self.scene_list = self.get_scene_list()
        self.current_scene = self.get_current_scene()

    def refresh(self):
        self.scene_list = self.get_scene_list()
        self.current_scene = self.get_current_scene()

    def get_scene_list(self):
        return self.command(['scene', 'list']).split('\n')[:-1]

    def get_current_scene(self):
        return self.command(['scene', 'get']).split('\n')[0]

    def switch_scene(self, scene):
        return self.command(['scene', 'switch', scene]).split('\n')[0]

    def command(self, args):
        base_command = [
            'obs-cli',
            '--host', self.config.host,
            '--password', self.config.password,
            '--port', self.config.port
        ]
        result = subprocess.check_output(
            base_command + args
        )
        return result.decode("utf-8")

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

def main():
    config = Config()
    obs = Obs(config)
    while True:
        obs.refresh()
        clear()
        print(f'OBS Scenes ({obs.config.host})')
        print('')
        for i,scene in enumerate(obs.scene_list):
            if obs.current_scene == scene:
                print(f'{i+1}: {scene} (active)')
            else:
                print(f'{i+1}: {scene}')
        print('')
        c = input('Switch scenes. Enter scene number and press [ENTER]: ')
        try:
            if int(c):
                obs.switch_scene(
                    obs.scene_list[int(c)-1]
                )
        except:
            pass

if __name__ == "__main__":
    main()
