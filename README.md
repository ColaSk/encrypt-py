# encryptpy
# 包

- Cython==0.29.24
- PyYAML==5.4.1
  
# 简介

- 用于加密python文件，python项目
- 应该秉承足够简洁, 思路清晰的原则

# docs

- 可支持的加密方式
  - [x] py->.so
  - 代码混淆 (未完成)

# 用法

> encrypt -i xxx project dir -o output dir

## 参数

### -h, --help

> - 显示所有参数的含义

### -i INPUT, --input INPUT

> 项目的路径, 支持相对路径

### -o OUTPUT, --output OUTPUT

> 加密项目路径，支持相对路径
> 默认: ./build

### -t TYPE, --type TYPE

> 加密类型, 当前只支持so加密方式
> 默认: 1

### -k KEEP_STEP, --keep_step KEEP_STEP

> 保存加密过程中产生的中间文件
> 默认：False

### -d IGNORED [IGNORED ...], --ignored IGNORED [IGNORED ...]

> 排除的文件夹目录, 当前仅支持目录名称，后续增加正则
> 默认：[.git, __pycache__, .vscode, tests, migrations, __pycache__]

###  -f IGNORE_PF [IGNORE_PF ...], --ignore_pf IGNORE_PF [IGNORE_PF ...]

> 排除不需要加密的python文件,目前仅支持文件名，后续增加正则
> 默认：[server.py, config.py]

### -c CONFIG, --config CONFIG

> 支持配置文件，目前仅支持yaml文件，下文详细说明配置方法
> 需要注意的是应用配置文件其他参数将失效切记


## yaml文件配置

```yaml
version: 1.0.0

input: /home/sk/project/solar_platform/solar_iter_api_original
output: /home/sk/project/solar_platform/solar_iter_api
type: '1'
keep_step: True

filter:
  ignored: [.git, __pycache__, .vscode, tests, migrations, __pycache__]
  ignore_pf: [server.py, config.py]

```
# 参考方案致谢
- <https://github.com/Boris-code/jmpy>