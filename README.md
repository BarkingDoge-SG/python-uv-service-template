# Python Service Template (uv-based)

## 基础说明
这是一个基于 **uv** 管理 Python 依赖的项目模板，适合用于 **模型服务 / API 服务 / 长期运行的 Linux 后台服务** 等。
模板内置了包括 uv 项目默认文件，以及如下自定义文件：
- 配置文件 `config.yaml`。
- `.env` 环境变量管理。
- 日志系统（支持定时清理、指定日志名）。
- `systemd` 自启动服务模板。

## 目录说明
`data/`：用于存放项目运行过程中使用的数据（如模型文件、缓存数据等）。

`lgos/`：日志输出目录，由 `common_utils/logger.py` 自动创建和维护，支持：
- 按天滚动。
- 自动清理历史日志。
- 自定义日志名。

`wheels/`：用于存放 本地 wheel 包（如 `flash-attention2`，⚠️ 当前目录中的 wheel 文件为空文件，仅用于演示）。

`common_utils/`：公共工具模块。
- `get_env.py`：负责加载 `.env` 文件中的环境变量（基于 `python-dotenv`）。
- `conf_loader.py`：读取并解析 config.yaml，用于加载**日志、模型**等配置。
- `logger.py`：对 logging 的封装，自动创建日志目录、按天滚动，可在 `config.yaml` 中配置日志级别 / 保存天数。

`src`：项目核心代码目录。
约定：
- 一级目录（如 `some_proj`）：项目主逻辑。
- api/ 子目录：对外服务入口（以 `FastAPI` 为例）。
e.g.
``` text
src/
└─some_proj/
   ├─ some_file.py        # 项目核心逻辑
   └─ api/
      └─ server.py        # 服务启动入口
```

## 配置文件说明
- `.env`：用于设置环境变量（如 API Key、CUDA 设备等），可以直接通过 `from common_utils import get_env` 来确保 .env 被正确加载（huggingface 默认使用镜像）。
- `.python-version`：默认 `3.12`。
- `config.yaml` 集中管理项目配置，如日志配置、模型参数等。由 `common_utils.conf_loader.ConfigLoader` 统一读取。

## 依赖管理
- 在 `pyproject.toml` 中定义了模板默认依赖
- 默认 `pytorch` 和 `torchvison` 源：使用交大源的 CUDA 版本（`torch2.8+cu126`）。
- 默认 `python` 源：清华源。
- 本地 wheel 依赖：`pyproject.toml` 中注释的 `flash-attn` 部分，取消注释即可
- `[tool.setuptools.packages.find] where = ["src"]` 避免项目根目录被误当作包，会影响 `pip install ...`，`uv pip install .` 及打包等行为

## 服务启动方式（FastAPI）
### 推荐的本地启动方式
`uv run -m src.some_proj.api.server`
### systemd 自启动服务（Linux）
该模板用于创建 Linux systemd 服务，已包含：
- 文件句柄限制（避免高并发性能瓶颈）
- 内存限制（需根据实际情况调整）
- systemctl 常用命令:
  - service 文件修改后须执行 `sudo systemctl daemon-reexec` 和 `sudo systemctl daemon-reload`
  - 允许自启动：`sudo systemctl enable some_project`
  - 开始、重启、停止服务：`sudo systemctl start / restart/ stop some_project`
  - 查看服务状态：`sudo systemctl status some_project`