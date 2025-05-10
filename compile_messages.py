#!/usr/bin/env python
"""
编译项目中的翻译文件，而不是所有依赖包中的翻译文件。
同时检测并修复重复的消息定义问题。
"""
import os
import subprocess
import re
import tempfile
import shutil
from pathlib import Path
from collections import OrderedDict

def find_duplicate_messages(po_file_path):
    """
    查找po文件中的重复消息定义
    返回一个字典，键为msgid，值为该msgid在文件中出现的所有行号
    """
    msgid_pattern = re.compile(r'^msgid "(.*)"$')
    duplicate_msgs = {}
    current_msgid = None
    line_number = 0
    
    with open(po_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line_number += 1
            match = msgid_pattern.match(line.strip())
            if match:
                current_msgid = match.group(1)
                if current_msgid not in duplicate_msgs:
                    duplicate_msgs[current_msgid] = []
                duplicate_msgs[current_msgid].append(line_number)
    
    return {k: v for k, v in duplicate_msgs.items() if len(v) > 1}

def fix_duplicate_messages(po_file_path):
    """
    修复po文件中的重复消息定义问题
    """
    duplicates = find_duplicate_messages(po_file_path)
    if not duplicates:
        return False  # 没有重复，无需修复
    
    print(f"在 {po_file_path} 中发现 {len(duplicates)} 个重复消息定义")
    
    # 读取原始文件内容
    with open(po_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 创建一个有序字典来保存唯一的消息条目
    unique_entries = OrderedDict()
    
    # 解析po文件格式，提取每个消息条目
    entry_lines = []
    in_entry = False
    current_msgid = None
    
    for line in lines:
        if line.strip().startswith('msgid "'):
            if entry_lines and current_msgid is not None:
                unique_entries[current_msgid] = entry_lines
            entry_lines = []
            in_entry = True
            # 提取msgid值，处理多行msgid的情况
            msgid_content = line.strip()[6:].strip('"')
            current_msgid = msgid_content
        elif line.strip().startswith('"') and in_entry and current_msgid is not None:
            # 处理多行msgid的情况
            if not line.strip().startswith('msgstr'):
                current_msgid += line.strip().strip('"')
        
        if in_entry:
            entry_lines.append(line)
        
        if line.strip().startswith('msgstr "') and in_entry:
            # 寻找该条目的结束（空行或下一个条目开始）
            continue
        
        if line.strip() == "" and in_entry and entry_lines:
            # 条目结束
            if current_msgid is not None:
                unique_entries[current_msgid] = entry_lines
            in_entry = False
            current_msgid = None
            entry_lines = []
    
    # 处理最后一个条目
    if entry_lines and current_msgid is not None:
        unique_entries[current_msgid] = entry_lines
    
    # 重写po文件，只保留唯一的条目
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', delete=False) as tmp:
        # 寻找文件头部 - 查找第一个以msgid开头的行之前的所有内容
        header_lines = []
        found_first_msgid = False
        header_msgid_line = -1
        
        for i, line in enumerate(lines):
            if line.strip().startswith('msgid "') and not found_first_msgid:
                found_first_msgid = True
                header_msgid_line = i
                break
            header_lines.append(line)
        
        # 写入文件头
        for line in header_lines:
            tmp.write(line)
        
        # 如果有头部msgid ""条目，写入它
        if header_msgid_line >= 0:
            header_msgstr_found = False
            header_ended = False
            
            for i in range(header_msgid_line, len(lines)):
                line = lines[i]
                tmp.write(line)
                
                if line.strip().startswith('msgstr "'):
                    header_msgstr_found = True
                
                # 头部消息后的空行表示头部结束
                if header_msgstr_found and line.strip() == "":
                    header_ended = True
                    break
            
            if not header_ended:
                tmp.write('\n')  # 确保在头部后有空行
        
        # 写入唯一的条目
        for msgid, entry_lines in unique_entries.items():
            if msgid != "":  # 跳过空msgid（头部信息）
                tmp.write('\n')  # 条目间添加空行
                for line in entry_lines:
                    tmp.write(line)
    
    # 备份原始文件并替换为修复后的文件
    backup_file = po_file_path + '.bak'
    shutil.copy2(po_file_path, backup_file)
    shutil.move(tmp.name, po_file_path)
    
    print(f"已修复重复问题，原始文件备份为 {backup_file}")
    return True

def main():
    # 获取项目根目录
    BASE_DIR = Path(__file__).resolve().parent
    
    # 项目的语言文件目录
    locale_dir = os.path.join(BASE_DIR, 'locale')
    
    if not os.path.exists(locale_dir):
        print(f"翻译目录 {locale_dir} 不存在!")
        return
    
    print(f"正在编译项目翻译文件 {locale_dir}...")
    
    # 对每个语言文件单独运行 django-admin compilemessages
    for lang_code in os.listdir(locale_dir):
        lang_dir = os.path.join(locale_dir, lang_code)
        if not os.path.isdir(lang_dir):
            continue
        
        # 检查并修复LC_MESSAGES目录下的django.po文件
        po_file = os.path.join(lang_dir, 'LC_MESSAGES', 'django.po')
        if os.path.exists(po_file):
            print(f"检查 {lang_code} 的翻译文件是否有重复...")
            fixed = fix_duplicate_messages(po_file)
            if fixed:
                print(f"已修复 {lang_code} 的重复消息定义")
        
        print(f"编译 {lang_code} 的翻译...")
        try:
            # 只编译指定语言的翻译文件
            subprocess.run(
                ['django-admin', 'compilemessages', '--locale', lang_code],
                cwd=BASE_DIR,
                check=True
            )
            print(f"✅ {lang_code} 编译成功")
        except subprocess.CalledProcessError as e:
            print(f"❌ {lang_code} 编译失败: {e}")
    
    print("完成!")

if __name__ == "__main__":
    main()
