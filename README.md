# ai-sdk

THUAI 2021 抢金蛋 AI SDK

## Usage

构建好的版本请见 `build/` 文件夹。

C++: 下载SDK，再用cmake将 `cpp/` 下相应.cpp文件一同编译。

提交时，只打包 `cpp/` 文件夹为 zip 文件提交。

对于 Linux/Mac：
```bash
$ cmake .
$ make
```

对于 Windows: 安装 Visual Studio 2019，并且使用 cmake 图形界面编译。

Python: 下载SDK，然后直接在 `main.py` 书写代码。

## LICENSE

MIT License

nlohmann/json.hpp: MIT License
