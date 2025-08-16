#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoStringsCatalogsTranslator
A powerful, dictionary-first translation tool for iOS/macOS localization strings

Features:
- 🎯 Automatic language detection from input files
- 📚 Dictionary-first translation with CSV support
- 🌐 Multiple translation services (Google, Youdao, Baidu, Tencent)
- 🎨 Beautiful terminal interface with gradient colors
- 📱 Native support for .xcstrings and .json formats
- 🌍 Bilingual interface (English/Chinese)
- ⚡ Extensible dictionary system

Author: Claude Code Assistant
License: MIT
Version: 1.0.0
"""

import json
import requests
import time
import hashlib
import random
import urllib.parse
import hmac
import base64
import uuid
from typing import Dict, List, Optional, Tuple, Set
import os
import csv
import sys

__version__ = "1.0.0"
__author__ = "Claude Code Assistant"
__license__ = "MIT"

# 全局主题状态
class AppState:
    """应用程序全局状态管理"""
    current_theme = "blue"  # 默认使用蓝色主题
    current_language = "en"  # 默认使用英文界面
    config_file = ".autotranslator_config.json"
    
    @classmethod
    def load_config(cls):
        """加载配置文件"""
        try:
            if os.path.exists(cls.config_file):
                with open(cls.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    if 'theme' in config and config['theme'] in ColorTheme.THEMES:
                        cls.current_theme = config['theme']
                    if 'language' in config and config['language'] in ['zh', 'en']:
                        cls.current_language = config['language']
        except Exception:
            # 如果配置文件有问题，使用默认设置
            pass
    
    @classmethod
    def save_config(cls):
        """保存配置文件"""
        try:
            config = {
                'theme': cls.current_theme,
                'language': cls.current_language,
                'version': __version__
            }
            with open(cls.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception:
            # 保存失败也不影响程序运行
            pass
    
    @classmethod
    def set_theme(cls, theme_key: str):
        """设置当前主题"""
        cls.current_theme = theme_key
        cls.save_config()  # 自动保存配置
    
    @classmethod
    def get_theme(cls) -> str:
        """获取当前主题"""
        return cls.current_theme
    
    @classmethod
    def set_language(cls, language: str):
        """设置当前界面语言"""
        cls.current_language = language
        cls.save_config()  # 自动保存配置
    
    @classmethod
    def get_language(cls) -> str:
        """获取当前界面语言"""
        return cls.current_language


class ColorTheme:
    """颜色主题类 - 基于健康应用的配色方案"""
    
    # 健康应用渐变配色方案
    THEMES = {
        "blue": {
            "name": "Blue", 
            "colors": ((53, 163, 253), (76, 216, 255)),  # #35A3FD -> #4CD8FF
            "emoji": "🔵"
        },
        "orange": {
            "name": "Orange",
            "colors": ((255, 191, 0), (255, 106, 0)),  # #FFBF00 -> #FF6A00
            "emoji": "🟠"
        },
        "purple": {
            "name": "Purple",
            "colors": ((53, 110, 255), (255, 0, 67)),  # #356EFF -> #FF0043
            "emoji": "🟣"
        },
        "red": {
            "name": "Red",
            "colors": ((255, 176, 127), (236, 0, 4)),  # #FFB07F -> #EC0004
            "emoji": "🔴"
        },
        "pink": {
            "name": "Pink",
            "colors": ((255, 43, 160), (255, 76, 0)),  # #FF2BA0 -> #FF4C00
            "emoji": "🩷"
        },
        "green": {
            "name": "Green",
            "colors": ((164, 218, 0), (68, 158, 0)),  # #A4DA00 -> #449E00
            "emoji": "🟢"
        },
        "violet": {
            "name": "Violet",
            "colors": ((142, 81, 255), (26, 106, 255)),  # #8E51FF -> #1A6AFF
            "emoji": "🟦"
        },
        "cyan": {
            "name": "Cyan",
            "colors": ((0, 166, 255), (118, 215, 0)),  # #00A6FF -> #76D700
            "emoji": "🔷"
        },
        "yellow": {
            "name": "Yellow",
            "colors": ((255, 197, 82), (0, 157, 255)),  # #FFC552 -> #009DFF
            "emoji": "🟡"
        },
        "coral": {
            "name": "Coral",
            "colors": ((255, 128, 128), (78, 55, 255)),  # #FF8080 -> #4E37FF
            "emoji": "🪸"
        },
        "amber": {
            "name": "Amber",
            "colors": ((63, 82, 255), (255, 157, 0)),  # #3F52FF -> #FF9D00
            "emoji": "🟨"
        }
    }
    
    @classmethod
    def get_theme_list(cls) -> List[Dict]:
        """获取主题列表"""
        return [
            {
                "key": key,
                "name": theme["name"],
                "emoji": theme["emoji"],
                "colors": theme["colors"]
            }
            for key, theme in cls.THEMES.items()
        ]
    
    @classmethod
    def get_theme_colors(cls, theme_key: str) -> Tuple[Tuple[int, int, int], Tuple[int, int, int]]:
        """获取指定主题的颜色"""
        if theme_key in cls.THEMES:
            return cls.THEMES[theme_key]["colors"]
        # 默认返回蓝色主题
        return cls.THEMES["blue"]["colors"]


class TerminalColors:
    """终端颜色和样式类"""
    
    # ANSI 颜色代码
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # 基础颜色
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # 亮色
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # 背景色
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    @staticmethod
    def gradient_text(text: str, start_color: tuple = (255, 0, 128), end_color: tuple = (0, 255, 255)) -> str:
        """创建渐变色文本"""
        if len(text) == 0:
            return text
        
        result = ""
        for i, char in enumerate(text):
            # 计算当前字符的颜色
            ratio = i / max(len(text) - 1, 1)
            r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            
            # RGB转ANSI 256色
            color_code = f"\033[38;2;{r};{g};{b}m"
            result += color_code + char
        
        return result + TerminalColors.RESET
    
    @staticmethod
    def rainbow_text(text: str) -> str:
        """创建彩虹色文本"""
        colors = [
            (255, 0, 0),    # 红
            (255, 127, 0),  # 橙
            (255, 255, 0),  # 黄
            (0, 255, 0),    # 绿
            (0, 255, 255),  # 青
            (0, 0, 255),    # 蓝
            (148, 0, 211)   # 紫
        ]
        
        result = ""
        for i, char in enumerate(text):
            if char.isspace():
                result += char
                continue
            
            color_index = i % len(colors)
            r, g, b = colors[color_index]
            color_code = f"\033[38;2;{r};{g};{b}m"
            result += color_code + char
        
        return result + TerminalColors.RESET
    
    @staticmethod
    def themed_text(text: str, theme_key: str = "step_count", intensity: float = 1.0) -> str:
        """根据主题为文本着色"""
        start_color, end_color = ColorTheme.get_theme_colors(theme_key)
        
        # 根据强度调整颜色深度
        if intensity < 1.0:
            # 向白色混合以降低强度
            start_color = tuple(int(c + (255 - c) * (1 - intensity)) for c in start_color)
            end_color = tuple(int(c + (255 - c) * (1 - intensity)) for c in end_color)
        
        # 使用渐变中点的颜色
        mid_r = int((start_color[0] + end_color[0]) / 2)
        mid_g = int((start_color[1] + end_color[1]) / 2)
        mid_b = int((start_color[2] + end_color[2]) / 2)
        
        color_code = f"\033[38;2;{mid_r};{mid_g};{mid_b}m"
        return color_code + text + TerminalColors.RESET


def select_color_theme(lang: str = "zh") -> str:
    """选择颜色主题"""
    # 多语言文本
    texts = {
        "header": {
            "zh": "🎨 选择颜色主题 (Select Color Theme)",
            "en": "🎨 Select Color Theme"
        },
        "prompt": {
            "zh": f"请选择主题 (1-{{count}}) 或输入 0 跳过 [默认: 1]: ",
            "en": f"Select theme (1-{{count}}) or enter 0 to skip [default: 1]: "
        },
        "selected": {
            "zh": "✅ 已选择主题: {name}",
            "en": "✅ Theme selected: {name}"
        },
        "skipped": {
            "zh": "⏭️ 跳过主题选择，使用当前主题",
            "en": "⏭️ Skipped theme selection, using current theme"
        },
        "invalid_range": {
            "zh": "❌ 请输入 1-{count} 之间的数字或 0 跳过",
            "en": "❌ Please enter a number between 1-{count} or 0 to skip"
        },
        "invalid_number": {
            "zh": "❌ 请输入有效的数字或 0 跳过",
            "en": "❌ Please enter a valid number or 0 to skip"
        }
    }
    
    header_text = TerminalColors.themed_text(texts["header"][lang], AppState.get_theme(), 1.0)
    print(f"\n{TerminalColors.BOLD}{header_text}{TerminalColors.RESET}")
    print("=" * 60)
    
    themes = ColorTheme.get_theme_list()
    
    for i, theme in enumerate(themes, 1):
        start_color, end_color = theme["colors"]
        sample_text = f"{theme['name']}"
        colored_sample = TerminalColors.gradient_text(sample_text, start_color, end_color)
        print(f"{i:2d}. {colored_sample}")
    
    # 添加跳过选项
    skip_text = TerminalColors.themed_text("跳过 (Skip)" if lang == "zh" else "Skip", AppState.get_theme(), 0.8)
    print(f" 0. {skip_text}")
    
    print()
    
    while True:
        try:
            prompt_text = TerminalColors.themed_text(texts["prompt"][lang].format(count=len(themes)), AppState.get_theme(), 1.0)
            choice = input(f"{prompt_text}")
            if not choice.strip():
                return themes[0]["key"]  # 默认选择第一个主题
            
            # 检查是否选择跳过
            if choice == '0':
                confirmation_text = TerminalColors.themed_text(texts["skipped"][lang], AppState.get_theme(), 0.9)
                print(f"\n{confirmation_text}")
                return AppState.get_theme()  # 返回当前主题
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(themes):
                selected_theme = themes[choice_num - 1]
                confirmation_text = TerminalColors.themed_text(texts["selected"][lang].format(name=selected_theme['name']), AppState.get_theme(), 0.9)
                print(f"\n{confirmation_text}")
                return selected_theme["key"]
            else:
                error_text = texts["invalid_range"][lang].format(count=len(themes))
                error_themed_text = TerminalColors.themed_text(error_text, "red", 0.8)
            print(f"{error_themed_text}")
        except ValueError:
            error_text = texts["invalid_number"][lang]
            error_themed_text = TerminalColors.themed_text(error_text, "red", 0.8)
        print(f"{error_themed_text}")


def display_app_title(theme_key: str = "step_count"):
    """显示应用程序标题（超大ASCII艺术字，支持多种主题渐变色）"""
    print()
    
    # 超大ASCII艺术字标题
    ascii_art = [
        " █████╗ ██╗   ██╗████████╗ ██████╗ ",
        "██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗",
        "███████║██║   ██║   ██║   ██║   ██║",
        "██╔══██║██║   ██║   ██║   ██║   ██║",
        "██║  ██║╚██████╔╝   ██║   ╚██████╔╝",
        "╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ",
        "",
        "███████╗████████╗██████╗ ██╗███╗   ██╗ ██████╗ ███████╗",
        "██╔════╝╚══██╔══╝██╔══██╗██║████╗  ██║██╔════╝ ██╔════╝",
        "███████╗   ██║   ██████╔╝██║██╔██╗ ██║██║  ███╗███████╗",
        "╚════██║   ██║   ██╔══██╗██║██║╚██╗██║██║   ██║╚════██║",
        "███████║   ██║   ██║  ██║██║██║ ╚████║╚██████╔╝███████║",
        "╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝",
        "",
        " ██████╗ █████╗ ████████╗ █████╗ ██╗      ██████╗  ██████╗ ███████╗",
        "██╔════╝██╔══██╗╚══██╔══╝██╔══██╗██║     ██╔═══██╗██╔════╝ ██╔════╝",
        "██║     ███████║   ██║   ███████║██║     ██║   ██║██║  ███╗███████╗",
        "██║     ██╔══██║   ██║   ██╔══██║██║     ██║   ██║██║   ██║╚════██║",
        "╚██████╗██║  ██║   ██║   ██║  ██║███████╗╚██████╔╝╚██████╔╝███████║",
        " ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝ ╚══════╝",
        "",
        "████████╗██████╗  █████╗ ███╗   ██╗███████╗██╗      █████╗ ████████╗ ██████╗ ██████╗ ",
        "╚══██╔══╝██╔══██╗██╔══██╗████╗  ██║██╔════╝██║     ██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗",
        "   ██║   ██████╔╝███████║██╔██╗ ██║███████╗██║     ███████║   ██║   ██║   ██║██████╔╝",
        "   ██║   ██╔══██╗██╔══██║██║╚██╗██║╚════██║██║     ██╔══██║   ██║   ██║   ██║██╔══██╗",
        "   ██║   ██║  ██║██║  ██║██║ ╚████║███████║███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║",
        "   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝"
    ]
    
    # 获取选定主题的渐变颜色
    start_color, end_color = ColorTheme.get_theme_colors(theme_key)
    
    # 计算总字符数用于渐变
    total_chars = sum(len(line.replace(' ', '')) for line in ascii_art)
    char_count = 0
    
    # 逐行显示带渐变色的ASCII艺术
    for line in ascii_art:
        colored_line = ""
        for char in line:
            if char != ' ' and char != '':
                # 计算当前字符的渐变位置
                ratio = char_count / max(total_chars - 1, 1)
                r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
                g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
                b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
                
                color_code = f"\033[38;2;{r};{g};{b}m"
                colored_line += color_code + char
                char_count += 1
            else:
                colored_line += char
        
        colored_line += TerminalColors.RESET
        print(f"{colored_line}")  # 左对齐显示
    
    # 版本信息
    print()
    version_text = f"v{__version__}"
    version_gradient = TerminalColors.gradient_text(version_text, start_color, end_color)
    print(f"{TerminalColors.BOLD}{version_gradient}{TerminalColors.RESET}")
    
    # 特性介绍 - 使用渐变色
    features = [
        "🎯 Automatic Language Detection",
        "📚 Dictionary-First Translation", 
        "🌐 Multiple Translation Services",
        "🎨 Beautiful Terminal Interface"
    ]
    
    print()
    for i, feature in enumerate(features):
        ratio = i / max(len(features) - 1, 1)
        r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
        color_code = f"\033[38;2;{r};{g};{b}m"
        
        print(f"{color_code}{feature}{TerminalColors.RESET}")
    
    print()
    
    # 底部分隔线 - 渐变色
    separator = "═" * 70
    gradient_separator = TerminalColors.gradient_text(separator, start_color, end_color)
    print(f"{gradient_separator}")
    print()


class LanguageDetector:
    """语言检测器 - 自动检测输入文件中需要翻译的语言"""
    
    @staticmethod
    def detect_target_languages(file_path: str) -> Set[str]:
        """
        检测输入文件中包含的目标语言
        
        Args:
            file_path: 输入文件路径
            
        Returns:
            目标语言代码集合
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            target_languages = set()
            strings_data = data.get('strings', {})
            
            for key, value in strings_data.items():
                if 'localizations' in value:
                    localizations = value['localizations']
                    for lang_code in localizations.keys():
                        # 跳过源语言（通常是英文）
                        if lang_code not in ['en', 'en-US', 'Base']:
                            target_languages.add(lang_code)
            
            return target_languages
            
        except Exception as e:
            error_text = TerminalColors.themed_text(f"❌ {get_text('language_detection_failed', 'zh')}: {e}", "red", 0.8)
            print(f"{error_text}")
            return set()
    
    @staticmethod
    def get_language_name(lang_code: str, interface_lang: str = "zh") -> str:
        """获取语言的显示名称"""
        language_names = {
            "zh": {
                "it": "意大利语",
                "ja": "日语", 
                "zh-Hans": "简体中文",
                "zh-Hant": "繁体中文",
                "ko": "韩语",
                "fr": "法语",
                "de": "德语",
                "es": "西班牙语",
                "pt": "葡萄牙语",
                "ru": "俄语",
                "ar": "阿拉伯语",
                "hi": "印地语",
                "th": "泰语",
                "vi": "越南语"
            },
            "en": {
                "it": "Italian",
                "ja": "Japanese",
                "zh-Hans": "Simplified Chinese",
                "zh-Hant": "Traditional Chinese", 
                "ko": "Korean",
                "fr": "French",
                "de": "German",
                "es": "Spanish",
                "pt": "Portuguese",
                "ru": "Russian",
                "ar": "Arabic",
                "hi": "Hindi",
                "th": "Thai",
                "vi": "Vietnamese"
            }
        }
        
        return language_names.get(interface_lang, {}).get(lang_code, lang_code)


class DictionaryManager:
    """
    Dictionary Manager - Supports multiple CSV dictionary files
    
    CSV Format Requirements:
    - First column: English (lookup key)
    - Other columns: Various language translations
    - First row: Language code headers
    """
    
    def __init__(self):
        self.dictionaries = {}
        self.language_mapping = {
            'zh-Hans': '简体中文',
            'zh-Hant': '繁體中文', 
            'ja': '日本語',
            'it': 'Italiano',
            'ko': '한국어',
            'fr': 'Français',
            'de': 'Deutsch',
            'es': 'Español',
            'pt': 'Português',
            'ru': 'Русский'
        }
    
    def load_dictionary(self, csv_file_path: str, dictionary_name: Optional[str] = None, lang: str = "zh") -> bool:
        """
        Load CSV dictionary file
        
        Args:
            csv_file_path: Path to CSV file
            dictionary_name: Dictionary name, uses filename if None
        
        Returns:
            True if successful, False otherwise
        """
        if dictionary_name is None:
            dictionary_name = os.path.basename(csv_file_path).replace('.csv', '')
        
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader)  # First row contains language headers
                
                # Build language column index mapping
                lang_indices = {}
                for i, header in enumerate(headers):
                    if i == 0:  # First column is English
                        continue
                    lang_indices[header] = i
                
                # Read data and build dictionary
                dictionary_data = {}
                for row in reader:
                    if len(row) < 2:  # Skip empty or incomplete rows
                        continue
                    
                    english_text = row[0].strip()
                    if not english_text:
                        continue
                    
                    translations = {}
                    for lang_header, index in lang_indices.items():
                        if index < len(row) and row[index].strip():
                            translations[lang_header] = row[index].strip()
                    
                    dictionary_data[english_text] = translations
                
                self.dictionaries[dictionary_name] = {
                    'data': dictionary_data,
                    'headers': headers,
                    'lang_indices': lang_indices
                }
                
                success_text = TerminalColors.themed_text(f"✅ {get_text('dictionary_loaded', lang)} '{dictionary_name}': {len(dictionary_data)} {get_text('entries', lang)}", AppState.get_theme(), 0.8)
                print(f"{success_text}")
                return True
                
        except Exception as e:
            error_text = TerminalColors.themed_text(f"❌ {get_text('dictionary_load_failed', lang)} {csv_file_path}: {e}", AppState.get_theme(), 0.8)
            print(f"{error_text}")
            return False
    
    def lookup_translation(self, english_text: str, target_language: str) -> Optional[str]:
        """
        Look up translation in all dictionaries
        
        Args:
            english_text: English source text
            target_language: Target language code (e.g., 'zh-Hans', 'ja', 'it')
        
        Returns:
            Translation result, None if not found
        """
        # Map language code to CSV column name
        csv_lang = self.language_mapping.get(target_language)
        if not csv_lang:
            return None
        
        # Search in all dictionaries (exact match first)
        for dict_name, dict_info in self.dictionaries.items():
            if english_text in dict_info['data']:
                translations = dict_info['data'][english_text]
                if csv_lang in translations:
                    match_text = TerminalColors.themed_text(f"📚 {get_text('dictionary_match', 'zh')} ({dict_name}): \"{english_text}\" -> \"{translations[csv_lang]}\"", AppState.get_theme(), 0.7)
                    print(f"  {match_text}")
                    return translations[csv_lang]
        
        # Try fuzzy matching (ignore case, spaces, hyphens, underscores)
        normalized_text = english_text.lower().replace(' ', '').replace('-', '').replace('_', '')
        for dict_name, dict_info in self.dictionaries.items():
            for key, translations in dict_info['data'].items():
                normalized_key = key.lower().replace(' ', '').replace('-', '').replace('_', '')
                if normalized_key == normalized_text and csv_lang in translations:
                    fuzzy_text = TerminalColors.themed_text(f"📚 {get_text('dictionary_fuzzy_match', 'zh')} ({dict_name}): \"{english_text}\" -> \"{translations[csv_lang]}\"", AppState.get_theme(), 0.7)
                    print(f"  {fuzzy_text}")
                    return translations[csv_lang]
        
        return None
    
    def get_dictionary_info(self) -> List[Dict]:
        """Get information about loaded dictionaries"""
        info = []
        for dict_name, dict_info in self.dictionaries.items():
            info.append({
                'name': dict_name,
                'entries': len(dict_info['data']),
                'languages': list(dict_info['lang_indices'].keys())
            })
        return info


class TranslationService:
    """Base class for translation services"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def translate(self, text: str, target_lang: str, **kwargs) -> str:
        """Override this method in subclasses"""
        raise NotImplementedError


class GoogleTranslator(TranslationService):
    """Google Translate (Free API)"""
    
    def translate(self, text: str, target_lang: str, **kwargs) -> str:
        try:
            url = "https://translate.googleapis.com/translate_a/single"
            params = {
                'client': 'gtx',
                'sl': 'en',
                'tl': target_lang,
                'dt': 't',
                'q': text
            }
            
            response = self.session.get(url, params=params, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if result and result[0] and result[0][0]:
                    return result[0][0][0]
            else:
                if response.status_code == 429:
                    print(f"{TerminalColors.themed_text('⚠️ ' + get_text('google_translate_rate_limit', 'zh') + f': HTTP {response.status_code}', AppState.get_theme(), 0.8)}")
                else:
                    print(f"{TerminalColors.themed_text('⚠️ ' + get_text('google_translate_failed', 'zh') + f': HTTP {response.status_code}', AppState.get_theme(), 0.8)}")
        except Exception as e:
            print(f"{TerminalColors.themed_text('⚠️ ' + get_text('google_translate_error', 'zh') + f': {e}', AppState.get_theme(), 0.8)}")
        return text


class YoudaoTranslator(TranslationService):
    """Youdao Translate API"""
    
    def translate(self, text: str, target_lang: str, app_key: str = "", app_secret: str = "", interface_lang: str = "zh", **kwargs) -> str:
        if not app_key or not app_secret:
            print(f"{TerminalColors.themed_text('⚠️ ' + get_text('youdao_config_required', interface_lang), AppState.get_theme(), 0.8)}")
            return text
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                salt = str(random.randint(1, 65536))
                curtime = str(int(time.time()))
                signStr = app_key + text + salt + curtime + app_secret
                sign = hashlib.sha256(signStr.encode('utf-8')).hexdigest()
                
                url = "https://openapi.youdao.com/api"
                params = {
                    'q': text,
                    'from': 'en',
                    'to': target_lang,
                    'appKey': app_key,
                    'salt': salt,
                    'sign': sign,
                    'signType': 'v3',
                    'curtime': curtime
                }
                
                response = self.session.post(url, data=params, timeout=15)
                if response.status_code == 200:
                    result = response.json()
                    if result.get('errorCode') == '0':
                        return result['translation'][0]
                    elif result.get('errorCode') == '411':
                        print(f"{TerminalColors.themed_text('⚠️ ' + get_text('youdao_api_error_411', interface_lang) + f', {get_text("retry", interface_lang)} {attempt + 1}/{max_retries}', AppState.get_theme(), 0.8)}")
                        if attempt < max_retries - 1:
                            time.sleep(2)
                            continue
                    else:
                        print(f"{TerminalColors.themed_text('⚠️ ' + get_text('youdao_api_error', 'zh') + f': {result.get("errorCode")}', AppState.get_theme(), 0.8)}")
                        break
                else:
                    print(f"{TerminalColors.themed_text('⚠️ ' + get_text('youdao_http_error', 'zh') + f': {response.status_code}', AppState.get_theme(), 0.8)}")
                    if attempt < max_retries - 1:
                        time.sleep(2)
                        continue
            except Exception as e:
                print(f"{TerminalColors.themed_text('⚠️ ' + get_text('youdao_translate_failed', interface_lang) + f' ({get_text("attempt", interface_lang)} {attempt + 1}/{max_retries}): {e}', AppState.get_theme(), 0.8)}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
        return text


class BaiduTranslator(TranslationService):
    """Baidu Translate API"""
    
    def translate(self, text: str, target_lang: str, app_id: str = "", app_key: str = "", interface_lang: str = "zh", **kwargs) -> str:
        if not app_id or not app_key:
            print(TerminalColors.themed_text(f"⚠️ {get_text('baidu_config_required', interface_lang)}", AppState.get_theme(), 0.8))
            return text
        
        try:
            salt = str(random.randint(32768, 65536))
            sign_str = app_id + text + salt + app_key
            sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
            
            url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
            params = {
                'q': text,
                'from': 'en',
                'to': target_lang,
                'appid': app_id,
                'salt': salt,
                'sign': sign
            }
            
            response = self.session.get(url, params=params, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if 'trans_result' in result:
                    return result['trans_result'][0]['dst']
                else:
                    print(TerminalColors.themed_text(f"⚠️ {get_text('baidu_api_error', 'zh')}: {result.get('error_msg', get_text('unknown_error', 'zh'))}", AppState.get_theme(), 0.8))
        except Exception as e:
            print(TerminalColors.themed_text(f"⚠️ {get_text('baidu_translate_failed', 'zh')}: {e}", AppState.get_theme(), 0.8))
        return text


class TencentTranslator(TranslationService):
    """Tencent Cloud Translation API"""
    
    def translate(self, text: str, target_lang: str, secret_id: str = "", secret_key: str = "", interface_lang: str = "zh", **kwargs) -> str:
        if not secret_id or not secret_key:
            print(TerminalColors.themed_text(f"⚠️ {get_text('tencent_config_required', interface_lang)}", AppState.get_theme(), 0.8))
            return text
        
        try:
            import datetime
            
            # Tencent Cloud API signing algorithm
            algorithm = "TC3-HMAC-SHA256"
            service = "tmt"
            version = "2018-03-21"
            action = "TextTranslate"
            region = "ap-beijing"
            
            timestamp = int(time.time())
            date = datetime.datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
            
            # Build request payload
            payload = json.dumps({
                "SourceText": text,
                "Source": "en",
                "Target": target_lang,
                "ProjectId": 0
            })
            
            # Build signature
            canonical_headers = f"content-type:application/json; charset=utf-8\nhost:tmt.tencentcloudapi.com\n"
            signed_headers = "content-type;host"
            hashed_request_payload = hashlib.sha256(payload.encode('utf-8')).hexdigest()
            
            canonical_request = f"POST\n/\n\n{canonical_headers}\n{signed_headers}\n{hashed_request_payload}"
            
            credential_scope = f"{date}/{service}/tc3_request"
            string_to_sign = f"{algorithm}\n{timestamp}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"
            
            signing_key = self._get_signing_key(secret_key, date, service)
            signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
            
            authorization = f"{algorithm} Credential={secret_id}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}"
            
            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json; charset=utf-8',
                'Host': 'tmt.tencentcloudapi.com',
                'X-TC-Action': action,
                'X-TC-Timestamp': str(timestamp),
                'X-TC-Version': version,
                'X-TC-Region': region
            }
            
            response = self.session.post('https://tmt.tencentcloudapi.com/', 
                                       headers=headers, data=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if 'Response' in result and 'TargetText' in result['Response']:
                    return result['Response']['TargetText']
                else:
                    print(TerminalColors.themed_text(f"⚠️ {get_text('tencent_api_error', 'zh')}: {result.get('Response', {}).get('Error', {}).get('Message', get_text('unknown_error', 'zh'))}", AppState.get_theme(), 0.8))
        except Exception as e:
            print(TerminalColors.themed_text(f"⚠️ {get_text('tencent_translate_failed', 'zh')}: {e}", AppState.get_theme(), 0.8))
        return text
    
    def _get_signing_key(self, secret_key: str, date: str, service: str) -> bytes:
        """Generate Tencent Cloud signing key"""
        k_date = hmac.new(("TC3" + secret_key).encode('utf-8'), date.encode('utf-8'), hashlib.sha256).digest()
        k_service = hmac.new(k_date, service.encode('utf-8'), hashlib.sha256).digest()
        k_signing = hmac.new(k_service, "tc3_request".encode('utf-8'), hashlib.sha256).digest()
        return k_signing


class AutoStringsCatalogsTranslator:
    """Main translation engine with dictionary-first approach and automatic language detection"""
    
    def __init__(self):
        self.dictionary_manager = DictionaryManager()
        self.translators = {
            'google': GoogleTranslator(),
            'youdao': YoudaoTranslator(),
            'baidu': BaiduTranslator(),
            'tencent': TencentTranslator()
        }
        
        # Language code mappings for different services
        self.language_mapping = {
            'it': {
                'google': 'it',
                'youdao': 'it',
                'baidu': 'it',
                'tencent': 'it'
            },
            'ja': {
                'google': 'ja',
                'youdao': 'ja',
                'baidu': 'jp',
                'tencent': 'ja'
            },
            'zh-Hans': {
                'google': 'zh-cn',
                'youdao': 'zh-CHS',
                'baidu': 'zh',
                'tencent': 'zh'
            },
            'zh-Hant': {
                'google': 'zh-tw',
                'youdao': 'zh-CHT',
                'baidu': 'cht',
                'tencent': 'zh-TW'
            },
            'ko': {
                'google': 'ko',
                'youdao': 'ko',
                'baidu': 'kor',
                'tencent': 'ko'
            },
            'fr': {
                'google': 'fr',
                'youdao': 'fr',
                'baidu': 'fra',
                'tencent': 'fr'
            },
            'de': {
                'google': 'de',
                'youdao': 'de',
                'baidu': 'de',
                'tencent': 'de'
            },
            'es': {
                'google': 'es',
                'youdao': 'es',
                'baidu': 'spa',
                'tencent': 'es'
            },
            'pt': {
                'google': 'pt',
                'youdao': 'pt',
                'baidu': 'pt',
                'tencent': 'pt'
            },
            'ru': {
                'google': 'ru',
                'youdao': 'ru',
                'baidu': 'ru',
                'tencent': 'ru'
            }
        }
    
    def get_api_credentials(self, method: str) -> Dict:
        """Get API credentials from environment variables"""
        credentials = {}
        
        if method == "youdao":
            credentials = {
                'app_key': os.getenv('YOUDAO_APP_KEY', ''),
                'app_secret': os.getenv('YOUDAO_APP_SECRET', '')
            }
        elif method == "baidu":
            credentials = {
                'app_id': os.getenv('BAIDU_APP_ID', ''),
                'app_key': os.getenv('BAIDU_APP_KEY', '')
            }
        elif method == "tencent":
            credentials = {
                'secret_id': os.getenv('TENCENT_SECRET_ID', ''),
                'secret_key': os.getenv('TENCENT_SECRET_KEY', '')
            }
        
        return credentials
    
    def translate_with_dictionary(self, text: str, target_lang: str, method: str = "google", 
                                fallback_method: Optional[str] = None, interface_lang: str = "zh") -> str:
        """
        Dictionary-first translation approach
        
        Args:
            text: Text to translate
            target_lang: Target language code
            method: Primary translation method
            fallback_method: Fallback translation method
        
        Returns:
            Translation result
        """
        # First try dictionary lookup
        dict_result = self.dictionary_manager.lookup_translation(text, target_lang)
        if dict_result:
            return dict_result
        
        # Dictionary not found, use translation API
        print(f"  {TerminalColors.DIM}🌐 {get_text('using_api_translation', interface_lang)}: {method}{TerminalColors.RESET}")
        return self.translate_text(text, target_lang, method, fallback_method)
    
    def translate_text(self, text: str, target_lang: str = "zh", method: str = "google", 
                      fallback_method: Optional[str] = None) -> str:
        """Unified translation interface"""
        result = text
        
        # Get API language code for the method
        api_lang = self.language_mapping.get(target_lang, {}).get(method, target_lang)
        
        # Get API credentials
        credentials = self.get_api_credentials(method)
        
        # Execute translation
        translator = self.translators.get(method)
        if translator:
            result = translator.translate(text, api_lang, **credentials)
        else:
            # Fallback to Google if method not found
            result = self.translators['google'].translate(text, api_lang)
        
        # Try fallback method if primary failed
        if result == text and fallback_method and fallback_method != method:
            print(TerminalColors.themed_text(f"{get_text('primary_method_failed_trying_fallback', 'zh')} '{fallback_method}'...", AppState.get_theme(), 0.8))
            api_lang_fallback = self.language_mapping.get(target_lang, {}).get(fallback_method, target_lang)
            fallback_credentials = self.get_api_credentials(fallback_method)
            
            fallback_translator = self.translators.get(fallback_method)
            if fallback_translator:
                result = fallback_translator.translate(text, api_lang_fallback, **fallback_credentials)
        
        return result


def translate_xcstrings_file(input_file: str, output_file: str, target_languages: Set[str], 
                           method: str = "google", fallback_method: Optional[str] = None, 
                           skip_translated: bool = False, dictionary_paths: Optional[List[str]] = None,
                           lang: str = "zh") -> None:
    """
    Translate xcstrings file with automatic language detection
    
    Args:
        input_file: Input file path
        output_file: Output file path
        target_languages: Set of target languages detected from input file
        method: Primary translation method
        fallback_method: Fallback translation method
        skip_translated: Whether to skip already translated content
        dictionary_paths: List of dictionary file paths
    """
    translator = AutoStringsCatalogsTranslator()
    
    # Load dictionary files
    if dictionary_paths:
        for dict_path in dictionary_paths:
            if os.path.exists(dict_path):
                translator.dictionary_manager.load_dictionary(dict_path, lang=lang)
            else:
                print(TerminalColors.themed_text(f"⚠️ {get_text('dict_file_not_found', lang)}: {dict_path}", AppState.get_theme(), 0.8))
    
    # Display dictionary information
    dict_info = translator.dictionary_manager.get_dictionary_info()
    if dict_info:
        print(TerminalColors.themed_text(f"\n📚 {get_text('dict_loaded', lang).format(len(dict_info))}", AppState.get_theme(), 0.8))
        for info in dict_info:
            print(TerminalColors.themed_text(f"  • {info['name']}: {get_text('dict_entries', lang).format(info['entries'])}, {get_text('supported_languages', lang)}: {', '.join(info['languages'])}", AppState.get_theme(), 0.6))
    else:
        print(TerminalColors.themed_text(f"⚠️ {get_text('no_dict_loaded', lang)}", AppState.get_theme(), 0.8))
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        strings_data = data.get('strings', {})
        total_count = 0
        translated_count = 0
        skipped_count = 0
        
        # Count entries that need translation
        for key, value in strings_data.items():
            if not key or 'localizations' not in value:
                continue
            
            if value.get('shouldTranslate') == False:
                continue
                
            localizations = value['localizations']
            for lang_code in target_languages:
                if lang_code in localizations:
                    lang_unit = localizations[lang_code]['stringUnit']
                    en_value = localizations.get('en', {}).get('stringUnit', {}).get('value', key)
                    
                    # Get current translation value
                    current_value = lang_unit.get('value', '')
                    
                    # Check if translation is needed
                    if skip_translated:
                        # Skip mode: translate 'new', empty, or same-as-english meaningful text
                        should_translate = (
                            lang_unit.get('state') == 'new' or 
                            lang_unit.get('value') == '' or
                            (current_value == en_value and 
                             len(en_value) > 2 and
                             not en_value.startswith('%') and
                             not en_value.startswith('/') and
                             not en_value.isdigit() and
                             not all(c in '-: /' for c in en_value) and  # 跳过纯符号
                             any(c.isalpha() for c in en_value))  # 必须包含字母
                        )
                    else:
                        # Full mode: translate all qualifying entries
                        should_translate = (
                            lang_unit.get('state') == 'new' or 
                            lang_unit.get('value') == '' or
                            lang_unit.get('state') == 'needs_review' or
                            (current_value == en_value and 
                             len(en_value) > 2 and
                             not en_value.startswith('%') and
                             not en_value.startswith('/') and
                             not en_value.isdigit() and
                             not all(c in '-: /' for c in en_value) and  # 跳过纯符号
                             any(c.isalpha() for c in en_value))  # 必须包含字母
                        )
                    
                    if should_translate:
                        total_count += 1
        
        start_text = TerminalColors.themed_text(f"\n🚀 {get_text('start_translation', lang)}", AppState.get_theme(), 1.0)
        print(start_text)
        mode_text = TerminalColors.themed_text(f"{get_text('translation_mode', lang)}: {get_text('skip_translated_mode', lang) if skip_translated else get_text('full_translation_mode', lang)}", AppState.get_theme(), 0.7)
        print(mode_text)
        target_lang_text = TerminalColors.themed_text(f"{get_text('target_languages', lang)}: {', '.join(sorted(target_languages))}", AppState.get_theme(), 0.7)
        print(target_lang_text)
        total_text = TerminalColors.themed_text(f"{get_text('total_entries', lang)}: {total_count}", AppState.get_theme(), 0.7)
        print(total_text)
        method_text = TerminalColors.themed_text(f"{get_text('translation_method', lang)}: {method}" + (f" ({get_text('fallback', lang)}: {fallback_method})" if fallback_method else ""), AppState.get_theme(), 0.7)
        print(method_text)
        print()
        
        current_count = 0
        
        for key, value in strings_data.items():
            if not key or 'localizations' not in value:
                continue
            
            if value.get('shouldTranslate') == False:
                # Don't translate entries, just copy English value
                for lang_code in target_languages:
                    if lang_code in value['localizations']:
                        lang_unit = value['localizations'][lang_code]['stringUnit']
                        if lang_unit.get('state') == 'new' or lang_unit.get('value') == '':
                            lang_unit['value'] = key
                            lang_unit['state'] = 'translated'
                continue
            
            localizations = value['localizations']
            
            for lang_code in target_languages:
                if lang_code not in localizations:
                    continue
                
                lang_unit = localizations[lang_code]['stringUnit']
                en_value = localizations.get('en', {}).get('stringUnit', {}).get('value', key)
                
                # Get current translation value
                current_value = lang_unit.get('value', '')
                
                # Determine if translation is needed
                if skip_translated:
                    # Skip mode: translate 'new', empty, or same-as-english meaningful text
                    should_translate = (
                        lang_unit.get('state') == 'new' or 
                        lang_unit.get('value') == '' or
                        (current_value == en_value and 
                         len(en_value) > 2 and
                         not en_value.startswith('%') and
                         not en_value.startswith('/') and
                         not en_value.isdigit() and
                         not all(c in '-: /' for c in en_value) and  # 跳过纯符号
                         any(c.isalpha() for c in en_value))  # 必须包含字母
                    )
                else:
                    # Full mode: translate all qualifying entries (including already translated ones)
                    should_translate = (
                        len(en_value) > 2 and
                        not en_value.startswith('%') and
                        not en_value.startswith('/') and
                        not en_value.isdigit() and
                        not all(c in '-: /' for c in en_value) and  # 跳过纯符号
                        any(c.isalpha() for c in en_value)  # 必须包含字母
                    )
                
                if should_translate:
                    current_count += 1
                    lang_name = LanguageDetector.get_language_name(lang_code, lang)
                    progress_text = TerminalColors.themed_text(f"[{current_count}/{total_count}] {get_text('translating', lang)} {lang_name} ({lang_code}): ", AppState.get_theme(), 1.0) + TerminalColors.YELLOW + f"\"{key}\"" + TerminalColors.RESET
                    print(progress_text)
                    
                    # Use dictionary-first translation method
                    translated = translator.translate_with_dictionary(key, lang_code, method, fallback_method, lang)
                    
                    if translated and translated != key:
                        lang_unit['value'] = translated
                        lang_unit['state'] = 'translated'
                        translated_count += 1
                        success_text = TerminalColors.BRIGHT_GREEN + f"  ✅ \"{translated}\"" + TerminalColors.RESET
                        print(success_text)
                    else:
                        lang_unit['value'] = key
                        lang_unit['state'] = 'translated'
                        keep_text = TerminalColors.themed_text(f"  ➡️ {get_text('keep_original', lang)}", AppState.get_theme(), 0.6)
                        print(keep_text)
                    
                    # Rate limiting
                    if method in ["google", "youdao", "baidu", "tencent"]:
                        time.sleep(0.5 if method == "youdao" else 0.3)
                
                else:
                    # Only skip if in skip_translated mode and entry is already translated
                    if skip_translated and lang_unit.get('state') == 'translated':
                        skipped_count += 1
                    else:
                        # Debug: Show why this entry was skipped (only in skip mode)
                        if skip_translated and lang_code == 'zh-Hans':  # Only show debug for Chinese in skip mode
                            lang_name = LanguageDetector.get_language_name(lang_code, lang)
                            current_state = lang_unit.get('state', 'unknown')
                            current_value = lang_unit.get('value', '')
                            skip_msg = f"🔍 {get_text('skipped', lang)} {lang_name} ({lang_code}): \"{key}\" - {get_text('status', lang)}: {current_state}, {get_text('value', lang)}: \"{current_value[:20]}...\""
                            print(TerminalColors.themed_text(skip_msg, AppState.get_theme(), 0.6))
        
        # Save translated file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        completion_text = TerminalColors.themed_text(f"\n✅ {get_text('translation_completed', lang)}", AppState.get_theme(), 1.0)
        print(completion_text)
        total_entries_text = TerminalColors.themed_text(f"{get_text('total_entries', lang)}: {total_count}", AppState.get_theme(), 0.7)
        print(total_entries_text)
        success_count_text = TerminalColors.themed_text(f"{get_text('successfully_translated', lang)}: {translated_count}", AppState.get_theme(), 0.7)
        print(success_count_text)
        if skip_translated:
            skipped_text = TerminalColors.themed_text(f"{get_text('skipped_translated', lang)}: {skipped_count}", AppState.get_theme(), 0.7)
            print(skipped_text)
        output_text = TerminalColors.themed_text(f"{get_text('output_file', lang)}: {output_file}", AppState.get_theme(), 1.0)
        print(output_text)
        
    except Exception as e:
        print(TerminalColors.themed_text(f"❌ {get_text('translation_failed', lang)}: {e}", AppState.get_theme(), 0.8))


def get_available_translators(lang: str = "zh") -> Dict:
    """Get list of available translation services"""
    translators = {
        "google": {
            "name": get_text("google_translator_name", lang),
            "description": get_text("google_translator_desc", lang),
            "requires_auth": False
        },
        "youdao": {
            "name": get_text("youdao_translator_name", lang),
            "description": get_text("youdao_translator_desc", lang),
            "requires_auth": True,
            "env_vars": ["YOUDAO_APP_KEY", "YOUDAO_APP_SECRET"]
        },
        "baidu": {
            "name": get_text("baidu_translator_name", lang),
            "description": get_text("baidu_translator_desc", lang),
            "requires_auth": True,
            "env_vars": ["BAIDU_APP_ID", "BAIDU_APP_KEY"]
        },
        "tencent": {
            "name": get_text("tencent_translator_name", lang),
            "description": get_text("tencent_translator_desc", lang),
            "requires_auth": True,
            "env_vars": ["TENCENT_SECRET_ID", "TENCENT_SECRET_KEY"]
        }
    }
    return translators


def interactive_select_language():
    """Interactive language selection for interface"""
    # 使用默认蓝色主题来显示语言选择界面
    default_theme = "blue"
    header_text = TerminalColors.themed_text("🌍 请选择界面语言 / Please select interface language:", default_theme, 1.0)
    print(f"{header_text}")
    separator_text = TerminalColors.themed_text('═' * 50, AppState.get_theme(), 0.5)
    print(separator_text)
    
    option1_text = TerminalColors.themed_text("1.", default_theme, 0.8)
    option2_text = TerminalColors.themed_text("2.", default_theme, 0.8)
    print(f"{option1_text} {get_text('chinese', 'zh')}")
    print(f"{option2_text} English")
    print()
    
    while True:
        try:
            prompt_text = TerminalColors.themed_text(get_text('select_language_prompt', 'zh'), default_theme, 1.0)
            choice = input(f"{prompt_text}").strip()
            if choice == "1":
                return "zh"
            elif choice == "2":
                return "en"
            else:
                print(TerminalColors.themed_text(get_text('invalid_choice_12', 'zh'), AppState.get_theme(), 0.8))
        except KeyboardInterrupt:
            print(TerminalColors.themed_text(f"\n{get_text('operation_cancelled', 'zh')}", AppState.get_theme(), 0.8))
            return None


def get_text(key: str, lang: str = "zh") -> str:
    """Get multilingual text"""
    texts = {
        "usage": {
            "zh": "用法:",
            "en": "Usage:"
        },
        "interactive_mode": {
            "zh": "进入交互式配置模式...",
            "en": "Entering interactive configuration mode..."
        },
        "input_file_prompt": {
            "zh": "请输入要翻译的文件路径 (.xcstrings 或 .json): ",
            "en": "Please enter the file path to translate (.xcstrings or .json): "
        },
        "detected_languages": {
            "zh": "检测到目标语言",
            "en": "Detected target languages"
        },
        "select_mode": {
            "zh": "📋 选择翻译模式:",
            "en": "📋 Select translation mode:"
        },
        "mode_skip": {
            "zh": "跳过已翻译 - 只翻译状态为'new'或空值的条目",
            "en": "Skip translated - Only translate 'new' or empty entries"
        },
        "mode_full": {
            "zh": "全量翻译 - 重新翻译所有符合条件的条目",
            "en": "Full translation - Retranslate all qualifying entries"
        },
        "select_service": {
            "zh": "🌐 可用的翻译服务:",
            "en": "🌐 Available translation services:"
        },
        "requires_key": {
            "zh": "需要API密钥",
            "en": "Requires API key"
        },
        "free_usage": {
            "zh": "免费使用",
            "en": "Free to use"
        },
        "missing_vars": {
            "zh": "缺少环境变量",
            "en": "Missing environment variables"
        },
        "vars_configured": {
            "zh": "环境变量已配置",
            "en": "Environment variables configured"
        },
        "select_translator": {
            "zh": "请选择翻译服务 (1-4): ",
            "en": "Please select translation service (1-4): "
        },
        "invalid_choice": {
            "zh": "❌ 无效选择，请输入1-4之间的数字",
            "en": "❌ Invalid choice, please enter a number between 1-4"
        },
        "select_mode_prompt": {
            "zh": "请选择模式 (1-2): ",
            "en": "Please select mode (1-2): "
        },
        "invalid_mode": {
            "zh": "❌ 无效选择，请输入1或2",
            "en": "❌ Invalid choice, please enter 1 or 2"
        },
        "cancelled": {
            "zh": "👋 用户取消操作",
            "en": "👋 Operation cancelled"
        },
        "fallback_service": {
            "zh": "是否需要设置备用翻译服务?",
            "en": "Do you want to set up a fallback translation service?"
        },
        "select_fallback": {
            "zh": "选择备用翻译服务:",
            "en": "Select fallback translation service:"
        },
        "add_more_dict": {
            "zh": "是否添加更多词典文件? (y/N): ",
            "en": "Add more dictionary files? (y/N): "
        },
        "dict_path_prompt": {
            "zh": "请输入词典文件路径: ",
            "en": "Please enter dictionary file path: "
        },
        "dict_added": {
            "zh": "✅ 已添加词典",
            "en": "✅ Dictionary added"
        },
        "file_not_exist": {
            "zh": "❌ 文件不存在",
            "en": "❌ File does not exist"
        },
        "invalid_format": {
            "zh": "❌ 文件格式不支持，请使用 .xcstrings 或 .json 文件",
            "en": "❌ Unsupported file format, please use .xcstrings or .json files"
        },
        "no_input_file": {
            "zh": "❌ 未指定输入文件",
            "en": "❌ No input file specified"
        },
        "auto_dict": {
            "zh": "📚 自动发现词典",
            "en": "📚 Auto-discovered dictionary"
        },
        "using_api_translation": {
            "zh": "使用API翻译",
            "en": "Using API translation"
        },
        "output_format_prompt": {
            "zh": "请选择输出格式:",
            "en": "Please select output format:"
        },
        "output_format_same": {
            "zh": "保持与输入文件相同格式",
            "en": "Keep same format as input file"
        },
        "output_format_xcstrings": {
            "zh": "输出为 .xcstrings 格式",
            "en": "Output as .xcstrings format"
        },
        "output_format_json": {
            "zh": "输出为 .json 格式",
            "en": "Output as .json format"
        },
        "custom_output_prompt": {
            "zh": "请输入输出文件路径 (回车使用默认): ",
            "en": "Please enter output file path (Enter for default): "
        },
        "invalid_output_choice": {
            "zh": "❌ 无效选择，请输入1、2或3",
            "en": "❌ Invalid choice, please enter 1, 2 or 3"
        },
        "google_translator_name": {
            "zh": "Google翻译",
            "en": "Google Translate"
        },
        "google_translator_desc": {
            "zh": "免费API，无需密钥，可能有请求频率限制",
            "en": "Free API, no key required, may have rate limits"
        },
        "youdao_translator_name": {
            "zh": "有道翻译",
            "en": "Youdao Translate"
        },
        "youdao_translator_desc": {
            "zh": "需要APP_KEY和APP_SECRET，免费额度",
            "en": "Requires APP_KEY and APP_SECRET, free quota available"
        },
        "baidu_translator_name": {
            "zh": "百度翻译",
            "en": "Baidu Translate"
        },
        "baidu_translator_desc": {
            "zh": "每月免费200万字符，需要APP_ID和APP_KEY",
            "en": "2M free characters per month, requires APP_ID and APP_KEY"
        },
        "language_detection_failed": {
            "zh": "检测语言失败",
            "en": "Language detection failed"
        },
        "dictionary_loaded": {
            "zh": "已加载词典",
            "en": "Dictionary loaded"
        },
        "dictionary_load_failed": {
            "zh": "加载词典失败",
            "en": "Failed to load dictionary"
        },
        "dictionary_match": {
            "zh": "词典匹配",
            "en": "Dictionary match"
        },
        "dictionary_fuzzy_match": {
            "zh": "词典模糊匹配",
            "en": "Dictionary fuzzy match"
        },
        "google_translate_rate_limit": {
            "zh": "Google翻译请求过多",
            "en": "Google Translate rate limit exceeded"
        },
        "google_translate_failed": {
            "zh": "Google翻译失败",
            "en": "Google Translate failed"
        },
        "google_translate_error": {
            "zh": "Google翻译错误",
            "en": "Google Translate error"
        },
        "youdao_config_required": {
            "zh": "有道翻译需要配置APP_KEY和APP_SECRET",
            "en": "Youdao Translate requires APP_KEY and APP_SECRET configuration"
        },
        "youdao_api_error_411": {
            "zh": "有道翻译API错误411, 重试",
            "en": "Youdao Translate API error 411, retrying"
        },
        "youdao_api_error": {
            "zh": "有道翻译API错误",
            "en": "Youdao Translate API error"
        },
        "youdao_translate_failed": {
            "zh": "有道翻译失败",
            "en": "Youdao Translate failed"
        },
        "baidu_config_required": {
            "zh": "百度翻译需要配置APP_ID和APP_KEY",
            "en": "Baidu Translate requires APP_ID and APP_KEY configuration"
        },
        "baidu_api_error": {
            "zh": "百度翻译API错误",
            "en": "Baidu Translate API error"
        },
        "baidu_translate_failed": {
            "zh": "百度翻译失败",
            "en": "Baidu Translate failed"
        },
        "tencent_api_error": {
            "zh": "腾讯翻译API错误",
            "en": "Tencent Translate API error"
        },
        "tencent_translate_failed": {
            "zh": "腾讯翻译失败",
            "en": "Tencent Translate failed"
        },
        "primary_method_failed_trying_fallback": {
            "zh": "主要翻译方法失败，尝试备用方法",
            "en": "Primary translation method failed, trying fallback method"
        },
        "tencent_translator_name": {
            "zh": "腾讯翻译君",
            "en": "Tencent Translator"
        },
        "tencent_translator_desc": {
            "zh": "每月免费500万字符，需要SECRET_ID和SECRET_KEY",
            "en": "5M free characters per month, requires SECRET_ID and SECRET_KEY"
        },
        "dict_file_not_found": {
            "zh": "词典文件不存在",
            "en": "Dictionary file not found"
        },
        "dict_loaded": {
            "zh": "已加载 {} 个词典:",
            "en": "Loaded {} dictionaries:"
        },
        "dict_entries": {
            "zh": "{} 个条目",
            "en": "{} entries"
        },
        "supported_languages": {
            "zh": "支持语言",
            "en": "Supported languages"
        },
        "no_dict_loaded": {
            "zh": "未加载任何词典，将仅使用API翻译",
            "en": "No dictionaries loaded, will use API translation only"
        },
        "entries": {
            "zh": "个条目",
            "en": "entries"
        },
        "start_translation": {
            "zh": "开始翻译...",
            "en": "Starting translation..."
        },
        "translation_mode": {
            "zh": "翻译模式",
            "en": "Translation mode"
        },
        "skip_translated_mode": {
            "zh": "跳过已翻译",
            "en": "Skip translated"
        },
        "full_translation_mode": {
            "zh": "全量翻译",
            "en": "Full translation"
        },
        "target_languages": {
            "zh": "目标语言",
            "en": "Target languages"
        },
        "total_entries": {
            "zh": "总条目数",
            "en": "Total entries"
        },
        "translation_method": {
            "zh": "翻译方法",
            "en": "Translation method"
        },
        "fallback": {
            "zh": "备用",
            "en": "Fallback"
        },
        "translating": {
            "zh": "翻译",
            "en": "Translating"
        },
        "keep_original": {
            "zh": "保持原文",
            "en": "Keep original"
        },
        "skipped": {
            "zh": "跳过",
            "en": "Skipped"
        },
        "status": {
            "zh": "状态",
            "en": "Status"
        },
        "value": {
            "zh": "值",
            "en": "Value"
        },
        "translation_completed": {
            "zh": "翻译完成!",
            "en": "Translation completed!"
        },
        "successfully_translated": {
            "zh": "成功翻译",
            "en": "Successfully translated"
        },
        "skipped_translated": {
            "zh": "跳过已翻译",
            "en": "Skipped translated"
        },
        "output_file": {
            "zh": "输出文件",
            "en": "Output file"
        },
        "translation_failed": {
            "zh": "翻译失败",
            "en": "Translation failed"
        },
        "chinese": {
            "zh": "中文",
            "en": "Chinese"
        },
        "select_language_prompt": {
            "zh": "选择语言 / Select language (1-2): ",
            "en": "Select language (1-2): "
        },
        "invalid_choice_12": {
            "zh": "❌ 无效选择 / Invalid choice，请输入1或2",
            "en": "❌ Invalid choice, please enter 1 or 2"
        },
        "operation_cancelled": {
            "zh": "👋 用户取消操作 / Operation cancelled",
            "en": "👋 Operation cancelled"
        }
    }
    return texts.get(key, {}).get(lang, key)


def interactive_select_translator(lang: str = "zh"):
    """Interactive translation service selection"""
    translators = get_available_translators(lang)
    
    header_text = TerminalColors.themed_text(get_text('select_service', lang), AppState.get_theme(), 1.0)
    print(f"\n{header_text}")
    separator_text = TerminalColors.themed_text('═' * 60, AppState.get_theme(), 0.3)
    print(f"{separator_text}")
    
    for i, (key, info) in enumerate(translators.items(), 1):
        auth_status = f"🔑 {get_text('requires_key', lang)}" if info["requires_auth"] else f"🆓 {get_text('free_usage', lang)}"
        number_text = TerminalColors.themed_text(f"{i}.", AppState.get_theme(), 0.8)
        name_text = TerminalColors.themed_text(info['name'], AppState.get_theme(), 1.0)
        print(f"{number_text} {name_text} - {auth_status}")
        desc_text = TerminalColors.themed_text(f"   {info['description']}", AppState.get_theme(), 0.5)
        print(f"{desc_text}")
        
        if info["requires_auth"]:
            missing_vars = []
            for var in info["env_vars"]:
                if not os.getenv(var):
                    missing_vars.append(var)
            
            if missing_vars:
                warning_text = TerminalColors.themed_text(f"   ⚠️  {get_text('missing_vars', lang)}: {', '.join(missing_vars)}", "yellow", 0.8)
                print(f"{warning_text}")
            else:
                success_text = TerminalColors.themed_text(f"   ✅ {get_text('vars_configured', lang)}", "green", 0.8)
                print(f"{success_text}")
        print()
    
    while True:
        try:
            prompt_text = TerminalColors.themed_text(get_text('select_translator', lang), AppState.get_theme(), 1.0)
            choice = input(f"{prompt_text}").strip()
            if choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(translators):
                    selected_key = list(translators.keys())[choice_num - 1]
                    return selected_key
            error_text = TerminalColors.themed_text(get_text('invalid_choice', lang), "red", 0.8)
            print(f"{error_text}")
        except KeyboardInterrupt:
            cancel_text = TerminalColors.themed_text(f"\n{get_text('cancelled', lang)}", "yellow", 0.8)
            print(f"{cancel_text}")
            return None


def interactive_select_mode(lang: str = "zh"):
    """Interactive translation mode selection"""
    header_text = TerminalColors.themed_text(get_text('select_mode', lang), AppState.get_theme(), 1.0)
    print(f"\n{header_text}")
    separator_text = TerminalColors.themed_text('═' * 40, AppState.get_theme(), 0.3)
    print(f"{separator_text}")
    option1_text = TerminalColors.themed_text("1.", AppState.get_theme(), 0.8)
    option2_text = TerminalColors.themed_text("2.", AppState.get_theme(), 0.8)
    print(f"{option1_text} {get_text('mode_skip', lang)}")
    print(f"{option2_text} {get_text('mode_full', lang)}")
    print()
    
    while True:
        try:
            prompt_text = TerminalColors.themed_text(get_text('select_mode_prompt', lang), AppState.get_theme(), 1.0)
            choice = input(f"{prompt_text}").strip()
            if choice == "1":
                return True  # Skip translated
            elif choice == "2":
                return False  # Full translation
            else:
                error_text = TerminalColors.themed_text(get_text('invalid_mode', lang), "red", 0.8)
                print(f"{error_text}")
        except KeyboardInterrupt:
            cancel_text = TerminalColors.themed_text(f"\n{get_text('cancelled', lang)}", "yellow", 0.8)
            print(f"{cancel_text}")
            return None


def interactive_select_output_format(input_file: str, lang: str = "zh"):
    """Interactive output format selection"""
    header_text = TerminalColors.themed_text(get_text('output_format_prompt', lang), AppState.get_theme(), 1.0)
    print(f"\n{header_text}")
    separator_text = TerminalColors.themed_text('═' * 40, AppState.get_theme(), 0.3)
    print(f"{separator_text}")
    option1_text = TerminalColors.themed_text("1.", AppState.get_theme(), 0.8)
    option2_text = TerminalColors.themed_text("2.", AppState.get_theme(), 0.8)
    option3_text = TerminalColors.themed_text("3.", AppState.get_theme(), 0.8)
    print(f"{option1_text} {get_text('output_format_same', lang)}")
    print(f"{option2_text} {get_text('output_format_xcstrings', lang)}")
    print(f"{option3_text} {get_text('output_format_json', lang)}")
    print()
    
    while True:
        try:
            prompt_text = TerminalColors.themed_text(get_text('select_mode_prompt', lang), AppState.get_theme(), 1.0)
            choice = input(f"{prompt_text}").strip()
            if choice == "1":
                # Keep same format
                if input_file.endswith('.xcstrings'):
                    return generate_output_filename(input_file, '.xcstrings')
                elif input_file.endswith('.json'):
                    return generate_output_filename(input_file, '.json')
            elif choice == "2":
                return generate_output_filename(input_file, '.xcstrings')
            elif choice == "3":
                return generate_output_filename(input_file, '.json')
            else:
                error_text = TerminalColors.themed_text(get_text('invalid_output_choice', lang), "red", 0.8)
                print(f"{error_text}")
        except KeyboardInterrupt:
            cancel_text = TerminalColors.themed_text(f"\n{get_text('cancelled', lang)}", "yellow", 0.8)
            print(f"{cancel_text}")
            return None


def generate_output_filename(input_file: str, extension: str) -> str:
    """Generate output filename based on input file and extension"""
    # Get file directory and base name
    directory = os.path.dirname(input_file)
    basename = os.path.basename(input_file)
    
    # Remove original extension
    if basename.endswith('.xcstrings'):
        base_name = basename[:-10]  # Remove .xcstrings
    elif basename.endswith('.json'):
        base_name = basename[:-5]   # Remove .json
    else:
        base_name = os.path.splitext(basename)[0]
    
    # Generate new filename
    output_filename = f"{base_name}_translated{extension}"
    
    if directory:
        return os.path.join(directory, output_filename)
    else:
        return output_filename


def validate_input_file(file_path: str, lang: str = "zh") -> Tuple[bool, str]:
    """Validate input file format"""
    if not file_path:
        return False, get_text('no_input_file', lang)
    
    if not os.path.exists(file_path):
        return False, f"{get_text('file_not_exist', lang)}: {file_path}"
    
    if not (file_path.endswith('.xcstrings') or file_path.endswith('.json')):
        return False, get_text('invalid_format', lang)
    
    return True, ""


def main():
    """Main function for command-line interface"""
    # Load saved configuration
    AppState.load_config()
    
    # Display beautiful app title with saved/default theme
    display_app_title(AppState.get_theme())
    
    # Use saved language preference, or ask user if not set
    interface_lang = AppState.get_language()
    if not interface_lang or interface_lang not in ['zh', 'en']:
        interface_lang = interactive_select_language()
        if not interface_lang:
            sys.exit(1)
        # Save the selected language
        AppState.set_language(interface_lang)
    
    # Then select color theme (will apply to subsequent interactions)
    color_theme = select_color_theme(interface_lang)
    AppState.set_theme(color_theme)
    
    # Show theme selection confirmation
    theme_info = ColorTheme.THEMES[color_theme]
    if interface_lang == "en":
        confirmation_text = f"✅ Theme set to {theme_info['name']}, will take effect on next startup"
    else:
        confirmation_text = f"✅ 主题已设置为 {theme_info['name']}，将在下次启动时生效"
    
    themed_confirmation = TerminalColors.themed_text(confirmation_text, color_theme, 0.9)
    print(f"\n{themed_confirmation}")
    print()
    
    print()
    separator_text = TerminalColors.themed_text('═' * 70, AppState.get_theme(), 0.3)
    print(f"{separator_text}")
    
    # Interactive mode
    if len(sys.argv) < 2:
        usage_text = TerminalColors.themed_text(get_text('usage', interface_lang), AppState.get_theme(), 0.8)
        print(f"\n{usage_text}")
        command_text = TerminalColors.themed_text("  python3 auto_strings_catalogs_translator.py <input_file> [output_file] [dict1.csv] [dict2.csv] ...", AppState.get_theme(), 0.4)
        print(f"{command_text}")
        print()
        interactive_text = TerminalColors.themed_text(get_text('interactive_mode', interface_lang), AppState.get_theme(), 0.6)
        print(f"{interactive_text}")
        
        # Input file selection and validation
        while True:
            prompt_text = TerminalColors.themed_text(get_text('input_file_prompt', interface_lang), AppState.get_theme(), 1.0)
            input_file = input(f"\n{prompt_text}").strip()
            valid, error_msg = validate_input_file(input_file, interface_lang)
            if valid:
                break
            else:
                error_text = TerminalColors.themed_text(error_msg, "red", 0.8)
                print(f"{error_text}")
                if not input_file:  # User pressed Enter to exit
                    sys.exit(1)
        
        # Detect target languages from input file
        target_languages = LanguageDetector.detect_target_languages(input_file)
        if target_languages:
            detected_text = TerminalColors.themed_text(f"🎯 {get_text('detected_languages', interface_lang)}:", AppState.get_theme(), 0.9)
            print(f"\n{detected_text}")
            for lang_code in sorted(target_languages):
                lang_name = LanguageDetector.get_language_name(lang_code, interface_lang)
                lang_text = TerminalColors.themed_text(f"  • {lang_name} ({lang_code})", AppState.get_theme(), 0.5)
                print(f"{lang_text}")
        else:
            error_text = TerminalColors.themed_text("❌ 未检测到目标语言", "red", 0.8)
            print(f"{error_text}")
            sys.exit(1)
        
        # Select output format and auto-generate filename
        output_file = interactive_select_output_format(input_file, interface_lang)
        if not output_file:
            sys.exit(1)
        
        # Ask for custom output path
        prompt_text = TerminalColors.themed_text(get_text('custom_output_prompt', interface_lang), AppState.get_theme(), 1.0)
        custom_output = input(f"\n{prompt_text}").strip()
        if custom_output:
            output_file = custom_output
        
        # Select translation mode
        skip_translated = interactive_select_mode(interface_lang)
        if skip_translated is None:
            sys.exit(1)
        
        # Select translation service
        method = interactive_select_translator(interface_lang)
        if not method:
            sys.exit(1)
        
        # Select fallback translation service
        fallback_text = TerminalColors.themed_text(get_text('fallback_service', interface_lang), AppState.get_theme(), 0.8)
        print(f"\n{fallback_text}")
        choice_text = TerminalColors.themed_text("(y/N): ", AppState.get_theme(), 1.0)
        fallback_choice = input(f"{choice_text}").strip().lower()
        fallback_method = None
        if fallback_choice in ['y', 'yes']:
            select_text = TerminalColors.themed_text(get_text('select_fallback', interface_lang), AppState.get_theme(), 0.8)
            print(f"{select_text}")
            fallback_method = interactive_select_translator(interface_lang)
        
        # Dictionary file configuration
        dictionary_paths = []
        
        # Default dictionary path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        default_dict = os.path.join(script_dir, "dictionaries", "AppleWatchWorkoutTypes.csv")
        if os.path.exists(default_dict):
            dictionary_paths.append(default_dict)
            auto_dict_text = TerminalColors.themed_text(f"{get_text('auto_dict', interface_lang)}: {default_dict}", AppState.get_theme(), 0.7)
            print(f"\n{auto_dict_text}")
        
        # Ask for additional dictionaries
        while True:
            add_dict_text = TerminalColors.themed_text(get_text('add_more_dict', interface_lang), AppState.get_theme(), 1.0)
            add_dict = input(f"\n{add_dict_text}").strip().lower()
            if add_dict in ['y', 'yes']:
                dict_path_text = TerminalColors.themed_text(get_text('dict_path_prompt', interface_lang), AppState.get_theme(), 1.0)
                dict_path = input(f"{dict_path_text}").strip()
                if dict_path and os.path.exists(dict_path):
                    dictionary_paths.append(dict_path)
                    success_text = TerminalColors.themed_text(f"{get_text('dict_added', interface_lang)}: {dict_path}", "green", 0.8)
                    print(f"{success_text}")
                elif dict_path:
                    error_text = TerminalColors.themed_text(f"{get_text('file_not_exist', interface_lang)}: {dict_path}", "red", 0.8)
                    print(f"{error_text}")
            else:
                break
    else:
        # Command line mode - use saved language preference
        interface_lang = AppState.get_language()
        
        input_file = sys.argv[1]
        
        # Validate input file
        valid, error_msg = validate_input_file(input_file, interface_lang)
        if not valid:
            error_text = TerminalColors.themed_text(error_msg, "red", 0.8)
            print(f"{error_text}")
            sys.exit(1)
        
        # Detect target languages
        target_languages = LanguageDetector.detect_target_languages(input_file)
        if not target_languages:
            error_text = TerminalColors.themed_text("❌ 未检测到目标语言", "red", 0.8)
            print(f"{error_text}")
            sys.exit(1)
        
        output_file = sys.argv[2] if len(sys.argv) > 2 else generate_output_filename(input_file, 
            '.xcstrings' if input_file.endswith('.xcstrings') else '.json')
        
        # Dictionary files from command line arguments
        dictionary_paths = sys.argv[3:] if len(sys.argv) > 3 else []
        
        # Default settings
        skip_translated = False
        method = "google"
        fallback_method = None
        
        # If no dictionaries specified, try to use default
        if not dictionary_paths:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            default_dict = os.path.join(script_dir, "dictionaries", "AppleWatchWorkoutTypes.csv")
            if os.path.exists(default_dict):
                dictionary_paths.append(default_dict)
    
    # Execute translation
    start_text = "🔄 开始翻译..." if interface_lang == "zh" else "🔄 Starting translation..."
    input_text = "输入文件" if interface_lang == "zh" else "Input file"
    output_text = "输出文件" if interface_lang == "zh" else "Output file"
    dict_text = "词典文件" if interface_lang == "zh" else "Dictionary files"
    
    separator_text = TerminalColors.themed_text('═' * 70, AppState.get_theme(), 0.3)
    print(f"\n{separator_text}")
    start_themed_text = TerminalColors.themed_text(start_text, "green", 0.9)
    print(f"\n{start_themed_text}")
    input_themed_text = TerminalColors.themed_text(f"{input_text}: {input_file}", AppState.get_theme(), 0.4)
    print(f"{input_themed_text}")
    output_themed_text = TerminalColors.themed_text(f"{output_text}: {output_file}", AppState.get_theme(), 0.4)
    print(f"{output_themed_text}")
    if dictionary_paths:
        dict_themed_text = TerminalColors.themed_text(f"{dict_text}: {', '.join(dictionary_paths)}", AppState.get_theme(), 0.4)
        print(f"{dict_themed_text}")
    
    translate_xcstrings_file(input_file, output_file, target_languages, method, fallback_method, skip_translated, dictionary_paths, interface_lang)


if __name__ == "__main__":
    main()