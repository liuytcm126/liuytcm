#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情绪障碍评估量表模块
开发人员：LIUYING
包含：HAMD、HAMA、SDS等量表
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json

class EmotionScales:
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        self.current_scale = None
        self.current_responses = {}
        
    def show_hamd_assessment(self):
        """显示HAMD评估界面"""
        self.current_scale = 'HAMD'
        self.current_responses = {}
        
        # 清空父容器
        for widget in self.parent.winfo_children():
            widget.destroy()
            
        # 创建HAMD评估界面
        self.create_hamd_interface()
        
    def create_hamd_interface(self):
        """创建HAMD评估界面"""
        # 主容器
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 标题区域
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = ttk.Label(title_frame,
                               text="汉密尔顿抑郁量表 (HAMD-17)",
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
        
        # HAMD评估项目
        self.create_hamd_items(scrollable_frame)
        
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
        
        # 评估日期
        ttk.Label(info_grid, text="评估日期:").grid(row=1, column=0, sticky='w', padx=(0, 10), pady=(10, 0))
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        date_entry = ttk.Entry(info_grid, textvariable=self.date_var, width=12)
        date_entry.grid(row=1, column=1, sticky='w', padx=(0, 20), pady=(10, 0))
        
        # 评估者
        ttk.Label(info_grid, text="评估者:").grid(row=1, column=2, sticky='w', padx=(0, 10), pady=(10, 0))
        self.assessor_var = tk.StringVar()
        assessor_entry = ttk.Entry(info_grid, textvariable=self.assessor_var, width=15)
        assessor_entry.grid(row=1, column=3, sticky='w', padx=(0, 20), pady=(10, 0))
        
    def create_hamd_items(self, parent):
        """创建HAMD评估项目"""
        self.hamd_vars = {}
        
        # HAMD-17评估项目数据
        hamd_items = [
            {
                'name': '抑郁情绪',
                'description': '这项评估患者的抑郁心境，包括悲伤、绝望、无助、无价值感',
                'options': [
                    '0 = 无',
                    '1 = 仅在询问时才诉述这些感受',
                    '2 = 在谈话中自发地表达这些感受',
                    '3 = 不用言语交流也能观察到这些感受（如表情、姿势、声音、哭泣）',
                    '4 = 患者几乎只能表达这些感受'
                ]
            },
            {
                'name': '有罪感',
                'description': '评估患者的自责、内疚感和罪恶感',
                'options': [
                    '0 = 无',
                    '1 = 自责，认为自己让别人失望了',
                    '2 = 有罪恶观念或反复思考以往的错误或罪恶行为',
                    '3 = 现在的疾病是一种惩罚，有罪恶妄想',
                    '4 = 听到谴责或指责的声音，和/或有威胁性的视幻觉'
                ]
            },
            {
                'name': '自杀',
                'description': '评估患者的自杀观念和行为',
                'options': [
                    '0 = 无',
                    '1 = 觉得活着没有意思',
                    '2 = 希望自己死去或有任何自杀念头',
                    '3 = 自杀观念或姿态',
                    '4 = 自杀企图（任何严重的企图）'
                ]
            },
            {
                'name': '入睡困难',
                'description': '评估患者入睡的困难程度',
                'options': [
                    '0 = 无困难',
                    '1 = 偶尔有入睡困难（超过半小时）',
                    '2 = 每夜都有入睡困难'
                ]
            },
            {
                'name': '睡眠不深',
                'description': '评估患者夜间睡眠质量',
                'options': [
                    '0 = 无困难',
                    '1 = 睡眠不安、不深，整夜似睡非睡',
                    '2 = 夜间醒来，除了起床大小便外，任何夜间起床都算2分'
                ]
            },
            {
                'name': '早醒',
                'description': '评估患者早晨醒来的时间',
                'options': [
                    '0 = 无困难',
                    '1 = 比平时早醒1-2小时，但能重新入睡',
                    '2 = 比平时早醒2小时以上，不能重新入睡'
                ]
            },
            {
                'name': '工作和兴趣',
                'description': '评估患者对工作和活动的兴趣',
                'options': [
                    '0 = 无困难',
                    '1 = 对活动、工作或爱好的想法和感受表明有所下降',
                    '2 = 对活动、工作或爱好的兴趣实际下降，从患者的直接诉述或间接表现（如犹豫不决、踌躇）看出',
                    '3 = 花在活动上的时间减少或生产率下降',
                    '4 = 由于目前的疾病而停止工作'
                ]
            },
            {
                'name': '阻滞（思维和言语迟缓，注意力不集中，活动减少）',
                'description': '评估患者的精神运动性阻滞',
                'options': [
                    '0 = 言语、思维正常',
                    '1 = 在会谈中有轻微的迟缓',
                    '2 = 在会谈中有明显的迟缓',
                    '3 = 会谈困难',
                    '4 = 完全木僵'
                ]
            },
            {
                'name': '激越（不安）',
                'description': '评估患者的精神运动性激越',
                'options': [
                    '0 = 无',
                    '1 = 坐立不安',
                    '2 = 玩弄双手、头发等',
                    '3 = 不能静坐，走来走去',
                    '4 = 搓手、咬指甲、拉头发、咬嘴唇'
                ]
            },
            {
                'name': '精神性焦虑',
                'description': '评估患者的心理焦虑症状',
                'options': [
                    '0 = 无困难',
                    '1 = 主观的紧张和易激惹',
                    '2 = 为小事担心',
                    '3 = 担心的态度明显表现在面部或言谈中',
                    '4 = 患者不询问就自发地表达恐惧'
                ]
            },
            {
                'name': '躯体性焦虑',
                'description': '评估患者焦虑的躯体症状',
                'options': [
                    '0 = 无',
                    '1 = 轻微',
                    '2 = 中等',
                    '3 = 严重',
                    '4 = 极严重'
                ],
                'note': '躯体症状包括：胃肠道（口干、胀气、消化不良、腹泻、痉挛、嗳气）；心血管（心悸、头痛）；呼吸（过度换气、叹息）；尿频；出汗'
            },
            {
                'name': '胃肠道症状',
                'description': '评估患者的胃肠道症状',
                'options': [
                    '0 = 无',
                    '1 = 食欲下降，但无需他人鼓励进食，有沉重感',
                    '2 = 进食困难，需要他人催促进食'
                ]
            },
            {
                'name': '一般躯体症状',
                'description': '评估患者的一般躯体症状',
                'options': [
                    '0 = 无',
                    '1 = 四肢、背部或头部沉重感，背痛、头痛、肌肉痛，精力丧失、易疲劳',
                    '2 = 任何明确的症状'
                ]
            },
            {
                'name': '性症状',
                'description': '评估患者的性功能变化',
                'options': [
                    '0 = 无',
                    '1 = 轻微',
                    '2 = 严重'
                ],
                'note': '如性兴趣减退、月经紊乱等'
            },
            {
                'name': '疑病',
                'description': '评估患者的疑病症状',
                'options': [
                    '0 = 无',
                    '1 = 专注自身（身体）',
                    '2 = 关注健康',
                    '3 = 频繁地抱怨，要求帮助等',
                    '4 = 疑病妄想'
                ]
            },
            {
                'name': '体重减轻',
                'description': '评估患者的体重变化',
                'options': [
                    '0 = 无体重减轻',
                    '1 = 可能有体重减轻',
                    '2 = 明确的体重减轻（据患者说）'
                ]
            },
            {
                'name': '自知力',
                'description': '评估患者对疾病的认识',
                'options': [
                    '0 = 承认自己有病，需要治疗',
                    '1 = 承认自己有病，但归咎于食物、气候、工作过度、病毒感染、需要休息等',
                    '2 = 否认自己有病'
                ]
            }
        ]
        
        for i, item_data in enumerate(hamd_items):
            # 创建项目框架
            item_frame = ttk.LabelFrame(parent, 
                                      text=f"{i+1}. {item_data['name']}",
                                      padding=15)
            item_frame.pack(fill='x', pady=10)
            
            # 项目描述
            desc_label = ttk.Label(item_frame,
                                 text=item_data['description'],
                                 font=('Microsoft YaHei', 10),
                                 foreground='#6C757D',
                                 wraplength=800)
            desc_label.pack(anchor='w', pady=(0, 10))
            
            # 如果有注释，显示注释
            if 'note' in item_data:
                note_label = ttk.Label(item_frame,
                                     text=f"注：{item_data['note']}",
                                     font=('Microsoft YaHei', 9),
                                     foreground='#FD7E14',
                                     wraplength=800)
                note_label.pack(anchor='w', pady=(0, 10))
            
            # 评分选项
            self.hamd_vars[i] = tk.IntVar()
            
            options_frame = ttk.Frame(item_frame)
            options_frame.pack(fill='x')
            
            for j, option in enumerate(item_data['options']):
                rb = ttk.Radiobutton(options_frame,
                                   text=option,
                                   variable=self.hamd_vars[i],
                                   value=j)
                rb.pack(anchor='w', pady=2)
                
    def create_bottom_buttons(self, parent):
        """创建底部按钮"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', pady=(20, 0))
        
        # 计算总分按钮
        calc_btn = ttk.Button(button_frame,
                             text="计算总分",
                             command=self.calculate_hamd_score)
        calc_btn.pack(side='left', padx=(0, 10))
        
        # 保存结果按钮
        save_btn = ttk.Button(button_frame,
                             text="保存结果",
                             command=self.save_hamd_result)
        save_btn.pack(side='left', padx=(0, 10))
        
        # 重置按钮
        reset_btn = ttk.Button(button_frame,
                              text="重置",
                              command=self.reset_hamd)
        reset_btn.pack(side='left')
        
        # 总分显示
        self.score_label = ttk.Label(button_frame,
                                    text=f"总分：{total_score} / 52",
                                    font=('Microsoft YaHei', 14, 'bold'),
                                    foreground='#2E86AB')
        self.score_label.pack(side='right')
        
    def calculate_hamd_score(self):
        """计算HAMD总分"""
        total_score = sum(var.get() for var in self.hamd_vars.values())
        
        # 更新显示
        self.score_label.config(text=f"总分：{total_score} / 52")
        
        # 显示解释
        self.show_hamd_interpretation(total_score)
        
        return total_score
        
    def show_hamd_interpretation(self, score):
        """显示HAMD评分解释"""
        if score <= 7:
            interpretation = "正常"
            color = "#28A745"  # 绿色
            detail = "无抑郁症状或症状极轻微"
        elif score <= 17:
            interpretation = "轻度抑郁"
            color = "#FFC107"  # 黄色
            detail = "可能存在轻度抑郁症状，建议进一步评估"
        elif score <= 23:
            interpretation = "中度抑郁"
            color = "#FD7E14"  # 橙色
            detail = "存在中度抑郁症状，建议专业治疗"
        else:
            interpretation = "重度抑郁"
            color = "#DC3545"  # 红色
            detail = "存在重度抑郁症状，需要立即专业干预"
            
        # 创建解释窗口
        interpretation_window = tk.Toplevel(self.parent)
        interpretation_window.title("HAMD评分解释")
        interpretation_window.geometry("450x350")
        interpretation_window.resizable(False, False)
        
        # 居中显示
        interpretation_window.transient(self.parent)
        interpretation_window.grab_set()
        
        main_frame = ttk.Frame(interpretation_window, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # 分数显示
        score_label = ttk.Label(main_frame,
                               text=f"HAMD总分：{score} / 52",
                               font=('Microsoft YaHei', 16, 'bold'))
        score_label.pack(pady=(0, 15))
        
        # 解释显示
        interp_label = ttk.Label(main_frame,
                                text=interpretation,
                                font=('Microsoft YaHei', 14, 'bold'),
                                foreground=color)
        interp_label.pack(pady=(0, 10))
        
        # 详细说明
        detail_label = ttk.Label(main_frame,
                                text=detail,
                                font=('Microsoft YaHei', 11),
                                wraplength=400)
        detail_label.pack(pady=(0, 20))
        
        # 评分标准
        standard_text = """
评分标准：
• ≤7分：正常
• 8-17分：轻度抑郁
• 18-23分：中度抑郁
• ≥24分：重度抑郁

注意事项：
• 本量表需由专业人员评估
• 评分应结合临床观察
• 如有自杀风险请立即处理
        """
        
        standard_label = ttk.Label(main_frame,
                                  text=standard_text,
                                  font=('Microsoft YaHei', 10),
                                  justify='left')
        standard_label.pack(pady=(0, 20))
        
        # 关闭按钮
        close_btn = ttk.Button(main_frame,
                              text="关闭",
                              command=interpretation_window.destroy)
        close_btn.pack()
        
    def save_hamd_result(self):
        """保存HAMD评估结果"""
        # 检查患者信息
        if not self.name_var.get().strip():
            messagebox.showerror("错误", "请输入患者姓名")
            return
            
        # 计算总分
        total_score = self.calculate_hamd_score()
        
        # 准备保存数据
        result_data = {
            'scale_type': 'HAMD-17',
            'patient_info': {
                'name': self.name_var.get(),
                'age': self.age_var.get(),
                'gender': self.gender_var.get(),
                'assessment_date': self.date_var.get(),
                'assessor': self.assessor_var.get()
            },
            'scores': {str(i): var.get() for i, var in self.hamd_vars.items()},
            'total_score': total_score,
            'max_score': 52,
            'timestamp': datetime.now().isoformat()
        }
        
        # 保存到文件
        try:
            import os
            if not os.path.exists('results'):
                os.makedirs('results')
                
            filename = f"results/HAMD_{self.name_var.get()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
                
            messagebox.showinfo("成功", f"评估结果已保存到：{filename}")
            
        except Exception as e:
            messagebox.showerror("错误", f"保存失败：{str(e)}")
            
    def reset_hamd(self):
        """重置HAMD评估"""
        if messagebox.askyesno("确认", "确定要重置所有评估内容吗？"):
            for var in self.hamd_vars.values():
                var.set(0)
            self.score_label.config(text="总分：-- / 52")
            
    def show_hama_assessment(self):
        """显示HAMA评估界面"""
        self.current_scale = 'HAMA'
        self.current_responses = {}
        
        # 清空父容器
        for widget in self.parent.winfo_children():
            widget.destroy()
            
        # 创建HAMA评估界面
        self.create_hama_interface()
        
    def create_hama_interface(self):
        """创建HAMA评估界面"""
        # 主容器
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 标题区域
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = ttk.Label(title_frame,
                               text="汉密尔顿焦虑量表 (HAMA)",
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
        
        # HAMA评估项目
        self.create_hama_items(scrollable_frame)
        
        # 底部按钮区域
        self.create_hama_bottom_buttons(main_frame)
        
    def create_hama_items(self, parent):
        """创建HAMA评估项目"""
        self.hama_vars = {}
        
        # HAMA评估项目数据
        hama_items = [
            {
                'name': '焦虑心境',
                'description': '担心、担忧、感到有最坏的事将要发生、易激惹'
            },
            {
                'name': '紧张',
                'description': '紧张感、易疲劳、不能放松、情绪反应、易哭、颤抖、坐立不安'
            },
            {
                'name': '害怕',
                'description': '害怕黑暗、陌生人、一个人留下、动物、交通、人群'
            },
            {
                'name': '失眠',
                'description': '难以入睡、断断续续的睡眠、不能熟睡、疲劳、醒后不适、恶梦、夜惊'
            },
            {
                'name': '认知症状',
                'description': '注意力不集中、记忆力差'
            },
            {
                'name': '抑郁心境',
                'description': '丧失兴趣、对以往爱好缺乏快感、抑郁、早醒、昼重夜轻'
            },
            {
                'name': '肌肉系统症状',
                'description': '肌肉疼痛、肌肉僵硬、肌肉抽动、齿颤、声音发抖'
            },
            {
                'name': '感觉系统症状',
                'description': '耳鸣、视物模糊、潮热和寒战、软弱感、刺痛感'
            },
            {
                'name': '心血管系统症状',
                'description': '心动过速、心悸、胸痛、血管跳动、昏厥感、心跳停顿感'
            },
            {
                'name': '呼吸系统症状',
                'description': '胸部压迫感、窒息感、叹气、呼吸短促'
            },
            {
                'name': '胃肠道症状',
                'description': '吞咽困难、腹胀、腹痛、胃灼热感、腹部胀满感、恶心、呕吐、便秘、腹泻、肠鸣'
            },
            {
                'name': '泌尿生殖系统症状',
                'description': '尿频、尿急、闭经、月经紊乱、性欲缺乏、阳痿'
            },
            {
                'name': '植物神经症状',
                'description': '口干、潮红、苍白、易出汗、眩晕、紧张性头痛、毛发竖起'
            },
            {
                'name': '会谈时行为表现',
                'description': '坐立不安、””或震颤、愁眉苦脸、面部肌肉抽动、吞咽、嗳气、心率快、呼吸急促、出汗、眨眼'
            }
        ]
        
        # 评分选项
        score_options = [
            '0 = 无症状',
            '1 = 轻度：症状轻，持续时间短',
            '2 = 中度：症状中等',
            '3 = 重度：症状重，持续时间长',
            '4 = 极重度：症状极重，持续存在'
        ]
        
        for i, item_data in enumerate(hama_items):
            # 创建项目框架
            item_frame = ttk.LabelFrame(parent, 
                                      text=f"{i+1}. {item_data['name']}",
                                      padding=15)
            item_frame.pack(fill='x', pady=10)
            
            # 项目描述
            desc_label = ttk.Label(item_frame,
                                 text=item_data['description'],
                                 font=('Microsoft YaHei', 10),
                                 foreground='#6C757D',
                                 wraplength=800)
            desc_label.pack(anchor='w', pady=(0, 10))
            
            # 评分选项
            self.hama_vars[i] = tk.IntVar()
            
            options_frame = ttk.Frame(item_frame)
            options_frame.pack(fill='x')
            
            for j, option in enumerate(score_options):
                rb = ttk.Radiobutton(options_frame,
                                   text=option,
                                   variable=self.hama_vars[i],
                                   value=j)
                rb.pack(anchor='w', pady=2)
                
    def create_hama_bottom_buttons(self, parent):
        """创建HAMA底部按钮"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', pady=(20, 0))
        
        # 计算总分按钮
        calc_btn = ttk.Button(button_frame,
                             text="计算总分",
                             command=self.calculate_hama_score)
        calc_btn.pack(side='left', padx=(0, 10))
        
        # 保存结果按钮
        save_btn = ttk.Button(button_frame,
                             text="保存结果",
                             command=self.save_hama_result)
        save_btn.pack(side='left', padx=(0, 10))
        
        # 重置按钮
        reset_btn = ttk.Button(button_frame,
                              text="重置",
                              command=self.reset_hama)
        reset_btn.pack(side='left')
        
        # 总分显示
        self.hama_score_label = ttk.Label(button_frame,
                                         text="总分：-- / 56",
                                         font=('Microsoft YaHei', 14, 'bold'),
                                         foreground='#2E86AB')
        self.hama_score_label.pack(side='right')
        
    def calculate_hama_score(self):
        """计算HAMA总分"""
        total_score = sum(var.get() for var in self.hama_vars.values())
        
        # 更新显示
        self.hama_score_label.config(text=f"总分：{total_score} / 56")
        
        # 显示解释
        self.show_hama_interpretation(total_score)
        
        return total_score
        
    def show_hama_interpretation(self, score):
        """显示HAMA评分解释"""
        if score <= 6:
            interpretation = "无焦虑"
            color = "#28A745"  # 绿色
            detail = "无明显焦虑症状"
        elif score <= 14:
            interpretation = "轻度焦虑"
            color = "#FFC107"  # 黄色
            detail = "可能存在轻度焦虑症状"
        elif score <= 20:
            interpretation = "中度焦虑"
            color = "#FD7E14"  # 橙色
            detail = "存在中度焦虑症状，建议专业评估"
        else:
            interpretation = "重度焦虑"
            color = "#DC3545"  # 红色
            detail = "存在重度焦虑症状，需要专业治疗"
            
        # 创建解释窗口
        interpretation_window = tk.Toplevel(self.parent)
        interpretation_window.title("HAMA评分解释")
        interpretation_window.geometry("400x300")
        interpretation_window.resizable(False, False)
        
        # 居中显示
        interpretation_window.transient(self.parent)
        interpretation_window.grab_set()
        
        main_frame = ttk.Frame(interpretation_window, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # 分数显示
        score_label = ttk.Label(main_frame,
                               text=f"HAMA总分：{score} / 56",
                               font=('Microsoft YaHei', 16, 'bold'))
        score_label.pack(pady=(0, 15))
        
        # 解释显示
        interp_label = ttk.Label(main_frame,
                                text=interpretation,
                                font=('Microsoft YaHei', 14, 'bold'),
                                foreground=color)
        interp_label.pack(pady=(0, 10))
        
        # 详细说明
        detail_label = ttk.Label(main_frame,
                                text=detail,
                                font=('Microsoft YaHei', 11))
        detail_label.pack(pady=(0, 20))
        
        # 评分标准
        standard_text = """
评分标准：
• ≤6分：无焦虑
• 7-14分：轻度焦虑
• 15-20分：中度焦虑
• ≥21分：重度焦虑

注意：
• 需由专业人员评估
• 结合临床表现综合判断
        """
        
        standard_label = ttk.Label(main_frame,
                                  text=standard_text,
                                  font=('Microsoft YaHei', 10),
                                  justify='left')
        standard_label.pack(pady=(0, 20))
        
        # 关闭按钮
        close_btn = ttk.Button(main_frame,
                              text="关闭",
                              command=interpretation_window.destroy)
        close_btn.pack()
        
    def save_hama_result(self):
        """保存HAMA评估结果"""
        # 检查患者信息
        if not self.name_var.get().strip():
            messagebox.showerror("错误", "请输入患者姓名")
            return
            
        # 计算总分
        total_score = self.calculate_hama_score()
        
        # 准备保存数据
        result_data = {
            'scale_type': 'HAMA',
            'patient_info': {
                'name': self.name_var.get(),
                'age': self.age_var.get(),
                'gender': self.gender_var.get(),
                'assessment_date': self.date_var.get(),
                'assessor': self.assessor_var.get()
            },
            'scores': {str(i): var.get() for i, var in self.hama_vars.items()},
            'total_score': total_score,
            'max_score': 56,
            'timestamp': datetime.now().isoformat()
        }
        
        # 保存到文件
        try:
            import os
            if not os.path.exists('results'):
                os.makedirs('results')
                
            filename = f"results/HAMA_{self.name_var.get()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
                
            messagebox.showinfo("成功", f"评估结果已保存到：{filename}")
            
        except Exception as e:
            messagebox.showerror("错误", f"保存失败：{str(e)}")
            
    def reset_hama(self):
        """重置HAMA评估"""
        if messagebox.askyesno("确认", "确定要重置所有评估内容吗？"):
            for var in self.hama_vars.values():
                var.set(0)
            self.hama_score_label.config(text="总分：-- / 56")
            
    def show_sds_assessment(self):
        """显示SDS评估界面"""
        messagebox.showinfo("提示", "SDS量表评估功能正在开发中...")
        
    def back_to_category(self):
        """返回分类页面"""
        self.main_app.show_scale_category('emotion')