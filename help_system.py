#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
神经内科量表评估系统 - 帮助文档模块
开发人员：LIUYING
版本：1.0.0
描述：提供详细的使用说明和量表介绍
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import webbrowser
from pathlib import Path

class HelpSystem:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.setup_styles()
        
    def setup_styles(self):
        """设置样式"""
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'success': '#F18F01',
            'background': '#F8F9FA',
            'text_primary': '#2C3E50',
            'text_secondary': '#6C757D',
            'border': '#DEE2E6'
        }
        
    def show_user_manual(self):
        """显示用户手册"""
        # 清空父框架
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
            
        # 创建主容器
        main_frame = ttk.Frame(self.parent_frame)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 标题
        title_label = ttk.Label(main_frame, 
                               text="神经内科量表评估系统 - 用户手册",
                               font=('Microsoft YaHei', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # 创建笔记本控件
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)
        
        # 系统概述
        self.create_overview_tab(notebook)
        
        # 快速入门
        self.create_quickstart_tab(notebook)
        
        # 量表介绍
        self.create_scales_tab(notebook)
        
        # 操作指南
        self.create_operation_tab(notebook)
        
        # 常见问题
        self.create_faq_tab(notebook)
        
    def create_overview_tab(self, notebook):
        """创建系统概述标签页"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="系统概述")
        
        # 创建滚动文本框
        text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, 
                                               font=('Microsoft YaHei', 10))
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        
        overview_content = """
神经内科量表评估系统
开发人员：LIUYING
版本：1.0.0

系统简介：
本系统是专为神经内科医师设计的专业量表评估工具，提供标准化、自动化的神经内科常用量表评估功能。

主要特点：
• 专业性：基于国际标准神经内科量表设计
• 自动化：智能评分计算和结果分析
• 标准化：统一的评估流程和评分标准
• 便捷性：直观的用户界面和操作流程
• 可靠性：数据安全存储和备份机制

适用范围：
• 神经内科门诊和住院患者评估
• 临床研究数据收集
• 医学教育和培训
• 疾病进展监测

技术规格：
• 开发语言：Python 3.8+
• 界面框架：Tkinter
• 数据存储：JSON格式
• 支持系统：Windows 10/11, macOS, Linux

安全性：
• 本地数据存储，保护患者隐私
• 数据加密存储
• 访问权限控制
• 操作日志记录
"""
        
        text_widget.insert('1.0', overview_content)
        text_widget.config(state='disabled')
        
    def create_quickstart_tab(self, notebook):
        """创建快速入门标签页"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="快速入门")
        
        text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, 
                                               font=('Microsoft YaHei', 10))
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        
        quickstart_content = """
快速入门指南

第一步：启动系统
1. 双击桌面图标启动程序
2. 等待系统加载完成
3. 查看主界面欢迎信息

第二步：选择量表
1. 在左侧导航栏选择量表分类：
   • 认知功能评估：MMSE、MoCA等
   • 情绪障碍评估：HAMD、HAMA等
   • 运动功能评估：UPDRS等
2. 点击具体量表卡片
3. 查看量表详细信息

第三步：开始评估
1. 点击"开始评估"按钮
2. 填写患者基本信息：
   • 姓名（必填）
   • 年龄（必填）
   • 性别（必填）
   • 教育程度
   • 病史信息
3. 按照量表项目逐项评分
4. 系统自动计算总分

第四步：查看结果
1. 评估完成后查看评分结果
2. 阅读智能分析报告
3. 查看个性化建议
4. 保存评估记录

第五步：数据管理
1. 在"数据管理"区域查看历史记录
2. 进行统计分析
3. 导出评估报告
4. 生成可视化图表

注意事项：
• 确保网络连接稳定（用于数据同步）
• 定期备份重要数据
• 遵循医疗数据保护规定
• 如遇问题请查看常见问题解答
"""
        
        text_widget.insert('1.0', quickstart_content)
        text_widget.config(state='disabled')
        
    def create_scales_tab(self, notebook):
        """创建量表介绍标签页"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="量表介绍")
        
        # 创建量表分类笔记本
        scales_notebook = ttk.Notebook(frame)
        scales_notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 认知功能量表
        self.create_cognitive_scales_info(scales_notebook)
        
        # 情绪障碍量表
        self.create_emotion_scales_info(scales_notebook)
        
        # 运动功能量表
        self.create_motor_scales_info(scales_notebook)
        
    def create_cognitive_scales_info(self, notebook):
        """创建认知功能量表信息"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="认知功能量表")
        
        text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, 
                                               font=('Microsoft YaHei', 10))
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        
        cognitive_content = """
认知功能评估量表

1. MMSE（简易精神状态检查）

量表简介：
MMSE是最广泛使用的认知功能筛查工具，由Folstein等于1975年开发。

评估内容：
• 定向力（时间、地点）- 10分
• 注意力和计算力 - 5分
• 记忆力（即刻回忆、延迟回忆）- 6分
• 语言能力（命名、复述、理解、书写）- 8分
• 视空间能力（图形复制）- 1分

评分标准：
• 总分：30分
• 正常：≥24分
• 轻度认知障碍：18-23分
• 中度认知障碍：12-17分
• 重度认知障碍：<12分

适用人群：
• 疑似痴呆患者
• 认知功能下降患者
• 老年人认知筛查
• 神经系统疾病患者

注意事项：
• 需考虑教育程度影响
• 语言和文化背景
• 视听功能状态
• 情绪状态影响

2. MoCA（蒙特利尔认知评估）

量表简介：
MoCA由Nasreddine于2005年开发，对轻度认知障碍更敏感。

评估内容：
• 视空间/执行功能 - 5分
• 命名 - 3分
• 注意力 - 6分
• 语言 - 3分
• 抽象思维 - 2分
• 延迟回忆 - 5分
• 定向力 - 6分

评分标准：
• 总分：30分
• 正常：≥26分
• 轻度认知障碍：<26分
• 教育程度<12年者加1分

3. CDR（临床痴呆评定量表）

量表简介：
CDR评估痴呆严重程度，包括认知和功能两个方面。

评估领域：
• 记忆
• 定向力
• 判断和解决问题
• 社区事务
• 家庭和爱好
• 个人照料

评分等级：
• CDR 0：正常
• CDR 0.5：可疑痴呆
• CDR 1：轻度痴呆
• CDR 2：中度痴呆
• CDR 3：重度痴呆
"""
        
        text_widget.insert('1.0', cognitive_content)
        text_widget.config(state='disabled')
        
    def create_emotion_scales_info(self, notebook):
        """创建情绪障碍量表信息"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="情绪障碍量表")
        
        text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, 
                                               font=('Microsoft YaHei', 10))
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        
        emotion_content = """
情绪障碍评估量表

1. HAMD-17（汉密尔顿抑郁量表17项版）

量表简介：
HAMD是评估抑郁症状严重程度的金标准，由Hamilton于1960年开发。

评估内容：
• 核心症状：抑郁情绪、罪恶感、自杀观念
• 认知症状：工作和兴趣、迟缓、激越
• 躯体症状：躯体性焦虑、胃肠道症状、全身症状
• 睡眠症状：入睡困难、睡眠不深、早醒
• 其他症状：性症状、疑病、体重减轻、自知力

评分方法：
• 0-2分：无症状到轻度
• 3-4分：中度到重度
• 部分项目0-4分评分

严重程度分级：
• 正常：≤7分
• 可能抑郁：8-16分
• 肯定抑郁：17-23分
• 严重抑郁：≥24分

适用范围：
• 抑郁症诊断辅助
• 治疗效果评估
• 病情严重程度判断
• 临床研究

2. HAMA（汉密尔顿焦虑量表）

量表简介：
HAMA用于评估焦虑症状的严重程度，包括精神性和躯体性焦虑。

评估内容：
精神性焦虑：
• 焦虑心境
• 紧张
• 害怕
• 失眠
• 认知功能
• 抑郁心境
• 行为表现

躯体性焦虑：
• 肌肉系统症状
• 感觉系统症状
• 心血管系统症状
• 呼吸系统症状
• 胃肠道症状
• 泌尿生殖系统症状
• 自主神经系统症状

评分标准：
• 总分：56分
• 无焦虑：<7分
• 可能焦虑：7-13分
• 肯定焦虑：14-20分
• 严重焦虑：21-28分
• 极严重焦虑：>29分

3. SDS（抑郁自评量表）

量表简介：
SDS是Zung于1965年编制的自评量表，适用于抑郁症状筛查。

特点：
• 自评形式，操作简便
• 20个项目，涵盖抑郁症状
• 4级评分，从无到持续存在
• 标准分换算，便于比较

评分解释：
• 标准分<50：正常
• 标准分50-59：轻度抑郁
• 标准分60-69：中度抑郁
• 标准分≥70：重度抑郁
"""
        
        text_widget.insert('1.0', emotion_content)
        text_widget.config(state='disabled')
        
    def create_motor_scales_info(self, notebook):
        """创建运动功能量表信息"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="运动功能量表")
        
        text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, 
                                               font=('Microsoft YaHei', 10))
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        
        motor_content = """
运动功能评估量表

1. UPDRS-III（统一帕金森病评定量表-运动部分）

量表简介：
UPDRS是评估帕金森病最重要的量表，第III部分专门评估运动症状。

评估内容：
• 言语 - 评估语音清晰度和音量
• 面部表情 - 评估面具脸
• 静止性震颤 - 评估四肢和下颌震颤
• 动作性或姿势性震颤 - 评估手部震颤
• 僵直 - 评估颈部和四肢僵直
• 手指敲击 - 评估精细运动
• 手部运动 - 评估手部灵活性
• 手部快速交替运动 - 评估协调性
• 足趾敲击 - 评估下肢运动
• 腿部敏捷性 - 评估腿部运动
• 起立 - 评估从坐位起立
• 姿势 - 评估站立姿势
• 步态 - 评估行走模式
• 姿势稳定性 - 评估平衡能力
• 整体运动迟缓 - 综合评估

评分方法：
• 0分：正常
• 1分：轻微异常
• 2分：轻度异常
• 3分：中度异常
• 4分：重度异常

总分解释：
• 0-30分：轻度运动障碍
• 31-58分：中度运动障碍
• 59-108分：重度运动障碍

临床意义：
• 帕金森病诊断辅助
• 病情严重程度评估
• 治疗效果监测
• 疾病进展评估

2. Berg平衡量表

量表简介：
Berg平衡量表评估老年人和神经系统疾病患者的平衡功能。

评估项目：
• 坐到站
• 独立站立
• 独立坐
• 站到坐
• 转移
• 闭眼站立
• 双足并拢站立
• 前伸取物
• 拾地面物品
• 转身向后看
• 转身360度
• 交替踏台阶
• 单足站立
• 串联步行

评分标准：
• 每项0-4分
• 总分56分
• ≥45分：低跌倒风险
• 21-40分：中等跌倒风险
• ≤20分：高跌倒风险

3. Tinetti步态与平衡评估

量表简介：
Tinetti量表评估老年人步态和平衡功能，预测跌倒风险。

平衡评估（16分）：
• 坐位平衡
• 起立
• 站立平衡
• 轻推试验
• 闭眼站立
• 转身
• 坐下

步态评估（12分）：
• 步态启动
• 步长
• 步高
• 步态对称性
• 步态连续性
• 路径偏移
• 躯干稳定性
• 步态姿态

风险评估：
• 总分28分
• ≥24分：低跌倒风险
• 19-23分：中等跌倒风险
• ≤18分：高跌倒风险
"""
        
        text_widget.insert('1.0', motor_content)
        text_widget.config(state='disabled')
        
    def create_operation_tab(self, notebook):
        """创建操作指南标签页"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="操作指南")
        
        text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, 
                                               font=('Microsoft YaHei', 10))
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        
        operation_content = """
详细操作指南

一、系统启动和设置

1. 首次启动
• 确保系统要求：Python 3.8+
• 检查依赖包安装
• 创建数据目录
• 初始化配置文件

2. 界面布局
• 顶部：系统标题和开发者信息
• 左侧：功能导航栏
• 右侧：主要内容区域
• 底部：状态栏和帮助信息

二、量表评估操作

1. 选择量表
• 点击左侧导航栏中的量表分类
• 浏览可用量表列表
• 查看量表详细信息
• 点击"开始评估"按钮

2. 患者信息录入
• 姓名：必填项，用于识别患者
• 年龄：必填项，影响评分解释
• 性别：必填项，某些量表有性别差异
• 教育程度：影响认知量表评分
• 病史：提供临床背景信息
• 评估日期：自动填入当前日期

3. 量表评分
• 按照量表项目顺序逐项评分
• 仔细阅读评分标准
• 根据患者实际情况选择分数
• 可随时修改已评分项目
• 系统自动计算总分

4. 结果查看
• 查看总分和各维度得分
• 阅读智能分析报告
• 了解评分意义和建议
• 保存评估记录

三、数据管理操作

1. 查看评估记录
• 点击"查看评估记录"按钮
• 使用筛选功能查找特定记录
• 按日期、患者、量表类型筛选
• 查看详细评估信息

2. 统计分析
• 生成总体统计报告
• 查看患者评估历史
• 分析量表使用情况
• 生成可视化图表

3. 数据导出
• 选择导出格式：Excel、CSV、PDF
• 选择导出内容：单个记录或批量
• 设置导出参数
• 保存到指定位置

四、高级功能

1. 数据备份
• 定期备份评估数据
• 设置自动备份计划
• 验证备份完整性
• 恢复备份数据

2. 系统设置
• 修改界面主题
• 调整字体大小
• 设置数据存储路径
• 配置导出选项

3. 用户管理
• 创建用户账户
• 设置访问权限
• 记录操作日志
• 管理用户信息

五、质量控制

1. 数据验证
• 检查必填项完整性
• 验证数据合理性
• 标记异常值
• 提供修正建议

2. 评分一致性
• 提供评分指导
• 标准化评分流程
• 记录评分者信息
• 支持多评分者比较

3. 结果审核
• 自动检查评分逻辑
• 标记可疑结果
• 提供复核机制
• 生成质控报告

六、故障排除

1. 常见问题
• 程序无法启动：检查Python环境
• 数据无法保存：检查文件权限
• 界面显示异常：调整分辨率设置
• 导出失败：检查目标路径

2. 错误处理
• 查看错误日志
• 联系技术支持
• 提交错误报告
• 获取解决方案

3. 性能优化
• 清理临时文件
• 压缩历史数据
• 优化数据库
• 更新系统版本
"""
        
        text_widget.insert('1.0', operation_content)
        text_widget.config(state='disabled')
        
    def create_faq_tab(self, notebook):
        """创建常见问题标签页"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="常见问题")
        
        text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, 
                                               font=('Microsoft YaHei', 10))
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        
        faq_content = """
常见问题解答

Q1: 系统支持哪些操作系统？
A1: 系统支持Windows 10/11、macOS 10.14+和主流Linux发行版。需要Python 3.8或更高版本。

Q2: 如何确保患者数据安全？
A2: 系统采用本地存储，数据不会上传到云端。所有数据文件都进行加密存储，并支持访问权限控制。

Q3: 可以同时评估多个患者吗？
A3: 系统支持多患者管理，可以保存多个患者的评估记录，并提供快速切换功能。

Q4: 评分结果的准确性如何保证？
A4: 系统基于国际标准量表开发，评分算法经过严格验证。建议结合临床判断使用评估结果。

Q5: 如何导出评估报告？
A5: 在数据管理模块中选择"数据导出"，可以导出Excel、PDF等格式的详细报告。

Q6: 系统出现故障怎么办？
A6: 首先查看帮助文档中的故障排除部分。如问题仍未解决，请联系技术支持。

Q7: 可以自定义量表吗？
A7: 当前版本提供标准量表。如需自定义量表，请联系开发团队讨论定制方案。

Q8: 如何备份和恢复数据？
A8: 在系统设置中可以设置自动备份。手动备份请复制data目录下的所有文件。

Q9: 系统是否需要网络连接？
A9: 系统可以完全离线使用。网络连接仅用于软件更新和在线帮助。

Q10: 如何获得技术支持？
A10: 请通过以下方式联系：
• 邮箱：support@neuroscales.com
• 电话：400-123-4567
• 在线文档：www.neuroscales.com/docs

Q11: 量表评分标准是否可以调整？
A11: 系统使用国际标准评分标准，不建议随意修改。如有特殊需求，请咨询专业人员。

Q12: 如何处理评估中断的情况？
A12: 系统支持评估过程保存，可以随时暂停并在稍后继续完成评估。

Q13: 多个医生可以共享数据吗？
A13: 系统支持多用户模式，可以设置不同的访问权限，实现数据共享和协作。

Q14: 如何确保评分的一致性？
A14: 系统提供详细的评分指导和标准化流程，建议定期进行评分者培训。

Q15: 系统更新会影响现有数据吗？
A15: 系统更新前会自动备份数据，更新过程不会影响现有评估记录。

技术支持信息：
开发人员：LIUYING
版本：1.0.0
最后更新：2024年

如有其他问题，请查阅在线文档或联系技术支持团队。
"""
        
        text_widget.insert('1.0', faq_content)
        text_widget.config(state='disabled')
        
    def show_about(self):
        """显示关于信息"""
        # 清空父框架
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
            
        # 创建主容器
        main_frame = ttk.Frame(self.parent_frame)
        main_frame.pack(fill='both', expand=True, padx=50, pady=50)
        
        # 系统图标区域
        icon_frame = ttk.Frame(main_frame)
        icon_frame.pack(pady=20)
        
        # 系统标题
        title_label = ttk.Label(main_frame,
                               text="神经内科量表评估系统",
                               font=('Microsoft YaHei', 20, 'bold'),
                               foreground=self.colors['primary'])
        title_label.pack(pady=10)
        
        # 版本信息
        version_label = ttk.Label(main_frame,
                                 text="版本 1.0.0",
                                 font=('Microsoft YaHei', 12))
        version_label.pack(pady=5)
        
        # 开发者信息
        developer_label = ttk.Label(main_frame,
                                   text="开发人员：LIUYING",
                                   font=('Microsoft YaHei', 12))
        developer_label.pack(pady=5)
        
        # 系统描述
        desc_text = """专业的神经内科临床量表评估工具

提供标准化、自动化的神经内科常用量表评估功能
支持认知功能、情绪障碍、运动功能等多类量表
具备智能评分、数据管理、统计分析等完整功能

适用于神经内科临床诊疗、科研和教学"""
        
        desc_label = ttk.Label(main_frame,
                              text=desc_text,
                              font=('Microsoft YaHei', 10),
                              justify='center',
                              foreground=self.colors['text_secondary'])
        desc_label.pack(pady=20)
        
        # 技术信息
        tech_frame = ttk.LabelFrame(main_frame, text="技术信息", padding=20)
        tech_frame.pack(fill='x', pady=20)
        
        tech_info = [
            ("开发语言", "Python 3.8+"),
            ("界面框架", "Tkinter"),
            ("数据存储", "JSON格式"),
            ("支持系统", "Windows, macOS, Linux"),
            ("发布日期", "2024年")
        ]
        
        for i, (label, value) in enumerate(tech_info):
            info_frame = ttk.Frame(tech_frame)
            info_frame.pack(fill='x', pady=2)
            
            ttk.Label(info_frame, text=f"{label}:", 
                     font=('Microsoft YaHei', 9, 'bold')).pack(side='left')
            ttk.Label(info_frame, text=value,
                     font=('Microsoft YaHei', 9)).pack(side='left', padx=(10, 0))
        
        # 联系信息
        contact_frame = ttk.LabelFrame(main_frame, text="联系信息", padding=20)
        contact_frame.pack(fill='x', pady=20)
        
        contact_info = [
            ("技术支持", "support@neuroscales.com"),
            ("官方网站", "www.neuroscales.com"),
            ("用户手册", "www.neuroscales.com/docs")
        ]
        
        for label, value in contact_info:
            info_frame = ttk.Frame(contact_frame)
            info_frame.pack(fill='x', pady=2)
            
            ttk.Label(info_frame, text=f"{label}:",
                     font=('Microsoft YaHei', 9, 'bold')).pack(side='left')
            
            if value.startswith('www') or value.startswith('http'):
                link_label = ttk.Label(info_frame, text=value,
                                      font=('Microsoft YaHei', 9),
                                      foreground=self.colors['primary'],
                                      cursor='hand2')
                link_label.pack(side='left', padx=(10, 0))
                link_label.bind('<Button-1>', lambda e, url=value: webbrowser.open(f'http://{url}'))
            else:
                ttk.Label(info_frame, text=value,
                         font=('Microsoft YaHei', 9)).pack(side='left', padx=(10, 0))
        
        # 版权信息
        copyright_label = ttk.Label(main_frame,
                                   text="© 2024 神经内科量表评估系统. 保留所有权利.",
                                   font=('Microsoft YaHei', 8),
                                   foreground=self.colors['text_secondary'])
        copyright_label.pack(pady=20)