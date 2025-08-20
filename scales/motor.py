#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运动功能评估量表模块
开发人员：LIUYING
包含：UPDRS、Berg平衡量表、Tinetti步态与平衡评估等量表
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json

class MotorScales:
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        self.current_scale = None
        self.current_responses = {}
        
    def show_updrs_assessment(self):
        """显示UPDRS评估界面"""
        self.current_scale = 'UPDRS'
        self.current_responses = {}
        
        # 清空父容器
        for widget in self.parent.winfo_children():
            widget.destroy()
            
        # 创建UPDRS评估界面
        self.create_updrs_interface()
        
    def create_updrs_interface(self):
        """创建UPDRS评估界面"""
        # 主容器
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 标题区域
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = ttk.Label(title_frame,
                               text="统一帕金森病评定量表 (UPDRS-III)",
                               font=('Microsoft YaHei', 18, 'bold'),
                               foreground='#2E86AB')
        title_label.pack(side='left')
        
        # 返回按钮
        back_btn = ttk.Button(title_frame,
                             text="返回",
                             command=self.back_to_category,
                             style='Accent.TButton')
        back_btn.pack(side='right')
        
        # 创建滚动区域
        canvas = tk.Canvas(main_frame, bg='white')
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 患者信息区域
        self.create_patient_info_section(scrollable_frame)
        
        # UPDRS评估项目
        self.create_updrs_items(scrollable_frame)
        
        # 底部按钮
        self.create_bottom_buttons(scrollable_frame)
        
        # 布局滚动区域
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 绑定鼠标滚轮
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
    def create_patient_info_section(self, parent):
        """创建患者信息区域"""
        info_frame = ttk.LabelFrame(parent, text="患者信息", padding=15)
        info_frame.pack(fill='x', pady=(0, 20))
        
        # 第一行：姓名、性别、年龄
        row1 = ttk.Frame(info_frame)
        row1.pack(fill='x', pady=5)
        
        ttk.Label(row1, text="姓名:").pack(side='left')
        self.name_var = tk.StringVar()
        ttk.Entry(row1, textvariable=self.name_var, width=15).pack(side='left', padx=(5, 20))
        
        ttk.Label(row1, text="性别:").pack(side='left')
        self.gender_var = tk.StringVar()
        gender_combo = ttk.Combobox(row1, textvariable=self.gender_var, values=['男', '女'], width=8, state='readonly')
        gender_combo.pack(side='left', padx=(5, 20))
        
        ttk.Label(row1, text="年龄:").pack(side='left')
        self.age_var = tk.StringVar()
        ttk.Entry(row1, textvariable=self.age_var, width=8).pack(side='left', padx=(5, 0))
        
        # 第二行：病程、评估日期
        row2 = ttk.Frame(info_frame)
        row2.pack(fill='x', pady=5)
        
        ttk.Label(row2, text="病程(年):").pack(side='left')
        self.duration_var = tk.StringVar()
        ttk.Entry(row2, textvariable=self.duration_var, width=10).pack(side='left', padx=(5, 20))
        
        ttk.Label(row2, text="评估日期:").pack(side='left')
        self.date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        ttk.Entry(row2, textvariable=self.date_var, width=15).pack(side='left', padx=(5, 0))
        
    def create_updrs_items(self, parent):
        """创建UPDRS评估项目"""
        items_frame = ttk.LabelFrame(parent, text="UPDRS-III 运动检查 (共14项)", padding=15)
        items_frame.pack(fill='x', pady=(0, 20))
        
        # UPDRS-III评估项目
        updrs_items = [
            {
                'id': 1,
                'title': '3.1 言语',
                'description': '评估患者的言语清晰度和音量',
                'options': ['0-正常', '1-轻度言语不清或音量小', '2-中度言语不清', '3-重度言语不清', '4-言语不能理解或失语']
            },
            {
                'id': 2,
                'title': '3.2 面部表情',
                'description': '评估面部表情的丰富程度',
                'options': ['0-正常', '1-轻微面具脸', '2-轻度面具脸', '3-中度面具脸', '4-重度面具脸']
            },
            {
                'id': 3,
                'title': '3.3 颈部僵硬',
                'description': '评估颈部肌肉僵硬程度',
                'options': ['0-无', '1-轻微僵硬', '2-轻度僵硬', '3-中度僵硬', '4-重度僵硬']
            },
            {
                'id': 4,
                'title': '3.4 上肢僵硬',
                'description': '评估上肢肌肉僵硬程度',
                'options': ['0-无', '1-轻微僵硬', '2-轻度僵硬', '3-中度僵硬', '4-重度僵硬']
            },
            {
                'id': 5,
                'title': '3.5 下肢僵硬',
                'description': '评估下肢肌肉僵硬程度',
                'options': ['0-无', '1-轻微僵硬', '2-轻度僵硬', '3-中度僵硬', '4-重度僵硬']
            },
            {
                'id': 6,
                'title': '3.6 手指敲击',
                'description': '评估手指敲击动作的幅度和速度',
                'options': ['0-正常', '1-轻度减慢或幅度减小', '2-中度减慢或幅度减小', '3-重度减慢或幅度减小', '4-几乎不能完成']
            },
            {
                'id': 7,
                'title': '3.7 手部动作',
                'description': '评估握拳和张开手掌的动作',
                'options': ['0-正常', '1-轻度减慢或幅度减小', '2-中度减慢或幅度减小', '3-重度减慢或幅度减小', '4-几乎不能完成']
            },
            {
                'id': 8,
                'title': '3.8 手部快速交替动作',
                'description': '评估手部快速交替动作能力',
                'options': ['0-正常', '1-轻度减慢或幅度减小', '2-中度减慢或幅度减小', '3-重度减慢或幅度减小', '4-几乎不能完成']
            },
            {
                'id': 9,
                'title': '3.9 腿部敏捷性',
                'description': '评估腿部快速抬起和放下的动作',
                'options': ['0-正常', '1-轻度减慢或幅度减小', '2-中度减慢或幅度减小', '3-重度减慢或幅度减小', '4-几乎不能完成']
            },
            {
                'id': 10,
                'title': '3.10 从椅子上起立',
                'description': '评估从椅子上起立的能力',
                'options': ['0-正常', '1-缓慢或需要多次尝试', '2-需要扶手帮助', '3-需要他人帮助', '4-无法起立']
            },
            {
                'id': 11,
                'title': '3.11 姿势',
                'description': '评估站立时的姿势',
                'options': ['0-正常直立', '1-轻微弯腰', '2-中度弯腰', '3-重度弯腰但能保持平衡', '4-严重弯腰需要支撑']
            },
            {
                'id': 12,
                'title': '3.12 步态',
                'description': '评估行走时的步态',
                'options': ['0-正常', '1-轻微异常', '2-中度异常但无需帮助', '3-重度异常需要帮助', '4-无法行走']
            },
            {
                'id': 13,
                'title': '3.13 姿势稳定性',
                'description': '评估姿势稳定性（拉拽试验）',
                'options': ['0-正常', '1-1-2步恢复', '2-3-5步恢复', '3->5步恢复', '4-无法恢复或跌倒']
            },
            {
                'id': 14,
                'title': '3.14 整体运动迟缓',
                'description': '评估整体运动迟缓程度',
                'options': ['0-无', '1-轻微迟缓', '2-轻度迟缓', '3-中度迟缓', '4-重度迟缓']
            }
        ]
        
        self.updrs_vars = {}
        
        for i, item in enumerate(updrs_items):
            # 创建项目框架
            item_frame = ttk.Frame(items_frame)
            item_frame.pack(fill='x', pady=10, padx=10)
            
            # 项目标题和描述
            title_frame = ttk.Frame(item_frame)
            title_frame.pack(fill='x', pady=(0, 5))
            
            title_label = ttk.Label(title_frame, 
                                   text=item['title'],
                                   font=('Microsoft YaHei', 11, 'bold'),
                                   foreground='#2E86AB')
            title_label.pack(side='left')
            
            desc_label = ttk.Label(item_frame,
                                  text=item['description'],
                                  font=('Microsoft YaHei', 9),
                                  foreground='#666666')
            desc_label.pack(anchor='w', pady=(0, 5))
            
            # 选项按钮
            options_frame = ttk.Frame(item_frame)
            options_frame.pack(fill='x')
            
            var = tk.IntVar()
            self.updrs_vars[item['id']] = var
            
            for j, option in enumerate(item['options']):
                rb = ttk.Radiobutton(options_frame,
                                    text=option,
                                    variable=var,
                                    value=j)
                rb.pack(side='left', padx=(0, 15))
            
            # 分隔线
            if i < len(updrs_items) - 1:
                separator = ttk.Separator(items_frame, orient='horizontal')
                separator.pack(fill='x', pady=5)
                
    def create_bottom_buttons(self, parent):
        """创建底部按钮"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', pady=20)
        
        # 计算得分按钮
        calc_btn = ttk.Button(button_frame,
                             text="计算得分",
                             command=self.calculate_updrs_score,
                             style='Accent.TButton')
        calc_btn.pack(side='left', padx=(0, 10))
        
        # 保存结果按钮
        save_btn = ttk.Button(button_frame,
                             text="保存结果",
                             command=self.save_updrs_result)
        save_btn.pack(side='left', padx=(0, 10))
        
        # 重置按钮
        reset_btn = ttk.Button(button_frame,
                              text="重置",
                              command=self.reset_updrs)
        reset_btn.pack(side='left')
        
    def calculate_updrs_score(self):
        """计算UPDRS得分"""
        # 检查是否所有项目都已评分
        for item_id in range(1, 15):
            if item_id not in self.updrs_vars or self.updrs_vars[item_id].get() == -1:
                messagebox.showwarning("提示", f"请完成第{item_id}项的评分")
                return
        
        # 计算总分
        total_score = sum(var.get() for var in self.updrs_vars.values())
        
        # 显示结果
        self.show_updrs_interpretation(total_score)
        
    def show_updrs_interpretation(self, score):
        """显示UPDRS评分解释"""
        # 评分解释
        if score <= 17:
            severity = "轻度"
            interpretation = "运动症状轻微，对日常生活影响较小"
            color = "#28a745"  # 绿色
        elif score <= 33:
            severity = "中度"
            interpretation = "运动症状明显，对日常生活有一定影响"
            color = "#ffc107"  # 黄色
        elif score <= 50:
            severity = "中重度"
            interpretation = "运动症状较重，对日常生活影响较大"
            color = "#fd7e14"  # 橙色
        else:
            severity = "重度"
            interpretation = "运动症状严重，严重影响日常生活"
            color = "#dc3545"  # 红色
            
        # 创建结果窗口
        result_window = tk.Toplevel(self.parent)
        result_window.title("UPDRS评估结果")
        result_window.geometry("500x400")
        result_window.resizable(False, False)
        
        # 居中显示
        result_window.transient(self.parent)
        result_window.grab_set()
        
        # 主框架
        main_frame = ttk.Frame(result_window, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame,
                               text="UPDRS-III 评估结果",
                               font=('Microsoft YaHei', 16, 'bold'),
                               foreground='#2E86AB')
        title_label.pack(pady=(0, 20))
        
        # 得分显示
        score_frame = ttk.Frame(main_frame)
        score_frame.pack(fill='x', pady=10)
        
        score_label = ttk.Label(score_frame,
                               text=f"总分：{score} 分 (满分56分)",
                               font=('Microsoft YaHei', 14, 'bold'))
        score_label.pack()
        
        # 严重程度
        severity_label = ttk.Label(score_frame,
                                  text=f"严重程度：{severity}",
                                  font=('Microsoft YaHei', 12, 'bold'),
                                  foreground=color)
        severity_label.pack(pady=5)
        
        # 解释说明
        interpretation_frame = ttk.LabelFrame(main_frame, text="结果解释", padding=15)
        interpretation_frame.pack(fill='both', expand=True, pady=10)
        
        interpretation_text = tk.Text(interpretation_frame,
                                     height=8,
                                     wrap='word',
                                     font=('Microsoft YaHei', 10))
        interpretation_text.pack(fill='both', expand=True)
        
        # 插入解释内容
        content = f"""{interpretation}

UPDRS-III评分标准：
• 0-17分：轻度运动障碍
• 18-33分：中度运动障碍  
• 34-50分：中重度运动障碍
• 51-56分：重度运动障碍

注意事项：
• 本量表主要评估帕金森病患者的运动症状
• 评估应在患者服药状态下进行
• 建议结合临床表现综合判断
• 定期评估有助于监测病情变化"""
        
        interpretation_text.insert('1.0', content)
        interpretation_text.config(state='disabled')
        
        # 关闭按钮
        close_btn = ttk.Button(main_frame,
                              text="关闭",
                              command=result_window.destroy,
                              style='Accent.TButton')
        close_btn.pack(pady=10)
        
    def save_updrs_result(self):
        """保存UPDRS评估结果"""
        # 检查患者信息
        if not self.name_var.get().strip():
            messagebox.showwarning("提示", "请输入患者姓名")
            return
            
        # 检查是否已评分
        if not self.updrs_vars or len(self.updrs_vars) < 14:
            messagebox.showwarning("提示", "请先完成评估")
            return
            
        # 计算总分
        total_score = sum(var.get() for var in self.updrs_vars.values())
        
        # 准备保存数据
        result_data = {
            'scale_type': 'UPDRS-III',
            'patient_info': {
                'name': self.name_var.get(),
                'gender': self.gender_var.get(),
                'age': self.age_var.get(),
                'duration': self.duration_var.get(),
                'assessment_date': self.date_var.get()
            },
            'responses': {str(k): v.get() for k, v in self.updrs_vars.items()},
            'total_score': total_score,
            'max_score': 56,
            'assessment_time': datetime.now().isoformat(),
            'assessor': 'LIUYING'
        }
        
        # 保存到文件
        try:
            import os
            data_dir = 'data'
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
                
            filename = f"{data_dir}/UPDRS_{self.name_var.get()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
                
            messagebox.showinfo("成功", f"评估结果已保存到：{filename}")
            
        except Exception as e:
            messagebox.showerror("错误", f"保存失败：{str(e)}")
            
    def reset_updrs(self):
        """重置UPDRS评估"""
        # 重置所有变量
        for var in self.updrs_vars.values():
            var.set(-1)
        
        # 重置患者信息
        self.name_var.set('')
        self.gender_var.set('')
        self.age_var.set('')
        self.duration_var.set('')
        self.date_var.set(datetime.now().strftime('%Y-%m-%d'))
        
        messagebox.showinfo("提示", "已重置所有内容")
        
    def show_berg_assessment(self):
        """显示Berg平衡量表评估界面"""
        self.current_scale = 'Berg'
        self.current_responses = {}
        
        # 清空父容器
        for widget in self.parent.winfo_children():
            widget.destroy()
            
        # 创建Berg评估界面
        self.create_berg_interface()
        
    def create_berg_interface(self):
        """创建Berg平衡量表评估界面"""
        # 主容器
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 标题区域
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = ttk.Label(title_frame,
                               text="Berg平衡量表 (BBS)",
                               font=('Microsoft YaHei', 18, 'bold'),
                               foreground='#2E86AB')
        title_label.pack(side='left')
        
        # 返回按钮
        back_btn = ttk.Button(title_frame,
                             text="返回",
                             command=self.back_to_category)
        back_btn.pack(side='right')
        
        # 创建滚动区域
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 患者信息区域
        self.create_patient_info_section(scrollable_frame)
        
        # Berg评估项目
        self.create_berg_items(scrollable_frame)
        
        # 底部按钮
        self.create_berg_bottom_buttons(scrollable_frame)
        
        # 布局滚动区域
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 绑定鼠标滚轮
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
    def create_berg_items(self, parent):
        """创建Berg平衡量表评估项目"""
        # Berg平衡量表14个项目
        berg_items = [
            {
                'title': '1. 坐到站',
                'instruction': '请患者从有扶手的椅子上站起来。不要使用手支撑。',
                'scores': [
                    {'score': 4, 'description': '能够独立站起'},
                    {'score': 3, 'description': '能够独立站起，使用手支撑'},
                    {'score': 2, 'description': '能够站起，使用手支撑，需要几次尝试'},
                    {'score': 1, 'description': '需要最少的帮助才能站起或稳定'},
                    {'score': 0, 'description': '需要中等或最大的帮助才能站起'}
                ]
            },
            {
                'title': '2. 独立站立',
                'instruction': '请患者独立站立2分钟。',
                'scores': [
                    {'score': 4, 'description': '能够安全地独立站立2分钟'},
                    {'score': 3, 'description': '能够独立站立2分钟，需要监督'},
                    {'score': 2, 'description': '能够独立站立30秒'},
                    {'score': 1, 'description': '需要几次尝试才能独立站立30秒'},
                    {'score': 0, 'description': '无法独立站立30秒，需要帮助'}
                ]
            },
            {
                'title': '3. 无支撑坐立，脚平放在地面上',
                'instruction': '请患者坐在椅子上，双臂交叉放在胸前，坐立2分钟。',
                'scores': [
                    {'score': 4, 'description': '能够安全地坐立2分钟'},
                    {'score': 3, 'description': '能够坐立2分钟，需要监督'},
                    {'score': 2, 'description': '能够坐立30秒'},
                    {'score': 1, 'description': '能够坐立10秒'},
                    {'score': 0, 'description': '无法在没有支撑的情况下坐立10秒'}
                ]
            },
            {
                'title': '4. 站到坐',
                'instruction': '请患者坐下。',
                'scores': [
                    {'score': 4, 'description': '安全地坐下，最少使用手'},
                    {'score': 3, 'description': '控制下降，使用手'},
                    {'score': 2, 'description': '使用腿后部控制下降'},
                    {'score': 1, 'description': '坐下，但判断距离不准确，重重地落在椅子上'},
                    {'score': 0, 'description': '需要帮助坐下'}
                ]
            },
            {
                'title': '5. 转移',
                'instruction': '安排椅子，一个有扶手，一个没有扶手。请患者从一个转移到另一个。',
                'scores': [
                    {'score': 4, 'description': '能够安全地转移，只需要最少的手的使用'},
                    {'score': 3, 'description': '能够安全地转移，明显需要使用手'},
                    {'score': 2, 'description': '能够转移，需要口头提示和/或监督'},
                    {'score': 1, 'description': '需要一个人帮助'},
                    {'score': 0, 'description': '需要两个人帮助或监督才能安全'}
                ]
            },
            {
                'title': '6. 闭眼独立站立',
                'instruction': '请患者闭眼站立10秒。',
                'scores': [
                    {'score': 4, 'description': '能够安全地站立10秒'},
                    {'score': 3, 'description': '能够站立10秒，需要监督'},
                    {'score': 2, 'description': '能够站立3秒'},
                    {'score': 1, 'description': '无法保持闭眼3秒，但能够稳定站立'},
                    {'score': 0, 'description': '需要帮助以免跌倒'}
                ]
            },
            {
                'title': '7. 双脚并拢站立',
                'instruction': '请患者将脚并拢独立站立。',
                'scores': [
                    {'score': 4, 'description': '能够安全地将脚并拢独立站立1分钟'},
                    {'score': 3, 'description': '能够将脚并拢独立站立1分钟，需要监督'},
                    {'score': 2, 'description': '能够将脚并拢独立站立30秒'},
                    {'score': 1, 'description': '需要帮助达到位置，但能够站立15秒，脚并拢'},
                    {'score': 0, 'description': '需要帮助达到位置，无法保持15秒'}
                ]
            },
            {
                'title': '8. 站立时向前伸手',
                'instruction': '请患者抬起手臂90度。伸出手指，尽可能向前伸。',
                'scores': [
                    {'score': 4, 'description': '能够自信地向前伸展>25cm（10英寸）'},
                    {'score': 3, 'description': '能够安全地向前伸展>12.5cm（5英寸）'},
                    {'score': 2, 'description': '能够安全地向前伸展>5cm（2英寸）'},
                    {'score': 1, 'description': '向前伸展，但需要监督'},
                    {'score': 0, 'description': '失去平衡，需要外部支撑'}
                ]
            },
            {
                'title': '9. 站立时从地面拾起物体',
                'instruction': '请患者拾起放在脚前的拖鞋/鞋子。',
                'scores': [
                    {'score': 4, 'description': '能够安全且轻松地拾起拖鞋'},
                    {'score': 3, 'description': '能够拾起拖鞋，但需要监督'},
                    {'score': 2, 'description': '无法拾起，但能够到达距离拖鞋2-5cm（1-2英寸），并保持独立站立'},
                    {'score': 1, 'description': '无法拾起，需要监督尝试'},
                    {'score': 0, 'description': '无法尝试/需要帮助以免失去平衡或跌倒'}
                ]
            },
            {
                'title': '10. 站立时转身看后面',
                'instruction': '请患者转身看后面的左肩和右肩。',
                'scores': [
                    {'score': 4, 'description': '向两侧看，体重转移良好'},
                    {'score': 3, 'description': '向一侧看，另一侧显示较少的体重转移'},
                    {'score': 2, 'description': '只能转向一侧，但保持平衡'},
                    {'score': 1, 'description': '需要监督转身'},
                    {'score': 0, 'description': '需要帮助以免失去平衡或跌倒'}
                ]
            },
            {
                'title': '11. 转身360度',
                'instruction': '请患者转身一整圈。暂停。然后转向另一个方向。',
                'scores': [
                    {'score': 4, 'description': '能够安全地转身360度，4秒或更少'},
                    {'score': 3, 'description': '能够安全地转身360度，一个方向，4秒或更少'},
                    {'score': 2, 'description': '能够安全地转身360度，但缓慢'},
                    {'score': 1, 'description': '需要密切监督或口头提示'},
                    {'score': 0, 'description': '需要帮助转身'}
                ]
            },
            {
                'title': '12. 站立时交替踏步到脚凳或台阶上',
                'instruction': '请患者交替将脚放在台阶/脚凳上。继续直到每只脚触碰台阶/脚凳四次。',
                'scores': [
                    {'score': 4, 'description': '能够独立站立并安全地完成8次台阶，20秒内'},
                    {'score': 3, 'description': '能够独立站立并完成8次台阶，>20秒'},
                    {'score': 2, 'description': '能够完成4次台阶，没有帮助，需要监督'},
                    {'score': 1, 'description': '能够完成>2次台阶，需要最少的帮助'},
                    {'score': 0, 'description': '需要帮助以免跌倒/无法尝试'}
                ]
            },
            {
                'title': '13. 无支撑单脚站立',
                'instruction': '请患者单脚站立，尽可能长时间。',
                'scores': [
                    {'score': 4, 'description': '能够独立抬起腿并保持>10秒'},
                    {'score': 3, 'description': '能够独立抬起腿并保持5-10秒'},
                    {'score': 2, 'description': '能够独立抬起腿并保持≥3秒'},
                    {'score': 1, 'description': '尝试抬起腿，无法保持3秒，但仍然独立站立'},
                    {'score': 0, 'description': '无法尝试或需要帮助以免跌倒'}
                ]
            },
            {
                'title': '14. 前后脚站立',
                'instruction': '请患者将一只脚直接放在另一只脚前面。如果感觉无法将脚直接放在前面，尝试向前迈出足够远的距离，使一只脚的脚跟在另一只脚的脚趾前面。',
                'scores': [
                    {'score': 4, 'description': '能够独立将脚前后放置并保持30秒'},
                    {'score': 3, 'description': '能够独立将一只脚放在另一只脚前面并保持30秒'},
                    {'score': 2, 'description': '能够迈出一小步独立站立30秒'},
                    {'score': 1, 'description': '需要帮助迈步，但能够保持15秒'},
                    {'score': 0, 'description': '失去平衡，迈步或站立'}
                ]
            }
        ]
        
        # 评估说明
        instruction_frame = ttk.LabelFrame(parent, text="评估说明", padding=15)
        instruction_frame.pack(fill='x', pady=(0, 20))
        
        instruction_text = (
            "Berg平衡量表包含14个项目，每项0-4分，总分56分。\n"
            "评分标准：0分=无法完成，1分=需要大量帮助，2分=需要少量帮助，3分=需要监督，4分=独立完成"
        )
        instruction_label = ttk.Label(instruction_frame, text=instruction_text,
                                    font=('Microsoft YaHei', 10),
                                    foreground='#6C757D')
        instruction_label.pack(anchor='w')
        
        # 创建评估项目
        self.berg_vars = {}
        
        for i, item in enumerate(berg_items):
            item_frame = ttk.LabelFrame(parent, text=item['title'], padding=15)
            item_frame.pack(fill='x', pady=10)
            
            # 项目说明
            instruction_label = ttk.Label(item_frame,
                                        text=item['instruction'],
                                        font=('Microsoft YaHei', 10),
                                        foreground='#6C757D')
            instruction_label.pack(anchor='w', pady=(0, 10))
            
            # 评分选项
            var_name = f"item_{i}"
            self.berg_vars[var_name] = tk.IntVar()
            
            for score_option in item['scores']:
                option_frame = ttk.Frame(item_frame)
                option_frame.pack(fill='x', pady=2)
                
                rb = ttk.Radiobutton(option_frame,
                                   text=f"{score_option['score']}分 - {score_option['description']}",
                                   variable=self.berg_vars[var_name],
                                   value=score_option['score'])
                rb.pack(anchor='w')
                
    def create_berg_bottom_buttons(self, parent):
        """创建Berg底部按钮"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', pady=(20, 0))
        
        # 计算总分按钮
        calc_btn = ttk.Button(button_frame,
                             text="计算Berg评分",
                             command=self.calculate_berg_score,
                             style='Accent.TButton')
        calc_btn.pack(side='left', padx=(0, 10))
        
        # 保存结果按钮
        save_btn = ttk.Button(button_frame,
                             text="保存结果",
                             command=self.save_berg_result)
        save_btn.pack(side='left', padx=(0, 10))
        
        # 重置按钮
        reset_btn = ttk.Button(button_frame,
                              text="重置",
                              command=self.reset_berg)
        reset_btn.pack(side='left')
        
    def calculate_berg_score(self):
        """计算Berg平衡量表评分"""
        try:
            # 检查是否所有项目都已评分
            total_score = 0
            for var_name, var in self.berg_vars.items():
                score = var.get()
                if score == 0 and var_name in [f"item_{i}" for i in range(14)]:
                    # 检查是否真的选择了0分还是没有选择
                    if not any(var.get() == j for j in range(5)):
                        messagebox.showwarning("警告", "请完成所有项目的评估")
                        return
                total_score += score
            
            # 显示结果解释
            self.show_berg_interpretation(total_score)
            
        except Exception as e:
            messagebox.showerror("错误", f"计算Berg评分时出错：{str(e)}")
            
    def show_berg_interpretation(self, total_score):
        """显示Berg平衡量表评分解释"""
        # 评分解释
        if total_score >= 56:
            risk_level = "无跌倒风险"
            risk_color = "#27AE60"
            recommendations = [
                "平衡功能良好，继续保持",
                "可进行常规体育活动",
                "定期进行平衡功能评估"
            ]
        elif total_score >= 54:
            risk_level = "低跌倒风险"
            risk_color = "#F39C12"
            recommendations = [
                "平衡功能较好，需要注意安全",
                "建议进行平衡训练",
                "避免在不平整地面行走"
            ]
        elif total_score >= 46:
            risk_level = "中等跌倒风险"
            risk_color = "#E67E22"
            recommendations = [
                "需要进行平衡康复训练",
                "使用辅助器具（如手杖）",
                "改善居家环境安全",
                "定期随访评估"
            ]
        else:
            risk_level = "高跌倒风险"
            risk_color = "#E74C3C"
            recommendations = [
                "需要密切监护和帮助",
                "必须使用辅助器具",
                "进行专业康复治疗",
                "全面评估跌倒风险因素",
                "考虑物理治疗介入"
            ]
        
        # 创建结果窗口
        result_window = tk.Toplevel(self.parent)
        result_window.title("Berg平衡量表评估结果")
        result_window.geometry("600x500")
        result_window.resizable(False, False)
        
        # 居中显示
        result_window.transient(self.parent)
        result_window.grab_set()
        
        # 主框架
        main_frame = ttk.Frame(result_window, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame,
                               text="Berg平衡量表评估结果",
                               font=('Microsoft YaHei', 16, 'bold'),
                               foreground='#2E86AB')
        title_label.pack(pady=(0, 20))
        
        # 评分结果
        score_frame = ttk.LabelFrame(main_frame, text="评分结果", padding=15)
        score_frame.pack(fill='x', pady=(0, 15))
        
        score_text = f"Berg总分：{total_score}/56\n跌倒风险：{risk_level}"
        score_label = ttk.Label(score_frame,
                               text=score_text,
                               font=('Microsoft YaHei', 12, 'bold'),
                               foreground=risk_color)
        score_label.pack()
        
        # 结果解释
        interp_frame = ttk.LabelFrame(main_frame, text="评估解释", padding=15)
        interp_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        interp_text = f"根据Berg平衡量表评分，患者的平衡功能处于{risk_level}水平。"
        interp_label = ttk.Label(interp_frame,
                                text=interp_text,
                                font=('Microsoft YaHei', 11),
                                wraplength=500)
        interp_label.pack(anchor='w', pady=(0, 10))
        
        # 建议
        rec_label = ttk.Label(interp_frame,
                             text="建议：",
                             font=('Microsoft YaHei', 11, 'bold'))
        rec_label.pack(anchor='w')
        
        for i, rec in enumerate(recommendations, 1):
            rec_text = ttk.Label(interp_frame,
                               text=f"{i}. {rec}",
                               font=('Microsoft YaHei', 10),
                               wraplength=500)
            rec_text.pack(anchor='w', padx=(20, 0), pady=2)
        
        # 关闭按钮
        close_btn = ttk.Button(main_frame,
                              text="关闭",
                              command=result_window.destroy)
        close_btn.pack(pady=(15, 0))
        
    def save_berg_result(self):
        """保存Berg平衡量表评估结果"""
        try:
            # 获取患者信息
            patient_info = {
                'name': getattr(self, 'name_var', tk.StringVar()).get(),
                'age': getattr(self, 'age_var', tk.StringVar()).get(),
                'gender': getattr(self, 'gender_var', tk.StringVar()).get()
            }
            
            # 获取评估结果
            item_scores = {}
            total_score = 0
            
            berg_item_names = [
                '坐到站', '独立站立', '无支撑坐立', '站到坐', '转移',
                '闭眼独立站立', '双脚并拢站立', '站立时向前伸手', '站立时从地面拾起物体',
                '站立时转身看后面', '转身360度', '站立时交替踏步', '无支撑单脚站立', '前后脚站立'
            ]
            
            for i, (var_name, var) in enumerate(self.berg_vars.items()):
                score = var.get()
                item_scores[berg_item_names[i]] = score
                total_score += score
            
            # 确定跌倒风险等级
            if total_score >= 56:
                risk_level = "无跌倒风险"
            elif total_score >= 54:
                risk_level = "低跌倒风险"
            elif total_score >= 46:
                risk_level = "中等跌倒风险"
            else:
                risk_level = "高跌倒风险"
            
            # 保存数据
            result_data = {
                'scale_type': 'Berg',
                'scale_name': 'Berg平衡量表',
                'patient_info': patient_info,
                'assessment_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'item_scores': item_scores,
                'total_score': total_score,
                'max_score': 56,
                'risk_level': risk_level
            }
            
            # 调用主应用的保存方法
            if hasattr(self.main_app, 'data_manager'):
                self.main_app.data_manager.save_assessment_result(result_data)
                messagebox.showinfo("成功", "Berg平衡量表评估结果已保存")
            else:
                messagebox.showwarning("警告", "数据管理器不可用，无法保存结果")
                
        except Exception as e:
            messagebox.showerror("错误", f"保存失败：{str(e)}")
            
    def reset_berg(self):
        """重置Berg平衡量表评估"""
        if hasattr(self, 'berg_vars'):
            for var in self.berg_vars.values():
                var.set(0)
        messagebox.showinfo("提示", "Berg平衡量表评估已重置")

    def show_tinetti_assessment(self):
        """显示Tinetti步态与平衡评估界面"""
        self.current_scale = 'Tinetti'
        self.current_responses = {}
        
        # 清空父容器
        for widget in self.parent.winfo_children():
            widget.destroy()
            
        # 创建Tinetti评估界面
        self.create_tinetti_interface()
        
    def create_tinetti_interface(self):
        """创建Tinetti步态与平衡评估界面"""
        # 主容器
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 标题区域
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = ttk.Label(title_frame,
                               text="Tinetti步态与平衡评估量表 (POMA)",
                               font=('Microsoft YaHei', 18, 'bold'),
                               foreground='#2E86AB')
        title_label.pack(side='left')
        
        # 返回按钮
        back_btn = ttk.Button(title_frame,
                             text="返回",
                             command=self.back_to_category)
        back_btn.pack(side='right')
        
        # 创建滚动区域
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 患者信息区域
        self.create_patient_info_section(scrollable_frame)
        
        # Tinetti评估项目
        self.create_tinetti_items(scrollable_frame)
        
        # 底部按钮
        self.create_tinetti_bottom_buttons(scrollable_frame)
        
        # 布局滚动区域
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 绑定鼠标滚轮
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
    def create_tinetti_items(self, parent):
        """创建Tinetti评估项目"""
        # Tinetti评估分为平衡测试和步态测试两部分
        
        # 平衡测试项目
        balance_items = [
            {
                'title': '1. 坐位平衡',
                'scores': [
                    {'score': 0, 'description': '向一侧倾斜或滑落'},
                    {'score': 1, 'description': '稳定、安全'}
                ]
            },
            {
                'title': '2. 起立',
                'scores': [
                    {'score': 0, 'description': '无法起立，无需用手帮助'},
                    {'score': 1, 'description': '能够起立，但需用手帮助'},
                    {'score': 2, 'description': '能够起立，无需用手帮助'}
                ]
            },
            {
                'title': '3. 试图起立',
                'scores': [
                    {'score': 0, 'description': '无法起立，无需用手帮助'},
                    {'score': 1, 'description': '能够起立，但需要>1次尝试'},
                    {'score': 2, 'description': '能够起立，1次尝试'}
                ]
            },
            {
                'title': '4. 立即站立平衡（前5秒）',
                'scores': [
                    {'score': 0, 'description': '不稳定（摇摆、移动脚、明显的躯干摆动）'},
                    {'score': 1, 'description': '稳定，但使用助行器或其他支撑'},
                    {'score': 2, 'description': '稳定，无需支撑'}
                ]
            },
            {
                'title': '5. 站立平衡',
                'scores': [
                    {'score': 0, 'description': '不稳定'},
                    {'score': 1, 'description': '稳定，但步态宽（脚跟分开>10cm）或使用手杖或其他支撑'},
                    {'score': 2, 'description': '双脚并拢，无需支撑'}
                ]
            },
            {
                'title': '6. 轻推（患者双脚尽可能靠近，检查者用手掌轻推患者胸骨3次）',
                'scores': [
                    {'score': 0, 'description': '开始跌倒'},
                    {'score': 1, 'description': '摇摆，抓住，但保持直立'},
                    {'score': 2, 'description': '稳定'}
                ]
            },
            {
                'title': '7. 闭眼（在第6项的位置）',
                'scores': [
                    {'score': 0, 'description': '不稳定'},
                    {'score': 1, 'description': '稳定'}
                ]
            },
            {
                'title': '8. 转身360度',
                'scores': [
                    {'score': 0, 'description': '不连续的步伐'},
                    {'score': 1, 'description': '连续的步伐'},
                    {'score': 2, 'description': '不稳定（抓住或摇摆）'},
                    {'score': 3, 'description': '稳定'}
                ]
            },
            {
                'title': '9. 坐下',
                'scores': [
                    {'score': 0, 'description': '不安全（错误判断距离，重重地落在椅子上）'},
                    {'score': 1, 'description': '使用手或不是平滑的动作'},
                    {'score': 2, 'description': '安全，平滑的动作'}
                ]
            }
        ]
        
        # 步态测试项目
        gait_items = [
            {
                'title': '10. 步态启动（立即起步后）',
                'scores': [
                    {'score': 0, 'description': '任何犹豫或多次尝试开始'},
                    {'score': 1, 'description': '无犹豫'}
                ]
            },
            {
                'title': '11. 步长和步高（右脚）',
                'scores': [
                    {'score': 0, 'description': '右脚不能完全超过左脚'},
                    {'score': 1, 'description': '右脚超过左脚'},
                    {'score': 2, 'description': '右脚完全离开地面'}
                ]
            },
            {
                'title': '12. 步长和步高（左脚）',
                'scores': [
                    {'score': 0, 'description': '左脚不能完全超过右脚'},
                    {'score': 1, 'description': '左脚超过右脚'},
                    {'score': 2, 'description': '左脚完全离开地面'}
                ]
            },
            {
                'title': '13. 步态对称性',
                'scores': [
                    {'score': 0, 'description': '右脚和左脚步长不相等（目测）'},
                    {'score': 1, 'description': '右脚和左脚步长相等'}
                ]
            },
            {
                'title': '14. 步态连续性',
                'scores': [
                    {'score': 0, 'description': '停止或不连续的步伐'},
                    {'score': 1, 'description': '连续的步伐'}
                ]
            },
            {
                'title': '15. 路径（在约3米的过程中观察与地板瓷砖的偏离）',
                'scores': [
                    {'score': 0, 'description': '明显偏离'},
                    {'score': 1, 'description': '轻微/中度偏离或使用助行器'},
                    {'score': 2, 'description': '直线，无需助行器'}
                ]
            },
            {
                'title': '16. 躯干',
                'scores': [
                    {'score': 0, 'description': '明显摇摆或使用助行器'},
                    {'score': 1, 'description': '无摇摆，但屈曲膝盖或背部或张开手臂'},
                    {'score': 2, 'description': '无摇摆，无屈曲，无使用手臂，无使用助行器'}
                ]
            },
            {
                'title': '17. 步态宽度',
                'scores': [
                    {'score': 0, 'description': '脚跟分开'},
                    {'score': 1, 'description': '脚跟几乎接触行走'}
                ]
            }
        ]
        
        # 评估说明
        instruction_frame = ttk.LabelFrame(parent, text="评估说明", padding=15)
        instruction_frame.pack(fill='x', pady=(0, 20))
        
        instruction_text = (
            "Tinetti评估包括平衡测试（9项，16分）和步态测试（8项，12分），总分28分。\n"
            "评分：<19分=高跌倒风险，19-23分=中等跌倒风险，≥24分=低跌倒风险"
        )
        instruction_label = ttk.Label(instruction_frame, text=instruction_text,
                                    font=('Microsoft YaHei', 10),
                                    foreground='#6C757D')
        instruction_label.pack(anchor='w')
        
        # 创建平衡测试项目
        balance_frame = ttk.LabelFrame(parent, text="平衡测试（16分）", padding=15)
        balance_frame.pack(fill='x', pady=10)
        
        self.tinetti_vars = {}
        
        for i, item in enumerate(balance_items):
            item_frame = ttk.Frame(balance_frame)
            item_frame.pack(fill='x', pady=5)
            
            # 项目标题
            title_label = ttk.Label(item_frame,
                                  text=item['title'],
                                  font=('Microsoft YaHei', 10, 'bold'))
            title_label.pack(anchor='w', pady=(0, 5))
            
            # 评分选项
            var_name = f"balance_{i}"
            self.tinetti_vars[var_name] = tk.IntVar()
            
            for score_option in item['scores']:
                rb = ttk.Radiobutton(item_frame,
                                   text=f"{score_option['score']}分 - {score_option['description']}",
                                   variable=self.tinetti_vars[var_name],
                                   value=score_option['score'])
                rb.pack(anchor='w', padx=(20, 0))
        
        # 创建步态测试项目
        gait_frame = ttk.LabelFrame(parent, text="步态测试（12分）", padding=15)
        gait_frame.pack(fill='x', pady=10)
        
        for i, item in enumerate(gait_items):
            item_frame = ttk.Frame(gait_frame)
            item_frame.pack(fill='x', pady=5)
            
            # 项目标题
            title_label = ttk.Label(item_frame,
                                  text=item['title'],
                                  font=('Microsoft YaHei', 10, 'bold'))
            title_label.pack(anchor='w', pady=(0, 5))
            
            # 评分选项
            var_name = f"gait_{i}"
            self.tinetti_vars[var_name] = tk.IntVar()
            
            for score_option in item['scores']:
                rb = ttk.Radiobutton(item_frame,
                                   text=f"{score_option['score']}分 - {score_option['description']}",
                                   variable=self.tinetti_vars[var_name],
                                   value=score_option['score'])
                rb.pack(anchor='w', padx=(20, 0))
                
    def create_tinetti_bottom_buttons(self, parent):
        """创建Tinetti底部按钮"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', pady=(20, 0))
        
        # 计算总分按钮
        calc_btn = ttk.Button(button_frame,
                             text="计算Tinetti评分",
                             command=self.calculate_tinetti_score,
                             style='Accent.TButton')
        calc_btn.pack(side='left', padx=(0, 10))
        
        # 保存结果按钮
        save_btn = ttk.Button(button_frame,
                             text="保存结果",
                             command=self.save_tinetti_result)
        save_btn.pack(side='left', padx=(0, 10))
        
        # 重置按钮
        reset_btn = ttk.Button(button_frame,
                              text="重置",
                              command=self.reset_tinetti)
        reset_btn.pack(side='left')
        
    def calculate_tinetti_score(self):
        """计算Tinetti评分"""
        try:
            # 计算平衡测试分数
            balance_score = 0
            for i in range(9):  # 9个平衡测试项目
                var_name = f"balance_{i}"
                if var_name in self.tinetti_vars:
                    balance_score += self.tinetti_vars[var_name].get()
            
            # 计算步态测试分数
            gait_score = 0
            for i in range(8):  # 8个步态测试项目
                var_name = f"gait_{i}"
                if var_name in self.tinetti_vars:
                    gait_score += self.tinetti_vars[var_name].get()
            
            total_score = balance_score + gait_score
            
            # 显示结果解释
            self.show_tinetti_interpretation(total_score, balance_score, gait_score)
            
        except Exception as e:
            messagebox.showerror("错误", f"计算Tinetti评分时出错：{str(e)}")
            
    def show_tinetti_interpretation(self, total_score, balance_score, gait_score):
        """显示Tinetti评分解释"""
        # 评分解释
        if total_score >= 24:
            risk_level = "低跌倒风险"
            risk_color = "#27AE60"
            recommendations = [
                "平衡和步态功能良好",
                "继续保持活动水平",
                "定期进行功能评估"
            ]
        elif total_score >= 19:
            risk_level = "中等跌倒风险"
            risk_color = "#F39C12"
            recommendations = [
                "需要进行平衡和步态训练",
                "考虑使用辅助器具",
                "改善环境安全",
                "定期随访评估"
            ]
        else:
            risk_level = "高跌倒风险"
            risk_color = "#E74C3C"
            recommendations = [
                "需要密切监护",
                "必须使用辅助器具",
                "进行专业康复治疗",
                "全面跌倒风险评估",
                "考虑物理治疗介入"
            ]
        
        # 创建结果窗口
        result_window = tk.Toplevel(self.parent)
        result_window.title("Tinetti评估结果")
        result_window.geometry("600x500")
        result_window.resizable(False, False)
        
        # 居中显示
        result_window.transient(self.parent)
        result_window.grab_set()
        
        # 主框架
        main_frame = ttk.Frame(result_window, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame,
                               text="Tinetti评估结果",
                               font=('Microsoft YaHei', 16, 'bold'),
                               foreground='#2E86AB')
        title_label.pack(pady=(0, 20))
        
        # 评分结果
        score_frame = ttk.LabelFrame(main_frame, text="评分结果", padding=15)
        score_frame.pack(fill='x', pady=(0, 15))
        
        score_text = f"总分：{total_score}/28\n平衡测试：{balance_score}/16\n步态测试：{gait_score}/12\n跌倒风险：{risk_level}"
        score_label = ttk.Label(score_frame,
                               text=score_text,
                               font=('Microsoft YaHei', 12, 'bold'),
                               foreground=risk_color)
        score_label.pack()
        
        # 结果解释
        interp_frame = ttk.LabelFrame(main_frame, text="评估解释", padding=15)
        interp_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        interp_text = f"根据Tinetti评估结果，患者的平衡和步态功能处于{risk_level}水平。"
        interp_label = ttk.Label(interp_frame,
                                text=interp_text,
                                font=('Microsoft YaHei', 11),
                                wraplength=500)
        interp_label.pack(anchor='w', pady=(0, 10))
        
        # 建议
        rec_label = ttk.Label(interp_frame,
                             text="建议：",
                             font=('Microsoft YaHei', 11, 'bold'))
        rec_label.pack(anchor='w')
        
        for i, rec in enumerate(recommendations, 1):
            rec_text = ttk.Label(interp_frame,
                               text=f"{i}. {rec}",
                               font=('Microsoft YaHei', 10),
                               wraplength=500)
            rec_text.pack(anchor='w', padx=(20, 0), pady=2)
        
        # 关闭按钮
        close_btn = ttk.Button(main_frame,
                              text="关闭",
                              command=result_window.destroy)
        close_btn.pack(pady=(15, 0))
        
    def save_tinetti_result(self):
        """保存Tinetti评估结果"""
        try:
            # 获取患者信息
            patient_info = {
                'name': getattr(self, 'name_var', tk.StringVar()).get(),
                'age': getattr(self, 'age_var', tk.StringVar()).get(),
                'gender': getattr(self, 'gender_var', tk.StringVar()).get()
            }
            
            # 计算分数
            balance_score = 0
            gait_score = 0
            
            for i in range(9):  # 平衡测试
                var_name = f"balance_{i}"
                if var_name in self.tinetti_vars:
                    balance_score += self.tinetti_vars[var_name].get()
            
            for i in range(8):  # 步态测试
                var_name = f"gait_{i}"
                if var_name in self.tinetti_vars:
                    gait_score += self.tinetti_vars[var_name].get()
            
            total_score = balance_score + gait_score
            
            # 确定跌倒风险等级
            if total_score >= 24:
                risk_level = "低跌倒风险"
            elif total_score >= 19:
                risk_level = "中等跌倒风险"
            else:
                risk_level = "高跌倒风险"
            
            # 保存数据
            result_data = {
                'scale_type': 'Tinetti',
                'scale_name': 'Tinetti步态与平衡评估量表',
                'patient_info': patient_info,
                'assessment_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'balance_score': balance_score,
                'gait_score': gait_score,
                'total_score': total_score,
                'max_score': 28,
                'risk_level': risk_level
            }
            
            # 调用主应用的保存方法
            if hasattr(self.main_app, 'data_manager'):
                self.main_app.data_manager.save_assessment_result(result_data)
                messagebox.showinfo("成功", "Tinetti评估结果已保存")
            else:
                messagebox.showwarning("警告", "数据管理器不可用，无法保存结果")
                
        except Exception as e:
            messagebox.showerror("错误", f"保存失败：{str(e)}")
            
    def reset_tinetti(self):
        """重置Tinetti评估"""
        if hasattr(self, 'tinetti_vars'):
            for var in self.tinetti_vars.values():
                var.set(0)
        messagebox.showinfo("提示", "Tinetti评估已重置")
        
    def back_to_category(self):
        """返回运动功能量表分类页面"""
        self.main_app.show_scale_category('motor')