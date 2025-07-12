#!/usr/bin/env python3
"""
直接导入数据到 Supabase（自动去掉 id 字段，修正逗号分隔问题）
"""

import os
import csv
import io
from supabase import create_client, Client
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Initialize Supabase client
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)

def clean_value(value):
    """Clean a value by removing quotes and extra spaces, handle NULL"""
    if value is None:
        return None
    
    value = str(value).strip()
    
    # Handle NULL values
    if value.upper() == 'NULL' or value == '':
        return None
    
    # Remove surrounding quotes if they exist
    if (value.startswith("'") and value.endswith("'")) or \
       (value.startswith('"') and value.endswith('"')):
        value = value[1:-1]
    
    return value.strip()

def parse_sql_insert(sql_content, table_name, expected_columns):
    """Parse SQL INSERT statements and return list of dictionaries, mapping to expected columns"""
    records = []
    lines = sql_content.split('\n')
    for line in lines:
        line = line.strip()
        if f'INSERT INTO public.{table_name}' in line and 'VALUES' in line:
            # 提取 VALUES 后面的部分
            start_idx = line.find('VALUES')
            if start_idx == -1:
                continue
            values_part = line[start_idx + 6:].strip()
            # 移除结尾的分号
            if values_part.endswith(';'):
                values_part = values_part[:-1]
            # 移除开头的括号
            if values_part.startswith('('):
                values_part = values_part[1:]
            # 移除结尾的括号
            if values_part.endswith(')'):
                values_part = values_part[:-1]
            
            try:
                # 用 csv.reader 解析，支持带逗号和引号
                csv_reader = csv.reader([values_part], quotechar="'", delimiter=',', skipinitialspace=True)
                for row in csv_reader:
                    if row:
                        # 跳过 id 字段
                        row = row[1:]
                        # 补齐缺失字段
                        while len(row) < len(expected_columns):
                            row.append(None)
                        cleaned_values = [clean_value(val) for val in row[:len(expected_columns)]]
                        records.append(cleaned_values)
            except Exception as e:
                print(f"Error parsing line: {line}")
                print(f"Error: {e}")
                continue
    return records

def import_table_data(table_name, columns, sql_content):
    print(f"\n=== Importing {table_name} ===")
    records = parse_sql_insert(sql_content, table_name, columns)
    print(f"Found {len(records)} records to import")
    if not records:
        print(f"No data found for {table_name}")
        return
    success_count = 0
    error_count = 0
    for i, record in enumerate(records):
        try:
            record_dict = {col: record[j] for j, col in enumerate(columns)}
            result = supabase.table(table_name).insert(record_dict).execute()
            success_count += 1
            if success_count % 10 == 0:
                print(f"Imported {success_count} records...")
        except Exception as e:
            error_count += 1
            print(f"Error importing record {i+1}: {e}")
            print(f"Record data: {record}")
    print(f"Import completed for {table_name}: {success_count} successful, {error_count} failed")

def main():
    sql_file = 'local_work_rent_dump.sql'
    if not os.path.exists(sql_file):
        print(f"SQL dump file {sql_file} not found!")
        return
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    # rent_info: zipcode, address, content, created_at(None)
    rent_info_columns = [
        'zipcode', 'address', 'content', 'created_at'
    ]
    # work_info: name, zipcode, address, content, created_at(None)
    work_info_columns = [
        'name', 'zipcode', 'address', 'content', 'created_at'
    ]
    import_table_data('rent_info', rent_info_columns, sql_content)
    import_table_data('work_info', work_info_columns, sql_content)
    print("\n=== rent_info & work_info import completed ===")

if __name__ == "__main__":
    main() 