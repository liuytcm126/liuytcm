#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化评分计算系统
开发人员：LIUYING
功能：统一管理所有量表的评分逻辑、结果分析和数据处理
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Any
import pandas as pd
import numpy as np

class ScoringSystem:
    """自动化评分计算系统"""
    
    def __init__(self):
        self.data_dir = 'data'
        self.ensure_data_directory()
        
    def ensure_data_directory(self):
        """确保数据目录存在"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
    def calculate_mmse_score(self, responses: Dict[str, int]) -> Dict[str, Any]:
        """计算MMSE得分"""
        total_score = sum(responses.values())
        max_score = 30
        
        # 认知功能分级
        if total_score >= 27:
            level = "正常"
            interpretation = "认知功能正常"
            risk_level = "低"
        elif total_score >= 24:
            level = "轻度认知障碍"
            interpretation = "可能存在轻度认知功能下降，建议进一步评估"
            risk_level = "中"
        elif total_score >= 18:
            level = "中度认知障碍"
            interpretation = "存在明显认知功能障碍，建议医学干预"
            risk_level = "高"
        else:
            level = "重度认知障碍"
            interpretation = "存在严重认知功能障碍，需要立即医学干预"
            risk_level = "极高"
            
        # 各维度分析
        domain_analysis = self._analyze_mmse_domains(responses)
        
        return {
            'total_score': total_score,
            'max_score': max_score,
            'percentage': round((total_score / max_score) * 100, 1),
            'level': level,
            'interpretation': interpretation,
            'risk_level': risk_level,
            'domain_analysis': domain_analysis,
            'recommendations': self._get_mmse_recommendations(level)
        }
        
    def _analyze_mmse_domains(self, responses: Dict[str, int]) -> Dict[str, Dict]:
        """分析MMSE各认知域得分"""
        domains = {
            '定向力': {'items': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'max_score': 10},
            '记忆力': {'items': [11, 12, 13], 'max_score': 3},
            '注意力和计算': {'items': [14, 15, 16, 17, 18], 'max_score': 5},
            '回忆': {'items': [19, 20, 21], 'max_score': 3},
            '语言': {'items': [22, 23, 24, 25, 26, 27, 28, 29, 30], 'max_score': 9}
        }
        
        domain_results = {}
        for domain_name, domain_info in domains.items():
            domain_score = sum(responses.get(str(item), 0) for item in domain_info['items'])
            domain_percentage = round((domain_score / domain_info['max_score']) * 100, 1)
            
            if domain_percentage >= 80:
                domain_level = "正常"
            elif domain_percentage >= 60:
                domain_level = "轻度受损"
            elif domain_percentage >= 40:
                domain_level = "中度受损"
            else:
                domain_level = "重度受损"
                
            domain_results[domain_name] = {
                'score': domain_score,
                'max_score': domain_info['max_score'],
                'percentage': domain_percentage,
                'level': domain_level
            }
            
        return domain_results
        
    def _get_mmse_recommendations(self, level: str) -> List[str]:
        """获取MMSE评估建议"""
        recommendations = {
            "正常": [
                "继续保持良好的生活习惯",
                "定期进行认知功能评估",
                "保持社交活动和智力活动"
            ],
            "轻度认知障碍": [
                "建议进行详细的神经心理学评估",
                "加强认知训练和智力活动",
                "定期随访，监测认知功能变化",
                "保持健康的生活方式"
            ],
            "中度认知障碍": [
                "建议神经科专科就诊",
                "进行脑影像学检查",
                "考虑药物治疗",
                "加强日常生活能力训练"
            ],
            "重度认知障碍": [
                "立即神经科专科就诊",
                "全面的医学评估和检查",
                "制定个体化治疗方案",
                "家属护理指导和支持"
            ]
        }
        return recommendations.get(level, [])
        
    def calculate_hamd_score(self, responses: Dict[str, int]) -> Dict[str, Any]:
        """计算HAMD得分"""
        total_score = sum(responses.values())
        max_score = 52  # HAMD-17最高分
        
        # 抑郁严重程度分级
        if total_score < 8:
            level = "无抑郁"
            interpretation = "无明显抑郁症状"
            risk_level = "低"
        elif total_score < 17:
            level = "轻度抑郁"
            interpretation = "存在轻度抑郁症状，建议关注情绪变化"
            risk_level = "中"
        elif total_score < 24:
            level = "中度抑郁"
            interpretation = "存在中度抑郁症状，建议专业治疗"
            risk_level = "高"
        else:
            level = "重度抑郁"
            interpretation = "存在重度抑郁症状，需要立即专业干预"
            risk_level = "极高"
            
        # 症状维度分析
        symptom_analysis = self._analyze_hamd_symptoms(responses)
        
        return {
            'total_score': total_score,
            'max_score': max_score,
            'percentage': round((total_score / max_score) * 100, 1),
            'level': level,
            'interpretation': interpretation,
            'risk_level': risk_level,
            'symptom_analysis': symptom_analysis,
            'recommendations': self._get_hamd_recommendations(level)
        }
        
    def _analyze_hamd_symptoms(self, responses: Dict[str, int]) -> Dict[str, Dict]:
        """分析HAMD症状维度"""
        symptom_groups = {
            '情绪症状': {'items': [1, 2, 3], 'description': '抑郁情绪、罪恶感、自杀观念'},
            '认知症状': {'items': [9, 10, 15], 'description': '激越、精神性焦虑、疑病'},
            '躯体症状': {'items': [4, 5, 6, 11, 12, 13], 'description': '睡眠障碍、食欲、体重、躯体症状'},
            '精神运动症状': {'items': [8, 14], 'description': '精神运动性迟滞、工作和活动'},
            '其他症状': {'items': [7, 16, 17], 'description': '性症状、自知力、日夜变化'}
        }
        
        symptom_results = {}
        for group_name, group_info in symptom_groups.items():
            group_score = sum(responses.get(str(item), 0) for item in group_info['items'])
            max_possible = len(group_info['items']) * 4  # 每项最高4分
            group_percentage = round((group_score / max_possible) * 100, 1)
            
            if group_percentage < 25:
                severity = "轻微"
            elif group_percentage < 50:
                severity = "轻度"
            elif group_percentage < 75:
                severity = "中度"
            else:
                severity = "重度"
                
            symptom_results[group_name] = {
                'score': group_score,
                'max_score': max_possible,
                'percentage': group_percentage,
                'severity': severity,
                'description': group_info['description']
            }
            
        return symptom_results
        
    def _get_hamd_recommendations(self, level: str) -> List[str]:
        """获取HAMD评估建议"""
        recommendations = {
            "无抑郁": [
                "保持良好的心理状态",
                "定期进行情绪自我评估",
                "维持健康的生活方式"
            ],
            "轻度抑郁": [
                "建议心理咨询或心理治疗",
                "加强社会支持系统",
                "规律作息，适度运动",
                "定期随访评估"
            ],
            "中度抑郁": [
                "建议神经科专科就诊",
                "考虑药物治疗结合心理治疗",
                "密切监测症状变化",
                "家属支持和理解"
            ],
            "重度抑郁": [
                "立即神经科急诊就诊",
                "评估自杀风险",
                "考虑住院治疗",
                "24小时监护和支持"
            ]
        }
        return recommendations.get(level, [])
        
    def calculate_updrs_score(self, responses: Dict[str, int]) -> Dict[str, Any]:
        """计算UPDRS得分"""
        total_score = sum(responses.values())
        max_score = 56  # UPDRS-III最高分
        
        # 运动症状严重程度分级
        if total_score <= 17:
            level = "轻度"
            interpretation = "运动症状轻微，对日常生活影响较小"
            risk_level = "低"
        elif total_score <= 33:
            level = "中度"
            interpretation = "运动症状明显，对日常生活有一定影响"
            risk_level = "中"
        elif total_score <= 50:
            level = "中重度"
            interpretation = "运动症状较重，对日常生活影响较大"
            risk_level = "高"
        else:
            level = "重度"
            interpretation = "运动症状严重，严重影响日常生活"
            risk_level = "极高"
            
        # 运动功能维度分析
        motor_analysis = self._analyze_updrs_domains(responses)
        
        return {
            'total_score': total_score,
            'max_score': max_score,
            'percentage': round((total_score / max_score) * 100, 1),
            'level': level,
            'interpretation': interpretation,
            'risk_level': risk_level,
            'motor_analysis': motor_analysis,
            'recommendations': self._get_updrs_recommendations(level)
        }
        
    def _analyze_updrs_domains(self, responses: Dict[str, int]) -> Dict[str, Dict]:
        """分析UPDRS运动功能域"""
        motor_domains = {
            '言语和面部表情': {'items': [1, 2], 'description': '言语清晰度和面部表情'},
            '肌肉僵硬': {'items': [3, 4, 5], 'description': '颈部、上肢、下肢僵硬'},
            '手部功能': {'items': [6, 7, 8], 'description': '手指敲击、手部动作、快速交替动作'},
            '下肢功能': {'items': [9], 'description': '腿部敏捷性'},
            '姿势和步态': {'items': [10, 11, 12, 13], 'description': '起立、姿势、步态、姿势稳定性'},
            '整体运动': {'items': [14], 'description': '整体运动迟缓'}
        }
        
        domain_results = {}
        for domain_name, domain_info in motor_domains.items():
            domain_score = sum(responses.get(str(item), 0) for item in domain_info['items'])
            max_possible = len(domain_info['items']) * 4  # 每项最高4分
            domain_percentage = round((domain_score / max_possible) * 100, 1)
            
            if domain_percentage < 25:
                severity = "轻微"
            elif domain_percentage < 50:
                severity = "轻度"
            elif domain_percentage < 75:
                severity = "中度"
            else:
                severity = "重度"
                
            domain_results[domain_name] = {
                'score': domain_score,
                'max_score': max_possible,
                'percentage': domain_percentage,
                'severity': severity,
                'description': domain_info['description']
            }
            
        return domain_results
        
    def _get_updrs_recommendations(self, level: str) -> List[str]:
        """获取UPDRS评估建议"""
        recommendations = {
            "轻度": [
                "继续规律服药",
                "适度运动和物理治疗",
                "定期神经科随访",
                "保持积极的生活态度"
            ],
            "中度": [
                "调整药物治疗方案",
                "加强康复训练",
                "职业治疗评估",
                "家属护理指导"
            ],
            "中重度": [
                "神经科专科调整治疗",
                "考虑深部脑刺激术评估",
                "全面康复治疗",
                "日常生活辅助设备"
            ],
            "重度": [
                "立即神经科专科就诊",
                "评估手术治疗适应症",
                "全面护理支持",
                "家属培训和支持"
            ]
        }
        return recommendations.get(level, [])
        
    def save_assessment_result(self, scale_type: str, patient_info: Dict, 
                             responses: Dict, score_result: Dict) -> str:
        """保存评估结果"""
        result_data = {
            'scale_type': scale_type,
            'patient_info': patient_info,
            'responses': responses,
            'score_result': score_result,
            'assessment_time': datetime.now().isoformat(),
            'assessor': 'LIUYING',
            'system_version': '1.0.0'
        }
        
        # 生成文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        patient_name = patient_info.get('name', 'Unknown')
        filename = f"{self.data_dir}/{scale_type}_{patient_name}_{timestamp}.json"
        
        # 保存文件
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
            
        return filename
        
    def load_assessment_results(self, scale_type: str = None) -> List[Dict]:
        """加载评估结果"""
        results = []
        
        # 检查多个数据目录
        data_dirs = [self.data_dir, 'results']
        
        for data_dir in data_dirs:
            if not os.path.exists(data_dir):
                continue
                
            for filename in os.listdir(data_dir):
                if filename.endswith('.json'):
                    if scale_type and not filename.startswith(scale_type):
                        continue
                        
                    try:
                        with open(os.path.join(data_dir, filename), 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            
                            # 统一数据格式
                            normalized_data = self._normalize_data_format(data)
                            if normalized_data:
                                results.append(normalized_data)
                                
                    except Exception as e:
                        print(f"加载文件 {filename} 时出错: {e}")
                        
        # 按评估时间排序
        results.sort(key=lambda x: x.get('assessment_time', ''), reverse=True)
        return results
        
    def _normalize_data_format(self, data: Dict) -> Dict:
        """统一数据格式"""
        try:
            # 处理不同的数据格式
            normalized = {
                'scale_type': data.get('scale_type') or data.get('scale_name', ''),
                'patient_info': {},
                'responses': data.get('responses') or data.get('scores', {}),  # 修复：支持scores字段
                'score_result': {},
                'assessment_time': data.get('assessment_time') or data.get('assessment_date') or data.get('timestamp', ''),  # 修复：支持timestamp字段
                'assessor': data.get('assessor', 'Unknown')
            }
            
            # 处理患者信息
            if 'patient_info' in data:
                normalized['patient_info'] = data['patient_info']
            else:
                # 从其他字段推断患者信息
                normalized['patient_info'] = {
                    'name': data.get('patient_name', '匿名患者'),
                    'gender': data.get('gender', '未知'),
                    'age': data.get('age', '未知'),
                    'assessment_date': data.get('assessment_date', '')
                }
            
            # 处理评分结果
            normalized['score_result'] = {
                'total_score': data.get('total_score', 0),
                'max_score': data.get('max_score', 0),
                'level': data.get('severity') or data.get('level', ''),
                'risk_level': data.get('risk_level', '低'),
                'interpretation': data.get('interpretation', ''),
                'percentage': round((data.get('total_score', 0) / max(data.get('max_score', 1), 1)) * 100, 1)
            }
            
            # 处理特殊格式（如GCS）
            if 'eye_score' in data:
                normalized['score_result'].update({
                    'eye_score': data.get('eye_score'),
                    'verbal_score': data.get('verbal_score'),
                    'motor_score': data.get('motor_score')
                })
            
            return normalized
            
        except Exception as e:
            print(f"数据格式化错误: {e}")
            return None
        
    def generate_summary_report(self, patient_name: str = None) -> Dict[str, Any]:
        """生成汇总报告"""
        all_results = self.load_assessment_results()
        
        if patient_name:
            all_results = [r for r in all_results 
                          if r.get('patient_info', {}).get('name') == patient_name]
            
        if not all_results:
            return {'error': '未找到评估结果'}
            
        # 统计信息
        summary = {
            'total_assessments': len(all_results),
            'scale_types': {},
            'assessment_timeline': [],
            'risk_distribution': {'低': 0, '中': 0, '高': 0, '极高': 0}
        }
        
        for result in all_results:
            scale_type = result.get('scale_type', 'Unknown')
            summary['scale_types'][scale_type] = summary['scale_types'].get(scale_type, 0) + 1
            
            # 时间线
            summary['assessment_timeline'].append({
                'date': result.get('assessment_time', ''),
                'scale_type': scale_type,
                'score': result.get('score_result', {}).get('total_score', 0),
                'level': result.get('score_result', {}).get('level', '')
            })
            
            # 风险分布
            risk_level = result.get('score_result', {}).get('risk_level', '低')
            if risk_level in summary['risk_distribution']:
                summary['risk_distribution'][risk_level] += 1
                
        return summary
        
    def export_to_excel(self, filename: str = None) -> str:
        """导出结果到Excel"""
        if not filename:
            filename = f"神经内科量表评估报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
        all_results = self.load_assessment_results()
        
        if not all_results:
            raise ValueError("没有可导出的数据")
            
        # 准备数据
        export_data = []
        for result in all_results:
            patient_info = result.get('patient_info', {})
            score_result = result.get('score_result', {})
            
            export_data.append({
                '评估日期': result.get('assessment_time', ''),
                '量表类型': result.get('scale_type', ''),
                '患者姓名': patient_info.get('name', ''),
                '性别': patient_info.get('gender', ''),
                '年龄': patient_info.get('age', ''),
                '总分': score_result.get('total_score', ''),
                '满分': score_result.get('max_score', ''),
                '百分比': score_result.get('percentage', ''),
                '严重程度': score_result.get('level', ''),
                '风险等级': score_result.get('risk_level', ''),
                '解释': score_result.get('interpretation', ''),
                '评估者': result.get('assessor', '')
            })
            
        # 创建DataFrame并导出
        df = pd.DataFrame(export_data)
        df.to_excel(filename, index=False, engine='openpyxl')
        
        return filename