#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据存储和结果展示功能模块
开发人员：LIUYING
功能：数据管理、结果查看、统计分析、可视化展示
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from matplotlib import font_manager
import pandas as pd
from scoring_system import ScoringSystem

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class DataManager:
    """数据存储和结果展示管理器"""
    
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        self.scoring_system = ScoringSystem()
        self.current_data = []
        
    def show_data_management_interface(self):
        """显示数据管理界面"""
        # 清空父容器
        for widget in self.parent.winfo_children():
            widget.destroy()
            
        # 创建数据管理界面
        self.create_data_interface()
        
    def create_data_interface(self):
        """创建数据管理界面"""
        # 主容器
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 标题区域
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = ttk.Label(title_frame,
                               text="数据管理与结果展示",
                               font=('Microsoft YaHei', 18, 'bold'),
                               foreground='#2E86AB')
        title_label.pack(side='left')
        
        # 返回按钮
        back_btn = ttk.Button(title_frame,
                             text="返回主页",
                             command=self.back_to_main,
                             style='Accent.TButton')
        back_btn.pack(side='right')
        
        # 创建笔记本控件（选项卡）
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)
        
        # 数据查看选项卡
        self.create_data_view_tab(notebook)
        
        # 统计分析选项卡
        self.create_statistics_tab(notebook)
        
        # 可视化展示选项卡
        self.create_visualization_tab(notebook)
        
        # 数据导出选项卡
        self.create_export_tab(notebook)
        
    def create_data_view_tab(self, notebook):
        """创建数据查看选项卡"""
        data_frame = ttk.Frame(notebook)
        notebook.add(data_frame, text="数据查看")
        
        # 控制面板
        control_frame = ttk.LabelFrame(data_frame, text="查询控制", padding=10)
        control_frame.pack(fill='x', pady=(0, 10))
        
        # 筛选条件
        filter_frame = ttk.Frame(control_frame)
        filter_frame.pack(fill='x')
        
        # 量表类型筛选
        ttk.Label(filter_frame, text="量表类型:").pack(side='left')
        self.scale_type_var = tk.StringVar(value="全部")
        scale_combo = ttk.Combobox(filter_frame, 
                                  textvariable=self.scale_type_var,
                                  values=["全部", "MMSE", "HAMD", "UPDRS"],
                                  width=10, state='readonly')
        scale_combo.pack(side='left', padx=(5, 20))
        
        # 患者姓名筛选
        ttk.Label(filter_frame, text="患者姓名:").pack(side='left')
        self.patient_name_var = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=self.patient_name_var, width=15).pack(side='left', padx=(5, 20))
        
        # 查询按钮
        search_btn = ttk.Button(filter_frame,
                               text="查询",
                               command=self.search_data,
                               style='Accent.TButton')
        search_btn.pack(side='left', padx=5)
        
        # 刷新按钮
        refresh_btn = ttk.Button(filter_frame,
                                text="刷新",
                                command=self.refresh_data)
        refresh_btn.pack(side='left', padx=5)
        
        # 数据表格
        table_frame = ttk.Frame(data_frame)
        table_frame.pack(fill='both', expand=True)
        
        # 创建Treeview
        columns = ('评估日期', '量表类型', '患者姓名', '性别', '年龄', '总分', '严重程度', '风险等级')
        self.data_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # 设置列标题和宽度
        for col in columns:
            self.data_tree.heading(col, text=col)
            if col == '评估日期':
                self.data_tree.column(col, width=150)
            elif col in ['量表类型', '严重程度', '风险等级']:
                self.data_tree.column(col, width=100)
            elif col in ['性别', '年龄', '总分']:
                self.data_tree.column(col, width=60)
            else:
                self.data_tree.column(col, width=120)
                
        # 滚动条
        v_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.data_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal', command=self.data_tree.xview)
        self.data_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # 布局
        self.data_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # 双击查看详情
        self.data_tree.bind('<Double-1>', self.view_detail)
        
        # 底部按钮
        button_frame = ttk.Frame(data_frame)
        button_frame.pack(fill='x', pady=10)
        
        ttk.Button(button_frame, text="查看详情", command=self.view_selected_detail).pack(side='left', padx=5)
        ttk.Button(button_frame, text="删除记录", command=self.delete_selected).pack(side='left', padx=5)
        
        # 初始加载数据
        self.refresh_data()
        
    def create_statistics_tab(self, notebook):
        """创建统计分析选项卡"""
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="统计分析")
        
        # 统计信息显示区域
        stats_info_frame = ttk.LabelFrame(stats_frame, text="统计概览", padding=15)
        stats_info_frame.pack(fill='x', pady=(0, 10))
        
        self.stats_text = tk.Text(stats_info_frame, height=12, wrap='word', font=('Microsoft YaHei', 10))
        stats_scrollbar = ttk.Scrollbar(stats_info_frame, orient='vertical', command=self.stats_text.yview)
        self.stats_text.configure(yscrollcommand=stats_scrollbar.set)
        
        self.stats_text.pack(side='left', fill='both', expand=True)
        stats_scrollbar.pack(side='right', fill='y')
        
        # 控制按钮
        stats_button_frame = ttk.Frame(stats_frame)
        stats_button_frame.pack(fill='x', pady=10)
        
        ttk.Button(stats_button_frame, text="生成统计报告", 
                  command=self.generate_statistics, style='Accent.TButton').pack(side='left', padx=5)
        ttk.Button(stats_button_frame, text="按患者统计", 
                  command=self.patient_statistics).pack(side='left', padx=5)
        ttk.Button(stats_button_frame, text="按量表统计", 
                  command=self.scale_statistics).pack(side='left', padx=5)
        
    def create_visualization_tab(self, notebook):
        """创建可视化展示选项卡"""
        viz_frame = ttk.Frame(notebook)
        notebook.add(viz_frame, text="可视化展示")
        
        # 控制面板
        viz_control_frame = ttk.LabelFrame(viz_frame, text="图表控制", padding=10)
        viz_control_frame.pack(fill='x', pady=(0, 10))
        
        # 图表类型选择
        ttk.Label(viz_control_frame, text="图表类型:").pack(side='left')
        self.chart_type_var = tk.StringVar(value="评分趋势")
        chart_combo = ttk.Combobox(viz_control_frame,
                                  textvariable=self.chart_type_var,
                                  values=["评分趋势", "量表分布", "风险等级分布", "患者对比"],
                                  width=12, state='readonly')
        chart_combo.pack(side='left', padx=(5, 20))
        
        # 生成图表按钮
        ttk.Button(viz_control_frame, text="生成图表", 
                  command=self.generate_chart, style='Accent.TButton').pack(side='left', padx=5)
        ttk.Button(viz_control_frame, text="保存图表", 
                  command=self.save_chart).pack(side='left', padx=5)
        
        # 图表显示区域
        self.chart_frame = ttk.Frame(viz_frame)
        self.chart_frame.pack(fill='both', expand=True)
        
    def create_export_tab(self, notebook):
        """创建数据导出选项卡"""
        export_frame = ttk.Frame(notebook)
        notebook.add(export_frame, text="数据导出")
        
        # 导出选项
        export_options_frame = ttk.LabelFrame(export_frame, text="导出选项", padding=15)
        export_options_frame.pack(fill='x', pady=(0, 10))
        
        # 导出格式
        format_frame = ttk.Frame(export_options_frame)
        format_frame.pack(fill='x', pady=5)
        
        ttk.Label(format_frame, text="导出格式:").pack(side='left')
        self.export_format_var = tk.StringVar(value="Excel")
        format_combo = ttk.Combobox(format_frame,
                                   textvariable=self.export_format_var,
                                   values=["Excel", "CSV", "JSON", "PDF报告"],
                                   width=10, state='readonly')
        format_combo.pack(side='left', padx=(5, 20))
        
        # 导出范围
        range_frame = ttk.Frame(export_options_frame)
        range_frame.pack(fill='x', pady=5)
        
        ttk.Label(range_frame, text="导出范围:").pack(side='left')
        self.export_range_var = tk.StringVar(value="全部数据")
        range_combo = ttk.Combobox(range_frame,
                                  textvariable=self.export_range_var,
                                  values=["全部数据", "当前筛选", "指定患者", "指定时间段"],
                                  width=12, state='readonly')
        range_combo.pack(side='left', padx=(5, 20))
        
        # 导出按钮
        export_button_frame = ttk.Frame(export_frame)
        export_button_frame.pack(fill='x', pady=20)
        
        ttk.Button(export_button_frame, text="导出数据", 
                  command=self.export_data, style='Accent.TButton').pack(side='left', padx=5)
        ttk.Button(export_button_frame, text="生成报告", 
                  command=self.generate_report).pack(side='left', padx=5)
        
        # 导出状态显示
        self.export_status_text = tk.Text(export_frame, height=10, wrap='word', 
                                         font=('Microsoft YaHei', 10))
        export_status_scrollbar = ttk.Scrollbar(export_frame, orient='vertical', 
                                               command=self.export_status_text.yview)
        self.export_status_text.configure(yscrollcommand=export_status_scrollbar.set)
        
        self.export_status_text.pack(side='left', fill='both', expand=True)
        export_status_scrollbar.pack(side='right', fill='y')
        
    def search_data(self):
        """搜索数据"""
        scale_type = self.scale_type_var.get()
        patient_name = self.patient_name_var.get().strip()
        
        # 加载所有数据
        if scale_type == "全部":
            all_data = self.scoring_system.load_assessment_results()
        else:
            all_data = self.scoring_system.load_assessment_results(scale_type)
            
        # 按患者姓名筛选
        if patient_name:
            all_data = [data for data in all_data 
                       if patient_name.lower() in data.get('patient_info', {}).get('name', '').lower()]
            
        self.current_data = all_data
        self.update_data_tree()
        
    def refresh_data(self):
        """刷新数据"""
        self.current_data = self.scoring_system.load_assessment_results()
        self.update_data_tree()
        
    def update_data_tree(self):
        """更新数据表格"""
        # 清空现有数据
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
            
        # 插入新数据
        for data in self.current_data:
            patient_info = data.get('patient_info', {})
            score_result = data.get('score_result', {})
            
            # 格式化日期
            assessment_time = data.get('assessment_time', '')
            if assessment_time:
                try:
                    dt = datetime.fromisoformat(assessment_time.replace('Z', '+00:00'))
                    formatted_date = dt.strftime('%Y-%m-%d %H:%M')
                except:
                    formatted_date = assessment_time[:16]
            else:
                formatted_date = '未知'
                
            values = (
                formatted_date,
                data.get('scale_type', ''),
                patient_info.get('name', ''),
                patient_info.get('gender', ''),
                patient_info.get('age', ''),
                score_result.get('total_score', ''),
                score_result.get('level', ''),
                score_result.get('risk_level', '')
            )
            
            self.data_tree.insert('', 'end', values=values, tags=(data,))
            
    def view_detail(self, event):
        """双击查看详情"""
        self.view_selected_detail()
        
    def view_selected_detail(self):
        """查看选中项详情"""
        selection = self.data_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请选择要查看的记录")
            return
            
        item = self.data_tree.item(selection[0])
        data = item['tags'][0]
        
        # 创建详情窗口
        self.show_detail_window(data)
        
    def show_detail_window(self, data):
        """显示详情窗口"""
        detail_window = tk.Toplevel(self.parent)
        detail_window.title("评估详情")
        detail_window.geometry("800x600")
        detail_window.resizable(True, True)
        
        # 居中显示
        detail_window.transient(self.parent)
        detail_window.grab_set()
        
        # 创建滚动文本框
        text_frame = ttk.Frame(detail_window)
        text_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        detail_text = tk.Text(text_frame, wrap='word', font=('Microsoft YaHei', 10))
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=detail_text.yview)
        detail_text.configure(yscrollcommand=scrollbar.set)
        
        # 格式化详情内容
        content = self.format_detail_content(data)
        detail_text.insert('1.0', content)
        detail_text.config(state='disabled')
        
        detail_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # 关闭按钮
        close_btn = ttk.Button(detail_window, text="关闭", 
                              command=detail_window.destroy, style='Accent.TButton')
        close_btn.pack(pady=10)
        
    def format_detail_content(self, data):
        """格式化详情内容"""
        patient_info = data.get('patient_info', {})
        score_result = data.get('score_result', {})
        responses = data.get('responses', {})
        
        content = f"""=== 评估详情 ===

【基本信息】
量表类型：{data.get('scale_type', '')}
评估时间：{data.get('assessment_time', '')}
评估者：{data.get('assessor', '')}

【患者信息】
姓名：{patient_info.get('name', '')}
性别：{patient_info.get('gender', '')}
年龄：{patient_info.get('age', '')}
评估日期：{patient_info.get('assessment_date', '')}
"""
        
        if 'duration' in patient_info:
            content += f"病程：{patient_info.get('duration', '')}年\n"
            
        content += f"""
【评估结果】
总分：{score_result.get('total_score', '')} / {score_result.get('max_score', '')}
百分比：{score_result.get('percentage', '')}%
严重程度：{score_result.get('level', '')}
风险等级：{score_result.get('risk_level', '')}
结果解释：{score_result.get('interpretation', '')}
"""
        
        # 添加维度分析
        if 'domain_analysis' in score_result:
            content += "\n【认知域分析】\n"
            for domain, analysis in score_result['domain_analysis'].items():
                content += f"{domain}：{analysis.get('score', '')}分 ({analysis.get('percentage', '')}%) - {analysis.get('level', '')}\n"
                
        if 'symptom_analysis' in score_result:
            content += "\n【症状维度分析】\n"
            for symptom, analysis in score_result['symptom_analysis'].items():
                content += f"{symptom}：{analysis.get('score', '')}分 ({analysis.get('percentage', '')}%) - {analysis.get('severity', '')}\n"
                
        if 'motor_analysis' in score_result:
            content += "\n【运动功能分析】\n"
            for motor, analysis in score_result['motor_analysis'].items():
                content += f"{motor}：{analysis.get('score', '')}分 ({analysis.get('percentage', '')}%) - {analysis.get('severity', '')}\n"
                
        # 添加建议
        if 'recommendations' in score_result:
            content += "\n【专业建议】\n"
            for i, rec in enumerate(score_result['recommendations'], 1):
                content += f"{i}. {rec}\n"
                
        # 添加详细评分
        content += "\n【详细评分】\n"
        for item_id, score in responses.items():
            content += f"第{item_id}项：{score}分\n"
            
        return content
        
    def delete_selected(self):
        """删除选中的记录"""
        selection = self.data_tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请选择要删除的记录")
            return
            
        if messagebox.askyesno("确认", "确定要删除选中的记录吗？此操作不可撤销。"):
            # 这里应该实现删除文件的逻辑
            messagebox.showinfo("提示", "删除功能正在开发中...")
            
    def generate_statistics(self):
        """生成统计报告"""
        if not self.current_data:
            messagebox.showwarning("提示", "没有可统计的数据")
            return
            
        # 统计分析
        total_count = len(self.current_data)
        scale_counts = {}
        risk_counts = {'低': 0, '中': 0, '高': 0, '极高': 0}
        score_stats = {}
        
        for data in self.current_data:
            scale_type = data.get('scale_type', '')
            scale_counts[scale_type] = scale_counts.get(scale_type, 0) + 1
            
            risk_level = data.get('score_result', {}).get('risk_level', '低')
            if risk_level in risk_counts:
                risk_counts[risk_level] += 1
                
            total_score = data.get('score_result', {}).get('total_score', 0)
            if scale_type not in score_stats:
                score_stats[scale_type] = []
            score_stats[scale_type].append(total_score)
            
        # 生成报告内容
        report = f"""=== 统计分析报告 ===
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

【总体概况】
总评估次数：{total_count}

【量表分布】
"""
        
        for scale, count in scale_counts.items():
            percentage = (count / total_count) * 100
            report += f"{scale}：{count}次 ({percentage:.1f}%)\n"
            
        report += "\n【风险等级分布】\n"
        for risk, count in risk_counts.items():
            percentage = (count / total_count) * 100
            report += f"{risk}风险：{count}次 ({percentage:.1f}%)\n"
            
        report += "\n【评分统计】\n"
        for scale, scores in score_stats.items():
            if scores:
                avg_score = sum(scores) / len(scores)
                min_score = min(scores)
                max_score = max(scores)
                report += f"{scale}：平均{avg_score:.1f}分，最低{min_score}分，最高{max_score}分\n"
                
        # 显示报告
        self.stats_text.delete('1.0', 'end')
        self.stats_text.insert('1.0', report)
        
    def patient_statistics(self):
        """按患者统计"""
        if not self.current_data:
            messagebox.showwarning("提示", "没有可统计的数据")
            return
            
        patient_stats = {}
        for data in self.current_data:
            patient_name = data.get('patient_info', {}).get('name', '未知')
            if patient_name not in patient_stats:
                patient_stats[patient_name] = []
            patient_stats[patient_name].append(data)
            
        report = f"""=== 按患者统计报告 ===
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
        
        for patient, assessments in patient_stats.items():
            report += f"【患者：{patient}】\n"
            report += f"评估次数：{len(assessments)}\n"
            
            scale_types = set(a.get('scale_type', '') for a in assessments)
            report += f"评估量表：{', '.join(scale_types)}\n"
            
            latest = max(assessments, key=lambda x: x.get('assessment_time', ''))
            report += f"最近评估：{latest.get('assessment_time', '')[:10]}\n"
            report += f"最近结果：{latest.get('score_result', {}).get('level', '')}\n\n"
            
        self.stats_text.delete('1.0', 'end')
        self.stats_text.insert('1.0', report)
        
    def scale_statistics(self):
        """按量表统计"""
        if not self.current_data:
            messagebox.showwarning("提示", "没有可统计的数据")
            return
            
        scale_stats = {}
        for data in self.current_data:
            scale_type = data.get('scale_type', '未知')
            if scale_type not in scale_stats:
                scale_stats[scale_type] = []
            scale_stats[scale_type].append(data)
            
        report = f"""=== 按量表统计报告 ===
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
        
        for scale, assessments in scale_stats.items():
            report += f"【{scale}量表】\n"
            report += f"评估次数：{len(assessments)}\n"
            
            scores = [a.get('score_result', {}).get('total_score', 0) for a in assessments]
            if scores:
                report += f"平均分：{sum(scores)/len(scores):.1f}\n"
                report += f"分数范围：{min(scores)} - {max(scores)}\n"
                
            levels = [a.get('score_result', {}).get('level', '') for a in assessments]
            level_counts = {}
            for level in levels:
                level_counts[level] = level_counts.get(level, 0) + 1
                
            report += "严重程度分布：\n"
            for level, count in level_counts.items():
                percentage = (count / len(assessments)) * 100
                report += f"  {level}：{count}次 ({percentage:.1f}%)\n"
            report += "\n"
            
        self.stats_text.delete('1.0', 'end')
        self.stats_text.insert('1.0', report)
        
    def generate_chart(self):
        """生成图表"""
        if not self.current_data:
            messagebox.showwarning("提示", "没有可显示的数据")
            return
            
        chart_type = self.chart_type_var.get()
        
        # 清空现有图表
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
            
        try:
            if chart_type == "评分趋势":
                self.create_score_trend_chart()
            elif chart_type == "量表分布":
                self.create_scale_distribution_chart()
            elif chart_type == "风险等级分布":
                self.create_risk_distribution_chart()
            elif chart_type == "患者对比":
                self.create_patient_comparison_chart()
        except Exception as e:
            messagebox.showerror("错误", f"生成图表时出错：{str(e)}")
            
    def create_score_trend_chart(self):
        """创建评分趋势图"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 按量表类型分组
        scale_data = {}
        for data in self.current_data:
            scale_type = data.get('scale_type', '')
            if scale_type not in scale_data:
                scale_data[scale_type] = []
            scale_data[scale_type].append(data)
            
        colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
        color_idx = 0
        
        for scale_type, assessments in scale_data.items():
            # 按时间排序
            assessments.sort(key=lambda x: x.get('assessment_time', ''))
            
            dates = []
            scores = []
            
            for assessment in assessments:
                try:
                    date_str = assessment.get('assessment_time', '')
                    if date_str:
                        date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                        dates.append(date)
                        scores.append(assessment.get('score_result', {}).get('total_score', 0))
                except:
                    continue
                    
            if dates and scores:
                ax.plot(dates, scores, marker='o', label=scale_type, 
                       color=colors[color_idx % len(colors)], linewidth=2)
                color_idx += 1
                
        ax.set_xlabel('评估时间')
        ax.set_ylabel('评分')
        ax.set_title('评分趋势图')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # 格式化日期轴
        if len(self.current_data) > 0:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.xticks(rotation=45)
            
        plt.tight_layout()
        
        # 嵌入到tkinter
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        self.current_figure = fig
        
    def create_scale_distribution_chart(self):
        """创建量表分布饼图"""
        fig, ax = plt.subplots(figsize=(8, 6))
        
        scale_counts = {}
        for data in self.current_data:
            scale_type = data.get('scale_type', '')
            scale_counts[scale_type] = scale_counts.get(scale_type, 0) + 1
            
        if scale_counts:
            labels = list(scale_counts.keys())
            sizes = list(scale_counts.values())
            colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
            
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors[:len(labels)])
            ax.set_title('量表类型分布')
            
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        self.current_figure = fig
        
    def create_risk_distribution_chart(self):
        """创建风险等级分布柱状图"""
        fig, ax = plt.subplots(figsize=(8, 6))
        
        risk_counts = {'低': 0, '中': 0, '高': 0, '极高': 0}
        for data in self.current_data:
            risk_level = data.get('score_result', {}).get('risk_level', '低')
            if risk_level in risk_counts:
                risk_counts[risk_level] += 1
                
        labels = list(risk_counts.keys())
        counts = list(risk_counts.values())
        colors = ['#28a745', '#ffc107', '#fd7e14', '#dc3545']
        
        bars = ax.bar(labels, counts, color=colors)
        ax.set_xlabel('风险等级')
        ax.set_ylabel('评估次数')
        ax.set_title('风险等级分布')
        
        # 在柱子上显示数值
        for bar, count in zip(bars, counts):
            if count > 0:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                       str(count), ha='center', va='bottom')
                       
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        self.current_figure = fig
        
    def create_patient_comparison_chart(self):
        """创建患者对比图"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 获取患者数据
        patient_data = {}
        for data in self.current_data:
            patient_name = data.get('patient_info', {}).get('name', '未知')
            scale_type = data.get('scale_type', '')
            score = data.get('score_result', {}).get('total_score', 0)
            
            if patient_name not in patient_data:
                patient_data[patient_name] = {}
            if scale_type not in patient_data[patient_name]:
                patient_data[patient_name][scale_type] = []
            patient_data[patient_name][scale_type].append(score)
            
        # 计算平均分
        patient_avg_scores = {}
        for patient, scales in patient_data.items():
            patient_avg_scores[patient] = {}
            for scale, scores in scales.items():
                patient_avg_scores[patient][scale] = sum(scores) / len(scores)
                
        if not patient_avg_scores:
            ax.text(0.5, 0.5, '没有可对比的数据', ha='center', va='center', transform=ax.transAxes)
            ax.set_title('患者对比图')
        else:
            # 创建分组柱状图
            patients = list(patient_avg_scores.keys())[:5]  # 最多显示5个患者
            scale_types = set()
            for patient_scales in patient_avg_scores.values():
                scale_types.update(patient_scales.keys())
            scale_types = list(scale_types)
            
            x = range(len(patients))
            width = 0.25
            colors = ['#2E86AB', '#A23B72', '#F18F01']
            
            for i, scale_type in enumerate(scale_types[:3]):  # 最多显示3种量表
                scores = [patient_avg_scores[patient].get(scale_type, 0) for patient in patients]
                ax.bar([xi + i * width for xi in x], scores, width, 
                      label=scale_type, color=colors[i % len(colors)])
                      
            ax.set_xlabel('患者')
            ax.set_ylabel('平均评分')
            ax.set_title('患者评分对比')
            ax.set_xticks([xi + width for xi in x])
            ax.set_xticklabels(patients, rotation=45)
            ax.legend()
            
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        self.current_figure = fig
        
    def save_chart(self):
        """保存图表"""
        if not hasattr(self, 'current_figure'):
            messagebox.showwarning("提示", "请先生成图表")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG图片", "*.png"), ("PDF文件", "*.pdf"), ("所有文件", "*.*")]
        )
        
        if filename:
            try:
                self.current_figure.savefig(filename, dpi=300, bbox_inches='tight')
                messagebox.showinfo("成功", f"图表已保存到：{filename}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败：{str(e)}")
                
    def export_data(self):
        """导出数据"""
        if not self.current_data:
            messagebox.showwarning("提示", "没有可导出的数据")
            return
            
        export_format = self.export_format_var.get()
        
        try:
            if export_format == "Excel":
                filename = self.scoring_system.export_to_excel()
                self.export_status_text.insert('end', f"Excel文件已导出：{filename}\n")
            elif export_format == "CSV":
                self.export_to_csv()
            elif export_format == "JSON":
                self.export_to_json()
            elif export_format == "PDF报告":
                self.export_to_pdf()
                
        except Exception as e:
            messagebox.showerror("错误", f"导出失败：{str(e)}")
            
    def export_to_csv(self):
        """导出到CSV"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")]
        )
        
        if filename:
            # 准备CSV数据
            csv_data = []
            for data in self.current_data:
                patient_info = data.get('patient_info', {})
                score_result = data.get('score_result', {})
                
                csv_data.append({
                    '评估日期': data.get('assessment_time', ''),
                    '量表类型': data.get('scale_type', ''),
                    '患者姓名': patient_info.get('name', ''),
                    '性别': patient_info.get('gender', ''),
                    '年龄': patient_info.get('age', ''),
                    '总分': score_result.get('total_score', ''),
                    '满分': score_result.get('max_score', ''),
                    '百分比': score_result.get('percentage', ''),
                    '严重程度': score_result.get('level', ''),
                    '风险等级': score_result.get('risk_level', ''),
                    '解释': score_result.get('interpretation', '')
                })
                
            df = pd.DataFrame(csv_data)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            self.export_status_text.insert('end', f"CSV文件已导出：{filename}\n")
            
    def export_to_json(self):
        """导出到JSON"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
        )
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.current_data, f, ensure_ascii=False, indent=2)
            self.export_status_text.insert('end', f"JSON文件已导出：{filename}\n")
            
    def export_to_pdf(self):
        """导出PDF报告"""
        messagebox.showinfo("提示", "PDF报告导出功能正在开发中...")
        
    def generate_report(self):
        """生成综合报告"""
        if not self.current_data:
            messagebox.showwarning("提示", "没有可生成报告的数据")
            return
            
        # 生成综合分析报告
        summary = self.scoring_system.generate_summary_report()
        
        report_content = f"""=== 神经内科量表评估综合报告 ===
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

【总体统计】
总评估次数：{summary.get('total_assessments', 0)}

【量表类型统计】
"""
        
        for scale_type, count in summary.get('scale_types', {}).items():
            report_content += f"{scale_type}：{count}次\n"
            
        report_content += "\n【风险等级分布】\n"
        for risk_level, count in summary.get('risk_distribution', {}).items():
            report_content += f"{risk_level}风险：{count}次\n"
            
        # 显示报告
        self.export_status_text.delete('1.0', 'end')
        self.export_status_text.insert('1.0', report_content)
        
    def back_to_main(self):
        """返回主页"""
        self.main_app.show_welcome_screen()