#!/usr/bin/env python3
"""
Простой скрипт для просмотра результатов тестов из allure-results
"""
import json
import os
from pathlib import Path

def view_test_results():
    results_dir = Path("allure-results")
    if not results_dir.exists():
        print("Папка allure-results не найдена!")
        return
    
    result_files = list(results_dir.glob("*-result.json"))
    if not result_files:
        print("Результаты тестов не найдены!")
        return
    
    print(f"\n{'='*60}")
    print(f"Найдено результатов тестов: {len(result_files)}")
    print(f"{'='*60}\n")
    
    passed = 0
    failed = 0
    broken = 0
    
    for result_file in sorted(result_files):
        try:
            with open(result_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            name = data.get('name', 'Unknown')
            status = data.get('status', 'unknown')
            full_name = data.get('fullName', '')
            
            status_symbol = {
                'passed': '✅',
                'failed': '❌',
                'broken': '⚠️',
                'skipped': '⏭️'
            }.get(status, '❓')
            
            print(f"{status_symbol} {name}")
            print(f"   Статус: {status}")
            print(f"   Тест: {full_name}")
            
            if 'steps' in data:
                print(f"   Шагов: {len(data['steps'])}")
            
            if status == 'passed':
                passed += 1
            elif status == 'failed':
                failed += 1
            elif status == 'broken':
                broken += 1
            
            print()
            
        except Exception as e:
            print(f"Ошибка при чтении {result_file}: {e}")
    
    print(f"{'='*60}")
    print(f"Итого:")
    print(f"  ✅ Прошло: {passed}")
    print(f"  ❌ Упало: {failed}")
    print(f"  ⚠️  Сломано: {broken}")
    print(f"  📊 Всего: {len(result_files)}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    view_test_results()

