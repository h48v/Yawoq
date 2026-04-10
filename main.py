#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════
    Master Keyboard - لوحة المفاتيح الاحترافية
    Developer: DEW (@h40v_)
    Version: 2.0 (Kivy APK Edition)
═══════════════════════════════════════════════════════
"""

import os
import json
import random
import time
from threading import Thread

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from kivy.clock import Clock, mainthread
from kivy.core.window import Window
from kivy.utils import platform

# ألوان التطبيق
COLORS = {
    'bg': (0.1, 0.1, 0.12, 1),
    'primary': (0.2, 0.6, 1, 1),
    'success': (0.2, 0.8, 0.4, 1),
    'danger': (1, 0.3, 0.3, 1),
    'warning': (1, 0.7, 0.2, 1),
    'text': (1, 1, 1, 1),
    'secondary': (0.15, 0.15, 0.18, 1)
}

Window.clearcolor = COLORS['bg']

CONFIG_FILE = "master_config.json"


class MasterKeyboard:
    """فئة لوحة المفاتيح الرئيسية"""
    
    def __init__(self):
        self.config = self.load_config()
        self.is_running = False
        self.thread = None
        self.version = "2.0"
        self.status_callback = None
        
    def load_config(self):
        """تحميل الإعدادات"""
        default_config = {
            "speed": 150,
            "lines": 1,
            "list_1": [],
            "list_2": [],
            "list_3": [],
            "list_4": [],
            "decoration": "",
            "active_list": 1
        }
        
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    default_config.update(loaded)
            except:
                pass
        return default_config
    
    def save_config(self):
        """حفظ الإعدادات"""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
            return True
        except:
            return False
    
    def stealth(self, text):
        """حقن شفاف لتجاوز الفلاتر"""
        return '\u200D'.join(list(text))
    
    def start_machine(self, callback=None):
        """تشغيل الرشاش"""
        if self.is_running:
            return False
        
        active_list = self.config['active_list']
        list_key = f"list_{active_list}"
        raw_data = self.config.get(list_key, [])
        
        if not raw_data:
            return False
        
        self.status_callback = callback
        self.is_running = True
        self.thread = Thread(target=self._run_machine, daemon=True)
        self.thread.start()
        return True
    
    def _run_machine(self):
        """تنفيذ الرشاش"""
        speed = self.config['speed'] / 1000
        lines = self.config['lines']
        active_list = self.config['active_list']
        
        list_key = f"list_{active_list}"
        raw_data = self.config.get(list_key, [])
        decoration = self.config.get('decoration', '')
        
        target_list = list(raw_data)
        random.shuffle(target_list)
        
        sent_count = 0
        total = len(target_list) * lines
        
        try:
            for i in range(1, lines + 1):
                if not self.is_running:
                    break
                
                for idx, msg in enumerate(target_list, 1):
                    if not self.is_running:
                        break
                    
                    final_msg = self.stealth(msg) + decoration
                    sent_count += 1
                    
                    if self.status_callback:
                        progress = (sent_count / total) * 100
                        self.status_callback(f"إرسال: {sent_count}/{total}", progress)
                    
                    time.sleep(speed)
            
            if self.status_callback and self.is_running:
                self.status_callback(f"✅ اكتمل! تم إرسال {sent_count} رسالة", 100)
        
        except Exception as e:
            if self.status_callback:
                self.status_callback(f"❌ خطأ: {str(e)}", 0)
        finally:
            self.is_running = False
    
    def stop_machine(self):
        """إيقاف الرشاش"""
        self.is_running = False


class HomeScreen(Screen):
    """الشاشة الرئيسية"""
    
    def __init__(self, master, **kwargs):
        super().__init__(**kwargs)
        self.master = master
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # العنوان
        header = Label(
            text='⌨️ Master Keyboard Pro',
            font_size='28sp',
            size_hint_y=0.15,
            color=COLORS['primary'],
            bold=True
        )
        layout.add_widget(header)
        
        # معلومات الحالة
        self.status_grid = GridLayout(cols=2, spacing=10, size_hint_y=0.3)
        
        self.status_labels = {}
        status_items = [
            ('speed', '⚡ السرعة'),
            ('lines', '🔄 التكرار'),
            ('active_list', '🎯 القائمة'),
            ('running', '🔥 الحالة')
        ]
        
        for key, label_text in status_items:
            label = Label(text=label_text, size_hint_x=0.4, color=COLORS['warning'])
            value = Label(text='', size_hint_x=0.6, color=COLORS['success'])
            self.status_labels[key] = value
            self.status_grid.add_widget(label)
            self.status_grid.add_widget(value)
        
        layout.add_widget(self.status_grid)
        
        # شريط التقدم
        progress_box = BoxLayout(orientation='vertical', size_hint_y=0.15, spacing=5)
        self.progress_label = Label(text='جاهز للعمل', color=COLORS['text'])
        self.progress_bar = Slider(
            min=0, max=100, value=0,
            size_hint_y=0.3,
            cursor_size=(0, 0),
            disabled=True
        )
        progress_box.add_widget(self.progress_label)
        progress_box.add_widget(self.progress_bar)
        layout.add_widget(progress_box)
        
        # أزرار التحكم
        buttons_layout = GridLayout(cols=2, spacing=10, size_hint_y=0.4)
        
        self.start_btn = Button(
            text='▶️ تشغيل',
            background_color=COLORS['success'],
            font_size='18sp'
        )
        self.start_btn.bind(on_press=self.start_machine)
        
        self.stop_btn = Button(
            text='⏹️ إيقاف',
            background_color=COLORS['danger'],
            font_size='18sp',
            disabled=True
        )
        self.stop_btn.bind(on_press=self.stop_machine)
        
        settings_btn = Button(
            text='⚙️ الإعدادات',
            background_color=COLORS['primary'],
            font_size='18sp'
        )
        settings_btn.bind(on_press=self.goto_settings)
        
        lists_btn = Button(
            text='📝 القوائم',
            background_color=COLORS['primary'],
            font_size='18sp'
        )
        lists_btn.bind(on_press=self.goto_lists)
        
        buttons_layout.add_widget(self.start_btn)
        buttons_layout.add_widget(self.stop_btn)
        buttons_layout.add_widget(settings_btn)
        buttons_layout.add_widget(lists_btn)
        
        layout.add_widget(buttons_layout)
        
        # معلومات المطور
        footer = Label(
            text='Developer: DEW (@h40v_) | v2.0',
            size_hint_y=0.05,
            color=(0.5, 0.5, 0.5, 1),
            font_size='12sp'
        )
        layout.add_widget(footer)
        
        self.add_widget(layout)
        self.update_status()
    
    def update_status(self):
        """تحديث معلومات الحالة"""
        self.status_labels['speed'].text = f"{self.master.config['speed']} ms"
        self.status_labels['lines'].text = f"{self.master.config['lines']}x"
        self.status_labels['active_list'].text = f"القائمة {self.master.config['active_list']}"
        
        if self.master.is_running:
            self.status_labels['running'].text = '● يعمل'
            self.status_labels['running'].color = COLORS['success']
        else:
            self.status_labels['running'].text = '○ متوقف'
            self.status_labels['running'].color = COLORS['danger']
    
    @mainthread
    def update_progress(self, text, value):
        """تحديث شريط التقدم"""
        self.progress_label.text = text
        self.progress_bar.value = value
    
    def start_machine(self, instance):
        """تشغيل الرشاش"""
        if self.master.start_machine(callback=self.update_progress):
            self.start_btn.disabled = True
            self.stop_btn.disabled = False
            self.update_status()
        else:
            self.show_popup('تنبيه', 'القائمة النشطة فارغة!\nأضف نصوص أولاً')
    
    def stop_machine(self, instance):
        """إيقاف الرشاش"""
        self.master.stop_machine()
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        self.update_status()
        self.progress_label.text = 'تم الإيقاف'
        self.progress_bar.value = 0
    
    def goto_settings(self, instance):
        self.manager.current = 'settings'
    
    def goto_lists(self, instance):
        self.manager.current = 'lists'
    
    def show_popup(self, title, message):
        """عرض نافذة منبثقة"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        btn = Button(text='حسناً', size_hint_y=0.3)
        content.add_widget(btn)
        
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.4))
        btn.bind(on_press=popup.dismiss)
        popup.open()


class SettingsScreen(Screen):
    """شاشة الإعدادات"""
    
    def __init__(self, master, **kwargs):
        super().__init__(**kwargs)
        self.master = master
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # العنوان
        header = Label(
            text='⚙️ إعدادات الرشاش',
            font_size='24sp',
            size_hint_y=0.1,
            color=COLORS['primary']
        )
        layout.add_widget(header)
        
        # السرعة
        speed_box = BoxLayout(orientation='vertical', spacing=5, size_hint_y=0.15)
        self.speed_label = Label(
            text=f"⚡ السرعة: {self.master.config['speed']} ms",
            color=COLORS['text']
        )
        self.speed_slider = Slider(
            min=0, max=5000,
            value=self.master.config['speed'],
            step=10
        )
        self.speed_slider.bind(value=self.on_speed_change)
        speed_box.add_widget(self.speed_label)
        speed_box.add_widget(self.speed_slider)
        layout.add_widget(speed_box)
        
        # التكرار
        lines_box = BoxLayout(orientation='vertical', spacing=5, size_hint_y=0.15)
        self.lines_label = Label(
            text=f"🔄 التكرار: {self.master.config['lines']}x",
            color=COLORS['text']
        )
        self.lines_slider = Slider(
            min=1, max=100,
            value=self.master.config['lines'],
            step=1
        )
        self.lines_slider.bind(value=self.on_lines_change)
        lines_box.add_widget(self.lines_label)
        lines_box.add_widget(self.lines_slider)
        layout.add_widget(lines_box)
        
        # القائمة النشطة
        list_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.1)
        list_box.add_widget(Label(
            text='🎯 القائمة النشطة:',
            size_hint_x=0.5,
            color=COLORS['text']
        ))
        self.list_spinner = Spinner(
            text=f"القائمة {self.master.config['active_list']}",
            values=[f"القائمة {i}" for i in range(1, 5)],
            size_hint_x=0.5
        )
        self.list_spinner.bind(text=self.on_list_change)
        list_box.add_widget(self.list_spinner)
        layout.add_widget(list_box)
        
        # الزخرفة
        deco_box = BoxLayout(orientation='vertical', spacing=5, size_hint_y=0.2)
        deco_box.add_widget(Label(
            text='✨ الزخرفة (اختياري):',
            size_hint_y=0.3,
            color=COLORS['text']
        ))
        self.deco_input = TextInput(
            text=self.master.config.get('decoration', ''),
            multiline=False,
            size_hint_y=0.7
        )
        self.deco_input.bind(text=self.on_deco_change)
        deco_box.add_widget(self.deco_input)
        layout.add_widget(deco_box)
        
        # أزرار
        buttons = BoxLayout(spacing=10, size_hint_y=0.15)
        
        save_btn = Button(
            text='💾 حفظ',
            background_color=COLORS['success']
        )
        save_btn.bind(on_press=self.save_settings)
        
        back_btn = Button(
            text='◀️ رجوع',
            background_color=COLORS['secondary']
        )
        back_btn.bind(on_press=self.go_back)
        
        buttons.add_widget(save_btn)
        buttons.add_widget(back_btn)
        layout.add_widget(buttons)
        
        self.add_widget(layout)
    
    def on_speed_change(self, instance, value):
        self.speed_label.text = f"⚡ السرعة: {int(value)} ms"
    
    def on_lines_change(self, instance, value):
        self.lines_label.text = f"🔄 التكرار: {int(value)}x"
    
    def on_list_change(self, spinner, text):
        pass
    
    def on_deco_change(self, instance, value):
        pass
    
    def save_settings(self, instance):
        """حفظ الإعدادات"""
        self.master.config['speed'] = int(self.speed_slider.value)
        self.master.config['lines'] = int(self.lines_slider.value)
        self.master.config['active_list'] = int(self.list_spinner.text.split()[-1])
        self.master.config['decoration'] = self.deco_input.text
        
        if self.master.save_config():
            self.show_popup('نجح', 'تم حفظ الإعدادات بنجاح!')
            # تحديث الشاشة الرئيسية
            home = self.manager.get_screen('home')
            home.update_status()
        else:
            self.show_popup('خطأ', 'فشل حفظ الإعدادات')
    
    def go_back(self, instance):
        self.manager.current = 'home'
    
    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        btn = Button(text='حسناً', size_hint_y=0.3)
        content.add_widget(btn)
        
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.3))
        btn.bind(on_press=popup.dismiss)
        popup.open()


class ListsScreen(Screen):
    """شاشة إدارة القوائم"""
    
    def __init__(self, master, **kwargs):
        super().__init__(**kwargs)
        self.master = master
        self.current_list = 1
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # العنوان
        header = Label(
            text='📝 إدارة القوائم',
            font_size='24sp',
            size_hint_y=0.08,
            color=COLORS['primary']
        )
        layout.add_widget(header)
        
        # اختيار القائمة
        list_select = BoxLayout(size_hint_y=0.08, spacing=10)
        list_select.add_widget(Label(
            text='اختر القائمة:',
            size_hint_x=0.4,
            color=COLORS['text']
        ))
        self.list_selector = Spinner(
            text=f"القائمة {self.current_list}",
            values=[f"القائمة {i}" for i in range(1, 5)],
            size_hint_x=0.6
        )
        self.list_selector.bind(text=self.on_list_select)
        list_select.add_widget(self.list_selector)
        layout.add_widget(list_select)
        
        # عداد النصوص
        self.count_label = Label(
            text=self.get_count_text(),
            size_hint_y=0.05,
            color=COLORS['warning']
        )
        layout.add_widget(self.count_label)
        
        # عرض النصوص
        scroll = ScrollView(size_hint_y=0.5)
        self.texts_display = Label(
            text=self.get_texts_display(),
            size_hint_y=None,
            color=COLORS['text'],
            halign='right',
            valign='top'
        )
        self.texts_display.bind(texture_size=self.texts_display.setter('size'))
        scroll.add_widget(self.texts_display)
        layout.add_widget(scroll)
        
        # إدخال نص جديد
        input_box = BoxLayout(orientation='vertical', size_hint_y=0.15, spacing=5)
        input_box.add_widget(Label(
            text='➕ أضف نص جديد:',
            size_hint_y=0.3,
            color=COLORS['text']
        ))
        self.text_input = TextInput(
            hint_text='اكتب النص هنا...',
            multiline=False,
            size_hint_y=0.7
        )
        input_box.add_widget(self.text_input)
        layout.add_widget(input_box)
        
        # أزرار
        buttons = GridLayout(cols=3, spacing=10, size_hint_y=0.12)
        
        add_btn = Button(
            text='➕ إضافة',
            background_color=COLORS['success']
        )
        add_btn.bind(on_press=self.add_text)
        
        clear_btn = Button(
            text='🗑️ مسح الكل',
            background_color=COLORS['danger']
        )
        clear_btn.bind(on_press=self.clear_all)
        
        back_btn = Button(
            text='◀️ رجوع',
            background_color=COLORS['secondary']
        )
        back_btn.bind(on_press=self.go_back)
        
        buttons.add_widget(add_btn)
        buttons.add_widget(clear_btn)
        buttons.add_widget(back_btn)
        layout.add_widget(buttons)
        
        self.add_widget(layout)
    
    def on_list_select(self, spinner, text):
        """تغيير القائمة"""
        self.current_list = int(text.split()[-1])
        self.update_display()
    
    def get_current_list_key(self):
        return f"list_{self.current_list}"
    
    def get_current_list(self):
        return self.master.config.get(self.get_current_list_key(), [])
    
    def get_count_text(self):
        count = len(self.get_current_list())
        return f"📊 العدد: {count} نص"
    
    def get_texts_display(self):
        texts = self.get_current_list()
        if not texts:
            return "القائمة فارغة"
        return "\n".join([f"{i}. {t}" for i, t in enumerate(texts, 1)])
    
    def update_display(self):
        """تحديث العرض"""
        self.count_label.text = self.get_count_text()
        self.texts_display.text = self.get_texts_display()
    
    def add_text(self, instance):
        """إضافة نص جديد"""
        new_text = self.text_input.text.strip()
        if new_text:
            list_key = self.get_current_list_key()
            current = self.master.config.get(list_key, [])
            current.append(new_text)
            self.master.config[list_key] = current
            self.master.save_config()
            self.text_input.text = ''
            self.update_display()
            self.show_popup('نجح', 'تمت الإضافة بنجاح!')
        else:
            self.show_popup('تنبيه', 'الرجاء كتابة نص أولاً')
    
    def clear_all(self, instance):
        """حذف جميع النصوص"""
        # نافذة تأكيد
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text='هل أنت متأكد من حذف جميع النصوص؟'))
        
        btn_box = BoxLayout(spacing=10, size_hint_y=0.3)
        
        yes_btn = Button(text='نعم', background_color=COLORS['danger'])
        no_btn = Button(text='لا', background_color=COLORS['secondary'])
        
        btn_box.add_widget(yes_btn)
        btn_box.add_widget(no_btn)
        content.add_widget(btn_box)
        
        popup = Popup(title='تأكيد', content=content, size_hint=(0.8, 0.4))
        
        def confirm(inst):
            list_key = self.get_current_list_key()
            self.master.config[list_key] = []
            self.master.save_config()
            self.update_display()
            popup.dismiss()
            self.show_popup('نجح', 'تم الحذف بنجاح!')
        
        yes_btn.bind(on_press=confirm)
        no_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def go_back(self, instance):
        self.manager.current = 'home'
    
    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        btn = Button(text='حسناً', size_hint_y=0.3)
        content.add_widget(btn)
        
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.3))
        btn.bind(on_press=popup.dismiss)
        popup.open()


class MasterKeyboardApp(App):
    """التطبيق الرئيسي"""
    
    def build(self):
        # إنشاء نظام الإدارة
        self.master = MasterKeyboard()
        
        # إنشاء مدير الشاشات
        sm = ScreenManager()
        
        # إضافة الشاشات
        sm.add_widget(HomeScreen(self.master, name='home'))
        sm.add_widget(SettingsScreen(self.master, name='settings'))
        sm.add_widget(ListsScreen(self.master, name='lists'))
        
        return sm
    
    def on_pause(self):
        """عند إيقاف التطبيق مؤقتاً"""
        return True
    
    def on_resume(self):
        """عند استئناف التطبيق"""
        pass


if __name__ == '__main__':
    MasterKeyboardApp().run()
