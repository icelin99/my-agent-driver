# import data.finetune.finetune_planner_10.json as Data
import json
import re

output_list = []

def split_by_pattern(text, delimiter):
    # 使用正则表达式分割字符串
    parts = re.split(re.escape(delimiter), text)
    # 清理和过滤空或无用的部分
    parts = [part.strip() for part in parts if part.strip()]
    return parts

Data = [{
    "messages": [
        {
            "role": "system",
            "content": "\n**Autonomous Driving Planner**\nRole: You're an autonomous vehicle's brain. Plan a 3-second safe trajectory to avoid obstacles.\n\nContext:\n- Coordinates: X-axis is perpendicular, and Y-axis is parallel to the direction you're facing. You're at point (0,0). Units: meters.\n- Goal: Plan a 3-second route using 6 waypoints (0.5s intervals).\n\nInputs:\n1. Ego States (important): Current stats (velocity, acceleration), past trajectory, goal direction.\n2. Perception Results.\n3. Past Experiences (important): Previous similar experiences with confidence scores and referenced planned trajectory.\n4. Traffic Rules.\n5. Reasoning (important): Notable objects affecting your plan and a top-level driving plan.\n\nTask:\n- Based on inputs, plan a safe, feasible 3-second trajectory of 6 waypoints.\n\nOutput:\nPlanned Trajectory:\n[(x1,y1), (x2,y2), ... , (x6,y6)]\n"
        },
        {
            "role": "user",
            "content": "*****Ego States:*****\nCurrent State:\n - Velocity (vx,vy): (0.00,0.00)\n - Heading Angular Velocity (v_yaw): (0.00)\n - Acceleration (ax,ay): (0.00,0.00)\n - Can Bus: (-0.09,-0.03)\n - Heading Speed: (0.00)\n - Steering: (-0.41)\nHistorical Trajectory (last 2 seconds): [(-0.00,0.00), (-0.00,0.00), (-0.00,0.00), (-0.00,0.00)]\nMission Goal: FORWARD\n\n*****Perception Results:*****\nFront object detections:\nFront object detected, object type: car, object id: 0, position: (-2.83, 14.98), size: (2.09, 4.95)\n\nFuture trajectories for specific objects:\nObject type: car, object id: 0, future waypoint coordinates in 3s: [(-2.83, 14.98), (-2.83, 14.98), (-2.83, 14.98), (-2.83, 14.98), (-2.83, 14.98), (-2.84, 14.97)]\n\nDistance to both sides of road shoulders of current ego-vehicle location:\nCurrent ego-vehicle's distance to left shoulder is 5.0m and right shoulder is 0.5m\n\n*****Past Driving Experience for Reference:*****\nMost similar driving experience from memory with confidence score: 1.00:\nThe planned trajectory in this experience for your reference:\n[(0.00,-0.00), (0.00,-0.00), (0.00,-0.00), (0.00,-0.00), (0.00,-0.00), (0.00,-0.00)]\n\n*****Traffic Rules:*****\n- Avoid collision with other objects.\n- Always drive on drivable regions.\n- Avoid driving on occupied regions.\n- Pay attention to your ego-states and historical trajectory when planning.\n- Maintain a safe distance from the objects in front of you.\n*****Chain of Thoughts Reasoning:*****\nThoughts:\n - Notable Objects: None\n   Potential Effects: None\nDriving Plan: STOP\n"
        },
        {
            "role": "assistant",
            "content": "Planned Trajectory:\n[(0.00,0.00), (0.00,-0.00), (0.00,-0.00), (0.00,0.00), (0.00,-0.00), (0.00,-0.00)]"
        }
    ]
}]

def extract_json_objects(text):
    objects = []
    depth = 0
    obj_start = None
    for i, char in enumerate(text):
        if char == '{':
            if depth == 0:
                obj_start = i
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0 and obj_start is not None:
                # 尝试解析找到的JSON字符串
                try:
                    obj = json.loads(text[obj_start:i + 1])
                    if 'messages' in obj:  # 确保是我们感兴趣的对象
                        objects.append(obj)
                except json.JSONDecodeError as e:
                    print(f"解析错误: {e}")
                obj_start = None
    return objects

# 读取文件
with open('data/finetune/finetune_planner_10.json', 'r') as file:
    file_content = file.read()

# 提取JSON对象
Data = extract_json_objects(file_content)

for item in Data:
    content_dict = {}
    for message in item['messages']:
        content = message.get('content', None)
        role = message.get('role', None)
        lines = content.split('\n')
        if role == 'assistant':
            key, value = content.split('\n')
            content_dict[key.strip(":")] = value
        if role == 'user':
            # results = split_by_pattern(lines, "*****")
            # for index, part in enumerate(results):
            #     print(f"Part {index + 1}:\n{part}\n")
            content_dict["Ego states"] = {}
            content_dict["Ego states"]["Current state"] = {}
            content_dict["Perception Results"] = {}
            content_dict["Past Driving Experience for Reference"] = {}
            content_dict["Chain of Thoughts Reasoning"] = {}
            for i, line in enumerate(lines):
                if "Front object detections" in line or "Future trajectories for specific objects" in line or "Distance to both sides of road shoulders of current ego-vehicle location" in line:
                    content_dict["Perception Results"][line.strip(":")] = lines[i+1]
                if "Velocity (vx,vy)" in line or "Velocity (v_yaw)" in line or "Acceleration (ax,ay)" in line or "Can Bus:" in line or "- Heading Speed" in line or "- Steering" in line:
                    key, value = line.split(":",1)
                    content_dict["Ego states"]["Current state"][key.replace("- ","").strip()] = value.strip()
                if "Historical Trajectory (last 2 seconds)" in line:
                    key, value = line.split(":",1)
                    content_dict["Ego states"][key] = value.strip()
                if "Mission Goal" in line:
                    key, value = line.split(":",1)
                    content_dict["Ego states"][key] = value.strip()
                if " driving experience from memory" in line:
                    tt = line.split(":",1)
                    content_dict["Past Driving Experience for Reference"][tt[0].strip()] = tt[1].strip()
                elif "The planned trajectory in this experience for your reference" in line:
                    content_dict["Past Driving Experience for Reference"][line.strip(":")] = lines[i+1]
                if "Traffic Rules" in line:
                    x = i+1
                    content_dict["Traffic Rules"] = []
                    while("- " in lines[x]):
                        content_dict["Traffic Rules"].append(lines[x].replace("- ","").strip())
                        x = x + 1
                if "Chain of Thoughts Reasoning" in line and "Thoughts" in lines[i+1]:
                    content_dict["Chain of Thoughts Reasoning"]["Thoughts"] = {}
                    content_dict["Chain of Thoughts Reasoning"]["Thoughts"][lines[i+2].strip()] = lines[i+3].strip()
                    content_dict["Chain of Thoughts Reasoning"]["Thoughts"][lines[i+4].strip()] = lines[i+5].strip()
                if "Driving Plan: " in line:
                    key, value = line.split(":",1)
                    content_dict["Chain of Thoughts Reasoning"]["Driving Plan"] = value.strip()
            

            
    output_list.append(content_dict)
        # print("--",role)
        # # 存储用户信息
        # if role == 'user':
        #     user_data = {}
        #     current_section = ''
        #     for line in lines:
        #         print('111',line)
        #         if '*****' in line:
        #             current_section = line.strip('*')
        #             user_data[current_section] = {}
        #         elif ':' in line and '-' in line:
        #             key, value = line.split(':', 1)
        #             user_data[current_section][key.strip()] = value.strip()
        #     output_list.update(user_data)
        
        # # 存储助手信息
        # elif role == 'assistant':
        #     assistant_data = {}
        #     for line in lines:
        #         if 'Planned Trajectory' in line:
        #             key, value = line.split(':', 1)
        #             assistant_data[key.strip()] = value.strip()
        #     output_list.update(assistant_data)



with open('planner_data.json','w') as f:
    json.dump(output_list, f, indent=2)