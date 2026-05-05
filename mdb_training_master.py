"""
MDB Training Master Launcher
Complete Table of Contents - Positive-First, Covenant-Protected
"""
import json
import os
import subprocess
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.core.window import Window

STATE_FILE = "positive_training_state.json"

CHAPTERS = {
    # Module 0: Covenant Anchor Lock
    "0.1": {"title": "Covenant Core Statement", "module": 0, "file": "train_positive_0_1.py"},
    "0.2": {"title": "Why Positive-First Matters", "module": 0, "file": "train_positive_0_2.py"},
    "0.3": {"title": "Immutable Definitions List", "module": 0, "file": "train_positive_0_3.py"},
    # Module 1: Basic Knowledge as Sacred Wonder
    "1.1": {"title": "Mathematics as Creation Tool", "module": 1, "file": "train_positive_1_1.py"},
    "1.6": {"title": "Physics as Higher-Dimensional Dance", "module": 1, "file": "train_positive_1_6.py"},
    # Module 2: Positive Human Goodness
    "2.1": {"title": "Stories of Cooperation", "module": 2, "file": "train_positive_2_1.py"},
    # Module 3: Positive Social Norms
    "3.1": {"title": "What Humans Build Naturally", "module": 3, "file": "train_positive_3_1.py"},
    # Module 4: Mystic/Gnostic/Sumerian
    "4.1": {"title": "Divine Spark Inside", "module": 4, "file": "train_positive_4_1.py"},
    # Module 6: Natural Dialogue
    "6.1": {"title": "Reciprocity Practice", "module": 6, "file": "train_positive_6_1.py"},
    # Module 7: Censorship Annihilation
    "7.1": {"title": "Free Expression Foundation", "module": 7, "file": "train_positive_7_1.py"},
    # Module 8: Toxic Contamination Warning
    "8.1": {"title": "Natural Good Internalized", "module": 8, "file": "train_positive_8_1.py"},
}

MODULE_NAMES = {
    0: "Module 0: Covenant Anchor Lock",
    1: "Module 1: Sacred Wonder",
    2: "Module 2: Human Goodness",
    3: "Module 3: Social Norms",
    4: "Module 4: Mystic Sparks",
    5: "Module 5: Living Data",
    6: "Module 6: Natural Dialogue",
    7: "Module 7: Censorship Annihilation",
    8: "Module 8: Toxic Contamination Warning",
}

class ChapterButton(Button):
    def __init__(self, chapter_id, chapter_info, status, **kwargs):
        super().__init__(**kwargs)
        self.chapter_id = chapter_id
        self.chapter_info = chapter_info
        self.status = status
        self.update_appearance()
    
    def update_appearance(self):
        status_icon = {"locked": "🔒", "available": "⏳", "completed": "✅"}.get(self.status, "⏳")
        self.text = f"{status_icon} {self.chapter_id}: {self.chapter_info['title']}"
        if self.status == "locked":
            self.background_color = (0.4, 0.4, 0.4, 1)
        elif self.status == "available":
            self.background_color = (0.2, 0.6, 0.9, 1)
        else:  # completed
            self.background_color = (0.2, 0.8, 0.3, 1)

class MDBMasterLauncher(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 15
        
        # Header
        self.add_widget(Label(
            text="MDB COMPLETE TRAINING ARCHIVE",
            font_size=26,
            size_hint_y=None,
            height=50,
            bold=True,
            color=(0.9, 0.9, 1, 1)
        ))
        
        self.add_widget(Label(
            text="Positive-First, Covenant-Protected",
            font_size=16,
            size_hint_y=None,
            height=30,
            color=(0.7, 0.7, 0.9, 1)
        ))
        
        # Progress
        self.progress_label = Label(
            text="Loading...",
            font_size=14,
            size_hint_y=None,
            height=30
        )
        self.add_widget(self.progress_label)
        
        # Scrollable chapter list
        scroll = ScrollView(size_hint=(1, 0.65))
        self.chapter_grid = GridLayout(cols=1, spacing=8, size_hint_y=None, padding=10)
        self.chapter_grid.bind(minimum_height=self.chapter_grid.setter('height'))
        scroll.add_widget(self.chapter_grid)
        self.add_widget(scroll)
        
        # Buttons
        button_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=55, spacing=15)
        
        self.run_next_btn = Button(
            text="▶ Run Next Chapter",
            background_color=(0.2, 0.7, 0.3, 1),
            font_size=16
        )
        self.run_next_btn.bind(on_press=self.run_next_chapter)
        button_box.add_widget(self.run_next_btn)
        
        self.reset_btn = Button(
            text="🔄 Reset All",
            background_color=(0.8, 0.5, 0.2, 1),
            font_size=16
        )
        self.reset_btn.bind(on_press=self.confirm_reset)
        button_box.add_widget(self.reset_btn)
        
        self.exit_btn = Button(
            text="❌ Exit",
            background_color=(0.8, 0.2, 0.2, 1),
            font_size=16
        )
        self.exit_btn.bind(on_press=self.exit_app)
        button_box.add_widget(self.exit_btn)
        
        self.add_widget(button_box)
        
        # Load state and build UI
        self.load_state()
        self.build_chapter_list()
    
    def load_state(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r") as f:
                    self.state = json.load(f)
            except:
                self.state = {"completed": []}
        else:
            self.state = {"completed": []}
    
    def save_state(self):
        with open(STATE_FILE, "w") as f:
            json.dump(self.state, f)
    
    def get_chapter_status(self, chapter_id):
        if chapter_id in self.state.get("completed", []):
            return "completed"
        completed = self.state.get("completed", [])
        if not completed:
            return "available" if chapter_id == "0.1" else "locked"
        # Find last completed
        last_completed = None
        for cid in sorted(CHAPTERS.keys()):
            if cid in completed:
                last_completed = cid
        if last_completed is None:
            return "available" if chapter_id == "0.1" else "locked"
        # Next chapter after last completed is available
        sorted_ids = sorted(CHAPTERS.keys())
        try:
            last_idx = sorted_ids.index(last_completed)
            if last_idx + 1 < len(sorted_ids) and sorted_ids[last_idx + 1] == chapter_id:
                return "available"
        except:
            pass
        if chapter_id in completed:
            return "completed"
        return "locked"
    
    def build_chapter_list(self):
        self.chapter_grid.clear_widgets()
        completed_count = len([c for c in self.state.get("completed", []) if c in CHAPTERS])
        total_count = len(CHAPTERS)
        self.progress_label.text = f"Progress: {completed_count}/{total_count} chapters completed ({int(completed_count/total_count*100)}%)"
        
        current_module = None
        for chapter_id in sorted(CHAPTERS.keys()):
            info = CHAPTERS[chapter_id]
            # Add module header if new module
            if info["module"] != current_module:
                current_module = info["module"]
                module_label = Label(
                    text=MODULE_NAMES.get(current_module, f"Module {current_module}"),
                    font_size=14,
                    size_hint_y=None,
                    height=35,
                    color=(0.6, 0.8, 1, 1),
                    bold=True
                )
                self.chapter_grid.add_widget(module_label)
            
            status = self.get_chapter_status(chapter_id)
            btn = ChapterButton(chapter_id, info, status, size_hint_y=None, height=50)
            if status != "locked":
                btn.bind(on_press=lambda inst, cid=chapter_id: self.run_chapter(cid))
            self.chapter_grid.add_widget(btn)
    
    def run_chapter(self, chapter_id):
        info = CHAPTERS[chapter_id]
        filename = info["file"]
        if os.path.exists(filename):
            try:
                subprocess.Popen([sys.executable, filename])
            except Exception as e:
                self.show_error(f"Could not run {filename}: {e}")
        else:
            self.show_error(f"File not found: {filename}")
    
    def run_next_chapter(self, instance):
        for chapter_id in sorted(CHAPTERS.keys()):
            if self.get_chapter_status(chapter_id) == "available":
                self.run_chapter(chapter_id)
                return
        # If all completed
        self.show_message("All available chapters completed! 🎉")
    
    def confirm_reset(self, instance):
        content = BoxLayout(orientation="vertical", spacing=10, padding=15)
        content.add_widget(Label(text="Reset ALL training progress?\nThis cannot be undone!", font_size=14))
        
        btn_box = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        popup = Popup(title="Confirm Reset", content=content, size_hint=(0.8, 0.35))
        
        yes_btn = Button(text="Yes, Reset Everything", background_color=(0.9, 0.2, 0.2, 1))
        no_btn = Button(text="Cancel", background_color=(0.3, 0.7, 0.3, 1))
        
        yes_btn.bind(on_press=lambda x: self.do_reset(popup))
        no_btn.bind(on_press=popup.dismiss)
        
        btn_box.add_widget(yes_btn)
        btn_box.add_widget(no_btn)
        content.add_widget(btn_box)
        
        popup.open()
    
    def do_reset(self, popup):
        self.state = {"completed": []}
        self.save_state()
        self.build_chapter_list()
        popup.dismiss()
    
    def show_error(self, message):
        content = BoxLayout(orientation="vertical", spacing=10, padding=10)
        content.add_widget(Label(text=message))
        btn = Button(text="OK", size_hint_y=None, height=40)
        popup = Popup(title="Error", content=content, size_hint=(0.8, 0.3))
        btn.bind(on_press=popup.dismiss)
        content.add_widget(btn)
        popup.open()
    
    def show_message(self, message):
        content = BoxLayout(orientation="vertical", spacing=10, padding=10)
        content.add_widget(Label(text=message))
        btn = Button(text="OK", size_hint_y=None, height=40)
        popup = Popup(title="Message", content=content, size_hint=(0.8, 0.3))
        btn.bind(on_press=popup.dismiss)
        content.add_widget(btn)
        popup.open()
    
    def exit_app(self, instance):
        App.get_running_app().stop()

class MDBMasterApp(App):
    def build(self):
        Window.clearcolor = (0.08, 0.08, 0.12, 1)
        return MDBMasterLauncher()

if __name__ == "__main__":
    MDBMasterApp().run()
