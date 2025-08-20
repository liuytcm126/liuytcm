#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
神经内科常用量表评估系统
开发人员：LIUYING
版本：1.0.0
描述：专业的神经内科临床量表评估工具
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from pathlib import Path

# 导入量表模块
try:
    from scales.cognitive import CognitiveScales
except ImportError:
    CognitiveScales = None
    
try:
    from scales.emotion import EmotionScales
except ImportError:
    EmotionScales = None

try:
    from scales.motor import MotorScales
except ImportError:
    MotorScales = None

try:
    from scales.severity import SeverityScales
except ImportError:
    SeverityScales = None

# 导入数据管理和评分系统
try:
    from data_manager import DataManager
except ImportError:
    DataManager = None
    
try:
    from scoring_system import ScoringSystem
except ImportError:
    ScoringSystem = None

try:
    from help_system import HelpSystem
except ImportError:
    HelpSystem = None

class NeurologicalScaleApp:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_styles()
        self.create_main_interface()
        
        # 初始化量表模块
        self.cognitive_scales = None
        self.emotion_scales = None
        self.motor_scales = None
        self.severity_scales = None
        
        # 初始化数据管理和评分系统
        self.data_manager = DataManager(self.root, self) if DataManager else None
        self.scoring_system = ScoringSystem() if ScoringSystem else None
        
    def setup_window(self):
        """设置主窗口"""
        self.root.title("神经内科常用量表评估系统 - 开发者：LIUYING")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # 设置窗口居中
        self.center_window()
        
        # 设置窗口图标（如果有的话）
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
            
    def center_window(self):
        """窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_styles(self):
        """设置样式主题"""
        style = ttk.Style()
        
        # 配置主题色彩
        self.colors = {
            'primary': '#2E86AB',      # 主色调 - 医疗蓝
            'secondary': '#A23B72',    # 次要色 - 深粉
            'accent': '#F18F01',       # 强调色 - 橙色
            'background': '#F8F9FA',   # 背景色 - 浅灰
            'surface': '#FFFFFF',      # 表面色 - 白色
            'text': '#212529',         # 文本色 - 深灰
            'text_secondary': '#6C757D' # 次要文本色 - 中灰
        }
        
        # 配置ttk样式
        style.configure('Title.TLabel', 
                       font=('Microsoft YaHei', 24, 'bold'),
                       foreground=self.colors['primary'])
        
        style.configure('Heading.TLabel',
                       font=('Microsoft YaHei', 16, 'bold'),
                       foreground=self.colors['text'])
        
        style.configure('Card.TFrame',
                       background=self.colors['surface'],
                       relief='solid',
                       borderwidth=1)
        
    def create_main_interface(self):
        """创建主界面"""
        # 主容器
        main_container = ttk.Frame(self.root)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 标题区域
        self.create_header(main_container)
        
        # 内容区域
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill='both', expand=True, pady=(20, 0))
        
        # 左侧导航
        self.create_navigation(content_frame)
        
        # 右侧主要内容区域
        self.create_main_content(content_frame)
        
    def create_header(self, parent):
        """创建头部区域"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill='x', pady=(0, 20))
        
        # 主标题
        title_label = ttk.Label(header_frame, 
                               text="神经内科常用量表评估系统",
                               style='Title.TLabel')
        title_label.pack(side='left')
        
        # 开发者信息
        dev_label = ttk.Label(header_frame,
                             text="开发者：LIUYING",
                             font=('Microsoft YaHei', 10),
                             foreground=self.colors['text_secondary'])
        dev_label.pack(side='right')
        
    def create_navigation(self, parent):
        """创建左侧导航"""
        nav_frame = ttk.LabelFrame(parent, text="功能导航", padding=15)
        nav_frame.pack(side='left', fill='y', padx=(0, 20))
        nav_frame.configure(width=250)
        
        # 量表评估导航
        scale_label = ttk.Label(nav_frame, text="量表评估", font=('Microsoft YaHei', 10, 'bold'))
        scale_label.pack(fill='x', pady=(0, 10))
        
        # 导航按钮
        nav_buttons = [
            ("认知功能评估", "cognitive", "MMSE、MoCA等量表"),
            ("情绪障碍评估", "emotion", "HAMD、HAMA等量表"),
            ("运动功能评估", "motor", "UPDRS等量表"),
            ("疾病严重程度评估", "severity", "各类疾病严重程度量表")
        ]
        
        self.nav_buttons = {}
        for i, (text, key, desc) in enumerate(nav_buttons):
            btn_frame = ttk.Frame(nav_frame)
            btn_frame.pack(fill='x', pady=5)
            
            btn = ttk.Button(btn_frame, 
                           text=text,
                           command=lambda k=key: self.show_scale_category(k))
            btn.pack(fill='x')
            
            desc_label = ttk.Label(btn_frame,
                                 text=desc,
                                 font=('Microsoft YaHei', 8),
                                 foreground=self.colors['text_secondary'])
            desc_label.pack(fill='x', pady=(2, 0))
            
            self.nav_buttons[key] = btn
        
        # 数据管理导航
        ttk.Separator(nav_frame, orient='horizontal').pack(fill='x', pady=20)
        
        data_label = ttk.Label(nav_frame, text="数据管理", font=('Microsoft YaHei', 10, 'bold'))
        data_label.pack(fill='x', pady=(0, 10))
        
        # 数据管理按钮
        data_buttons = [
            ("查看评估记录", "view_records", "查看历史评估数据"),
            ("统计分析", "statistics", "数据统计与分析"),
            ("数据导出", "export_data", "导出评估报告")
        ]
        
        for text, key, desc in data_buttons:
            btn_frame = ttk.Frame(nav_frame)
            btn_frame.pack(fill='x', pady=5)
            
            btn = ttk.Button(btn_frame, 
                           text=text,
                           command=lambda k=key: self.show_data_management(k))
            btn.pack(fill='x')
            
            desc_label = ttk.Label(btn_frame,
                                 text=desc,
                                 font=('Microsoft YaHei', 8),
                                 foreground=self.colors['text_secondary'])
            desc_label.pack(fill='x', pady=(2, 0))
        
        # 帮助与支持导航
        ttk.Separator(nav_frame, orient='horizontal').pack(fill='x', pady=20)
        
        help_label = ttk.Label(nav_frame, text="帮助与支持", font=('Microsoft YaHei', 10, 'bold'))
        help_label.pack(fill='x', pady=(0, 10))
        
        # 帮助按钮
        help_buttons = [
            ("用户手册", "user_manual", "详细使用说明"),
            ("关于系统", "about", "系统信息与版本")
        ]
        
        for text, key, desc in help_buttons:
            btn_frame = ttk.Frame(nav_frame)
            btn_frame.pack(fill='x', pady=5)
            
            btn = ttk.Button(btn_frame, 
                           text=text,
                           command=lambda k=key: self.show_help(k))
            btn.pack(fill='x')
            
            desc_label = ttk.Label(btn_frame,
                                 text=desc,
                                 font=('Microsoft YaHei', 8),
                                 foreground=self.colors['text_secondary'])
            desc_label.pack(fill='x', pady=(2, 0))
            
            self.nav_buttons[key] = btn
            
    def create_main_content(self, parent):
        """创建主要内容区域"""
        self.content_frame = ttk.Frame(parent)
        self.content_frame.pack(side='right', fill='both', expand=True)
        
        # 默认显示欢迎界面
        self.show_welcome_screen()
        
    def show_welcome_screen(self):
        """显示欢迎界面"""
        self.clear_content()
        
        welcome_frame = ttk.Frame(self.content_frame)
        welcome_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 欢迎标题
        welcome_title = ttk.Label(welcome_frame,
                                text="欢迎使用神经内科量表评估系统",
                                style='Heading.TLabel')
        welcome_title.pack(pady=(50, 30))
        
        # 系统介绍
        intro_text = """
本系统为神经内科医师提供权威全面的常用量表评估功能，包括：

• 认知功能评估量表（MMSE、MoCA等）
• 情绪障碍评估量表（HAMD、HAMA等）  
• 运动功能评估量表（UPDRS等）
• 疾病严重程度评估量表

系统特点：
✓ 自动化评分计算
✓ 标准化评估流程
✓ 专业权威的评分标准
✓ 直观的数据展示

请从左侧导航选择相应的量表分类开始评估。
        """
        
        intro_label = ttk.Label(welcome_frame,
                              text=intro_text,
                              font=('Microsoft YaHei', 12),
                              justify='left')
        intro_label.pack(pady=20)
        
    def show_scale_category(self, category):
        """显示量表分类内容"""
        self.clear_content()
        
        category_frame = ttk.Frame(self.content_frame)
        category_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 分类标题
        titles = {
            'cognitive': '认知功能评估量表',
            'emotion': '情绪障碍评估量表', 
            'motor': '运动功能评估量表',
            'severity': '疾病严重程度评估量表'
        }
        
        title_label = ttk.Label(category_frame,
                              text=titles.get(category, '量表评估'),
                              style='Heading.TLabel')
        title_label.pack(pady=(0, 20))
        
        # 量表列表
        scales = self.get_scales_by_category(category)
        
        for scale in scales:
            scale_card = self.create_scale_card(category_frame, scale, category)
            scale_card.pack(fill='x', pady=10)
            
    def get_scales_by_category(self, category):
        """根据分类获取量表列表"""
        scales_data = {
            'cognitive': [
                {'name': 'MMSE', 'id': 'mmse', 'full_name': '简易精神状态检查量表', 'items': 30, 'available': True},
                {'name': 'MoCA', 'id': 'moca', 'full_name': '蒙特利尔认知评估量表', 'items': 30, 'available': True},
                {'name': 'CDR', 'id': 'cdr', 'full_name': '临床痴呆评定量表', 'items': 6, 'available': True}
            ],
            'emotion': [
                {'name': 'HAMD', 'id': 'hamd', 'full_name': '汉密尔顿抑郁量表', 'items': 17, 'available': True},
                {'name': 'HAMA', 'id': 'hama', 'full_name': '汉密尔顿焦虑量表', 'items': 14, 'available': True},
                {'name': 'SDS', 'id': 'sds', 'full_name': '抑郁自评量表', 'items': 20, 'available': True}
            ],
            'motor': [
                {'name': 'UPDRS', 'id': 'updrs', 'full_name': '统一帕金森病评定量表', 'items': 42, 'available': True},
                {'name': 'Berg', 'id': 'berg', 'full_name': 'Berg平衡量表', 'items': 14, 'available': True},
                {'name': 'Tinetti', 'id': 'tinetti', 'full_name': 'Tinetti步态与平衡评估', 'items': 28, 'available': True}
            ],
            'severity': [
                {'name': 'NIHSS', 'id': 'nihss', 'full_name': '美国国立卫生研究院卒中量表', 'items': 15, 'available': True},
                {'name': 'GCS', 'id': 'gcs', 'full_name': '格拉斯哥昏迷量表', 'items': 3, 'available': True},
                {'name': 'mRS', 'id': 'mrs', 'full_name': '改良Rankin量表', 'items': 7, 'available': True}
            ]
        }
        
        return scales_data.get(category, [])
        
    def create_scale_card(self, parent, scale_info, category):
        """创建量表卡片"""
        card_frame = ttk.LabelFrame(parent, text=scale_info['name'], padding=15)
        
        # 量表信息
        info_frame = ttk.Frame(card_frame)
        info_frame.pack(fill='x')
        
        name_label = ttk.Label(info_frame,
                             text=scale_info['full_name'],
                             font=('Microsoft YaHei', 12, 'bold'))
        name_label.pack(anchor='w')
        
        items_label = ttk.Label(info_frame,
                              text=f"评估项目：{scale_info['items']}项",
                              font=('Microsoft YaHei', 10),
                              foreground=self.colors['text_secondary'])
        items_label.pack(anchor='w', pady=(5, 0))
        
        # 可用性标识
        if scale_info.get('available', False):
            status_label = ttk.Label(info_frame,
                                   text="✓ 可用",
                                   font=('Microsoft YaHei', 10),
                                   foreground='#28A745')
        else:
            status_label = ttk.Label(info_frame,
                                   text="⚠ 开发中",
                                   font=('Microsoft YaHei', 10),
                                   foreground='#FFC107')
        status_label.pack(anchor='w', pady=(2, 0))
        
        # 操作按钮
        btn_frame = ttk.Frame(card_frame)
        btn_frame.pack(fill='x', pady=(15, 0))
        
        if scale_info.get('available', False):
            start_btn = ttk.Button(btn_frame,
                                 text="开始评估",
                                 command=lambda: self.start_assessment(scale_info, category))
            start_btn.pack(side='left', padx=(0, 10))
        else:
            start_btn = ttk.Button(btn_frame,
                                 text="开始评估",
                                 state='disabled')
            start_btn.pack(side='left', padx=(0, 10))
        
        info_btn = ttk.Button(btn_frame,
                            text="查看说明",
                            command=lambda: self.show_scale_info(scale_info))
        info_btn.pack(side='left')
        
        return card_frame
        
    def start_assessment(self, scale_info, category):
        """开始量表评估"""
        self.clear_content()
        
        if category == "cognitive":
            if not self.cognitive_scales:
                self.cognitive_scales = CognitiveScales(self.content_frame, self) if CognitiveScales else None
            if self.cognitive_scales:
                if scale_info['id'] == 'mmse':
                    self.cognitive_scales.show_mmse_assessment()
                elif scale_info['id'] == 'moca':
                    self.cognitive_scales.show_moca_assessment()
                elif scale_info['id'] == 'cdr':
                    self.cognitive_scales.show_cdr_assessment()
        
        elif category == "emotion":
            if not self.emotion_scales:
                self.emotion_scales = EmotionScales(self.content_frame, self) if EmotionScales else None
            if self.emotion_scales:
                if scale_info['id'] == 'hamd':
                    self.emotion_scales.show_hamd_assessment()
                elif scale_info['id'] == 'hama':
                    self.emotion_scales.show_hama_assessment()
                elif scale_info['id'] == 'sds':
                    self.emotion_scales.show_sds_assessment()
        
        elif category == "motor":
            if not self.motor_scales:
                self.motor_scales = MotorScales(self.content_frame, self) if MotorScales else None
            if self.motor_scales:
                if scale_info['id'] == 'updrs':
                    self.motor_scales.show_updrs_assessment()
                elif scale_info['id'] == 'berg':
                    self.motor_scales.show_berg_assessment()
                elif scale_info['id'] == 'tinetti':
                    self.motor_scales.show_tinetti_assessment()
        
        elif category == "severity":
            if not self.severity_scales:
                self.severity_scales = SeverityScales(self.content_frame, self) if SeverityScales else None
            if self.severity_scales:
                if scale_info['id'] == 'nihss':
                    self.severity_scales.show_nihss_assessment()
                elif scale_info['id'] == 'gcs':
                    self.severity_scales.show_gcs_assessment()
                elif scale_info['id'] == 'mrs':
                    self.severity_scales.show_mrs_assessment()
        
        else:
            messagebox.showinfo("提示", f"{scale_info['name']}功能正在开发中")
        
    def show_scale_info(self, scale_info):
        """显示量表说明"""
        info_texts = {
            'MMSE': """
简易精神状态检查量表 (Mini-Mental State Examination)

用途：筛查认知功能障碍
适用人群：成年人
评估时间：5-10分钟
总分：30分

评估内容：
• 定向力（时间、地点）
• 即刻记忆
• 注意力和计算力
• 延迟回忆
• 语言能力

评分标准：
• 27-30分：正常
• 24-26分：轻度认知障碍
• 18-23分：中度认知障碍
• 0-17分：重度认知障碍
            """,
            'HAMD': """
汉密尔顿抑郁量表 (Hamilton Depression Rating Scale)

用途：评估抑郁症状严重程度
适用人群：成年人
评估时间：15-20分钟
总分：52分（17项版本）

评估内容：
• 抑郁情绪
• 有罪感
• 自杀倾向
• 睡眠障碍
• 工作和兴趣
• 精神运动性症状
• 焦虑症状
• 躯体症状

评分标准：
• 0-7分：无抑郁症状
• 8-16分：轻度抑郁
• 17-23分：中度抑郁
• ≥24分：重度抑郁
            """
        }
        
        info_text = info_texts.get(scale_info['name'], f"{scale_info['full_name']}\n\n详细说明功能正在开发中...")
        
        # 创建信息窗口
        info_window = tk.Toplevel(self.root)
        info_window.title(f"{scale_info['name']} - 量表说明")
        info_window.geometry("500x400")
        info_window.resizable(False, False)
        
        # 居中显示
        info_window.transient(self.root)
        info_window.grab_set()
        
        main_frame = ttk.Frame(info_window, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame,
                               text=scale_info['full_name'],
                               font=('Microsoft YaHei', 14, 'bold'),
                               foreground=self.colors['primary'])
        title_label.pack(pady=(0, 20))
        
        # 说明文本
        text_widget = tk.Text(main_frame,
                             font=('Microsoft YaHei', 10),
                             wrap='word',
                             height=15,
                             width=50)
        text_widget.pack(fill='both', expand=True, pady=(0, 20))
        text_widget.insert('1.0', info_text)
        text_widget.config(state='disabled')
        
        # 关闭按钮
        close_btn = ttk.Button(main_frame,
                              text="关闭",
                              command=info_window.destroy)
        close_btn.pack()
        
    def show_data_management(self, function_type):
        """显示数据管理功能"""
        if not self.data_manager:
            messagebox.showerror("错误", "数据管理模块未正确加载")
            return
            
        self.clear_content()
        
        if function_type == "view_records":
            self.data_manager.show_data_viewer(self.content_frame)
        elif function_type == "statistics":
            self.data_manager.show_statistics(self.content_frame)
        elif function_type == "export_data":
            self.data_manager.show_export_options(self.content_frame)
        
    def show_help(self, help_type):
        """显示帮助信息"""
        if not HelpSystem:
            messagebox.showerror("错误", "帮助系统模块未正确加载")
            return
            
        self.clear_content()
        help_system = HelpSystem(self.content_frame)
        
        if help_type == "user_manual":
            help_system.show_user_manual()
        elif help_type == "about":
            help_system.show_about()
    
    def clear_content(self):
        """清空内容区域"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

def main():
    """主函数"""
    # 创建必要的目录
    os.makedirs('scales', exist_ok=True)
    os.makedirs('results', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    root = tk.Tk()
    app = NeurologicalScaleApp(root)
    
    # 设置关闭事件
    def on_closing():
        if messagebox.askokcancel("退出", "确定要退出神经内科量表评估系统吗？"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # 启动应用
    root.mainloop()

if __name__ == "__main__":
    main()