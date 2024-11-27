from pathlib import Path
from movies import rename_movie_files
from tv_show import rename_tv_show_folders

if __name__ == "__main__":
    # 指定目录和扩展名
    directory = Path("download")  # 替换为你的实际目录路径
    extensions = {".mp4", ".mkv"}  # 需要匹配的扩展名

    movie_directory = directory / "电影"
    rename_movie_files(movie_directory, extensions)

    tv_show_directory = directory / "电视剧"
    rename_tv_show_folders(tv_show_directory, extensions)
