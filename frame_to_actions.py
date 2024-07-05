# 打开文件并读取内容
import json

action_classes_path = 'action_classes.txt' #替换文件路径
prediction_result_path = 'masked_result.json'
with open(action_classes_path, 'r') as file: 
    # 创建一个空字典来存储 ID 和描述
    actions_dict = {}
    # 逐行读取文件内容
    for line in file:
        # 使用 split() 方法按空格分割每行，并且最多分割成两部分
        parts = line.strip().split(' ', 1)
        # 如果分割后的结果包含两部分（ID 和描述），则将其添加到字典中
        if len(parts) == 2:
            action_id, action_description = parts
            actions_dict[action_description] = action_id

with open(prediction_result_path, 'r') as file: #替换文件目录至数据文件
    result_dict = json.load(file)

def frame_to_time(frame_number, fps=24):
    return frame_number / fps

# 使用这个function查询结果
def frame_to_actions(video_id, frame_number, actions_dict=actions_dict, result_dict=result_dict):
    result_actions = []
    sec = frame_to_time(int(frame_number.lstrip('0')))
    # print(sec)
    for prediction in result_dict[video_id]:
        # print(prediction)
        if sec >= prediction["segment"][0] and sec <= prediction["segment"][1] and prediction["label"] in actions_dict:
            result_actions.append(actions_dict[prediction["label"]])
    return result_actions


