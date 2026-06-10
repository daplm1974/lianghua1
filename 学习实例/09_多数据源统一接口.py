#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EasyXT[EMOJI] 04 - [EMOJI]
=======================================================

[EMOJI]
1. [EMOJI]
2. [EMOJI]
3. [EMOJI]
4. [EMOJI]
5. [EMOJI]

[EMOJI]8[EMOJI]
- [EMOJI]1[EMOJI]
- [EMOJI]2[EMOJI]
- [EMOJI]3[EMOJI]
- [EMOJI]4[EMOJI]
- [EMOJI]5[EMOJI]
- [EMOJI]6[EMOJI]
- [EMOJI]7[EMOJI]
- [EMOJI]8[EMOJI]

[EMOJI]
[EMOJI] [EMOJI]
[EMOJI] [EMOJI]
[EMOJI] [EMOJI]

[EMOJI]: [EMOJI]quant
[EMOJI]: 2025-09-26
[EMOJI]: 2.0.0 ([EMOJI])
"""

import sys
import os
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import logging
import threading
import queue
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings
warnings.filterwarnings('ignore')

# [EMOJI]
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# [EMOJI]
from easy_xt.realtime_data.providers.tdx_provider import TdxDataProvider
from easy_xt.realtime_data.providers.ths_provider import ThsDataProvider
from easy_xt.realtime_data.providers.eastmoney_provider import EastmoneyDataProvider

# [EMOJI]
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('multi_source_learning.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

class DataSourceHealthMonitor:
    """[EMOJI]"""
    
    def __init__(self):
        self.health_status = {}
        self.performance_metrics = {}
        self.error_counts = {}
        self.last_check_time = {}
        
    def check_source_health(self, source_name: str, provider) -> Dict[str, Any]:
        """[EMOJI]"""
        start_time = time.time()
        health_info = {
            'name': source_name,
            'status': 'unknown',
            'response_time': 0,
            'error_count': self.error_counts.get(source_name, 0),
            'last_check': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        try:
            # [EMOJI]
            if hasattr(provider, 'connect'):
                connected = provider.connect()
                if connected:
                    # [EMOJI]
                    test_quotes = provider.get_realtime_quotes(['000001'])
                    if test_quotes:
                        health_info['status'] = 'healthy'
                        health_info['response_time'] = round((time.time() - start_time) * 1000, 2)
                        # [EMOJI]
                        self.error_counts[source_name] = 0
                    else:
                        health_info['status'] = 'degraded'
                        health_info['response_time'] = round((time.time() - start_time) * 1000, 2)
                else:
                    health_info['status'] = 'disconnected'
            else:
                # [EMOJI]connect[EMOJI]
                test_data = provider.get_hot_stocks() if hasattr(provider, 'get_hot_stocks') else []
                if test_data:
                    health_info['status'] = 'healthy'
                    health_info['response_time'] = round((time.time() - start_time) * 1000, 2)
                    self.error_counts[source_name] = 0
                else:
                    health_info['status'] = 'degraded'
                    
        except Exception as e:
            health_info['status'] = 'error'
            health_info['error_message'] = str(e)
            self.error_counts[source_name] = self.error_counts.get(source_name, 0) + 1
            
        self.health_status[source_name] = health_info
        self.last_check_time[source_name] = time.time()
        
        return health_info
    
    def get_best_source(self, required_capability: str = None) -> str:
        """[EMOJI]"""
        healthy_sources = []
        
        for source_name, status in self.health_status.items():
            if status['status'] == 'healthy':
                healthy_sources.append((source_name, status['response_time']))
        
        if healthy_sources:
            # [EMOJI]
            healthy_sources.sort(key=lambda x: x[1])
            return healthy_sources[0][0]
        
        # [EMOJI]
        if self.health_status:
            status_priority = {'healthy': 0, 'degraded': 1, 'disconnected': 2, 'error': 3}
            best_source = min(self.health_status.items(), 
                            key=lambda x: status_priority.get(x[1]['status'], 999))
            return best_source[0]
        
        return None

class MultiSourceDataFusion:
    """[EMOJI]"""
    
    def __init__(self):
        self.fusion_rules = {
            'price_data': self._fuse_price_data,
            'volume_data': self._fuse_volume_data,
            'concept_data': self._fuse_concept_data,
            'fund_flow_data': self._fuse_fund_flow_data
        }
        
    def _fuse_price_data(self, data_sources: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """[EMOJI]"""
        if not data_sources:
            return pd.DataFrame()
        
        # [EMOJI] > [EMOJI] > [EMOJI]
        priority_order = ['TdxProvider', 'ThsProvider', 'EastmoneyProvider']
        
        for source in priority_order:
            if source in data_sources and not data_sources[source].empty:
                result = data_sources[source].copy()
                result['data_source'] = source
                result['fusion_confidence'] = 0.9 if source == 'TdxProvider' else 0.8
                return result
        
        return pd.DataFrame()
    
    def _fuse_volume_data(self, data_sources: Dict[str, Any]) -> Dict[str, Any]:
        """[EMOJI]"""
        fused_data = {}
        
        for source, data in data_sources.items():
            if data:
                fused_data[f'{source}_volume'] = data
        
        # [EMOJI]
        if fused_data:
            volumes = [v for v in fused_data.values() if isinstance(v, (int, float))]
            if volumes:
                fused_data['fused_volume'] = sum(volumes) / len(volumes)
                fused_data['confidence'] = min(1.0, len(volumes) / 3)  # [EMOJI]
        
        return fused_data
    
    def _fuse_concept_data(self, data_sources: Dict[str, List]) -> List[Dict]:
        """[EMOJI]"""
        concept_scores = {}
        
        for source, concepts in data_sources.items():
            weight = 0.6 if source == 'ThsProvider' else 0.4  # [EMOJI]
            
            for concept in concepts:
                concept_name = concept.get('name', concept.get('concept_name', ''))
                if concept_name:
                    if concept_name not in concept_scores:
                        concept_scores[concept_name] = {'score': 0, 'sources': [], 'details': concept}
                    
                    concept_scores[concept_name]['score'] += weight
                    concept_scores[concept_name]['sources'].append(source)
        
        # [EMOJI]
        fused_concepts = []
        for name, info in sorted(concept_scores.items(), key=lambda x: x[1]['score'], reverse=True):
            fused_concepts.append({
                'name': name,
                'fusion_score': info['score'],
                'source_count': len(info['sources']),
                'sources': info['sources'],
                'details': info['details']
            })
        
        return fused_concepts[:20]  # [EMOJI]20[EMOJI]
    
    def _fuse_fund_flow_data(self, data_sources: Dict[str, Dict]) -> Dict[str, Any]:
        """[EMOJI]"""
        fused_flow = {
            'net_inflow': 0,
            'main_inflow': 0,
            'retail_inflow': 0,
            'confidence': 0,
            'sources': []
        }
        
        total_weight = 0
        for source, flow_data in data_sources.items():
            if flow_data:
                weight = 0.7 if source == 'EastmoneyProvider' else 0.3  # [EMOJI]
                
                fused_flow['net_inflow'] += flow_data.get('net_inflow', 0) * weight
                fused_flow['main_inflow'] += flow_data.get('main_inflow', 0) * weight
                fused_flow['retail_inflow'] += flow_data.get('retail_inflow', 0) * weight
                fused_flow['sources'].append(source)
                total_weight += weight
        
        if total_weight > 0:
            fused_flow['net_inflow'] /= total_weight
            fused_flow['main_inflow'] /= total_weight
            fused_flow['retail_inflow'] /= total_weight
            fused_flow['confidence'] = min(1.0, total_weight)
        
        return fused_flow

class RealTimeAlertSystem:
    """[EMOJI]"""
    
    def __init__(self):
        self.alert_rules = []
        self.alert_history = []
        self.alert_queue = queue.Queue()
        self.running = False
        
    def add_alert_rule(self, rule_name: str, condition_func, alert_level: str = 'INFO'):
        """[EMOJI]"""
        self.alert_rules.append({
            'name': rule_name,
            'condition': condition_func,
            'level': alert_level,
            'last_triggered': None
        })
        
    def check_alerts(self, market_data: Dict[str, Any]):
        """[EMOJI]"""
        current_time = datetime.now()
        
        for rule in self.alert_rules:
            try:
                if rule['condition'](market_data):
                    # [EMOJI]5[EMOJI]
                    if (rule['last_triggered'] is None or 
                        (current_time - rule['last_triggered']).seconds > 300):
                        
                        alert = {
                            'rule_name': rule['name'],
                            'level': rule['level'],
                            'message': f"[EMOJI]: {rule['name']}",
                            'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                            'data': market_data
                        }
                        
                        self.alert_queue.put(alert)
                        self.alert_history.append(alert)
                        rule['last_triggered'] = current_time
                        
                        # [EMOJI]
                        level_emoji = {'INFO': '[EMOJI]', 'WARNING': '[!]', 'ERROR': '[EMOJI]'}
                        print(f"{level_emoji.get(rule['level'], '[EMOJI]')} {alert['message']} - {alert['timestamp']}")
                        
            except Exception as e:
                logger.error(f"[EMOJI] {rule['name']} [EMOJI]: {e}")

class AdvancedMultiSourceAnalyzer:
    """
    [EMOJI]
    
    [EMOJI]
    """
    
    def __init__(self):
        """[EMOJI]"""
        print("[LAUNCH] [EMOJI]...")
        
        # [EMOJI]V3[EMOJI]
        tdx_config = {
            'servers': [
                # [EMOJI]
                {"host": "115.238.90.165", "port": 7709, "name": "[EMOJI]-[EMOJI]"},  # V3[EMOJI]0.19[EMOJI]
                
                # [EMOJI]
                {"host": "119.147.212.81", "port": 7709, "name": "[EMOJI]"},
                {"host": "60.12.136.250", "port": 7709, "name": "[EMOJI]"},
                {"host": "115.238.56.198", "port": 7709, "name": "[EMOJI]"},
                
                # [EMOJI]
                {"host": "218.108.47.69", "port": 7709, "name": "[EMOJI]"},
                {"host": "218.108.98.244", "port": 7709, "name": "[EMOJI]"},
                {"host": "123.125.108.23", "port": 7709, "name": "[EMOJI]"},
                {"host": "180.153.18.171", "port": 7709, "name": "[EMOJI]"},
                
                # [EMOJI]
                {"host": "114.80.63.12", "port": 7709, "name": "[EMOJI]"},
                {"host": "180.153.39.51", "port": 7709, "name": "[EMOJI]"},
                {"host": "103.48.67.20", "port": 7709, "name": "[EMOJI]"}
            ],
            'timeout': 2,  # V3[EMOJI]2[EMOJI]
            'retry_count': 1,  # V3[EMOJI]
            'retry_delay': 0.3  # V3[EMOJI]
        }
        
        # [EMOJI]
        self.providers = {
            'TdxProvider': TdxDataProvider(tdx_config),
            'ThsProvider': ThsDataProvider(),
            'EastmoneyProvider': EastmoneyDataProvider()
        }
        
        # [EMOJI]
        self.health_monitor = DataSourceHealthMonitor()
        self.data_fusion = MultiSourceDataFusion()
        self.alert_system = RealTimeAlertSystem()
        
        # [EMOJI]
        self.cache = {
            'market_data': {},
            'concept_data': {},
            'fund_flow': {},
            'alerts': []
        }
        
        # [EMOJI]
        self.performance_stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'avg_response_time': 0,
            'data_source_usage': {}
        }
        
        logger.info("[EMOJI]")
        print("[OK] [EMOJI]")

    def lesson_01_setup_and_optimization(self):
        """[EMOJI]1[EMOJI]"""
        print("\n[TIP] [EMOJI]")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        
        print("\n[TOOL] 1.1 [EMOJI]")
        print("-" * 50)
        
        connection_results = {}
        
        for name, provider in self.providers.items():
            print(f"\n[EMOJI] {name} [EMOJI]...")
            start_time = time.time()
            
            try:
                if hasattr(provider, 'connect'):
                    success = provider.connect()
                    connect_time = time.time() - start_time
                    
                    if success:
                        print(f"[OK] {name} [EMOJI]: {connect_time:.3f}[EMOJI]")
                        if hasattr(provider, 'current_server') and provider.current_server:
                            print(f"   [EMOJI] [EMOJI]: {provider.current_server.get('name', 'Unknown')}")
                            print(f"   [EMOJI] [EMOJI]: {provider.current_server.get('host', 'Unknown')}:{provider.current_server.get('port', 'Unknown')}")
                        connection_results[name] = {'status': 'success', 'time': connect_time}
                    else:
                        print(f"[X] {name} [EMOJI]")
                        connection_results[name] = {'status': 'failed', 'time': connect_time}
                else:
                    # [EMOJI]
                    test_data = provider.get_hot_stocks() if hasattr(provider, 'get_hot_stocks') else []
                    connect_time = time.time() - start_time
                    
                    if test_data:
                        print(f"[OK] {name} [EMOJI]: {connect_time:.3f}[EMOJI]")
                        connection_results[name] = {'status': 'success', 'time': connect_time}
                    else:
                        print(f"[!] {name} [EMOJI]")
                        connection_results[name] = {'status': 'empty', 'time': connect_time}
                        
            except Exception as e:
                connect_time = time.time() - start_time
                print(f"[X] {name} [EMOJI]: {e}")
                connection_results[name] = {'status': 'error', 'time': connect_time, 'error': str(e)}
        
        print(f"\n[CHART] 1.2 [EMOJI]")
        print("-" * 50)
        
        successful_connections = [r for r in connection_results.values() if r['status'] == 'success']
        if successful_connections:
            avg_time = sum(r['time'] for r in successful_connections) / len(successful_connections)
            fastest = min(successful_connections, key=lambda x: x['time'])
            slowest = max(successful_connections, key=lambda x: x['time'])
            
            print(f"[OK] [EMOJI]: {len(successful_connections)}/{len(self.providers)}")
            print(f"[EMOJI] [EMOJI]: {avg_time:.3f}[EMOJI]")
            print(f"[LAUNCH] [EMOJI]: {fastest['time']:.3f}[EMOJI]")
            print(f"[EMOJI] [EMOJI]: {slowest['time']:.3f}[EMOJI]")
            
            # [EMOJI]
            if avg_time < 0.5:
                print("[EMOJI] [EMOJI]: [EMOJI]")
            elif avg_time < 1.0:
                print("[EMOJI] [EMOJI]: [EMOJI]")
            elif avg_time < 2.0:
                print("[EMOJI] [EMOJI]: [EMOJI]")
            else:
                print("[EMOJI] [EMOJI]: [EMOJI]")
        else:
            print("[X] [EMOJI]")
        
        print(f"\n[TIP] 1.3 [EMOJI]")
        print("-" * 50)
        
        for name, result in connection_results.items():
            if result['status'] == 'success':
                if result['time'] < 0.5:
                    print(f"[OK] {name}: [EMOJI]")
                elif result['time'] < 2.0:
                    print(f"[EMOJI] {name}: [EMOJI]")
                else:
                    print(f"[TOOL] {name}: [EMOJI]")
            elif result['status'] == 'failed':
                print(f"[TOOL] {name}: [EMOJI]")
            elif result['status'] == 'error':
                print(f"[EMOJI] {name}: [EMOJI]: {result.get('error', '')}")
        
        print(f"\n[BOOK] [EMOJI]:")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        
        return connection_results

    def lesson_02_health_monitoring(self):
        """[EMOJI]2[EMOJI]"""
        print("\n[TIP] [EMOJI]")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        
        print("\n[EMOJI] 2.1 [EMOJI]")
        print("-" * 50)
        
        health_results = {}
        
        for name, provider in self.providers.items():
            print(f"\n[EMOJI] {name} [EMOJI]...")
            health_info = self.health_monitor.check_source_health(name, provider)
            health_results[name] = health_info
            
            # [EMOJI]
            status_emoji = {
                'healthy': '[EMOJI]',
                'degraded': '[EMOJI]', 
                'disconnected': '[EMOJI]',
                'error': '[EMOJI]',
                'unknown': '[EMOJI]'
            }
            
            emoji = status_emoji.get(health_info['status'], '[EMOJI]')
            print(f"{emoji} [EMOJI]: {health_info['status']}")
            print(f"[TIME] [EMOJI]: {health_info['response_time']}ms")
            print(f"[X] [EMOJI]: {health_info['error_count']}")
            print(f"[EMOJI] [EMOJI]: {health_info['last_check']}")
            
            if 'error_message' in health_info:
                print(f"[EMOJI] [EMOJI]: {health_info['error_message']}")
        
        print(f"\n[TARGET] 2.2 [EMOJI]")
        print("-" * 50)
        
        # [EMOJI]
        scenarios = [
            ('[EMOJI]', 'quotes'),
            ('[EMOJI]', 'concepts'),
            ('[EMOJI]', 'fund_flow'),
            ('[EMOJI]', None)
        ]
        
        for scenario_name, capability in scenarios:
            best_source = self.health_monitor.get_best_source(capability)
            if best_source:
                health_info = health_results[best_source]
                print(f"[CHART] {scenario_name}: [EMOJI] {best_source}")
                print(f"   [EMOJI]: {health_info['status']}, [EMOJI]: {health_info['response_time']}ms")
            else:
                print(f"[X] {scenario_name}: [EMOJI]")
        
        print(f"\n[UP] 2.3 [EMOJI]")
        print("-" * 50)
        
        # [EMOJI]
        healthy_count = sum(1 for h in health_results.values() if h['status'] == 'healthy')
        total_count = len(health_results)
        availability = (healthy_count / total_count) * 100 if total_count > 0 else 0
        
        avg_response_time = sum(h['response_time'] for h in health_results.values() if h['response_time'] > 0)
        avg_response_time = avg_response_time / len([h for h in health_results.values() if h['response_time'] > 0]) if any(h['response_time'] > 0 for h in health_results.values()) else 0
        
        print(f"[TARGET] [EMOJI]: {availability:.1f}% ({healthy_count}/{total_count})")
        print(f"[EMOJI] [EMOJI]: {avg_response_time:.1f}ms")
        print(f"[R] [EMOJI]: {'[EMOJI]' if healthy_count > 1 else '[EMOJI]'}")
        
        # [EMOJI]
        print(f"\n[EMOJI] 2.4 [EMOJI]")
        print("-" * 50)
        print("[OK] [EMOJI]: 60[EMOJI]")
        print("[OK] [EMOJI]: [EMOJI]")
        print("[OK] [EMOJI]: [EMOJI]")
        print("[OK] [EMOJI]: 24[EMOJI]")
        
        print(f"\n[BOOK] [EMOJI]:")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        
        return health_results

    def lesson_03_data_fusion(self):
        """[EMOJI]3[EMOJI]"""
        print("\n[TIP] [EMOJI]")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        
        print("\n[R] 3.1 [EMOJI]")
        print("-" * 50)
        
        # [EMOJI]
        test_codes = ['000001', '000002', '600000']
        fusion_results = {}
        
        for code in test_codes:
            print(f"\n[EMOJI] {code} [EMOJI]...")
            source_data = {}
            
            for name, provider in self.providers.items():
                try:
                    if hasattr(provider, 'get_realtime_quotes'):
                        quotes = provider.get_realtime_quotes([code])
                        if quotes:
                            source_data[name] = pd.DataFrame(quotes)
                            print(f"[OK] {name}: [EMOJI] {len(quotes)} [EMOJI]")
                        else:
                            print(f"[!] {name}: [EMOJI]")
                except Exception as e:
                    print(f"[X] {name}: [EMOJI] - {e}")
            
            # [EMOJI]
            if source_data:
                fused_data = self.data_fusion._fuse_price_data(source_data)
                if not fused_data.empty:
                    fusion_results[code] = fused_data
                    print(f"[TARGET] [EMOJI]: [EMOJI] {fused_data.iloc[0]['data_source']} [EMOJI]")
                    print(f"[CHART] [EMOJI]: {fused_data.iloc[0]['fusion_confidence']:.1%}")
                else:
                    print(f"[X] [EMOJI]: [EMOJI]")
            else:
                print(f"[X] [EMOJI]")
        
        print(f"\n[CHART] 3.2 [EMOJI]")
        print("-" * 50)
        
        concept_sources = {}
        
        # [EMOJI]
        try:
            if hasattr(self.providers['ThsProvider'], 'get_concept_ranks'):
                ths_concepts = self.providers['ThsProvider'].get_concept_ranks(limit=10)
                if ths_concepts:
                    concept_sources['ThsProvider'] = ths_concepts
                    print(f"[OK] [EMOJI]: [EMOJI] {len(ths_concepts)} [EMOJI]")
        except Exception as e:
            print(f"[X] [EMOJI]: {e}")
        
        # [EMOJI]
        try:
            if hasattr(self.providers['EastmoneyProvider'], 'get_concept_boards'):
                em_concepts = self.providers['EastmoneyProvider'].get_concept_boards(limit=10)
                if em_concepts:
                    concept_sources['EastmoneyProvider'] = em_concepts
                    print(f"[OK] [EMOJI]: [EMOJI] {len(em_concepts)} [EMOJI]")
        except Exception as e:
            print(f"[X] [EMOJI]: {e}")
        
        # [EMOJI]
        if concept_sources:
            fused_concepts = self.data_fusion._fuse_concept_data(concept_sources)
            print(f"\n[TARGET] [EMOJI] ([EMOJI]5[EMOJI]):")
            for i, concept in enumerate(fused_concepts[:5], 1):
                print(f"{i}. {concept['name']}")
                print(f"   [EMOJI]: {concept['fusion_score']:.2f}")
                print(f"   [EMOJI]: {concept['source_count']}")
                print(f"   [EMOJI]: {', '.join(concept['sources'])}")
        else:
            print("[X] [EMOJI]")
        
        print(f"\n[SEARCH] 3.3 [EMOJI]")
        print("-" * 50)
        
        quality_metrics = {
            'completeness': 0,  # [EMOJI]
            'consistency': 0,   # [EMOJI]
            'timeliness': 0,    # [EMOJI]
            'accuracy': 0       # [EMOJI]
        }
        
        # [EMOJI]
        total_sources = len(self.providers)
        available_sources = len([name for name, provider in self.providers.items() 
                               if self.health_monitor.health_status.get(name, {}).get('status') == 'healthy'])
        quality_metrics['completeness'] = (available_sources / total_sources) * 100
        
        # [EMOJI]
        if fusion_results:
            consistency_scores = []
            for code, data in fusion_results.items():
                if 'fusion_confidence' in data.columns:
                    consistency_scores.append(data.iloc[0]['fusion_confidence'])
            quality_metrics['consistency'] = (sum(consistency_scores) / len(consistency_scores)) * 100 if consistency_scores else 0
        
        # [EMOJI]
        response_times = [h.get('response_time', 0) for h in self.health_monitor.health_status.values()]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        quality_metrics['timeliness'] = max(0, 100 - (avg_response_time / 10))  # [EMOJI]
        
        # [EMOJI]
        error_counts = [h.get('error_count', 0) for h in self.health_monitor.health_status.values()]
        total_errors = sum(error_counts)
        quality_metrics['accuracy'] = max(0, 100 - (total_errors * 10))  # [EMOJI]
        
        print("[UP] [EMOJI]:")
        for metric, score in quality_metrics.items():
            metric_names = {
                'completeness': '[EMOJI]',
                'consistency': '[EMOJI]', 
                'timeliness': '[EMOJI]',
                'accuracy': '[EMOJI]'
            }
            
            if score >= 90:
                grade = "[EMOJI] [EMOJI]"
            elif score >= 80:
                grade = "[EMOJI] [OK]"
            elif score >= 70:
                grade = "[EMOJI] [!]"
            else:
                grade = "[EMOJI] [X]"
                
            print(f"  {metric_names[metric]}: {score:.1f}% - {grade}")
        
        overall_quality = sum(quality_metrics.values()) / len(quality_metrics)
        print(f"\n[TARGET] [EMOJI]: {overall_quality:.1f}%")
        
        print(f"\n[BOOK] [EMOJI]:")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        
        return fusion_results, quality_metrics

    def lesson_04_realtime_monitoring(self):
        """[EMOJI]4[EMOJI]"""
        print("\n[TIP] [EMOJI]")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        
        print("\n[CHART] 4.1 [EMOJI]")
        print("-" * 50)
        
        # [EMOJI]
        monitor_stocks = ['000001', '000002', '600000', '600036', '000858']
        print(f"[EMOJI] [EMOJI]: {', '.join(monitor_stocks)}")
        
        # [EMOJI]
        realtime_data = {}
        
        for code in monitor_stocks:
            try:
                # [EMOJI]
                best_source = self.health_monitor.get_best_source('quotes')
                if best_source and best_source in self.providers:
                    provider = self.providers[best_source]
                    if hasattr(provider, 'get_realtime_quotes'):
                        quotes = provider.get_realtime_quotes([code])
                        if quotes:
                            realtime_data[code] = quotes[0]
                            print(f"[OK] {code}: [EMOJI] {quotes[0].get('price', 0):.2f}, [EMOJI] {quotes[0].get('change_pct', 0):.2f}%")
                        else:
                            print(f"[!] {code}: [EMOJI]")
                    else:
                        print(f"[X] {code}: [EMOJI]")
                else:
                    print(f"[X] {code}: [EMOJI]")
            except Exception as e:
                print(f"[X] {code}: [EMOJI] - {e}")
        
        print(f"\n[EMOJI] 4.2 [EMOJI]")
        print("-" * 50)
        
        # [EMOJI]
        def price_spike_alert(data):
            """[EMOJI]"""
            for code, quote in data.items():
                change_pct = abs(quote.get('change_pct', 0))
                if change_pct > 5:  # [EMOJI]5%
                    return True
            return False
        
        def volume_spike_alert(data):
            """[EMOJI]"""
            for code, quote in data.items():
                volume = quote.get('volume', 0)
                if volume > 10000000:  # [EMOJI]1000[EMOJI]
                    return True
            return False
        
        def price_limit_alert(data):
            """[EMOJI]"""
            for code, quote in data.items():
                change_pct = quote.get('change_pct', 0)
                if abs(change_pct) > 9.5:  # [EMOJI]
                    return True
            return False
        
        # [EMOJI]
        self.alert_system.add_alert_rule("[EMOJI]", price_spike_alert, "WARNING")
        self.alert_system.add_alert_rule("[EMOJI]", volume_spike_alert, "INFO")
        self.alert_system.add_alert_rule("[EMOJI]", price_limit_alert, "ERROR")
        
        print("[OK] [EMOJI]: [EMOJI] > 5%")
        print("[OK] [EMOJI]: [EMOJI] > 1000[EMOJI]")
        print("[OK] [EMOJI]: [EMOJI] > 9.5%")
        
        print(f"\n[EMOJI] 4.3 [EMOJI]")
        print("-" * 50)
        
        # [EMOJI]
        if realtime_data:
            print("[EMOJI]...")
            self.alert_system.check_alerts(realtime_data)
            
            # [EMOJI]
            if self.alert_system.alert_history:
                print(f"[EMOJI] [EMOJI] {len(self.alert_system.alert_history)} [EMOJI]:")
                for alert in self.alert_system.alert_history[-5:]:  # [EMOJI]5[EMOJI]
                    print(f"  {alert['timestamp']}: {alert['message']} [{alert['level']}]")
            else:
                print("[OK] [EMOJI]")
        else:
            print("[X] [EMOJI]")
        
        print(f"\n[UP] 4.4 [EMOJI]")
        print("-" * 50)
        
        if realtime_data:
            # [EMOJI]
            prices = [quote.get('price', 0) for quote in realtime_data.values()]
            changes = [quote.get('change_pct', 0) for quote in realtime_data.values()]
            volumes = [quote.get('volume', 0) for quote in realtime_data.values()]
            
            avg_price = sum(prices) / len(prices) if prices else 0
            avg_change = sum(changes) / len(changes) if changes else 0
            total_volume = sum(volumes)
            
            print(f"[CHART] [EMOJI]: {len(realtime_data)}")
            print(f"[MONEY] [EMOJI]: {avg_price:.2f}")
            print(f"[UP] [EMOJI]: {avg_change:.2f}%")
            print(f"[CHART] [EMOJI]: {total_volume:,}")
            
            # [EMOJI]
            up_count = sum(1 for change in changes if change > 0)
            down_count = sum(1 for change in changes if change < 0)
            
            if up_count > down_count:
                sentiment = "[EMOJI] [UP]"
            elif down_count > up_count:
                sentiment = "[EMOJI] [EMOJI]"
            else:
                sentiment = "[EMOJI] [EMOJI]"
            
            print(f"[EMOJI] [EMOJI]: {sentiment} ([EMOJI]:{up_count}, [EMOJI]:{down_count})")
        
        print(f"\n[BOOK] [EMOJI]:")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        
        return realtime_data

    def lesson_05_concept_analysis(self):
        """[EMOJI]5[EMOJI]"""
        print("\n[TIP] [EMOJI]")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        
        print("\n[EMOJI] 5.1 [EMOJI]")
        print("-" * 50)
        
        concept_data = {}
        
        # [EMOJI]
        try:
            ths_provider = self.providers['ThsProvider']
            if hasattr(ths_provider, 'get_concept_ranks'):
                ths_concepts = ths_provider.get_concept_ranks(limit=15)
                if ths_concepts:
                    concept_data['ThsProvider'] = ths_concepts
                    print(f"[OK] [EMOJI]: {len(ths_concepts)} [EMOJI]")
                    
                    # [EMOJI]5[EMOJI]
                    print("[EMOJI] [EMOJI] TOP5:")
                    for i, concept in enumerate(ths_concepts[:5], 1):
                        name = concept.get('name', concept.get('concept_name', 'Unknown'))
                        heat = concept.get('heat', concept.get('popularity', 0))
                        print(f"  {i}. {name} - [EMOJI]: {heat}")
        except Exception as e:
            print(f"[X] [EMOJI]: {e}")
        
        # [EMOJI]
        try:
            em_provider = self.providers['EastmoneyProvider']
            if hasattr(em_provider, 'get_concept_boards'):
                em_concepts = em_provider.get_concept_boards(limit=15)
                if em_concepts:
                    concept_data['EastmoneyProvider'] = em_concepts
                    print(f"[OK] [EMOJI]: {len(em_concepts)} [EMOJI]")
                    
                    # [EMOJI]5[EMOJI]
                    print("[CHART] [EMOJI] TOP5:")
                    for i, concept in enumerate(em_concepts[:5], 1):
                        name = concept.get('name', concept.get('board_name', 'Unknown'))
                        change = concept.get('change_pct', concept.get('pct_change', 0))
                        print(f"  {i}. {name} - [EMOJI]: {change:.2f}%")
        except Exception as e:
            print(f"[X] [EMOJI]: {e}")
        
        print(f"\n[TARGET] 5.2 [EMOJI]")
        print("-" * 50)
        
        if concept_data:
            # [EMOJI]
            fused_concepts = self.data_fusion._fuse_concept_data(concept_data)
            
            if fused_concepts:
                print(f"[R] [EMOJI] {len(concept_data)} [EMOJI]")
                print(f"[CHART] [EMOJI]: {len(fused_concepts)} [EMOJI]")
                
                print("\n[EMOJI] [EMOJI] TOP10:")
                for i, concept in enumerate(fused_concepts[:10], 1):
                    print(f"{i:2d}. {concept['name']}")
                    print(f"     [EMOJI]: {concept['fusion_score']:.2f}")
                    print(f"     [EMOJI]: {', '.join(concept['sources'])}")
                    print(f"     [EMOJI]: {concept['source_count']}/2")
                
                # [EMOJI]
                print(f"\n[UP] 5.3 [EMOJI]")
                print("-" * 50)
                
                # [EMOJI]
                hot_concepts = [c for c in fused_concepts if c['fusion_score'] >= 1.0]
                warm_concepts = [c for c in fused_concepts if 0.5 <= c['fusion_score'] < 1.0]
                cold_concepts = [c for c in fused_concepts if c['fusion_score'] < 0.5]
                
                print(f"[EMOJI] [EMOJI] ([EMOJI]≥1.0): {len(hot_concepts)} [EMOJI]")
                for concept in hot_concepts[:3]:
                    print(f"   • {concept['name']} ({concept['fusion_score']:.2f})")
                
                print(f"[EMOJI] [EMOJI] (0.5≤[EMOJI]<1.0): {len(warm_concepts)} [EMOJI]")
                for concept in warm_concepts[:3]:
                    print(f"   • {concept['name']} ({concept['fusion_score']:.2f})")
                
                print(f"[EMOJI] [EMOJI] ([EMOJI]<0.5): {len(cold_concepts)} [EMOJI]")
                
                # [EMOJI]
                print(f"\n[SEARCH] 5.4 [EMOJI]")
                print("-" * 50)
                
                consistent_concepts = [c for c in fused_concepts if c['source_count'] >= 2]
                unique_concepts = [c for c in fused_concepts if c['source_count'] == 1]
                
                print(f"[OK] [EMOJI]: {len(consistent_concepts)} [EMOJI] ({len(consistent_concepts)/len(fused_concepts)*100:.1f}%)")
                print(f"[!] [EMOJI]: {len(unique_concepts)} [EMOJI] ({len(unique_concepts)/len(fused_concepts)*100:.1f}%)")
                
                if consistent_concepts:
                    print("\n[TARGET] [EMOJI] TOP5:")
                    for i, concept in enumerate(consistent_concepts[:5], 1):
                        print(f"  {i}. {concept['name']} - [EMOJI]: {', '.join(concept['sources'])}")
                
                # [EMOJI]
                print(f"\n[TIP] 5.5 [EMOJI]")
                print("-" * 50)
                
                if hot_concepts:
                    print("[TARGET] [EMOJI]:")
                    for concept in hot_concepts[:3]:
                        print(f"  • {concept['name']}: [EMOJI]")
                
                if consistent_concepts:
                    print("[OK] [EMOJI]:")
                    for concept in consistent_concepts[:2]:
                        if concept not in hot_concepts:
                            print(f"  • {concept['name']}: [EMOJI]")
                
                print("[!] [EMOJI]: [EMOJI]")
                
                print(f"\n[BOOK] [EMOJI]:")
                print("  • [EMOJI]")
                print("  • [EMOJI]")
                print("  • [EMOJI]")
                
                return fused_concepts
            else:
                print("[X] [EMOJI]")
        else:
            print("[X] [EMOJI]")
        
        return []

    def lesson_06_fund_flow_analysis(self):
        """[EMOJI]6[EMOJI]"""
        print("\n[TIP] [EMOJI]")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        
        print("\n[MONEY] 6.1 [EMOJI]")
        print("-" * 50)
        
        fund_flow_data = {}
        monitor_stocks = ['000001', '000002', '600000', '600036', '000858']
        
        # [EMOJI]
        print("[CHART] [EMOJI]...")
        import random
        for code in monitor_stocks:
            fund_flow_data[code] = {
                'net_inflow': random.randint(-50000, 50000),
                'main_inflow': random.randint(-30000, 30000),
                'retail_inflow': random.randint(-20000, 20000),
                'super_large_inflow': random.randint(-15000, 15000),
                'large_inflow': random.randint(-15000, 15000),
                'medium_inflow': random.randint(-10000, 10000),
                'small_inflow': random.randint(-10000, 10000)
            }
            print(f"[CHART] {code}: [EMOJI] {fund_flow_data[code]['net_inflow']:,.0f}[EMOJI]")
        
        print(f"\n[EMOJI] 6.2 [EMOJI]")
        print("-" * 50)
        
        if fund_flow_data:
            # [EMOJI]
            main_inflow_stocks = []
            main_outflow_stocks = []
            
            for code, flow in fund_flow_data.items():
                main_flow = flow.get('main_inflow', 0)
                if main_flow > 1000:  # [EMOJI]1000[EMOJI]
                    main_inflow_stocks.append((code, main_flow))
                elif main_flow < -1000:  # [EMOJI]1000[EMOJI]
                    main_outflow_stocks.append((code, main_flow))
            
            # [EMOJI]
            main_inflow_stocks.sort(key=lambda x: x[1], reverse=True)
            main_outflow_stocks.sort(key=lambda x: x[1])
            
            print("[EMOJI] [EMOJI]:")
            if main_inflow_stocks:
                for code, flow in main_inflow_stocks:
                    print(f"  [UP] {code}: +{flow:,.0f}[EMOJI]")
            else:
                print("  [EMOJI]")
            
            print("\n[EMOJI] [EMOJI]:")
            if main_outflow_stocks:
                for code, flow in main_outflow_stocks:
                    print(f"  [EMOJI] {code}: {flow:,.0f}[EMOJI]")
            else:
                print("  [EMOJI]")
            
            print(f"\n[TARGET] 6.3 [EMOJI]")
            print("-" * 50)
            
            # [EMOJI]
            patterns = {
                'strong_inflow': [],      # [EMOJI]
                'weak_inflow': [],        # [EMOJI]
                'strong_outflow': [],     # [EMOJI]
                'weak_outflow': [],       # [EMOJI]
                'balanced': []            # [EMOJI]
            }
            
            for code, flow in fund_flow_data.items():
                net_flow = flow.get('net_inflow', 0)
                main_flow = flow.get('main_inflow', 0)
                
                if net_flow > 5000 and main_flow > 0:
                    patterns['strong_inflow'].append(code)
                elif net_flow > 0 and main_flow > 0:
                    patterns['weak_inflow'].append(code)
                elif net_flow < -5000 and main_flow < 0:
                    patterns['strong_outflow'].append(code)
                elif net_flow < 0 and main_flow < 0:
                    patterns['weak_outflow'].append(code)
                else:
                    patterns['balanced'].append(code)
            
            pattern_names = {
                'strong_inflow': '[EMOJI]',
                'weak_inflow': '[EMOJI]',
                'strong_outflow': '[EMOJI]',
                'weak_outflow': '[EMOJI]',
                'balanced': '[EMOJI]'
            }
            
            pattern_emojis = {
                'strong_inflow': '[LAUNCH]',
                'weak_inflow': '[UP]',
                'strong_outflow': '[EMOJI]',
                'weak_outflow': 'v',
                'balanced': '[EMOJI]'
            }
            
            for pattern, stocks in patterns.items():
                if stocks:
                    emoji = pattern_emojis[pattern]
                    name = pattern_names[pattern]
                    print(f"{emoji} {name}: {', '.join(stocks)}")
            
            print(f"\n[CHART] 6.4 [EMOJI]")
            print("-" * 50)
            
            # [EMOJI]
            total_net_inflow = sum(flow.get('net_inflow', 0) for flow in fund_flow_data.values())
            total_main_inflow = sum(flow.get('main_inflow', 0) for flow in fund_flow_data.values())
            total_retail_inflow = sum(flow.get('retail_inflow', 0) for flow in fund_flow_data.values())
            
            print(f"[MONEY] [EMOJI]: {total_net_inflow:,.0f}[EMOJI]")
            print(f"[EMOJI] [EMOJI]: {total_main_inflow:,.0f}[EMOJI]")
            print(f"[EMOJI] [EMOJI]: {total_retail_inflow:,.0f}[EMOJI]")
            
            # [EMOJI]
            if total_net_inflow > 10000:
                market_sentiment = "[EMOJI] [LAUNCH]"
            elif total_net_inflow > 0:
                market_sentiment = "[EMOJI] [UP]"
            elif total_net_inflow > -10000:
                market_sentiment = "[EMOJI] [!]"
            else:
                market_sentiment = "[EMOJI] [EMOJI]"
            
            print(f"[EMOJI] [EMOJI]: {market_sentiment}")
            
            # [EMOJI]
            if abs(total_main_inflow) > abs(total_retail_inflow):
                dominant_force = "[EMOJI]"
            else:
                dominant_force = "[EMOJI]"
            
            print(f"[EMOJI] [EMOJI]: {dominant_force}")
            
            print(f"\n[TIP] 6.5 [EMOJI]")
            print("-" * 50)
            
            if patterns['strong_inflow']:
                print(f"[TARGET] [EMOJI]: {', '.join(patterns['strong_inflow'])} - [EMOJI]")
            
            if patterns['strong_outflow']:
                print(f"[!] [EMOJI]: {', '.join(patterns['strong_outflow'])} - [EMOJI]")
            
            if total_main_inflow > 0 and total_retail_inflow < 0:
                print("[TIP] [EMOJI]: [EMOJI]")
            elif total_main_inflow < 0 and total_retail_inflow > 0:
                print("[!] [EMOJI]: [EMOJI]")
            
            print(f"\n[BOOK] [EMOJI]:")
            print("  • [EMOJI]")
            print("  • [EMOJI]")
            print("  • [EMOJI]")
            
            return fund_flow_data
        else:
            print("[X] [EMOJI]")
            return {}

    def lesson_07_signal_generation(self):
        """[EMOJI]7[EMOJI]"""
        print("\n[TIP] [EMOJI]")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        
        print("\n[TARGET] 7.1 [EMOJI]")
        print("-" * 50)
        
        # [EMOJI]
        signal_weights = {
            'price_momentum': 0.25,      # [EMOJI]
            'volume_pattern': 0.20,      # [EMOJI]
            'fund_flow': 0.25,          # [EMOJI]
            'concept_heat': 0.15,        # [EMOJI]
            'technical_indicator': 0.15   # [EMOJI]
        }
        
        print("[CHART] [EMOJI]:")
        for signal, weight in signal_weights.items():
            signal_names = {
                'price_momentum': '[EMOJI]',
                'volume_pattern': '[EMOJI]',
                'fund_flow': '[EMOJI]',
                'concept_heat': '[EMOJI]',
                'technical_indicator': '[EMOJI]'
            }
            print(f"  {signal_names[signal]}: {weight:.0%}")
        
        print(f"\n[UP] 7.2 [EMOJI]")
        print("-" * 50)
        
        # [EMOJI]
        test_stocks = ['000001', '000002', '600000']
        stock_signals = {}
        
        for code in test_stocks:
            print(f"\n[EMOJI] {code} [EMOJI]...")
            
            signals = {
                'price_momentum': 0,
                'volume_pattern': 0,
                'fund_flow': 0,
                'concept_heat': 0,
                'technical_indicator': 0
            }
            
            # [EMOJI]
            import random
            
            # 1. [EMOJI]
            change_pct = random.uniform(-5, 8)
            if change_pct > 3:
                signals['price_momentum'] = 0.8
            elif change_pct > 1:
                signals['price_momentum'] = 0.6
            elif change_pct > 0:
                signals['price_momentum'] = 0.4
            elif change_pct > -1:
                signals['price_momentum'] = 0.2
            else:
                signals['price_momentum'] = 0.0
            
            print(f"  [UP] [EMOJI]: {change_pct:.2f}% → [EMOJI]: {signals['price_momentum']:.1f}")
            
            # 2. [EMOJI]
            volume = random.randint(5000000, 100000000)
            if volume > 50000000:
                signals['volume_pattern'] = 0.8
            elif volume > 20000000:
                signals['volume_pattern'] = 0.6
            elif volume > 10000000:
                signals['volume_pattern'] = 0.4
            else:
                signals['volume_pattern'] = 0.2
            
            print(f"  [CHART] [EMOJI]: {volume:,} → [EMOJI]: {signals['volume_pattern']:.1f}")
            
            # 3. [EMOJI]
            net_inflow = random.randint(-10000, 10000)
            if net_inflow > 5000:
                signals['fund_flow'] = 0.8
            elif net_inflow > 1000:
                signals['fund_flow'] = 0.6
            elif net_inflow > 0:
                signals['fund_flow'] = 0.4
            elif net_inflow > -1000:
                signals['fund_flow'] = 0.2
            else:
                signals['fund_flow'] = 0.0
            
            print(f"  [MONEY] [EMOJI]: {net_inflow:,}[EMOJI] → [EMOJI]: {signals['fund_flow']:.1f}")
            
            # 4. [EMOJI]
            concept_heat = random.uniform(0, 1)
            signals['concept_heat'] = concept_heat
            print(f"  [EMOJI] [EMOJI]: {concept_heat:.2f} → [EMOJI]: {signals['concept_heat']:.1f}")
            
            # 5. [EMOJI]
            tech_score = random.uniform(0, 1)
            signals['technical_indicator'] = tech_score
            print(f"  [CHART] [EMOJI]: {tech_score:.2f} → [EMOJI]: {signals['technical_indicator']:.1f}")
            
            # [EMOJI]
            composite_signal = sum(signals[key] * signal_weights[key] for key in signals.keys())
            
            stock_signals[code] = {
                'individual_signals': signals,
                'composite_signal': composite_signal
            }
            
            print(f"  [TARGET] [EMOJI]: {composite_signal:.3f}")
        
        print(f"\n[EMOJI] 7.3 [EMOJI]")
        print("-" * 50)
        
        # [EMOJI]
        ranked_stocks = sorted(stock_signals.items(), 
                             key=lambda x: x[1]['composite_signal'], 
                             reverse=True)
        
        print("[CHART] [EMOJI]:")
        for i, (code, data) in enumerate(ranked_stocks, 1):
            signal_strength = data['composite_signal']
            
            if signal_strength >= 0.7:
                recommendation = "[EMOJI] [LAUNCH]"
                color = "[EMOJI]"
            elif signal_strength >= 0.5:
                recommendation = "[EMOJI] [UP]"
                color = "[EMOJI]"
            elif signal_strength >= 0.3:
                recommendation = "[EMOJI] [EMOJI]"
                color = "[EMOJI]"
            else:
                recommendation = "[EMOJI] [!]"
                color = "[EMOJI]"
            
            print(f"{i}. {code}: {signal_strength:.3f} {color} - {recommendation}")
        
        print(f"\n[EMOJI] 7.4 [EMOJI]")
        print("-" * 50)
        
        # [EMOJI]
        if ranked_stocks:
            top_stock = ranked_stocks[0]
            code, data = top_stock
            
            print(f"[TARGET] [EMOJI]: {code}")
            print("[EMOJI]:")
            
            signal_names = {
                'price_momentum': '[EMOJI]',
                'volume_pattern': '[EMOJI]',
                'fund_flow': '[EMOJI]',
                'concept_heat': '[EMOJI]',
                'technical_indicator': '[EMOJI]'
            }
            
            for signal_type, strength in data['individual_signals'].items():
                weight = signal_weights[signal_type]
                contribution = strength * weight
                name = signal_names[signal_type]
                
                print(f"  {name}: {strength:.3f} × {weight:.0%} = {contribution:.3f}")
            
            print(f"  [EMOJI]: {data['composite_signal']:.3f}")
        
        print(f"\n[TIP] 7.5 [EMOJI]")
        print("-" * 50)
        
        strong_signals = [code for code, data in stock_signals.items() if data['composite_signal'] >= 0.6]
        medium_signals = [code for code, data in stock_signals.items() if 0.4 <= data['composite_signal'] < 0.6]
        weak_signals = [code for code, data in stock_signals.items() if data['composite_signal'] < 0.4]
        
        if strong_signals:
            print(f"[LAUNCH] [EMOJI] ({len(strong_signals)}[EMOJI]): {', '.join(strong_signals)}")
            print("   [EMOJI]: [EMOJI]")
        
        if medium_signals:
            print(f"[UP] [EMOJI] ({len(medium_signals)}[EMOJI]): {', '.join(medium_signals)}")
            print("   [EMOJI]: [EMOJI]")
        
        if weak_signals:
            print(f"[!] [EMOJI] ({len(weak_signals)}[EMOJI]): {', '.join(weak_signals)}")
            print("   [EMOJI]: [EMOJI]")
        
        print("\n[!] [EMOJI]:")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        
        print(f"\n[BOOK] [EMOJI]:")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        
        return stock_signals

    def lesson_08_alert_system(self):
        """[EMOJI]8[EMOJI]"""
        print("\n[TIP] [EMOJI]")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        
        print("\n[EMOJI] 8.1 [EMOJI]")
        print("-" * 50)
        
        print("[EMOJI]:")
        print("  [CHART] [EMOJI]: [EMOJI]")
        print("  [SEARCH] [EMOJI]: [EMOJI]")
        print("  [EMOJI] [EMOJI]: [EMOJI]")
        print("  [UP] [EMOJI]: [EMOJI]")
        print("  [EMOJI] [EMOJI]: [EMOJI]")
        
        print(f"\n[EMOJI] 8.2 [EMOJI]")
        print("-" * 50)
        
        # [EMOJI]
        self.alert_system.alert_rules = []
        
        # [EMOJI]
        def price_breakout_alert(data):
            """[EMOJI]"""
            for code, quote in data.items():
                change_pct = abs(quote.get('change_pct', 0))
                if change_pct > 7:
                    return True
            return False
        
        def price_limit_approaching_alert(data):
            """[EMOJI]"""
            for code, quote in data.items():
                change_pct = quote.get('change_pct', 0)
                if abs(change_pct) > 9:
                    return True
            return False
        
        def volume_surge_alert(data):
            """[EMOJI]"""
            for code, quote in data.items():
                volume = quote.get('volume', 0)
                if volume > 100000000:
                    return True
            return False
        
        def large_fund_inflow_alert(data):
            """[EMOJI]"""
            import random
            return random.random() > 0.8
        
        def large_fund_outflow_alert(data):
            """[EMOJI]"""
            import random
            return random.random() > 0.9
        
        def technical_signal_alert(data):
            """[EMOJI]"""
            import random
            return random.random() > 0.85
        
        def market_sentiment_alert(data):
            """[EMOJI]"""
            if len(data) >= 3:
                changes = [quote.get('change_pct', 0) for quote in data.values()]
                avg_change = sum(changes) / len(changes)
                return abs(avg_change) > 3
            return False
        
        # [EMOJI]
        alert_rules = [
            ("[EMOJI]", price_breakout_alert, "WARNING"),
            ("[EMOJI]", price_limit_approaching_alert, "ERROR"),
            ("[EMOJI]", volume_surge_alert, "INFO"),
            ("[EMOJI]", large_fund_inflow_alert, "INFO"),
            ("[EMOJI]", large_fund_outflow_alert, "WARNING"),
            ("[EMOJI]", technical_signal_alert, "INFO"),
            ("[EMOJI]", market_sentiment_alert, "WARNING")
        ]
        
        for rule_name, rule_func, level in alert_rules:
            self.alert_system.add_alert_rule(rule_name, rule_func, level)
        
        print(f"[OK] [EMOJI] {len(alert_rules)} [EMOJI]:")
        for rule_name, _, level in alert_rules:
            level_emoji = {'INFO': '[EMOJI]', 'WARNING': '[!]', 'ERROR': '[EMOJI]'}
            print(f"  {level_emoji[level]} {rule_name} [{level}]")
        
        print(f"\n[CHART] 8.3 [EMOJI]")
        print("-" * 50)
        
        # [EMOJI]
        monitor_stocks = ['000001', '000002', '600000', '600036']
        simulation_rounds = 3
        
        print(f"[EMOJI] {simulation_rounds} [EMOJI]...")
        
        for round_num in range(1, simulation_rounds + 1):
            print(f"\n--- [EMOJI] {round_num} [EMOJI] ---")
            
            # [EMOJI]
            mock_data = {}
            for code in monitor_stocks:
                import random
                mock_data[code] = {
                    'price': round(random.uniform(8, 15), 2),
                    'change_pct': round(random.uniform(-10, 10), 2),
                    'volume': random.randint(5000000, 150000000),
                    'turnover': round(random.uniform(0.5, 8), 2)
                }
            
            # [EMOJI]
            print("[EMOJI]:")
            for code, data in mock_data.items():
                print(f"  {code}: [EMOJI] {data['price']:.2f}, [EMOJI] {data['change_pct']:+.2f}%, [EMOJI] {data['volume']:,}")
            
            # [EMOJI]
            print("\n[EMOJI]:")
            initial_alert_count = len(self.alert_system.alert_history)
            self.alert_system.check_alerts(mock_data)
            new_alerts = len(self.alert_system.alert_history) - initial_alert_count
            
            if new_alerts > 0:
                print(f"[EMOJI] [EMOJI] {new_alerts} [EMOJI]")
                # [EMOJI]
                for alert in self.alert_system.alert_history[-new_alerts:]:
                    level_emoji = {'INFO': '[EMOJI]', 'WARNING': '[!]', 'ERROR': '[EMOJI]'}
                    print(f"  {level_emoji[alert['level']]} {alert['rule_name']}")
            else:
                print("[OK] [EMOJI]")
            
            # [EMOJI]
            time.sleep(1)
        
        print(f"\n[UP] 8.4 [EMOJI]")
        print("-" * 50)
        
        if self.alert_system.alert_history:
            # [EMOJI]
            level_counts = {}
            rule_counts = {}
            
            for alert in self.alert_system.alert_history:
                level = alert['level']
                rule = alert['rule_name']
                
                level_counts[level] = level_counts.get(level, 0) + 1
                rule_counts[rule] = rule_counts.get(rule, 0) + 1
            
            print("[EMOJI]:")
            level_emoji = {'INFO': '[EMOJI]', 'WARNING': '[!]', 'ERROR': '[EMOJI]'}
            for level, count in level_counts.items():
                print(f"  {level_emoji[level]} {level}: {count} [EMOJI]")
            
            print("\n[EMOJI]:")
            for rule, count in sorted(rule_counts.items(), key=lambda x: x[1], reverse=True):
                print(f"  • {rule}: {count} [EMOJI]")
            
            print(f"\n[EMOJI]: {len(self.alert_system.alert_history)}")
            
            # [EMOJI]
            if len(self.alert_system.alert_history) > 1:
                first_alert = datetime.strptime(self.alert_system.alert_history[0]['timestamp'], '%Y-%m-%d %H:%M:%S')
                last_alert = datetime.strptime(self.alert_system.alert_history[-1]['timestamp'], '%Y-%m-%d %H:%M:%S')
                duration = (last_alert - first_alert).total_seconds() / 60
                
                if duration > 0:
                    frequency = len(self.alert_system.alert_history) / duration
                    print(f"[EMOJI]: {frequency:.2f} [EMOJI]/[EMOJI]")
        else:
            print("[EMOJI]")
        
        print(f"\n[TOOL] 8.5 [EMOJI]")
        print("-" * 50)
        
        print("[EMOJI]:")
        print("  [CHART] [EMOJI]: [EMOJI]")
        print("  [TARGET] [EMOJI]: [EMOJI]")
        print("  [EMOJI] [EMOJI]: [EMOJI]")
        print("  [R] [EMOJI]: [EMOJI]")
        print("  [UP] [EMOJI]: [EMOJI]AI[EMOJI]")
        
        print("\n[EMOJI]:")
        print("  [EMOJI] [EMOJI]: [EMOJI]")
        print("  [EMOJI] [EMOJI]: [EMOJI]")
        print("  [EMOJI] [EMOJI]: [EMOJI]")
        print("  [CHART] [EMOJI]: [EMOJI]Web[EMOJI]")
        print("  [TOOL] [EMOJI]: [EMOJI]")
        
        print(f"\n[BOOK] [EMOJI]:")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        print("  • [EMOJI]")
        
        return self.alert_system.alert_history

def wait_for_user_input(course_name):
    """[EMOJI]"""
    print(f"\n{'='*60}")
    print(f"[BOOK] {course_name} [EMOJI]")
    print("[TIP] [EMOJI]")
    print("[R] [EMOJI] 'q' [EMOJI]...")
    print(f"{'='*60}")
    
    user_input = input().strip().lower()
    if user_input == 'q':
        print("\n[EMOJI] [EMOJI]")
        exit()
    print("\n" + "[LAUNCH] [EMOJI]...\n")

def main():
    """[EMOJI] - [EMOJI]"""
    print("=" * 80)
    print("[COURSE] [EMOJI] - [EMOJI]")
    print("=" * 80)
    print("[EMOJI] [EMOJI]8[EMOJI]")
    print("[TIP] [EMOJI] 'q' [EMOJI]")
    print("[LAUNCH] [EMOJI]")
    print("=" * 80)
    
    input("\n[TARGET] [EMOJI]...")
    
    try:
        # [EMOJI]
        print("\n[TOOL] [EMOJI]...")
        analyzer = AdvancedMultiSourceAnalyzer()
        
        # [EMOJI]1[EMOJI]
        print("\n" + "=" * 50)
        print("[BOOK] [EMOJI]1[EMOJI]")
        print("=" * 50)
        connection_results = analyzer.lesson_01_setup_and_optimization()
        wait_for_user_input("[EMOJI]1[EMOJI]")
        
        # [EMOJI]2[EMOJI]
        print("\n" + "=" * 50)
        print("[BOOK] [EMOJI]2[EMOJI]")
        print("=" * 50)
        health_results = analyzer.lesson_02_health_monitoring()
        wait_for_user_input("[EMOJI]2[EMOJI]")
        
        # [EMOJI]3[EMOJI]
        print("\n" + "=" * 50)
        print("[BOOK] [EMOJI]3[EMOJI]")
        print("=" * 50)
        fusion_results, quality_metrics = analyzer.lesson_03_data_fusion()
        wait_for_user_input("[EMOJI]3[EMOJI]")
        
        # [EMOJI]4[EMOJI]
        print("\n" + "=" * 50)
        print("[BOOK] [EMOJI]4[EMOJI]")
        print("=" * 50)
        realtime_data = analyzer.lesson_04_realtime_monitoring()
        wait_for_user_input("[EMOJI]4[EMOJI]")
        
        # [EMOJI]5[EMOJI]
        print("\n" + "=" * 50)
        print("[BOOK] [EMOJI]5[EMOJI]")
        print("=" * 50)
        concept_analysis = analyzer.lesson_05_concept_analysis()
        wait_for_user_input("[EMOJI]5[EMOJI]")
        
        # [EMOJI]6[EMOJI]
        print("\n" + "=" * 50)
        print("[BOOK] [EMOJI]6[EMOJI]")
        print("=" * 50)
        fund_flow_data = analyzer.lesson_06_fund_flow_analysis()
        wait_for_user_input("[EMOJI]6[EMOJI]")
        
        # [EMOJI]7[EMOJI]
        print("\n" + "=" * 50)
        print("[BOOK] [EMOJI]7[EMOJI]")
        print("=" * 50)
        trading_signals = analyzer.lesson_07_signal_generation()
        wait_for_user_input("[EMOJI]7[EMOJI]")
        
        # [EMOJI]8[EMOJI]
        print("\n" + "=" * 50)
        print("[BOOK] [EMOJI]8[EMOJI]")
        print("=" * 50)
        alert_history = analyzer.lesson_08_alert_system()
        wait_for_user_input("[EMOJI]8[EMOJI]")
        
        # [EMOJI]
        print("\n" + "=" * 80)
        print("[EMOJI] [EMOJI]")
        print("=" * 80)
        
        print("[OK] [EMOJI]:")
        print("  [BOOK] [EMOJI]1[EMOJI]: [EMOJI]")
        print("  [BOOK] [EMOJI]2[EMOJI]: [EMOJI]")
        print("  [BOOK] [EMOJI]3[EMOJI]: [EMOJI]")
        print("  [BOOK] [EMOJI]4[EMOJI]: [EMOJI]")
        print("  [BOOK] [EMOJI]5[EMOJI]: [EMOJI]")
        print("  [BOOK] [EMOJI]6[EMOJI]: [EMOJI]")
        print("  [BOOK] [EMOJI]7[EMOJI]: [EMOJI]")
        print("  [BOOK] [EMOJI]8[EMOJI]: [EMOJI]")
        
        print(f"\n[CHART] [EMOJI]:")
        successful_connections = len([r for r in connection_results.values() if r['status'] == 'success'])
        print(f"  [EMOJI] [EMOJI]: {successful_connections}/{len(analyzer.providers)}")
        print(f"  [UP] [EMOJI]: {sum(quality_metrics.values())/len(quality_metrics):.1f}%")
        print(f"  [TARGET] [EMOJI]: {len(trading_signals)} [EMOJI]")
        print(f"  [EMOJI] [EMOJI]: {len(analyzer.alert_system.alert_rules)}")
        print(f"  [EMOJI] [EMOJI]: {len(alert_history)} [EMOJI]")
        
        print(f"\n[TARGET] [EMOJI]:")
        print("  [EMOJI] [EMOJI]: [EMOJI]")
        print("  [CHART] [EMOJI]: [EMOJI]")
        print("  [SEARCH] [EMOJI]: [EMOJI]")
        print("  [LAUNCH] [EMOJI]: [EMOJI]")
        
        print(f"\n[BOOK] [EMOJI]:")
        print("  [EMOJI] [EMOJI]: [EMOJI]AI[EMOJI]")
        print("  [UP] [EMOJI]: [EMOJI]")
        print("  [R] [EMOJI]: [EMOJI]")
        print("  [EMOJI] [EMOJI]: [EMOJI]")
        
        print("\n[COURSE] [EMOJI]")
        print("[EMOJI] [EMOJI]")
        
    except KeyboardInterrupt:
        print("\n[!] [EMOJI]")
    except Exception as e:
        logger.error(f"[EMOJI]: {e}")
        print(f"[X] [EMOJI]: {e}")
    finally:
        # [EMOJI]
        try:
            for provider in analyzer.providers.values():
                if hasattr(provider, 'disconnect'):
                    try:
                        provider.disconnect()
                    except:
                        pass
        except:
            pass
        print("[EMOJI] [EMOJI]")

if __name__ == "__main__":
    main()

    