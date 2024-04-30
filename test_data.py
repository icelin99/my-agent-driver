# 原始的文本信息
text_data = [
    {
        "role": "assistant",
        "content": "*****Ego States:*****\nCurrent State:\n - Velocity (vx,vy): (0.00,0.00)\n - Heading Angular Velocity (v_yaw): (0.00)\n - Acceleration (ax,ay): (0.00,0.00)\n - Can Bus: (-0.09,-0.03)\n - Heading Speed: (0.00)\n - Steering: (-0.41)\nHistorical Trajectory (last 2 seconds): [(-0.00,0.00), (-0.00,0.00), (-0.00,0.00), (-0.00,0.00)]\nMission Goal: FORWARD\n\n*****Perception Results:*****\nFront object detections:\nFront object detected, object type: car, object id: 0, position: (-2.83, 14.98), size: (2.09, 4.95)\n\nFuture trajectories for specific objects:\nObject type: car, object id: 0, future waypoint coordinates in 3s: [(-2.83, 14.98), (-2.83, 14.98), (-2.83, 14.98), (-2.83, 14.98), (-2.83, 14.98), (-2.84, 14.97)]\n\nDistance to both sides of road shoulders of current ego-vehicle location:\nCurrent ego-vehicle's distance to left shoulder is 5.0m and right shoulder is 0.5m\n\n*****Past Driving Experience for Reference:*****\nMost similar driving experience from memory with confidence score: 1.00:\nThe planned trajectory in this experience for your reference:\n[(0.00,-0.00), (0.00,-0.00), (0.00,-0.00), (0.00,-0.00), (0.00,-0.00), (0.00,-0.00)]\n\n*****Traffic Rules:*****\n- Avoid collision with other objects.\n- Always drive on drivable regions.\n- Avoid driving on occupied regions.\n- Pay attention to your ego-states and historical trajectory when planning.\n- Maintain a safe distance from the objects in front of you.\n*****Chain of Thoughts Reasoning:*****\nThoughts:\n - Notable Objects: None\n   Potential Effects: None\nDriving Plan: STOP\n"
    },
    {
        "role": "assistant",
        "content": "Planned Trajectory:\n[(0.00,0.00), (0.00,-0.00), (0.00,-0.00), (0.00,0.00), (0.00,-0.00), (0.00,-0.00)]"
    }
]

# 将原始文本转换为字典形式
data = {}
for item in text_data:
    if "Planned Trajectory" in item["content"]:
        planned_trajectory = item["content"].split(":")[1].strip()
        data["Planned Trajectory"] = {"Planned Trajectory": planned_trajectory}
    else:
        key_value_pairs = item["content"].split("\n")
        section_title = None
        section_data = {}
        for line in key_value_pairs:
            if "*****" in line:
                section_title = line.strip("*")
            elif ":" in line:
                key, value = line.split(":", 1)
                section_data[key.strip()] = value.strip()
        data[section_title] = section_data

# 打印最终的数据结构
print(data)
