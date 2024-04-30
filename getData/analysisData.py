import json

# 读取文件
with open('./planner_data.json', 'r') as file:
    data = json.load(file)

# 提取JSON对象
item_count = len(data)
print("项目数量:", item_count)  