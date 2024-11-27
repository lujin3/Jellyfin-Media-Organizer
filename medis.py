import os
from pathlib import Path


def get_media_structure(directory: Path, extensions: set) -> str:
    """
    获取目录的层级结构，仅包含指定扩展名的文件。

    Args:
        directory (Path): 要扫描的目录路径。
        extensions (set): 包含需要匹配的文件扩展名的集合。

    Returns:
        str: 目录层级结构的字符串表示。
    """

    def traverse_directory(path: Path, indent: int = 0) -> list:
        lines = []
        for item in path.iterdir():
            # 如果是文件并且扩展名符合要求
            if item.is_file() and item.suffix.lower() in extensions:
                lines.append("    " * indent + f"├── {item.name}")
            # 如果是目录，则递归处理
            elif item.is_dir():
                lines.append("    " * indent + f"├── {item.name}/")
                lines.extend(traverse_directory(item, indent + 1))
        return lines

    if not directory.is_dir():
        raise ValueError(f"The provided path '{directory}' is not a valid directory.")

    structure = traverse_directory(directory)
    return "\n".join(structure) if structure else "目录为空或无匹配文件。"


def rename_file(path, data):
    """
    在指定目录下修改文件名称和文件夹名称
    :param data: 字典，包含原始文件路径和重命名后的文件路径
    :param path: 要操作的基准目录路径
    """
    # 构造完整的文件路径
    original_path = os.path.join(path, data.get("original"))

    renamed_path = os.path.join(path, data.get("renamed"))

    if not data.get("original") or not data.get("renamed"):
        print("请输入有效的文件路径信息！")
        return

    # 检查文件是否存在
    if not os.path.exists(original_path):
        print(f"文件或文件夹 {original_path} 不存在！")
        return

    # 重命名文件或文件夹
    try:
        os.rename(original_path, renamed_path)
        print(f"已将 {original_path} 重命名为 {renamed_path}")
    except Exception as e:
        print(f"重命名失败: {e}")
