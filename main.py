import os
import random
from kivy.config import Config

# Танзими андозаи тиреза барои моделсозии телефон (дар компютер)
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', False)

from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDRaisedButton, MDFillRoundFlatButton, MDFlatButton
from kivymd.uix.list import MDList, OneLineAvatarListItem, ImageLeftWidget
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.slider import MDSlider
from kivy.uix.image import Image
from kivy.uix.screenmanager import SlideTransition
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivymd.icon_definitions import md_icons
# Модулҳо барои сохтани тирезаи Зум (Zoom Popup)
from kivy.uix.popup import Popup
from kivy.uix.scatter import Scatter
from kivy.uix.behaviors import ButtonBehavior

class ClickableImage(ButtonBehavior, Image):
    pass

# ==========================================
# ИМПОРТИ БАЗАҲО АЗ ФАЙЛҲОИ АЛОҲИДА
# ==========================================
try:
    import database_tg as db_tg
    import database_ru as db_ru
    import database_en as db_en
    
    DATABASES = {
        "tg": db_tg.counries,
        "ru": db_ru.counries,
        "en": db_en.counries
    }
except ImportError as e:
    print(f"Хатогӣ дар боркунии файлҳои база: {e}")
    # Базаи захиравӣ дар ҳолати набудани файлҳо
    DATABASES = {
        "tg": {"Давлатҳо": {}, "Дарёҳо": {}},
        "ru": {"Страны": {}, "Реки": {}},
        "en": {"Countries": {}, "Rivers": {}}
    }

# ТАРҶУМАИ ИНТЕРФЕЙСИ БАРНОМА
LANG_UI = {
    "tg": {
        "title": "Ҷуғрофия", "search": "Ҷустуҷӯ...", "settings": "Танзимот", 
        "games": "Интихоби Тезбинӣ (Бозиҳо)", "quiz": "Тест", "theme": "Иваз кардани Тема",
        "font": "Андозаи шрифт: {}", "timer_lbl": "Вақти тест (сония):", "result": "Натиҷа",
        "score": "Холи шумо: {}/{}", "close": "Пӯшидан", "zoom_title": "Намоиши расм (Зум)",
        "flag": "Парчам", "emblem": "Нишон", "game_btn": "Бозии {}", 
        "level_title": "Сатҳҳо: {}", "level_lbl": "🎯 Тест аз рӯи [b]{}[/b]:",
        "lvl_locked": "Сатҳи {}  🔒", "lvl_unlocked": "Сатҳи {}  🔓",
        "quiz_find": "[b]{}[/b]-ро барои [color=#2196F3]{}[/color] ёбед:", "q_timer": "Саволи {}/{} | Вақт: {}"
    },
    "ru": {
        "title": "География", "search": "Поиск...", "settings": "Настройки", 
        "games": "Выбор Игр (Игры)", "quiz": "Тест", "theme": "Сменить Тему",
        "font": "Размер шрифта: {}", "timer_lbl": "Время теста (сек):", "result": "Результат",
        "score": "Ваш балл: {}/{}", "close": "Закрыть", "zoom_title": "Просмотр изображения (Зум)",
        "flag": "Флаг", "emblem": "Герб", "game_btn": "Игра {}", 
        "level_title": "Уровни: {}", "level_lbl": "🎯 Тест по [b]{}[/b]:",
        "lvl_locked": "Уровень {}  🔒", "lvl_unlocked": "Уровень {}  🔓",
        "quiz_find": "Найдите [b]{}[/b] для [color=#2196F3]{}[/color]:", "q_timer": "Вопрос {}/{} | Время: {}"
    },
    "en": {
        "title": "Geography", "search": "Search...", "settings": "Settings", 
        "games": "Games Menu", "quiz": "Quiz", "theme": "Toggle Theme",
        "font": "Font size: {}", "timer_lbl": "Quiz timer (sec):", "result": "Result",
        "score": "Your score: {}/{}", "close": "Close", "zoom_title": "Image View (Zoom)",
        "flag": "Flag", "emblem": "Emblem", "game_btn": "{} Game", 
        "level_title": "Levels: {}", "level_lbl": "🎯 Quiz by [b]{}[/b]:",
        "lvl_locked": "Level {}  🔒", "lvl_unlocked": "Level {}  🔓",
        "quiz_find": "Find [b]{}[/b] for [color=#2196F3]{}[/color]:", "q_timer": "Question {}/{} | Time: {}"
    }
}

class MainScreen(MDScreen): pass

class DetailsScreen(MDScreen):
    def set_content(self, title, info, category):
        app = MDApp.get_running_app()
        tr = LANG_UI[app.lang]
        self.ids.toolbar.title = title
        img_dir = "images"
        
        self.ids.details_label.font_size = dp(app.font_size)
        self.ids.flag_img.source = os.path.join(img_dir, info.get('FlagFile', 'default.png'))
       
        # Муайян кардани категория новобаста аз забони интихобшуда
        if category in ["Давлатҳо", "Страны", "Countries", "Дарёҳо", "Реки", "Rivers"]:
            self.ids.image_grid.cols = 2
            self.ids.image_grid.height = dp(140)
            self.ids.emblem_container.opacity = 1
            self.ids.emblem_container.size_hint_x = 1
            self.ids.emblem_img.source = os.path.join(img_dir, info.get('EmblemFile', 'default.png'))
            self.ids.flag_label.text = tr["flag"]
            self.ids.emblem_label.text = tr["emblem"]
        else:
            self.ids.image_grid.cols = 1
            self.ids.image_grid.height = dp(250)
            self.ids.emblem_container.opacity = 0
            self.ids.emblem_container.size_hint_x = 0
            self.ids.flag_label.text = ""
            self.ids.emblem_label.text = ""

        text = f"[size={app.font_size + 4}][b]{title}[/b][/size]\n\n"
        for key, value in info.items():
            if "File" not in key:
                text += f"[b]{key}:[/b] {value}\n\n"
        self.ids.details_label.text = text

class GamesMenuScreen(MDScreen): pass
class LevelsScreen(MDScreen): pass
class SettingsScreen(MDScreen): pass
class QuizScreen(MDScreen): pass

class InfoApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        
        self.font_size = 18
        self.timer_seconds = 15
        self.time_left = self.timer_seconds
        
        # Сабти забон (базаи аввалия - тоҷикӣ)
        self.lang = "tg"
        self.store = JsonStore('game_progress.json')
        
        self.databases = DATABASES
        self.data = self.databases[self.lang]
        self.current_cat = list(self.data.keys())[0] if self.data.keys() else ""
        
        self.timer_event = None
        self.dialog = None

        self.sound_correct = SoundLoader.load('sounds/correct.mp3')
        self.sound_wrong = SoundLoader.load('sounds/wrong.mp3')

        self.sm = MDScreenManager(transition=SlideTransition())
        self.sm.add_widget(self.create_main_screen())
        self.sm.add_widget(self.create_details_screen())
        self.sm.add_widget(self.create_quiz_screen())
        self.sm.add_widget(self.create_games_menu())
        self.sm.add_widget(self.create_levels_screen())
        self.sm.add_widget(self.create_settings_screen())
        return self.sm

    # ==========================================
    # ФУНКСИЯИ АСОСӢ БАРОИ ИВАЗ КАРДАНИ ЗАБОН
    # ==========================================
    def change_language(self, lang_code):
        self.lang = lang_code
        self.data = self.databases[lang_code]  # Боркунии базаи нав
        
        if self.data.keys():
            self.current_cat = list(self.data.keys())[0]
        else:
            self.current_cat = ""
            
        tr = LANG_UI[self.lang]
        
        # Навсозии матнҳои интерфейс
        self.main_toolbar.title = tr["title"]
        self.search.hint_text = tr["search"]
        self.games_toolbar.title = tr["games"]
        self.settings_toolbar.title = tr["settings"]
        self.theme_btn.text = tr["theme"]
        self.font_lbl.text = tr["font"].format(self.font_size)
        self.timer_lbl.text = tr["timer_lbl"]
        
        # Азнавсозии ҳамаи тугмаҳо бо номҳои нави база
        self.rebuild_category_buttons()
        self.rebuild_games_menu_buttons()
        self.refresh_list()

    def create_main_screen(self):
        screen = MainScreen(name="main")
        layout = MDBoxLayout(orientation='vertical')
        self.main_toolbar = MDTopAppBar(
            title=LANG_UI[self.lang]["title"], 
            right_action_items=[["controller-classic", lambda x: self.change_screen("games_menu")], ["cog", lambda x: self.change_screen("settings")]]
        )
        layout.add_widget(self.main_toolbar)
        
        cat_scroll = MDScrollView(size_hint_y=None, height=dp(65))
        self.cat_box = MDBoxLayout(adaptive_width=True, padding=dp(8), spacing=dp(8))
        self.rebuild_category_buttons()
        cat_scroll.add_widget(self.cat_box); layout.add_widget(cat_scroll)
        
        self.search = MDTextField(hint_text=LANG_UI[self.lang]["search"], mode="round", size_hint_x=0.9, pos_hint={"center_x": 0.5})
        self.search.bind(text=self.refresh_list); layout.add_widget(self.search)
        
        scroll = MDScrollView(); self.list_view = MDList(); scroll.add_widget(self.list_view)
        layout.add_widget(scroll); screen.add_widget(layout); self.refresh_list(); return screen

    def rebuild_category_buttons(self):
        """Ин функсия тугмаҳои категорияро аз рӯи калидҳои базаи нав месозад"""
        self.cat_box.clear_widgets()
        for cat in self.data.keys():
            self.cat_box.add_widget(MDFillRoundFlatButton(text=cat, on_release=self.set_category))

    def set_category(self, instance): 
        self.current_cat = instance.text
        self.refresh_list()

    def refresh_list(self, *args):
        self.list_view.clear_widgets()
        search_text = self.search.text.lower().strip()
        img_dir = "images"
        
        count = 0
        if self.current_cat in self.data:
            for name in self.data[self.current_cat]:
                if name.lower().startswith(search_text):
                    info = self.data[self.current_cat][name]
                    img_name = info.get('FlagFile', 'default.png')
                    flag_path = os.path.join(img_dir, img_name)
                    
                    item = OneLineAvatarListItem(text=name, on_release=self.open_details)
                    left_img = ImageLeftWidget(source=flag_path)
                    item.add_widget(left_img)
                    self.list_view.add_widget(item)
                    count += 1
                    if count >= 20: break
                        
    def open_details(self, instance):
        self.sm.get_screen("details").set_content(instance.text, self.data[self.current_cat][instance.text], self.current_cat)
        self.change_screen("details")

    def create_details_screen(self):
        screen = DetailsScreen(name="details")
        layout = MDBoxLayout(orientation='vertical')
        tb = MDTopAppBar(title="", left_action_items=[["arrow-left", lambda x: self.change_screen("main")]])
        screen.ids['toolbar'] = tb
        layout.add_widget(tb)
        scroll = MDScrollView()
        content = MDBoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15), adaptive_height=True)
        grid = MDGridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(140))
        screen.ids['image_grid'] = grid
        
        box1 = MDBoxLayout(orientation='vertical')
        f_img = ClickableImage(allow_stretch=True, keep_ratio=True, on_release=self.show_zoom_popup)
        f_lbl = MDLabel(halign="center", font_style="Caption", adaptive_height=True)
        box1.add_widget(f_img); box1.add_widget(f_lbl); screen.ids['flag_img'] = f_img; screen.ids['flag_label'] = f_lbl
        
        box2 = MDBoxLayout(orientation='vertical')
        e_img = ClickableImage(allow_stretch=True, keep_ratio=True, on_release=self.show_zoom_popup)
        e_lbl = MDLabel(halign="center", font_style="Caption", adaptive_height=True)
        box2.add_widget(e_img); box2.add_widget(e_lbl); screen.ids['emblem_container'] = box2; screen.ids['emblem_img'] = e_img; screen.ids['emblem_label'] = e_lbl
        
        grid.add_widget(box1); grid.add_widget(box2); content.add_widget(grid)
        lbl = MDLabel(text="", markup=True, adaptive_height=True); screen.ids['details_label'] = lbl
        content.add_widget(lbl); scroll.add_widget(content); layout.add_widget(scroll); screen.add_widget(layout)
        return screen

    def show_zoom_popup(self, instance):
        if not instance.source or "default.png" in instance.source: return  
        tr = LANG_UI[self.lang]
        popup_layout = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        scatter = Scatter(do_rotation=False, size_hint=(1, 1))
        zoom_img = Image(source=instance.source, allow_stretch=True, keep_ratio=True, size=(400, 400))
        scatter.add_widget(zoom_img)
        popup_layout.add_widget(scatter)
        close_btn = MDRaisedButton(text=tr["close"], pos_hint={"center_x": 0.5}, size_hint_x=0.5)
        popup_layout.add_widget(close_btn)
        popup = Popup(title=tr["zoom_title"], content=popup_layout, size_hint=(0.95, 0.8))
        close_btn.bind(on_release=popup.dismiss)
        popup.open()

    def create_quiz_screen(self):
        screen = QuizScreen(name="quiz_screen")
        layout = MDBoxLayout(orientation='vertical')
        self.quiz_toolbar = MDTopAppBar(title=LANG_UI[self.lang]["quiz"])
        layout.add_widget(self.quiz_toolbar)
        self.quiz_content = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        self.question_label = MDLabel(text="", halign="center", font_style="H6", markup=True, adaptive_height=True)
        self.quiz_content.add_widget(self.question_label)
        self.options_layout = MDBoxLayout(orientation='vertical', spacing=dp(10), adaptive_height=True)
        self.quiz_content.add_widget(self.options_layout)
        layout.add_widget(self.quiz_content)
        layout.add_widget(MDBoxLayout())
        screen.add_widget(layout)
        return screen

    def create_games_menu(self):
        screen = GamesMenuScreen(name="games_menu")
        layout = MDBoxLayout(orientation='vertical')
        self.games_toolbar = MDTopAppBar(title=LANG_UI[self.lang]["games"], left_action_items=[["arrow-left", lambda x: self.change_screen("main")]])
        layout.add_widget(self.games_toolbar)
        
        self.games_btns = MDBoxLayout(orientation='vertical', padding=dp(30), spacing=dp(20), adaptive_height=True, pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.rebuild_games_menu_buttons()
        
        content = MDBoxLayout(); content.add_widget(self.games_btns); layout.add_widget(content); screen.add_widget(layout)
        return screen

    def rebuild_games_menu_buttons(self):
        """Ин функсия номи тугмаҳои менюи бозиро низ мувофиқи базаи нави забон месозад"""
        self.games_btns.clear_widgets()
        category_icons = {
            "Давлатҳо": "earth", "Страны": "earth", "Countries": "earth", 
            "Дарёҳо": "water-waves", "Реки": "water-waves", "Rivers": "water-waves", 
            "default": "gamepad-variant"
        }
        tr = LANG_UI[self.lang]
        for g_name in self.data.keys():
            if g_name not in["Олимон","Учёные", "Scientists"]:
                icon_name = category_icons.get(g_name, category_icons["default"])
                self.games_btns.add_widget(MDFillRoundFlatButton(
                    text=tr["game_btn"].format(g_name), icon=icon_name, font_style="H6", size_hint_x=0.9, pos_hint={"center_x": 0.5}, padding=dp(15),
                    on_release=lambda x, n=g_name: self.open_levels(n)
                ))

    def create_levels_screen(self):
        self.level_screen = LevelsScreen(name="levels")
        self.level_layout = MDBoxLayout(orientation='vertical')
        self.level_screen.add_widget(self.level_layout); return self.level_screen
        
    def open_levels(self, game_type):
        tr = LANG_UI[self.lang]
        self.current_game_type = game_type
        self.level_layout.clear_widgets()
        self.level_layout.add_widget(MDTopAppBar(title=tr["level_title"].format(game_type), left_action_items=[["arrow-left", lambda x: self.change_screen("games_menu")]]))
        
        scroll = MDScrollView()
        box = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15), size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))
        
        all_items = list(self.data[game_type].keys())
        if not all_items: return
        
        keys = [k for k in self.data[game_type][all_items[0]].keys() if "File" not in k]
        
        for q_key in keys:
            box.add_widget(MDLabel(text=tr["level_lbl"].format(q_key), markup=True, font_style="Subtitle1", adaptive_height=True, padding=(0, dp(10))))
            num_levels = (len(all_items) // 10) + (1 if len(all_items) % 10 != 0 else 0)
            grid_levels = MDGridLayout(cols=2, spacing=dp(12), size_hint_y=None, adaptive_height=True)
            
            for i in range(1, num_levels + 1):
                lvl_key = f"{self.lang}_{game_type}_{q_key}_lvl_{i}"  # Нигоҳдории пешравии алоҳида барои ҳар забон
                is_locked = i > 1 and not (self.store.exists(f"{self.lang}_{game_type}_{q_key}_lvl_{i-1}") and self.store.get(f"{self.lang}_{game_type}_{q_key}_lvl_{i-1}")['score'] >= 8)
                
                btn_text = tr["lvl_locked"].format(i) if is_locked else tr["lvl_unlocked"].format(i)
                btn_icon = "lock" if is_locked else "play-circle-outline"
                    
                btn = MDFillRoundFlatButton(text=btn_text, icon=btn_icon, disabled=is_locked, size_hint_x=1, on_release=lambda x, k=q_key, l=i: self.start_quiz(k, l))
                grid_levels.add_widget(btn)
            box.add_widget(grid_levels)
            
        scroll.add_widget(box); self.level_layout.add_widget(scroll); self.change_screen("levels")

    def start_quiz(self, q_key, lvl_num):
        self.current_q_key, self.current_lvl, self.quiz_score, self.q_idx = q_key, lvl_num, 0, 0
        all_names = list(self.data[self.current_game_type].keys())
        
        start_index = (lvl_num - 1) * 10
        end_index = lvl_num * 10
        self.quiz_items = [(n, q_key) for n in all_names[start_index:end_index]]
        
        random.shuffle(self.quiz_items)
        self.total_questions = len(self.quiz_items)
        
        if self.total_questions > 0: 
            self.change_screen("quiz_screen")
            self.next_question()

    def next_question(self):
        tr = LANG_UI[self.lang]
        if self.q_idx < len(self.quiz_items):
            item_name, q_key = self.quiz_items[self.q_idx]
            self.correct_ans = self.data[self.current_game_type][item_name][q_key]
            self.q_idx += 1
            
            all_wrong = list(set([
                str(self.data[self.current_game_type][n].get(q_key)) 
                for n in self.data[self.current_game_type] 
                if str(self.data[self.current_game_type][n].get(q_key)) != str(self.correct_ans)
            ]))
            
            num_choices = min(len(all_wrong), 3)
            options = random.sample(all_wrong, num_choices) if num_choices > 0 else []
            options.append(str(self.correct_ans))
            random.shuffle(options)
            
            self.question_label.text = tr["quiz_find"].format(q_key, item_name)
            self.options_layout.clear_widgets()
            
            for opt in options:
                self.options_layout.add_widget(MDRaisedButton(text=str(opt), size_hint_x=1, height=dp(50), on_release=self.check_quiz_ans))
            self.start_timer()
        else: self.finish_quiz()

    def check_quiz_ans(self, inst):
        self.stop_timer()
        if inst.text == str(self.correct_ans):
            self.quiz_score += 1
            if self.sound_correct: self.sound_correct.play()
        else:
            if self.sound_wrong: self.sound_wrong.play()
        self.next_question()

    def start_timer(self):
        self.time_left = self.timer_seconds
        tr = LANG_UI[self.lang]
        self.quiz_toolbar.title = tr["q_timer"].format(self.q_idx, self.total_questions, self.time_left)
        if self.timer_event: Clock.unschedule(self.timer_event)
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        self.time_left -= 1
        tr = LANG_UI[self.lang]
        self.quiz_toolbar.title = tr["q_timer"].format(self.q_idx, self.total_questions, self.time_left)
        if self.time_left <= 0: 
            self.stop_timer()
            self.next_question()

    def stop_timer(self):
        if self.timer_event: Clock.unschedule(self.timer_event)

    def finish_quiz(self):
        self.stop_timer()
        tr = LANG_UI[self.lang]
        lvl_key = f"{self.lang}_{self.current_game_type}_{self.current_q_key}_lvl_{self.current_lvl}"
        if not self.store.exists(lvl_key) or self.quiz_score > self.store.get(lvl_key)['score']:
            self.store.put(lvl_key, score=self.quiz_score)
        
        self.dialog = MDDialog(
            title=tr["result"], text=tr["score"].format(self.quiz_score, self.total_questions), 
            buttons=[MDFlatButton(text="OK", on_release=lambda x: self.back_to_levels())]
        )
        self.dialog.open()

    def back_to_levels(self):
        if self.dialog: self.dialog.dismiss()
        self.open_levels(self.current_game_type)

    def create_settings_screen(self):
        screen = SettingsScreen(name="settings")
        layout = MDBoxLayout(orientation='vertical')
        tr = LANG_UI[self.lang]
        self.settings_toolbar = MDTopAppBar(title=tr["settings"], left_action_items=[["arrow-left", lambda x: self.change_screen("main")]])
        layout.add_widget(self.settings_toolbar)
        
        content = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # СЕ ТУГМА БАРОИ ИНТИХОБИ ЗАБОН ВА БАЗАҲО
        lang_box = MDBoxLayout(spacing=dp(10), size_hint_y=None, height=dp(45))
        lang_box.add_widget(MDFillRoundFlatButton(text="Тоҷикӣ", on_release=lambda x: self.change_language("tg")))
        lang_box.add_widget(MDFillRoundFlatButton(text="Русский", on_release=lambda x: self.change_language("ru")))
        lang_box.add_widget(MDFillRoundFlatButton(text="English", on_release=lambda x: self.change_language("en")))
        content.add_widget(lang_box)
        
        self.theme_btn = MDRaisedButton(text=tr["theme"], size_hint_x=1, on_release=lambda x: self.toggle_theme())
        content.add_widget(self.theme_btn)
        
        self.font_lbl = MDLabel(text=tr["font"].format(self.font_size), adaptive_height=True)
        content.add_widget(self.font_lbl)
        f_slider = MDSlider(min=14, max=30, value=self.font_size, step=1)
        f_slider.bind(value=self.update_font_size)
        content.add_widget(f_slider)
        
        self.timer_lbl = MDLabel(text=tr["timer_lbl"], adaptive_height=True)
        content.add_widget(self.timer_lbl)
        t_input = MDTextField(text=str(self.timer_seconds), input_filter="int")
        t_input.bind(text=self.update_timer_val); content.add_widget(t_input)
        
        layout.add_widget(content); layout.add_widget(MDBoxLayout()); screen.add_widget(layout); return screen

    def toggle_theme(self): self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style =="Light" else "Light"
    def update_font_size(self, instance, value):
        self.font_size = int(value)
        self.font_lbl.text = LANG_UI[self.lang]["font"].format(self.font_size)
    def update_timer_val(self, instance, value):
        try: self.timer_seconds = int(value) if value else 15
        except: pass
    def change_screen(self, name): self.sm.current = name

if __name__ == "__main__":
    InfoApp().run()
