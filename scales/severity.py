#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
疾病严重程度评估量表模块
开发人员：LIUYING
包含：NIHSS、GCS、mRS等量表
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json

class SeverityScales:
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        self.current_scale = None
        self.current_responses = {}
        
    def show_nihss_assessment(self):
        """显示NIHSS评估界面"""
        self.current_scale = 'NIHSS'
        self.current_responses = {}
        
        # 清空父容器
        for widget in self.parent.winfo_children():
            widget.destroy()
            
        # 创建NIHSS评估界面
        self.create_nihss_interface()
        
    def create_nihss_interface(self):
        """创建NIHSS评估界面"""
        # 主标题
        title_frame = ttk.Frame(self.parent)
        title_frame.pack(fill='x', padx=20, pady=10)
        
        title_label = ttk.Label(title_frame, 
                               text="美国国立卫生研究院卒中量表 (NIHSS)",
                               font=('Microsoft YaHei', 16, 'bold'))
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame,
                                  text="National Institutes of Health Stroke Scale",
                                  font=('Microsoft YaHei', 10))
        subtitle_label.pack(pady=(0, 10))
        
        # 创建滚动框架
        canvas = tk.Canvas(self.parent)
        scrollbar = ttk.Scrollbar(self.parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 创建评估项目
        self.create_nihss_items(scrollable_frame)
        
        # 创建底部按钮
        self.create_nihss_bottom_buttons(scrollable_frame)
        
        # 布局滚动组件
        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=10)
        
        # 绑定鼠标滚轮
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
    def create_nihss_items(self, parent):
        """创建NIHSS评估项目"""
        self.nihss_vars = {}
        
        # NIHSS评估项目
        nihss_items = [
            {
                'id': '1a',
                'title': '1a. 意识水平',
                'options': [
                    (0, '清醒，立即反应'),
                    (1, '嗜睡，轻微刺激可唤醒'),
                    (2, '昏睡，需要反复刺激才能唤醒'),
                    (3, '昏迷，仅有反射性运动或无反应')
                ]
            },
            {
                'id': '1b',
                'title': '1b. 意识水平问题（询问月份和年龄）',
                'options': [
                    (0, '两个问题都正确'),
                    (1, '一个问题正确'),
                    (2, '两个问题都不正确')
                ]
            },
            {
                'id': '1c',
                'title': '1c. 意识水平指令（睁眼闭眼、握拳松拳）',
                'options': [
                    (0, '两个指令都正确执行'),
                    (1, '一个指令正确执行'),
                    (2, '两个指令都不能执行')
                ]
            },
            {
                'id': '2',
                'title': '2. 最佳凝视',
                'options': [
                    (0, '正常'),
                    (1, '部分凝视麻痹'),
                    (2, '强迫性偏视或完全凝视麻痹')
                ]
            },
            {
                'id': '3',
                'title': '3. 视野',
                'options': [
                    (0, '无视野缺损'),
                    (1, '部分偏盲'),
                    (2, '完全偏盲'),
                    (3, '双侧偏盲')
                ]
            },
            {
                'id': '4',
                'title': '4. 面瘫',
                'options': [
                    (0, '正常对称运动'),
                    (1, '轻微麻痹'),
                    (2, '部分麻痹'),
                    (3, '完全麻痹')
                ]
            },
            {
                'id': '5a',
                'title': '5a. 左上肢运动',
                'options': [
                    (0, '无偏移，维持90度10秒'),
                    (1, '偏移，但不触及床面'),
                    (2, '有抗重力运动，但不能维持'),
                    (3, '无抗重力运动'),
                    (4, '无运动')
                ]
            },
            {
                'id': '5b',
                'title': '5b. 右上肢运动',
                'options': [
                    (0, '无偏移，维持90度10秒'),
                    (1, '偏移，但不触及床面'),
                    (2, '有抗重力运动，但不能维持'),
                    (3, '无抗重力运动'),
                    (4, '无运动')
                ]
            },
            {
                'id': '6a',
                'title': '6a. 左下肢运动',
                'options': [
                    (0, '无偏移，维持30度5秒'),
                    (1, '偏移，但不触及床面'),
                    (2, '有抗重力运动，但不能维持'),
                    (3, '无抗重力运动'),
                    (4, '无运动')
                ]
            },
            {
                'id': '6b',
                'title': '6b. 右下肢运动',
                'options': [
                    (0, '无偏移，维持30度5秒'),
                    (1, '偏移，但不触及床面'),
                    (2, '有抗重力运动，但不能维持'),
                    (3, '无抗重力运动'),
                    (4, '无运动')
                ]
            },
            {
                'id': '7',
                'title': '7. 肢体共济失调',
                'options': [
                    (0, '无共济失调'),
                    (1, '一个肢体共济失调'),
                    (2, '两个肢体共济失调')
                ]
            },
            {
                'id': '8',
                'title': '8. 感觉',
                'options': [
                    (0, '正常，无感觉缺失'),
                    (1, '轻到中度感觉缺失'),
                    (2, '重度到完全感觉缺失')
                ]
            },
            {
                'id': '9',
                'title': '9. 最佳语言',
                'options': [
                    (0, '无失语'),
                    (1, '轻到中度失语'),
                    (2, '重度失语'),
                    (3, '哑或完全失语')
                ]
            },
            {
                'id': '10',
                'title': '10. 构音障碍',
                'options': [
                    (0, '正常'),
                    (1, '轻到中度构音障碍'),
                    (2, '重度构音障碍')
                ]
            },
            {
                'id': '11',
                'title': '11. 忽视征',
                'options': [
                    (0, '无异常'),
                    (1, '视觉、触觉、听觉、空间或个人忽视'),
                    (2, '重度偏侧忽视或忽视多种感觉方式')
                ]
            }
        ]
        
        for item in nihss_items:
            # 创建项目框架
            item_frame = ttk.LabelFrame(parent, text=item['title'], padding=10)
            item_frame.pack(fill='x', padx=10, pady=5)
            
            # 创建选项变量
            var = tk.IntVar(value=-1)
            self.nihss_vars[item['id']] = var
            
            # 创建选项
            for score, text in item['options']:
                rb = ttk.Radiobutton(item_frame, text=f"{score}分 - {text}",
                                   variable=var, value=score)
                rb.pack(anchor='w', pady=2)
                
    def create_nihss_bottom_buttons(self, parent):
        """创建底部按钮"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', padx=10, pady=20)
        
        # 计算分数按钮
        calc_btn = ttk.Button(button_frame, text="计算分数",
                             command=self.calculate_nihss_score,
                             style='Accent.TButton')
        calc_btn.pack(side='left', padx=(0, 10))
        
        # 重置按钮
        reset_btn = ttk.Button(button_frame, text="重置",
                              command=self.reset_nihss)
        reset_btn.pack(side='left', padx=(0, 10))
        
        # 返回按钮
        back_btn = ttk.Button(button_frame, text="返回",
                             command=lambda: self.main_app.show_scale_category('severity'))
        back_btn.pack(side='right')
        
    def calculate_nihss_score(self):
        """计算NIHSS分数"""
        # 检查是否所有项目都已评分
        for item_id, var in self.nihss_vars.items():
            if var.get() == -1:
                messagebox.showwarning("警告", f"请完成所有评估项目的评分")
                return
        
        # 计算总分
        total_score = sum(var.get() for var in self.nihss_vars.values())
        
        # 保存当前回答
        self.current_responses = {item_id: var.get() for item_id, var in self.nihss_vars.items()}
        
        # 显示结果
        self.show_nihss_interpretation(total_score)
        
    def show_nihss_interpretation(self, total_score):
        """显示NIHSS结果解释"""
        # 确定严重程度
        if total_score == 0:
            severity = "无卒中症状"
            interpretation = "无神经功能缺损"
        elif 1 <= total_score <= 4:
            severity = "轻微卒中"
            interpretation = "轻微神经功能缺损"
        elif 5 <= total_score <= 15:
            severity = "轻到中度卒中"
            interpretation = "轻到中度神经功能缺损"
        elif 16 <= total_score <= 20:
            severity = "中到重度卒中"
            interpretation = "中到重度神经功能缺损"
        elif total_score >= 21:
            severity = "重度卒中"
            interpretation = "重度神经功能缺损"
        
        # 创建结果窗口
        result_window = tk.Toplevel(self.parent)
        result_window.title("NIHSS评估结果")
        result_window.geometry("500x400")
        result_window.resizable(False, False)
        
        # 居中显示
        result_window.transient(self.main_app.root)
        result_window.grab_set()
        
        # 结果内容
        result_frame = ttk.Frame(result_window, padding=20)
        result_frame.pack(fill='both', expand=True)
        
        # 标题
        title_label = ttk.Label(result_frame, text="NIHSS评估结果",
                               font=('Microsoft YaHei', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # 分数显示
        score_frame = ttk.Frame(result_frame)
        score_frame.pack(fill='x', pady=10)
        
        score_label = ttk.Label(score_frame,
                               text=f"总分：{total_score}/42分",
                               font=('Microsoft YaHei', 14, 'bold'))
        score_label.pack()
        
        severity_label = ttk.Label(score_frame,
                                  text=f"严重程度：{severity}",
                                  font=('Microsoft YaHei', 12))
        severity_label.pack(pady=5)
        
        # 解释说明
        interpretation_label = ttk.Label(result_frame,
                                        text=f"结果解释：{interpretation}",
                                        font=('Microsoft YaHei', 11))
        interpretation_label.pack(pady=10)
        
        # 详细说明
        detail_text = tk.Text(result_frame, height=8, wrap=tk.WORD,
                             font=('Microsoft YaHei', 10))
        detail_text.pack(fill='both', expand=True, pady=10)
        
        detail_content = f"""
NIHSS评分说明：

• 0分：无卒中症状
• 1-4分：轻微卒中，预后良好
• 5-15分：轻到中度卒中，可能需要住院治疗
• 16-20分：中到重度卒中，需要积极治疗
• 21-42分：重度卒中，预后较差

注意事项：
• NIHSS评分应结合临床表现综合判断
• 评分可用于监测病情变化
• 建议定期复评以观察治疗效果
        """
        
        detail_text.insert('1.0', detail_content)
        detail_text.config(state='disabled')
        
        # 按钮框架
        button_frame = ttk.Frame(result_frame)
        button_frame.pack(fill='x', pady=(10, 0))
        
        # 保存结果按钮
        save_btn = ttk.Button(button_frame, text="保存结果",
                             command=lambda: self.save_nihss_result(total_score, severity))
        save_btn.pack(side='left')
        
        # 关闭按钮
        close_btn = ttk.Button(button_frame, text="关闭",
                              command=result_window.destroy)
        close_btn.pack(side='right')
        
    def save_nihss_result(self, total_score, severity):
        """保存NIHSS评估结果"""
        try:
            # 创建结果数据
            result_data = {
                'scale_name': 'NIHSS',
                'scale_full_name': '美国国立卫生研究院卒中量表',
                'assessment_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_score': total_score,
                'max_score': 42,
                'severity': severity,
                'responses': self.current_responses
            }
            
            # 保存到文件
            import os
            results_dir = 'results'
            os.makedirs(results_dir, exist_ok=True)
            
            filename = f"NIHSS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join(results_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
            
            messagebox.showinfo("成功", f"评估结果已保存到：{filepath}")
            
        except Exception as e:
            messagebox.showerror("错误", f"保存结果时出错：{str(e)}")
            
    def reset_nihss(self):
        """重置NIHSS评估"""
        for var in self.nihss_vars.values():
            var.set(-1)
        self.current_responses = {}
        messagebox.showinfo("提示", "已重置所有选项")
        
    def show_gcs_assessment(self):
        """显示GCS评估界面"""
        self.current_scale = 'GCS'
        self.current_responses = {}
        
        # 清空父容器
        for widget in self.parent.winfo_children():
            widget.destroy()
            
        # 创建GCS评估界面
        self.create_gcs_interface()
        
    def create_gcs_interface(self):
        """创建GCS评估界面"""
        # 主标题
        title_frame = ttk.Frame(self.parent)
        title_frame.pack(fill='x', padx=20, pady=10)
        
        title_label = ttk.Label(title_frame, 
                               text="格拉斯哥昏迷量表 (GCS)",
                               font=('Microsoft YaHei', 16, 'bold'))
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame,
                                  text="Glasgow Coma Scale",
                                  font=('Microsoft YaHei', 10))
        subtitle_label.pack(pady=(0, 10))
        
        # 创建滚动框架
        canvas = tk.Canvas(self.parent)
        scrollbar = ttk.Scrollbar(self.parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 创建评估项目
        self.create_gcs_items(scrollable_frame)
        
        # 创建底部按钮
        self.create_gcs_bottom_buttons(scrollable_frame)
        
        # 布局滚动组件
        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=10)
        
        # 绑定鼠标滚轮
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
    def create_gcs_items(self, parent):
        """创建GCS评估项目"""
        self.gcs_vars = {}
        
        # GCS评估项目
        gcs_items = [
            {
                'id': 'eye',
                'title': '睁眼反应 (Eye Opening, E)',
                'options': [
                    (4, '自发睁眼'),
                    (3, '呼唤睁眼'),
                    (2, '刺激睁眼'),
                    (1, '无睁眼反应')
                ]
            },
            {
                'id': 'verbal',
                'title': '语言反应 (Verbal Response, V)',
                'options': [
                    (5, '定向正确'),
                    (4, '对话混乱'),
                    (3, '词语混乱'),
                    (2, '发音不清'),
                    (1, '无语言反应')
                ]
            },
            {
                'id': 'motor',
                'title': '运动反应 (Motor Response, M)',
                'options': [
                    (6, '遵嘱运动'),
                    (5, '定位疼痛'),
                    (4, '屈曲逃避'),
                    (3, '异常屈曲'),
                    (2, '异常伸展'),
                    (1, '无运动反应')
                ]
            }
        ]
        
        for item in gcs_items:
            # 创建项目框架
            item_frame = ttk.LabelFrame(parent, text=item['title'], padding=15)
            item_frame.pack(fill='x', padx=10, pady=10)
            
            # 创建选项变量
            var = tk.IntVar(value=-1)
            self.gcs_vars[item['id']] = var
            
            # 创建选项
            for score, text in item['options']:
                rb = ttk.Radiobutton(item_frame, text=f"{score}分 - {text}",
                                   variable=var, value=score)
                rb.pack(anchor='w', pady=3)
                
    def create_gcs_bottom_buttons(self, parent):
        """创建底部按钮"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', padx=10, pady=20)
        
        # 计算分数按钮
        calc_btn = ttk.Button(button_frame, text="计算分数",
                             command=self.calculate_gcs_score,
                             style='Accent.TButton')
        calc_btn.pack(side='left', padx=(0, 10))
        
        # 重置按钮
        reset_btn = ttk.Button(button_frame, text="重置",
                              command=self.reset_gcs)
        reset_btn.pack(side='left', padx=(0, 10))
        
        # 返回按钮
        back_btn = ttk.Button(button_frame, text="返回",
                             command=lambda: self.main_app.show_scale_category('severity'))
        back_btn.pack(side='right')
        
    def calculate_gcs_score(self):
        """计算GCS分数"""
        # 检查是否所有项目都已评分
        for item_id, var in self.gcs_vars.items():
            if var.get() == -1:
                messagebox.showwarning("警告", f"请完成所有评估项目的评分")
                return
        
        # 计算总分和各项分数
        eye_score = self.gcs_vars['eye'].get()
        verbal_score = self.gcs_vars['verbal'].get()
        motor_score = self.gcs_vars['motor'].get()
        total_score = eye_score + verbal_score + motor_score
        
        # 保存当前回答
        self.current_responses = {
            'eye': eye_score,
            'verbal': verbal_score,
            'motor': motor_score
        }
        
        # 显示结果
        self.show_gcs_interpretation(total_score, eye_score, verbal_score, motor_score)
        
    def show_gcs_interpretation(self, total_score, eye_score, verbal_score, motor_score):
        """显示GCS结果解释"""
        # 确定严重程度
        if total_score >= 13:
            severity = "轻度意识障碍"
            interpretation = "轻度脑损伤"
        elif 9 <= total_score <= 12:
            severity = "中度意识障碍"
            interpretation = "中度脑损伤"
        elif 3 <= total_score <= 8:
            severity = "重度意识障碍"
            interpretation = "重度脑损伤/昏迷"
        else:
            severity = "评分异常"
            interpretation = "请检查评分"
        
        # 创建结果窗口
        result_window = tk.Toplevel(self.parent)
        result_window.title("GCS评估结果")
        result_window.geometry("500x450")
        result_window.resizable(False, False)
        
        # 居中显示
        result_window.transient(self.main_app.root)
        result_window.grab_set()
        
        # 结果内容
        result_frame = ttk.Frame(result_window, padding=20)
        result_frame.pack(fill='both', expand=True)
        
        # 标题
        title_label = ttk.Label(result_frame, text="GCS评估结果",
                               font=('Microsoft YaHei', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # 分数显示
        score_frame = ttk.Frame(result_frame)
        score_frame.pack(fill='x', pady=10)
        
        # 各项分数
        scores_text = f"E{eye_score} + V{verbal_score} + M{motor_score} = {total_score}"
        score_label = ttk.Label(score_frame,
                               text=f"GCS评分：{scores_text}/15分",
                               font=('Microsoft YaHei', 14, 'bold'))
        score_label.pack()
        
        severity_label = ttk.Label(score_frame,
                                  text=f"严重程度：{severity}",
                                  font=('Microsoft YaHei', 12))
        severity_label.pack(pady=5)
        
        # 解释说明
        interpretation_label = ttk.Label(result_frame,
                                        text=f"结果解释：{interpretation}",
                                        font=('Microsoft YaHei', 11))
        interpretation_label.pack(pady=10)
        
        # 详细说明
        detail_text = tk.Text(result_frame, height=10, wrap=tk.WORD,
                             font=('Microsoft YaHei', 10))
        detail_text.pack(fill='both', expand=True, pady=10)
        
        detail_content = f"""
GCS评分说明：

评分组成：
• 睁眼反应(E)：{eye_score}/4分
• 语言反应(V)：{verbal_score}/5分
• 运动反应(M)：{motor_score}/6分

严重程度分级：
• 13-15分：轻度意识障碍/轻度脑损伤
• 9-12分：中度意识障碍/中度脑损伤
• 3-8分：重度意识障碍/重度脑损伤(昏迷)

临床意义：
• GCS≤8分：定义为昏迷状态
• GCS评分可用于评估脑损伤严重程度
• 连续监测有助于判断病情变化
• 评分应结合其他临床表现综合判断
        """
        
        detail_text.insert('1.0', detail_content)
        detail_text.config(state='disabled')
        
        # 按钮框架
        button_frame = ttk.Frame(result_frame)
        button_frame.pack(fill='x', pady=(10, 0))
        
        # 保存结果按钮
        save_btn = ttk.Button(button_frame, text="保存结果",
                             command=lambda: self.save_gcs_result(total_score, eye_score, verbal_score, motor_score, severity))
        save_btn.pack(side='left')
        
        # 关闭按钮
        close_btn = ttk.Button(button_frame, text="关闭",
                              command=result_window.destroy)
        close_btn.pack(side='right')
        
    def save_gcs_result(self, total_score, eye_score, verbal_score, motor_score, severity):
        """保存GCS评估结果"""
        try:
            # 创建结果数据
            result_data = {
                'scale_name': 'GCS',
                'scale_full_name': '格拉斯哥昏迷量表',
                'assessment_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_score': total_score,
                'max_score': 15,
                'eye_score': eye_score,
                'verbal_score': verbal_score,
                'motor_score': motor_score,
                'severity': severity,
                'responses': self.current_responses
            }
            
            # 保存到文件
            import os
            results_dir = 'results'
            os.makedirs(results_dir, exist_ok=True)
            
            filename = f"GCS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join(results_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
            
            messagebox.showinfo("成功", f"评估结果已保存到：{filepath}")
            
        except Exception as e:
            messagebox.showerror("错误", f"保存结果时出错：{str(e)}")
            
    def reset_gcs(self):
        """重置GCS评估"""
        for var in self.gcs_vars.values():
            var.set(-1)
        self.current_responses = {}
        messagebox.showinfo("提示", "已重置所有选项")
        
    def show_mrs_assessment(self):
        """显示mRS评估界面"""
        self.current_scale = 'mRS'
        self.current_responses = {}
        
        # 清空父容器
        for widget in self.parent.winfo_children():
            widget.destroy()
            
        # 创建mRS评估界面
        self.create_mrs_interface()
        
    def create_mrs_interface(self):
        """创建mRS评估界面"""
        # 主标题
        title_frame = ttk.Frame(self.parent)
        title_frame.pack(fill='x', padx=20, pady=10)
        
        title_label = ttk.Label(title_frame, 
                               text="改良Rankin量表 (mRS)",
                               font=('Microsoft YaHei', 16, 'bold'))
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame,
                                  text="Modified Rankin Scale",
                                  font=('Microsoft YaHei', 10))
        subtitle_label.pack(pady=(0, 10))
        
        # 创建滚动框架
        canvas = tk.Canvas(self.parent)
        scrollbar = ttk.Scrollbar(self.parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 创建评估项目
        self.create_mrs_items(scrollable_frame)
        
        # 创建底部按钮
        self.create_mrs_bottom_buttons(scrollable_frame)
        
        # 布局滚动组件
        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=10)
        
        # 绑定鼠标滚轮
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
    def create_mrs_items(self, parent):
        """创建mRS评估项目"""
        self.mrs_var = tk.IntVar(value=-1)
        
        # 创建项目框架
        item_frame = ttk.LabelFrame(parent, text="功能残疾程度评估", padding=15)
        item_frame.pack(fill='x', padx=10, pady=10)
        
        # mRS评估选项
        mrs_options = [
            (0, "无症状", "完全无症状"),
            (1, "无明显残疾", "尽管有症状，但能胜任所有日常活动和工作"),
            (2, "轻度残疾", "不能胜任病前所有活动，但能独立处理自己的事务"),
            (3, "中度残疾", "需要一定帮助，但能独立行走"),
            (4, "中重度残疾", "不能独立行走，日常生活需要帮助"),
            (5, "重度残疾", "卧床不起，大小便失禁，日常生活完全需要照料"),
            (6, "死亡", "患者死亡")
        ]
        
        # 创建选项
        for score, title, description in mrs_options:
            option_frame = ttk.Frame(item_frame)
            option_frame.pack(fill='x', pady=5)
            
            rb = ttk.Radiobutton(option_frame, text=f"{score}分 - {title}",
                               variable=self.mrs_var, value=score)
            rb.pack(anchor='w')
            
            desc_label = ttk.Label(option_frame, text=f"    {description}",
                                  font=('Microsoft YaHei', 9),
                                  foreground='gray')
            desc_label.pack(anchor='w', padx=(20, 0))
                
    def create_mrs_bottom_buttons(self, parent):
        """创建底部按钮"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', padx=10, pady=20)
        
        # 计算分数按钮
        calc_btn = ttk.Button(button_frame, text="计算分数",
                             command=self.calculate_mrs_score,
                             style='Accent.TButton')
        calc_btn.pack(side='left', padx=(0, 10))
        
        # 重置按钮
        reset_btn = ttk.Button(button_frame, text="重置",
                              command=self.reset_mrs)
        reset_btn.pack(side='left', padx=(0, 10))
        
        # 返回按钮
        back_btn = ttk.Button(button_frame, text="返回",
                             command=lambda: self.main_app.show_scale_category('severity'))
        back_btn.pack(side='right')
        
    def calculate_mrs_score(self):
        """计算mRS分数"""
        # 检查是否已选择
        if self.mrs_var.get() == -1:
            messagebox.showwarning("警告", "请选择患者的功能状态")
            return
        
        # 获取分数
        score = self.mrs_var.get()
        
        # 保存当前回答
        self.current_responses = {'mrs_score': score}
        
        # 显示结果
        self.show_mrs_interpretation(score)
        
    def show_mrs_interpretation(self, score):
        """显示mRS结果解释"""
        # 确定功能状态和预后
        score_descriptions = {
            0: ("无症状", "完全正常", "预后极佳"),
            1: ("无明显残疾", "轻微症状但功能完全", "预后良好"),
            2: ("轻度残疾", "轻度功能受限", "预后较好"),
            3: ("中度残疾", "中度功能受限", "预后一般"),
            4: ("中重度残疾", "重度功能受限", "预后较差"),
            5: ("重度残疾", "完全依赖他人", "预后差"),
            6: ("死亡", "患者死亡", "最差结局")
        }
        
        severity, functional_status, prognosis = score_descriptions.get(score, ("未知", "未知", "未知"))
        
        # 创建结果窗口
        result_window = tk.Toplevel(self.parent)
        result_window.title("mRS评估结果")
        result_window.geometry("500x400")
        result_window.resizable(False, False)
        
        # 居中显示
        result_window.transient(self.main_app.root)
        result_window.grab_set()
        
        # 结果内容
        result_frame = ttk.Frame(result_window, padding=20)
        result_frame.pack(fill='both', expand=True)
        
        # 标题
        title_label = ttk.Label(result_frame, text="mRS评估结果",
                               font=('Microsoft YaHei', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # 分数显示
        score_frame = ttk.Frame(result_frame)
        score_frame.pack(fill='x', pady=10)
        
        score_label = ttk.Label(score_frame,
                               text=f"mRS评分：{score}/6分",
                               font=('Microsoft YaHei', 14, 'bold'))
        score_label.pack()
        
        severity_label = ttk.Label(score_frame,
                                  text=f"功能状态：{severity}",
                                  font=('Microsoft YaHei', 12))
        severity_label.pack(pady=5)
        
        # 解释说明
        interpretation_label = ttk.Label(result_frame,
                                        text=f"功能描述：{functional_status}",
                                        font=('Microsoft YaHei', 11))
        interpretation_label.pack(pady=5)
        
        prognosis_label = ttk.Label(result_frame,
                                   text=f"预后评估：{prognosis}",
                                   font=('Microsoft YaHei', 11))
        prognosis_label.pack(pady=5)
        
        # 详细说明
        detail_text = tk.Text(result_frame, height=8, wrap=tk.WORD,
                             font=('Microsoft YaHei', 10))
        detail_text.pack(fill='both', expand=True, pady=10)
        
        detail_content = f"""
mRS评分说明：

评分标准：
• 0分：无症状
• 1分：无明显残疾，能胜任所有日常活动
• 2分：轻度残疾，不能胜任病前所有活动但能独立生活
• 3分：中度残疾，需要一定帮助但能独立行走
• 4分：中重度残疾，不能独立行走，日常生活需要帮助
• 5分：重度残疾，卧床不起，完全需要照料
• 6分：死亡

临床应用：
• 评估卒中患者功能预后
• 监测康复治疗效果
• 临床药物试验终点指标
• 0-2分通常认为预后良好
• 3-5分提示有不同程度的功能残疾
        """
        
        detail_text.insert('1.0', detail_content)
        detail_text.config(state='disabled')
        
        # 按钮框架
        button_frame = ttk.Frame(result_frame)
        button_frame.pack(fill='x', pady=(10, 0))
        
        # 保存结果按钮
        save_btn = ttk.Button(button_frame, text="保存结果",
                             command=lambda: self.save_mrs_result(score, severity, functional_status, prognosis))
        save_btn.pack(side='left')
        
        # 关闭按钮
        close_btn = ttk.Button(button_frame, text="关闭",
                              command=result_window.destroy)
        close_btn.pack(side='right')
        
    def save_mrs_result(self, score, severity, functional_status, prognosis):
        """保存mRS评估结果"""
        try:
            # 创建结果数据
            result_data = {
                'scale_name': 'mRS',
                'scale_full_name': '改良Rankin量表',
                'assessment_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'score': score,
                'max_score': 6,
                'severity': severity,
                'functional_status': functional_status,
                'prognosis': prognosis,
                'responses': self.current_responses
            }
            
            # 保存到文件
            import os
            results_dir = 'results'
            os.makedirs(results_dir, exist_ok=True)
            
            filename = f"mRS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join(results_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
            
            messagebox.showinfo("成功", f"评估结果已保存到：{filepath}")
            
        except Exception as e:
            messagebox.showerror("错误", f"保存结果时出错：{str(e)}")
            
    def reset_mrs(self):
        """重置mRS评估"""
        self.mrs_var.set(-1)
        self.current_responses = {}
        messagebox.showinfo("提示", "已重置选项")