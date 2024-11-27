from pathlib import Path
from chat_ai import chat_ai
import json
from douban import fetch_movie_details


tv_show_prompt_template = """
你是一位熟悉媒体资源整理和文件命名规则的专家，尤其擅长按照 Jellyfin 媒体库的需求进行分类和重命名。

任务目标：帮助我整理以下媒体资源：
- 文件名：{file}

电视剧的描述信息如下：
- {movie_details}

请按照以下规则对资源进行分类和命名：
1. 按照 Jellyfin 的命名规则，将剧集重命名为格式：`S01E01 - 剧集名.扩展名`。
2. `S01` 是固定的，你只需根据文件信息获取正确的 `E01` 编号。
3. 剧集名称应基于文件描述信息，例如：
   - `S01E01` 的剧集名为 "第一集"。
   - `S01E02` 的剧集名为 "第二集"。
4. 仅返回一个 JSON 对象作为结果，结果中不包含多余内容。例如不要出现 ```json。
5. 不要修改原始文件名。

命名规则示例：
- 原始文件名：`episode1.mkv`
- 重命名后：`S01E01 - 第一集.mkv`

输出 JSON 格式：
{{
    "original": "原始文件名",
    "renamed": "重命名后的文件名"
}}

注意事项：
- 如果信息不足以完成重命名，则返回一个空的 JSON 对象。
- 仅返回 JSON 格式的结果，不要包含任何额外文字。
"""


def rename_tv_show_episode(file: Path, movie_details: dict, season_path: Path):
    """
    根据电影详情重命名TV节目文件
    Args:
        file (Path): 电影文件路径
        movie_details (dict): 电影详细信息
        new_folder_path (Path): 目标文件夹路径
    """
    try:
        prompt = tv_show_prompt_template.format(file=file, movie_details=movie_details)
        ai_resp = chat_ai(prompt)
        data = json.loads(ai_resp)

        if data and "renamed" in data:
            renamed_name = (
                f"{movie_details["name"]}{movie_details["year"]} - {data["renamed"]}"
            )
            new_file_path = season_path / renamed_name
            file.rename(new_file_path)
            print(f"Renamed '{file}' to '{new_file_path}'.")

    except json.JSONDecodeError:
        print(f"Error decoding JSON response for file: {file.name}")
    except Exception as e:
        print(f"Error processing file {file.name}: {e}")


def rename_tv_show_folder(folder: Path, extensions: set):
    """
    处理文件夹中的所有文件，根据电影详情重命名
    Args:
        folder (Path): 要处理的文件夹路径
    """
    try:
        # 获取电影详细信息
        movie_details = fetch_movie_details(folder.name)
        files = [f for f in folder.iterdir() if f.is_file() and f.suffix in extensions]
        # 创建Season 1文件夹
        season_path = folder / "Season 1"
        season_path.mkdir(parents=True, exist_ok=True)

        for file in files:
            rename_tv_show_episode(file, movie_details, season_path)
    except Exception as e:
        print(f"Error processing folder {folder.name}: {e}")


def rename_tv_show_folders(directory: Path, extensions: set):
    folders = [item for item in directory.iterdir() if item.is_dir()]
    for folder in folders:
        rename_tv_show_folder(folder, extensions)
