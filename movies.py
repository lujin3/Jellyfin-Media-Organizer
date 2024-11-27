from pathlib import Path
from chat_ai import chat_ai
import json
from douban import fetch_movie_details


movie_prompt_template = """
您是一位专家，擅长整理和重命名媒体文件，特别是针对 Jellyfin 媒体库。

任务：请帮助我根据 Jellyfin 的命名规范重命名以下电影文件：
- 文件名: {file}

电影详情：
- {movie_details}

规则：
1. 将电影文件重命名为以下格式：`电影名称 (年份).扩展名`。
2. 使用电影详情确保电影名称和年份准确无误。
3. 如果电影详情与文件信息不匹配或信息不足，则不要修改原文件。
4. 如果找不到匹配信息，跳过该文件，不进行重命名。不要使用任何默认或占位名称，例如 "Unknown"。
5. 仅返回一个 JSON 对象作为结果，结果中不包含多余内容。例如不要出现 ```json。
6. 不要修改原始文件名。

输出 JSON 格式：
{{
    "original": "原始文件名",
    "renamed": "重命名后的文件名"
}}

示例：
如果电影是 "Inception (2010).mp4"，结果应为：
{{
    "original": "inception_1080p.mp4",
    "renamed": "Inception (2010).mp4"
}}

重要：仅返回 JSON 对象。如果没有找到匹配信息，则返回一个空的 JSON 对象。不要包含额外的文本。
"""


def rename_movie_files(directory: Path, extensions: set):
    """
    根据目录结构生成电影文件重命名规则。
    Args:
        directory (Path): 要扫描的目录路径。
        extensions (set): 要处理的文件扩展名集合，默认为 {".mp4", ".mkv"}。
    """

    files = [f for f in directory.iterdir() if f.is_file() and f.suffix in extensions]

    for file in files:
        try:
            movie_details = fetch_movie_details(file.name)
            prompt = movie_prompt_template.format(
                file=file.name, movie_details=movie_details
            )
            ai_resp = chat_ai(prompt)
            data = json.loads(ai_resp)
            if data and "renamed" in data:
                renamed_file = data["renamed"]
                new_file_path = directory / renamed_file
                file.rename(new_file_path)
                print(f"Renamed '{file}' to '{new_file_path}'.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON response for file: {file.name}")
        except Exception as e:
            print(f"Error processing file {file.name}: {e}")
