"""

    Decode ScreenApp
        Displays and manages different screens
        
    
"""

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.config import Config
from kivy.clock import Clock

import config
from main import Main

import logging
from PIL.ImageChops import screen

# ==== global instances ====

app = None
api_url = config.SERVER_CONFIG['prod']
backend = Main(api_url)
backend.start()

# ==== SETTINGS ==== #

Config.set('graphics', 'width', '768')
Config.set('graphics', 'height', '1366')
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', '30')
Config.set('graphics', 'top', '30')
Config.write()

""" NOTES
    
        - first screen start without logic etc. TODO: either introduce a starting screen of tie in with Kivy logic
    
"""

SCREENS = [
        
        {
            'name' : 'start',
            'image' : 'assets/start.png',
            'action' : {
                    'loop_func' : None, # function to execute and loop untill there is data
                    'on_data_command' : 'NEXT_SCREEN', # when receiving data
                    'on_data_param' : 'start'
                }
        },
        {
            'name' : 'reading',
            'image' : 'assets/reading.png',
            'action' : {
                    'loop_func' : backend.get_mrz,
                    'on_data_command' : 'NEXT_SCREEN',
                    'on_data_param' : 'qr-code'
                }
        },
        {
            'name' : 'qr-code',
            'image' : 'assets/scan.png',
            'action' : {
                    'loop_func' : backend.test_loop,
                    'on_data_command' : 'NEXT_SCREEN',
                    'on_data_param' : 'start'
                }
        },
        
    ]


# ====


class ScreenApp(App):
    
    # NOTE: don't make a __init__() - follow structure of App parent class ( study super() workings of Kivy )
    # this could work:
    """
        def __init__(self):
        super(Main, self).__init__()
    """
    
        
    # ----
    
    def build(self):
        
        # build 
        
        self.screen_definitions = SCREENS # screen definition objects
        self.screens = [] # screen objects that are succesfully added
        self.cur_screen_index = 0
        self.cur_screen = None
        self.cur_loop_handler = None
        self.setup_screen_manager()
        self.data = {} # data score across all screen
        
        # init 
        self.setup()
        
        return self.screen_manager
        
    # ----
    
    def setup(self):
        
        self.setup_logger()
        self.make_screens()
        
    # ----
    
    def setup_screen_manager(self):
        
        self.screen_manager = ScreenManager()
        self.screen_manager._keyboard = Window.request_keyboard(self._keyboard_closed, self.screen_manager) # see: https://github.com/kivy/kivy/issues/4746
        self.screen_manager._keyboard.bind(on_key_down=self._on_keyboard_down)
        
    # ----
    
    def _keyboard_closed(self):
        
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
        
    # ----

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        
        if keycode[1] == 'spacebar':
            self.get_current_screen_info()
            self.goto_next_screen()
        
        return True
        
    # ----
    
    def setup_logger(self):
                
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level=logging.INFO)
        
        try:
            # logger handlers
            handler = logging.StreamHandler()
            handler.setLevel(logging.INFO) # does something?
            formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)-4s %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        except Exception as e:
            self.logger.error(e)
        
    # ----
    
    def make_screens(self):
        
        for screen_definition in self.screen_definitions:
            
            print screen_definition
            
            if screen_definition.get('name') is not None and screen_definition.get('image') is not None:
                
                screen = Screen(name=screen_definition.get('name') )
            
                self.logger.info("Make screen with image: {0}".format(screen_definition.get('image')))
                img = Image(source=screen_definition.get('image'))
                screen.add_widget(img)
                self.screen_manager.add_widget(screen)
                
                # succesful added screens
                self.screens.append(screen_definition)
                
                # set first screen
                if self.cur_screen is None:
                    self.cur_screen = screen_definition
                    
            else:
                
                self.logger.error("WARNING: screen definition has no name {0} or image {1}".format(screen_definition.get('name'), screen_definition.get('image')))

        
    # ----
        
    def set_loop_handler(self, screen):
        
        self.logger.info("=> set_loop_handler")
        
        Clock.unschedule(self.cur_loop_handler)
        self.cur_loop_handler = Clock.schedule_interval(self.do_loop, 1)
        
    # ----
    
    def do_loop(self, df):
        
        # df is time difference since last call
        
        print '==== loop action ===='
        
        loop_func = None
        on_data_command = None
        on_data_param = None
        if self.cur_screen.get('action'):
            loop_func = self.cur_screen.get('action').get('loop_func')
            on_data_command = self.cur_screen.get('action').get('on_data_command')
            on_data_param = self.cur_screen.get('action').get('on_data_param')
        
        if loop_func:
            self.logger.info("ScreenApp: do_loop: run '{}'".format(loop_func.__name__))
            # result = loop_func(self.data) # we provide the current data store to processes
            result = loop_func()
        
            if result is not None: 
                self.logger.info("result: {0}".format(result))
                # trigger command
                self.handle_on_data( on_data_command, on_data_param)
            else:
                # do nothing
                pass
        else:
            self.logger.info("ScreenApp: do_loop: no loop_func for screen '{0}'".format(self.cur_screen.get('name'))) 
           
    # ----
    
    def handle_on_data(self, on_data_command, on_data_param):
        
        CMD_TO_FUNC_MAP = {
                'NEXT_SCREEN' : self.goto_screen_name,
                # TODO
            }         
        
        cmd_action = CMD_TO_FUNC_MAP.get(on_data_command)
        
        if cmd_action is None:
            self.logger.error("ScreenApp: ERROR: on_data_handler no known 'on_data' command: {0}".format(on_data_command))
            return False
        
        cmd_action(on_data_param) # do action
    
    # ----
    
    def goto_screen_name(self, name):
        
        self.goto_screen( self.get_screen_by_name(name))
    
    # ----
    
    def goto_screen(self, screen):
        
        self.logger.info("ScreenApp: goto screen '{0}'".format(screen.get('name')) )
        
        self.cur_screen = screen
        self.cur_screen_index = self.screens.index(screen)
        self.screen_manager.current = screen.get('name') # # activate screen in screen manager
        
        self.set_loop_handler(self.cur_screen)
    
    
    # ----
    
    def goto_next_screen(self):
        
        if self.cur_screen_index < len(self.screens) - 1:
            
            self.goto_screen( self.screens[self.cur_screen_index+1])
    
            
    # ----
    
    def get_current_screen_info(self):
        
        self.logger.info('Current screen: "{0}" with index: {1}'.format(self.cur_screen.get('name'), self.cur_screen_index))
        
    # ----
    
    def get_screen_by_name(self, name):
        
        for screen_definition in self.screens:
            
            if screen_definition.get('name') == name:
                return screen_definition
        
        self.logger.error("Cannot find screen with name '{0'}".format(name))
        return None

        
# ==== MAIN ====

if __name__ == '__main__':
    
    app = ScreenApp().run() # app is global 
    