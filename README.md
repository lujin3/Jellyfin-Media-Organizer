# Jellyfin-Media-Organizer

Jellyfin-Media-Organizer 是一个基于 Python 和 OpenAI 的自动化工具，使用豆瓣信息整理和重命名原始的电影或电视剧文件，使其符合 [Jellyfin](https://jellyfin.org/) 媒体库的命名和分类要求。

## 功能特点

- 自动推断电影或电视剧的分类和元数据。
- 根据 Jellyfin 的要求重命名和组织文件。
- 支持多种文件格式和嵌套文件夹结构。
- 灵活的配置支持自定义规则。
- 利用 OpenAI API 提高元数据推断准确性。

## 使用
``` bash
poetry env  use 3.12
poetry install
export OPENAI_API_KEY=your_openai_api_key
export OPENAI_API_BASE=
export OPENAI_API_VERSION=
poetry run python main.py
```
``` bash
❯ poetry run python main.py
Renamed 'download/电影/西游记.mp4' to 'download/电影/西游记 (1986).mp4'.
Renamed 'download/电视剧/白夜破晓/01.mp4' to 'download/电视剧/白夜破晓/Season 1/白夜破晓(2024) - S01E01 - 第一集.mp4'.
Renamed 'download/电视剧/白夜破晓/02.mp4' to 'download/电视剧/白夜破晓/Season 1/白夜破晓(2024) - S01E02 - 第二集.mp4'.
```

## 更换 OpenAI api  
默认使用 AzureOpenAI
更换其他请修改 chat_ai.py 中 client 定义 参考[openai-python](https://github.com/openai/openai-python.git)
