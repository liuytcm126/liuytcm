#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
认知功能评估量表模块
开发人员：LIUYING
包含：MMSE、MoCA、CDR等量表
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json

class CognitiveScales:
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        self.current_scale = None
        self.current_responses = {}
        
    def show_mmse_assessment(self):
        """显示MMSE评估界面"""
        self.current_scale = 'MMSE'
        self.current_responses = {}
        
        # 清空父容器
        for widget in self.parent.winfo_children():
            widget.destroy()
            
        # 创建MMSE评估界面
        self.create_mmse_interface()
        
    def create_mmse_interface(self):
        """创建MMSE评估界面"""
        # 主容器
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 标题区域
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = ttk.Label(title_frame,
                               text="简易精神状态检查量表 (MMSE)",
                               font=('Microsoft YaHei', 18, 'bold'),
                               foreground='#2E86AB')
        title_label.pack(side='left')
        
        # 返回按钮
        back_btn = ttk.Button(title_frame,
                             text="返回",
                             command=self.back_to_category)
        back_btn.pack(side='right')
        
        # 患者信息区域
        self.create_patient_info_section(main_frame)
        
        # 评估内容区域
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill='both', expand=True, pady=(20, 0))
        
        # 创建滚动区域
        canvas = tk.Canvas(content_frame)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # MMSE评估项目
        self.create_mmse_items(scrollable_frame)
        
        # 底部按钮区域
        self.create_bottom_buttons(main_frame)
        
    def create_patient_info_section(self, parent):
        """创建患者信息区域"""
        info_frame = ttk.LabelFrame(parent, text="患者信息", padding=15)
        info_frame.pack(fill='x', pady=(0, 10))
        
        # 患者信息输入
        info_grid = ttk.Frame(info_frame)
        info_grid.pack(fill='x')
        
        # 姓名
        ttk.Label(info_grid, text="姓名:").grid(row=0, column=0, sticky='w', padx=(0, 10))
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(info_grid, textvariable=self.name_var, width=15)
        name_entry.grid(row=0, column=1, sticky='w', padx=(0, 20))
        
        # 年龄
        ttk.Label(info_grid, text="年龄:").grid(row=0, column=2, sticky='w', padx=(0, 10))
        self.age_var = tk.StringVar()
        age_entry = ttk.Entry(info_grid, textvariable=self.age_var, width=10)
        age_entry.grid(row=0, column=3, sticky='w', padx=(0, 20))
        
        # 性别
        ttk.Label(info_grid, text="性别:").grid(row=0, column=4, sticky='w', padx=(0, 10))
        self.gender_var = tk.StringVar(value="男")
        gender_combo = ttk.Combobox(info_grid, textvariable=self.gender_var, 
                                   values=["男", "女"], width=8, state="readonly")
        gender_combo.grid(row=0, column=5, sticky='w', padx=(0, 20))
        
        # 教育程度
        ttk.Label(info_grid, text="教育程度:").grid(row=1, column=0, sticky='w', padx=(0, 10), pady=(10, 0))
        self.education_var = tk.StringVar()
        education_combo = ttk.Combobox(info_grid, textvariable=self.education_var,
                                     values=["小学", "初中", "高中", "大专", "本科", "研究生"],
                                     width=15, state="readonly")
        education_combo.grid(row=1, column=1, sticky='w', padx=(0, 20), pady=(10, 0))
        
        # 评估日期
        ttk.Label(info_grid, text="评估日期:").grid(row=1, column=2, sticky='w', padx=(0, 10), pady=(10, 0))
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        date_entry = ttk.Entry(info_grid, textvariable=self.date_var, width=12)
        date_entry.grid(row=1, column=3, sticky='w', padx=(0, 20), pady=(10, 0))
        
    def create_mmse_items(self, parent):
        """创建MMSE评估项目"""
        self.mmse_vars = {}
        
        # MMSE评估项目数据
        mmse_items = [
            {
                'category': '定向力（时间）',
                'max_score': 5,
                'items': [
                    '现在是哪一年？',
                    '现在是哪个季节？',
                    '现在是几月份？',
                    '今天是几号？',
                    '今天是星期几？'
                ]
            },
            {
                'category': '定向力（地点）',
                'max_score': 5,
                'items': [
                    '我们现在在哪个省（直辖市）？',
                    '我们现在在哪个市（区）？',
                    '我们现在在什么地方？',
                    '我们现在在哪一层楼？',
                    '我们现在在哪个房间？'
                ]
            },
            {
                'category': '即刻记忆',
                'max_score': 3,
                'items': [
                    '重复三个词：苹果、硬币、桌子（各1分）'
                ],
                'instruction': '请患者重复这三个词，重复直到患者能正确说出为止，记录尝试次数'
            },
            {
                'category': '注意力和计算力',
                'max_score': 5,
                'items': [
                    '从100开始，每次减7：93、86、79、72、65（各1分）'
                ],
                'instruction': '或者让患者倒拼"WORLD"：D-L-R-O-W',
                'alternative': True
            },
            {
                'category': '延迟回忆',
                'max_score': 3,
                'items': [
                    '回忆刚才的三个词：苹果、硬币、桌子（各1分）'
                ]
            },
            {
                'category': '语言能力',
                'max_score': 9,
                'items': [
                    '命名：手表（1分）',
                    '命名：铅笔（1分）',
                    '重复："没有如果、和或但是"（1分）',
                    '三步指令："用右手拿起这张纸，对折，放在地上"（3分）',
                    '阅读并执行："闭上眼睛"（1分）',
                    '写一个句子（1分）',
                    '复制图形（1分）'
                ]
            }
        ]
        
        for i, category_data in enumerate(mmse_items):
            # 创建分类框架
            category_frame = ttk.LabelFrame(parent, 
                                          text=f"{category_data['category']} (最高{category_data['max_score']}分)",
                                          padding=15)
            category_frame.pack(fill='x', pady=10)
            
            # 如果有说明，显示说明
            if 'instruction' in category_data:
                instruction_label = ttk.Label(category_frame,
                                            text=f"说明：{category_data['instruction']}",
                                            font=('Microsoft YaHei', 10),
                                            foreground='#6C757D')
                instruction_label.pack(anchor='w', pady=(0, 10))
            
            # 创建评估项目
            for j, item in enumerate(category_data['items']):
                item_frame = ttk.Frame(category_frame)
                item_frame.pack(fill='x', pady=5)
                
                # 项目描述
                item_label = ttk.Label(item_frame, text=item, width=50)
                item_label.pack(side='left', anchor='w')
                
                # 评分选项
                var_name = f"{i}_{j}"
                self.mmse_vars[var_name] = tk.IntVar()
                
                score_frame = ttk.Frame(item_frame)
                score_frame.pack(side='right')
                
                # 根据项目类型创建不同的评分选项
                if '各1分' in item or category_data['category'] in ['定向力（时间）', '定向力（地点）']:
                    # 多个1分项目
                    if '各1分' in item:
                        max_val = 3 if '三个词' in item else 5
                    else:
                        max_val = 1
                        
                    for score in range(max_val + 1):
                        rb = ttk.Radiobutton(score_frame,
                                           text=str(score),
                                           variable=self.mmse_vars[var_name],
                                           value=score)
                        rb.pack(side='left', padx=5)
                else:
                    # 单个项目
                    for score in [0, 1]:
                        rb = ttk.Radiobutton(score_frame,
                                           text=str(score),
                                           variable=self.mmse_vars[var_name],
                                           value=score)
                        rb.pack(side='left', padx=5)
                        
    def create_bottom_buttons(self, parent):
        """创建底部按钮"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', pady=(20, 0))
        
        # 计算总分按钮
        calc_btn = ttk.Button(button_frame,
                             text="计算总分",
                             command=self.calculate_mmse_score)
        calc_btn.pack(side='left', padx=(0, 10))
        
        # 保存结果按钮
        save_btn = ttk.Button(button_frame,
                             text="保存结果",
                             command=self.save_mmse_result)
        save_btn.pack(side='left', padx=(0, 10))
        
        # 重置按钮
        reset_btn = ttk.Button(button_frame,
                              text="重置",
                              command=self.reset_mmse)
        reset_btn.pack(side='left')
        
        # 总分显示
        self.score_label = ttk.Label(button_frame,
                                    text="总分：-- / 30",
                                    font=('Microsoft YaHei', 14, 'bold'),
                                    foreground='#2E86AB')
        self.score_label.pack(side='right')
        
    def calculate_mmse_score(self):
        """计算MMSE总分"""
        total_score = 0
        
        # 定向力（时间）- 5分
        for i in range(5):
            total_score += self.mmse_vars[f"0_{i}"].get()
            
        # 定向力（地点）- 5分
        for i in range(5):
            total_score += self.mmse_vars[f"1_{i}"].get()
            
        # 即刻记忆 - 3分
        total_score += self.mmse_vars["2_0"].get()
        
        # 注意力和计算力 - 5分
        total_score += self.mmse_vars["3_0"].get()
        
        # 延迟回忆 - 3分
        total_score += self.mmse_vars["4_0"].get()
        
        # 语言能力 - 9分
        for i in range(7):
            if i == 3:  # 三步指令最高3分
                total_score += min(self.mmse_vars[f"5_{i}"].get(), 3)
            else:
                total_score += self.mmse_vars[f"5_{i}"].get()
                
        # 更新显示
        self.score_label.config(text=f"总分：{total_score} / 30")
        
        # 显示解释
        self.show_mmse_interpretation(total_score)
        
        return total_score
        
    def show_mmse_interpretation(self, score):
        """显示MMSE评分解释"""
        if score >= 27:
            interpretation = "正常认知功能"
            color = "#28A745"  # 绿色
        elif score >= 24:
            interpretation = "轻度认知功能障碍"
            color = "#FFC107"  # 黄色
        elif score >= 18:
            interpretation = "中度认知功能障碍"
            color = "#FD7E14"  # 橙色
        else:
            interpretation = "重度认知功能障碍"
            color = "#DC3545"  # 红色
            
        # 创建解释窗口
        interpretation_window = tk.Toplevel(self.parent)
        interpretation_window.title("MMSE评分解释")
        interpretation_window.geometry("400x300")
        interpretation_window.resizable(False, False)
        
        # 居中显示
        interpretation_window.transient(self.parent)
        interpretation_window.grab_set()
        
        main_frame = ttk.Frame(interpretation_window, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # 分数显示
        score_label = ttk.Label(main_frame,
                               text=f"MMSE总分：{score} / 30",
                               font=('Microsoft YaHei', 16, 'bold'))
        score_label.pack(pady=(0, 20))
        
        # 解释显示
        interp_label = ttk.Label(main_frame,
                                text=interpretation,
                                font=('Microsoft YaHei', 14, 'bold'),
                                foreground=color)
        interp_label.pack(pady=(0, 20))
        
        # 详细说明
        detail_text = """
评分标准：
• 27-30分：正常认知功能
• 24-26分：轻度认知功能障碍
• 18-23分：中度认知功能障碍
• 0-17分：重度认知功能障碍

注意：
• 评分需结合患者教育程度
• 建议结合其他检查综合判断
• 如有疑问请咨询专科医师
        """
        
        detail_label = ttk.Label(main_frame,
                                text=detail_text,
                                font=('Microsoft YaHei', 10),
                                justify='left')
        detail_label.pack(pady=(0, 20))
        
        # 关闭按钮
        close_btn = ttk.Button(main_frame,
                              text="关闭",
                              command=interpretation_window.destroy)
        close_btn.pack()
        
    def save_mmse_result(self):
        """保存MMSE评估结果"""
        # 检查患者信息
        if not self.name_var.get().strip():
            messagebox.showerror("错误", "请输入患者姓名")
            return
            
        # 计算总分
        total_score = self.calculate_mmse_score()
        
        # 准备保存数据
        result_data = {
            'scale_type': 'MMSE',
            'patient_info': {
                'name': self.name_var.get(),
                'age': self.age_var.get(),
                'gender': self.gender_var.get(),
                'education': self.education_var.get(),
                'assessment_date': self.date_var.get()
            },
            'scores': {var: val.get() for var, val in self.mmse_vars.items()},
            'total_score': total_score,
            'max_score': 30,
            'timestamp': datetime.now().isoformat()
        }
        
        # 保存到文件
        try:
            import os
            if not os.path.exists('results'):
                os.makedirs('results')
                
            filename = f"results/MMSE_{self.name_var.get()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
                
            messagebox.showinfo("成功", f"评估结果已保存到：{filename}")
            
        except Exception as e:
            messagebox.showerror("错误", f"保存失败：{str(e)}")
            
    def reset_mmse(self):
        """重置MMSE评估"""
        if messagebox.askyesno("确认", "确定要重置所有评估内容吗？"):
            for var in self.mmse_vars.values():
                var.set(0)
            self.score_label.config(text="总分：-- / 30")
            
    def back_to_category(self):
        """返回分类页面"""
        self.main_app.show_scale_category('cognitive')
        
    def show_moca_assessment(self):
        """显示MoCA评估界面"""
        self.current_scale = 'MoCA'
        self.current_responses = {}
        
        # 清空父容器
        for widget in self.parent.winfo_children():
            widget.destroy()
            
        # 创建MoCA评估界面
        self.create_moca_interface()
        
    def create_moca_interface(self):
        """创建MoCA评估界面"""
        # 主容器
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 标题区域
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = ttk.Label(title_frame,
                               text="蒙特利尔认知评估量表 (MoCA)",
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
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 患者信息区域
        self.create_patient_info_section(scrollable_frame)
        
        # MoCA评估项目
        self.create_moca_items(scrollable_frame)
        
        # 底部按钮
        self.create_moca_bottom_buttons(scrollable_frame)
        
    def create_moca_items(self, parent):
        """创建MoCA评估项目"""
        items_frame = ttk.LabelFrame(parent, text="MoCA评估项目", padding=15)
        items_frame.pack(fill='x', pady=10)
        
        # MoCA评估项目数据
        moca_items = [
            {
                'domain': '视空间/执行功能',
                'items': [
                    {'name': '连线测试', 'max_score': 1, 'description': '按数字和字母交替顺序连线'},
                    {'name': '立方体复制', 'max_score': 1, 'description': '复制立方体图形'},
                    {'name': '钟表绘制', 'max_score': 3, 'description': '画钟表并标出指定时间'}
                ]
            },
            {
                'domain': '命名',
                'items': [
                    {'name': '动物命名', 'max_score': 3, 'description': '说出狮子、犀牛、骆驼的名称'}
                ]
            },
            {
                'domain': '记忆',
                'items': [
                    {'name': '词语记忆', 'max_score': 0, 'description': '记住5个词语（不计分，用于延迟回忆）'}
                ]
            },
            {
                'domain': '注意力',
                'items': [
                    {'name': '数字广度', 'max_score': 2, 'description': '正向和反向重复数字序列'},
                    {'name': '警觉性', 'max_score': 1, 'description': '听到字母A时拍手'},
                    {'name': '连续减7', 'max_score': 3, 'description': '从100开始连续减7'}
                ]
            },
            {
                'domain': '语言',
                'items': [
                    {'name': '语句重复', 'max_score': 2, 'description': '重复两个句子'},
                    {'name': '语言流畅性', 'max_score': 1, 'description': '说出以F开头的词语'}
                ]
            },
            {
                'domain': '抽象思维',
                'items': [
                    {'name': '相似性', 'max_score': 2, 'description': '说出两个词语的相似性'}
                ]
            },
            {
                'domain': '延迟回忆',
                'items': [
                    {'name': '自由回忆', 'max_score': 5, 'description': '回忆之前记住的5个词语'}
                ]
            },
            {
                'domain': '定向力',
                'items': [
                    {'name': '时间定向', 'max_score': 4, 'description': '说出日期、月份、年份、星期'},
                    {'name': '地点定向', 'max_score': 2, 'description': '说出地点、城市'}
                ]
            }
        ]
        
        self.moca_responses = {}
        
        for domain_info in moca_items:
            domain_frame = ttk.LabelFrame(items_frame, text=domain_info['domain'], padding=10)
            domain_frame.pack(fill='x', pady=5)
            
            for item in domain_info['items']:
                item_frame = ttk.Frame(domain_frame)
                item_frame.pack(fill='x', pady=2)
                
                # 项目名称和描述
                name_label = ttk.Label(item_frame, 
                                      text=f"{item['name']} (最高{item['max_score']}分)",
                                      font=('Microsoft YaHei', 10, 'bold'))
                name_label.pack(anchor='w')
                
                desc_label = ttk.Label(item_frame,
                                     text=item['description'],
                                     font=('Microsoft YaHei', 9),
                                     foreground='#666666')
                desc_label.pack(anchor='w', padx=(20, 0))
                
                # 评分选项
                score_frame = ttk.Frame(item_frame)
                score_frame.pack(anchor='w', padx=(20, 0), pady=5)
                
                var = tk.IntVar()
                self.moca_responses[item['name']] = var
                
                for score in range(item['max_score'] + 1):
                    rb = ttk.Radiobutton(score_frame,
                                        text=str(score),
                                        variable=var,
                                        value=score)
                    rb.pack(side='left', padx=5)
    
    def create_moca_bottom_buttons(self, parent):
        """创建MoCA底部按钮"""
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill='x', pady=20)
        
        # 计算得分按钮
        calc_btn = ttk.Button(btn_frame,
                             text="计算得分",
                             command=self.calculate_moca_score)
        calc_btn.pack(side='left', padx=(0, 10))
        
        # 保存结果按钮
        save_btn = ttk.Button(btn_frame,
                             text="保存结果",
                             command=self.save_moca_result)
        save_btn.pack(side='left', padx=(0, 10))
        
        # 重置按钮
        reset_btn = ttk.Button(btn_frame,
                              text="重置",
                              command=self.reset_moca)
        reset_btn.pack(side='left')
        
    def calculate_moca_score(self):
        """计算MoCA得分"""
        if not hasattr(self, 'moca_responses'):
            messagebox.showwarning("警告", "请先完成评估")
            return
            
        total_score = sum(var.get() for var in self.moca_responses.values())
        self.show_moca_interpretation(total_score)
        
    def show_moca_interpretation(self, score):
        """显示MoCA结果解释"""
        # 教育程度校正
        education_correction = messagebox.askyesno("教育程度校正", 
                                                  "患者受教育年限是否≤12年？\n如果是，总分需要加1分")
        
        if education_correction:
            corrected_score = score + 1
            correction_text = f"原始得分：{score}分\n校正后得分：{corrected_score}分（教育程度校正+1分）"
        else:
            corrected_score = score
            correction_text = f"得分：{score}分"
            
        # 结果解释
        if corrected_score >= 26:
            interpretation = "认知功能正常"
            color = "#28A745"
        elif corrected_score >= 22:
            interpretation = "轻度认知障碍"
            color = "#FFC107"
        elif corrected_score >= 17:
            interpretation = "中度认知障碍"
            color = "#FF6B35"
        else:
            interpretation = "重度认知障碍"
            color = "#DC3545"
            
        # 创建结果窗口
        result_window = tk.Toplevel(self.parent)
        result_window.title("MoCA评估结果")
        result_window.geometry("400x300")
        result_window.resizable(False, False)
        
        # 居中显示
        result_window.transient(self.parent)
        result_window.grab_set()
        
        # 结果内容
        content_frame = ttk.Frame(result_window, padding=20)
        content_frame.pack(fill='both', expand=True)
        
        title_label = ttk.Label(content_frame,
                               text="MoCA评估结果",
                               font=('Microsoft YaHei', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        score_label = ttk.Label(content_frame,
                               text=correction_text,
                               font=('Microsoft YaHei', 12))
        score_label.pack(pady=5)
        
        result_label = ttk.Label(content_frame,
                                text=f"评估结果：{interpretation}",
                                font=('Microsoft YaHei', 14, 'bold'),
                                foreground=color)
        result_label.pack(pady=10)
        
        # 详细说明
        detail_text = """
评分标准：
• ≥26分：认知功能正常
• 22-25分：轻度认知障碍
• 17-21分：中度认知障碍
• <17分：重度认知障碍

注意：
• 教育年限≤12年者需加1分
• 建议结合临床表现综合判断
        """
        
        detail_label = ttk.Label(content_frame,
                                text=detail_text,
                                font=('Microsoft YaHei', 9),
                                justify='left')
        detail_label.pack(pady=10)
        
        # 关闭按钮
        close_btn = ttk.Button(content_frame,
                              text="关闭",
                              command=result_window.destroy)
        close_btn.pack(pady=10)
        
    def save_moca_result(self):
        """保存MoCA评估结果"""
        if not hasattr(self, 'moca_responses'):
            messagebox.showwarning("警告", "请先完成评估")
            return
            
        # 获取患者信息
        patient_info = {
            'name': self.patient_name_var.get(),
            'age': self.patient_age_var.get(),
            'gender': self.patient_gender_var.get(),
            'education': self.patient_education_var.get()
        }
        
        # 计算得分
        total_score = sum(var.get() for var in self.moca_responses.values())
        
        # 保存数据
        result_data = {
            'scale_type': 'MoCA',
            'patient_info': patient_info,
            'responses': {name: var.get() for name, var in self.moca_responses.items()},
            'total_score': total_score,
            'assessment_date': datetime.now().isoformat()
        }
        
        # 保存到文件
        try:
            import os
            os.makedirs('results', exist_ok=True)
            
            filename = f"results/MoCA_{patient_info['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
                
            messagebox.showinfo("成功", f"评估结果已保存到：{filename}")
        except Exception as e:
            messagebox.showerror("错误", f"保存失败：{str(e)}")
            
    def reset_moca(self):
        """重置MoCA评估"""
        if hasattr(self, 'moca_responses'):
            for var in self.moca_responses.values():
                var.set(0)
        messagebox.showinfo("提示", "MoCA评估已重置")
        
    def show_cdr_assessment(self):
        """显示CDR评估界面"""
        self.current_scale = 'CDR'
        self.current_responses = {}
        
        # 清空父容器
        for widget in self.parent.winfo_children():
            widget.destroy()
            
        # 创建CDR评估界面
        self.create_cdr_interface()
        
    def create_cdr_interface(self):
        """创建CDR评估界面"""
        # 主容器
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 标题区域
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = ttk.Label(title_frame,
                               text="临床痴呆评定量表 (CDR)",
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
        
        # CDR评估项目
        self.create_cdr_items(scrollable_frame)
        
        # 底部按钮
        self.create_cdr_bottom_buttons(scrollable_frame)
        
        # 布局滚动区域
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 绑定鼠标滚轮
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
    def create_cdr_items(self, parent):
        """创建CDR评估项目"""
        # CDR评估领域
        cdr_domains = [
            {
                'domain': '记忆',
                'description': '评估近期和远期记忆能力',
                'options': [
                    {'score': 0, 'text': '无记忆丧失或轻微健忘'},
                    {'score': 0.5, 'text': '轻度一致的健忘；部分回忆事件；"良性"健忘'},
                    {'score': 1, 'text': '中度记忆丧失；对近期事件更明显；干扰日常活动'},
                    {'score': 2, 'text': '严重记忆丧失；只保留高度学习的材料；新材料快速丢失'},
                    {'score': 3, 'text': '严重记忆丧失；只有片段保留'}
                ]
            },
            {
                'domain': '定向',
                'description': '评估时间、地点、人物定向能力',
                'options': [
                    {'score': 0, 'text': '完全定向'},
                    {'score': 0.5, 'text': '完全定向，除了对时间关系的轻微困难'},
                    {'score': 1, 'text': '中度定向困难；通常对时间有困难；可能对地点有困难'},
                    {'score': 2, 'text': '严重定向困难；通常对人物失去定向'},
                    {'score': 3, 'text': '只对人物有定向'}
                ]
            },
            {
                'domain': '判断和解决问题',
                'description': '评估解决日常问题和处理商务/财务事务的能力',
                'options': [
                    {'score': 0, 'text': '很好地解决日常问题；商务/财务事务处理良好'},
                    {'score': 0.5, 'text': '解决日常问题时轻微受损；判断社会情况的能力轻微受损'},
                    {'score': 1, 'text': '解决问题时中度困难；社会判断通常保持'},
                    {'score': 2, 'text': '严重受损解决问题；社会判断通常受损'},
                    {'score': 3, 'text': '无法做出判断或解决问题'}
                ]
            },
            {
                'domain': '社区事务',
                'description': '评估独立参与社区活动和事务的能力',
                'options': [
                    {'score': 0, 'text': '独立功能在通常水平的工作、购物、志愿和社会团体'},
                    {'score': 0.5, 'text': '这些活动轻微受损'},
                    {'score': 1, 'text': '无法独立在这些活动中功能，虽然可能仍然参与一些'},
                    {'score': 2, 'text': '无外观正常活动'},
                    {'score': 3, 'text': '无外观正常活动'}
                ]
            },
            {
                'domain': '家庭和爱好',
                'description': '评估家庭生活、爱好和兴趣的功能',
                'options': [
                    {'score': 0, 'text': '家庭生活、爱好、智力兴趣很好保持'},
                    {'score': 0.5, 'text': '家庭生活、爱好、智力兴趣轻微受损'},
                    {'score': 1, 'text': '家庭生活轻微但明确受损；放弃更困难的家务；放弃复杂的爱好和兴趣'},
                    {'score': 2, 'text': '只保持简单的家务；兴趣很受限且维持不好'},
                    {'score': 3, 'text': '无家庭功能'}
                ]
            },
            {
                'domain': '个人护理',
                'description': '评估个人卫生和护理能力',
                'options': [
                    {'score': 0, 'text': '完全有能力自我护理'},
                    {'score': 0.5, 'text': '完全有能力自我护理'},
                    {'score': 1, 'text': '需要提示'},
                    {'score': 2, 'text': '在穿衣、卫生、个人物品保管方面需要帮助'},
                    {'score': 3, 'text': '需要很多个人护理帮助；经常失禁'}
                ]
            }
        ]
        
        # 评估说明
        instruction_frame = ttk.LabelFrame(parent, text="评估说明", padding=15)
        instruction_frame.pack(fill='x', pady=(0, 20))
        
        instruction_text = (
            "CDR评估包括6个认知和功能领域。请根据患者的实际情况选择最符合的描述。\n"
            "评分：0=正常，0.5=可疑痴呆，1=轻度痴呆，2=中度痴呆，3=重度痴呆"
        )
        instruction_label = ttk.Label(instruction_frame, text=instruction_text,
                                    font=('Microsoft YaHei', 10),
                                    foreground='#6C757D')
        instruction_label.pack(anchor='w')
        
        # 创建评估项目
        self.cdr_vars = {}
        
        for i, domain in enumerate(cdr_domains):
            domain_frame = ttk.LabelFrame(parent, text=f"{i+1}. {domain['domain']}", padding=15)
            domain_frame.pack(fill='x', pady=10)
            
            # 领域描述
            desc_label = ttk.Label(domain_frame,
                                 text=domain['description'],
                                 font=('Microsoft YaHei', 10),
                                 foreground='#6C757D')
            desc_label.pack(anchor='w', pady=(0, 10))
            
            # 评分选项
            var_name = f"domain_{i}"
            self.cdr_vars[var_name] = tk.DoubleVar()
            
            for option in domain['options']:
                option_frame = ttk.Frame(domain_frame)
                option_frame.pack(fill='x', pady=2)
                
                rb = ttk.Radiobutton(option_frame,
                                   text=f"{option['score']} - {option['text']}",
                                   variable=self.cdr_vars[var_name],
                                   value=option['score'])
                rb.pack(anchor='w')
                
    def create_cdr_bottom_buttons(self, parent):
        """创建CDR底部按钮"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', pady=(20, 0))
        
        # 计算总分按钮
        calc_btn = ttk.Button(button_frame,
                             text="计算CDR评分",
                             command=self.calculate_cdr_score,
                             style='Accent.TButton')
        calc_btn.pack(side='left', padx=(0, 10))
        
        # 保存结果按钮
        save_btn = ttk.Button(button_frame,
                             text="保存结果",
                             command=self.save_cdr_result)
        save_btn.pack(side='left', padx=(0, 10))
        
        # 重置按钮
        reset_btn = ttk.Button(button_frame,
                              text="重置",
                              command=self.reset_cdr)
        reset_btn.pack(side='left')
        
    def calculate_cdr_score(self):
        """计算CDR评分"""
        try:
            # 检查是否所有领域都已评分
            scores = []
            for var_name, var in self.cdr_vars.items():
                score = var.get()
                if score == 0 and var_name not in ['domain_0', 'domain_1', 'domain_2', 'domain_3', 'domain_4', 'domain_5']:
                    messagebox.showwarning("警告", "请完成所有领域的评估")
                    return
                scores.append(score)
            
            # CDR总分计算规则（简化版）
            memory_score = scores[0]  # 记忆领域
            other_scores = scores[1:]  # 其他领域
            
            # 如果记忆和其他至少3个领域的评分相同，则CDR等于该评分
            if other_scores.count(memory_score) >= 3:
                cdr_score = memory_score
            else:
                # 否则使用多数规则
                from collections import Counter
                score_counts = Counter(scores)
                cdr_score = score_counts.most_common(1)[0][0]
            
            # 显示结果解释
            self.show_cdr_interpretation(cdr_score)
            
        except Exception as e:
            messagebox.showerror("错误", f"计算CDR评分时出错：{str(e)}")
            
    def show_cdr_interpretation(self, cdr_score):
        """显示CDR评分解释"""
        # 评分解释
        interpretations = {
            0: {
                'level': '正常',
                'description': '无痴呆症状',
                'recommendations': [
                    '继续保持健康的生活方式',
                    '定期进行认知功能检查',
                    '保持社交活动和智力刺激'
                ]
            },
            0.5: {
                'level': '可疑痴呆',
                'description': '轻微认知障碍，需要密切观察',
                'recommendations': [
                    '建议进一步神经心理学评估',
                    '定期随访监测认知变化',
                    '加强认知训练和康复',
                    '评估和治疗可逆性因素'
                ]
            },
            1: {
                'level': '轻度痴呆',
                'description': '明显的认知功能障碍，影响日常生活',
                'recommendations': [
                    '开始药物治疗（如胆碱酯酶抑制剂）',
                    '制定个性化的护理计划',
                    '家属教育和支持',
                    '安全评估和环境改造'
                ]
            },
            2: {
                'level': '中度痴呆',
                'description': '严重认知功能障碍，需要较多帮助',
                'recommendations': [
                    '调整药物治疗方案',
                    '加强日常生活护理',
                    '行为和心理症状管理',
                    '考虑日间照料服务'
                ]
            },
            3: {
                'level': '重度痴呆',
                'description': '严重认知功能障碍，需要全面护理',
                'recommendations': [
                    '全面护理和生活支持',
                    '症状性治疗',
                    '舒适护理和生活质量维护',
                    '家属心理支持'
                ]
            }
        }
        
        interpretation = interpretations.get(cdr_score, interpretations[0])
        
        # 创建结果窗口
        result_window = tk.Toplevel(self.parent)
        result_window.title("CDR评估结果")
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
                               text="CDR评估结果",
                               font=('Microsoft YaHei', 16, 'bold'),
                               foreground='#2E86AB')
        title_label.pack(pady=(0, 20))
        
        # 评分结果
        score_frame = ttk.LabelFrame(main_frame, text="评分结果", padding=15)
        score_frame.pack(fill='x', pady=(0, 15))
        
        score_text = f"CDR总分：{cdr_score}\n严重程度：{interpretation['level']}"
        score_label = ttk.Label(score_frame,
                               text=score_text,
                               font=('Microsoft YaHei', 12, 'bold'),
                               foreground='#E74C3C' if cdr_score >= 1 else '#27AE60')
        score_label.pack()
        
        # 结果解释
        interp_frame = ttk.LabelFrame(main_frame, text="结果解释", padding=15)
        interp_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        interp_label = ttk.Label(interp_frame,
                                text=interpretation['description'],
                                font=('Microsoft YaHei', 11),
                                wraplength=500)
        interp_label.pack(anchor='w', pady=(0, 10))
        
        # 建议
        rec_label = ttk.Label(interp_frame,
                             text="建议：",
                             font=('Microsoft YaHei', 11, 'bold'))
        rec_label.pack(anchor='w')
        
        for i, rec in enumerate(interpretation['recommendations'], 1):
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
        
    def save_cdr_result(self):
        """保存CDR评估结果"""
        try:
            # 获取患者信息
            patient_info = {
                'name': getattr(self, 'patient_name_var', tk.StringVar()).get(),
                'age': getattr(self, 'patient_age_var', tk.StringVar()).get(),
                'gender': getattr(self, 'patient_gender_var', tk.StringVar()).get(),
                'education': getattr(self, 'patient_education_var', tk.StringVar()).get()
            }
            
            # 获取评估结果
            domain_scores = {}
            domain_names = ['记忆', '定向', '判断和解决问题', '社区事务', '家庭和爱好', '个人护理']
            
            for i, (var_name, var) in enumerate(self.cdr_vars.items()):
                domain_scores[domain_names[i]] = var.get()
            
            # 计算总分
            scores = list(domain_scores.values())
            memory_score = scores[0]
            other_scores = scores[1:]
            
            if other_scores.count(memory_score) >= 3:
                total_score = memory_score
            else:
                from collections import Counter
                score_counts = Counter(scores)
                total_score = score_counts.most_common(1)[0][0]
            
            # 保存数据
            result_data = {
                'scale_type': 'CDR',
                'scale_name': '临床痴呆评定量表',
                'patient_info': patient_info,
                'assessment_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'domain_scores': domain_scores,
                'total_score': total_score,
                'severity_level': {
                    0: '正常',
                    0.5: '可疑痴呆', 
                    1: '轻度痴呆',
                    2: '中度痴呆',
                    3: '重度痴呆'
                }.get(total_score, '未知')
            }
            
            # 调用主应用的保存方法
            if hasattr(self.main_app, 'data_manager'):
                self.main_app.data_manager.save_assessment_result(result_data)
                messagebox.showinfo("成功", "CDR评估结果已保存")
            else:
                messagebox.showwarning("警告", "数据管理器不可用，无法保存结果")
                
        except Exception as e:
            messagebox.showerror("错误", f"保存失败：{str(e)}")
            
    def reset_cdr(self):
        """重置CDR评估"""
        if hasattr(self, 'cdr_vars'):
            for var in self.cdr_vars.values():
                var.set(0)
        messagebox.showinfo("提示", "CDR评估已重置")