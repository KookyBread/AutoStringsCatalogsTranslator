# AutoStringsCatalogsTranslator

A powerful, intelligent translation tool for iOS/macOS localization strings with automatic language detection, beautiful terminal interface, and dictionary-first approach.

[中文版本](#中文版本) | [English Version](#english-version)

---
<img width="1922" height="1546" alt="1" src="https://github.com/user-attachments/assets/524f50f7-aa20-42ca-b3d3-d6ce638acbac" />
<img width="1922" height="1546" alt="2" src="https://github.com/user-attachments/assets/b883732b-795a-4c24-b74a-767dc2626754" />
<img width="1922" height="1546" alt="8" src="https://github.com/user-attachments/assets/ae20d771-5e3c-4d21-92e7-42b82ba50597" />
---

## English Version

### 🚀 Features

- **🎯 Automatic Language Detection**: Intelligently detects target languages from input files
- **📚 Dictionary-First Translation**: Uses CSV dictionaries for consistent, accurate translations
- **🎨 Beautiful Terminal Interface**: Gradient colors and Claude Code-style presentation
- **🌐 Multiple Translation Services**: Google Translate, Youdao, Baidu, Tencent Cloud
- **🎯 Smart Translation Modes**: Skip already translated or full retranslation
- **📱 iOS/macOS Support**: Native support for `.xcstrings` and `.json` formats
- **🌍 Bilingual Interface**: Choose between English and Chinese interface
- **⚡ Extensible Dictionary System**: Easy to add custom translation dictionaries
- **🔄 Automatic Format Detection**: Intelligent input/output format handling
- **🛡️ Rate Limiting**: Built-in rate limiting to respect API limits

### 📋 Requirements

- Python 3.7+
- Internet connection for API-based translation services
- API keys for premium services (optional)

### 🚀 Quick Start

#### Installation

```bash
git clone https://github.com/KookyBread/AutoStringsCatalogsTranslator.git
cd AutoStringsCatalogsTranslator
pip install -r requirements.txt
```

#### Basic Usage

```bash
# Interactive mode (recommended for first-time users)
python3 auto_strings_catalogs_translator.py

# Command line mode
python3 auto_strings_catalogs_translator.py input.xcstrings output.xcstrings dictionaries/AppleWatchWorkoutTypes.csv
```

#### What's New in v1.0

- **🎨 Beautiful Terminal Interface**: Claude Code-style gradient title and colors
- **🎯 Smart Language Detection**: Automatically detects languages from input files
- **🌈 Enhanced User Experience**: Color-coded output and progress indicators

#### Interactive Mode Features

1. **Beautiful Interface**: Claude Code-style gradient title with terminal colors
2. **Language Selection**: Choose interface language (English/Chinese)
3. **Automatic Language Detection**: Detects target languages from input files
4. **File Format Validation**: Only accepts `.xcstrings` or `.json` files
5. **Output Format Selection**: 
   - Keep same format as input
   - Force output to `.xcstrings`
   - Force output to `.json`
6. **Translation Mode Selection**:
   - Skip already translated entries
   - Full retranslation of all qualifying entries
7. **Service Selection**: Choose primary and fallback translation services
8. **Dictionary Management**: Auto-discover and add custom dictionaries

### 🎯 Translation Services

| Service | Type | Requirements | Features |
|---------|------|--------------|----------|
| **Google Translate** | Free | None | No API key required, rate limited |
| **Youdao Translate** | Freemium | `YOUDAO_APP_KEY`, `YOUDAO_APP_SECRET` | Free quota available |
| **Baidu Translate** | Freemium | `BAIDU_APP_ID`, `BAIDU_APP_KEY` | 2M free characters/month |
| **Tencent Cloud** | Freemium | `TENCENT_SECRET_ID`, `TENCENT_SECRET_KEY` | 5M free characters/month |

### 🔧 Environment Setup

Set up API credentials as environment variables:

```bash
# Youdao Translate
export YOUDAO_APP_KEY="your_app_key"
export YOUDAO_APP_SECRET="your_app_secret"

# Baidu Translate
export BAIDU_APP_ID="your_app_id"
export BAIDU_APP_KEY="your_app_key"

# Tencent Cloud Translation
export TENCENT_SECRET_ID="your_secret_id"
export TENCENT_SECRET_KEY="your_secret_key"
```

Add these to your shell profile (`.bashrc`, `.zshrc`, etc.) for persistence.

### 📚 Dictionary System

#### Creating Custom Dictionaries

Create CSV files with the following format:

```csv
English,简体中文,繁體中文,日本語,Italiano
Running,跑步,跑步,ランニング,Corsa
Walking,步行,步行,ウォーキング,Camminata
Swimming,游泳,游泳,スイミング,Nuoto
```

#### Dictionary Features

- **Exact Matching**: Precise string matching for consistent translations
- **Fuzzy Matching**: Handles variations in spacing, case, and punctuation
- **Multi-Dictionary Support**: Load multiple dictionaries simultaneously
- **Priority System**: Dictionaries are searched in order of loading
- **Easy Extension**: Simply add new CSV files to expand vocabulary

#### Included Dictionaries

- `AppleWatchWorkoutTypes.csv`: 90+ workout types in 4 languages

### 💡 Usage Examples

#### Example 1: Interactive Mode (Recommended)

```bash
python3 auto_strings_catalogs_translator.py
# Experience the beautiful interface with:
# 1. Gradient title display
# 2. Language detection from input file
# 3. Color-coded progress indicators
# 4. Intelligent translation suggestions
```

#### Example 2: Command Line Mode

```bash
python3 auto_strings_catalogs_translator.py Localizable.xcstrings Localizable_translated.xcstrings dictionaries/AppleWatchWorkoutTypes.csv
```

#### Example 3: Multiple Dictionaries

```bash
python3 auto_strings_catalogs_translator.py input.json output.xcstrings dict1.csv dict2.csv dict3.csv
```

### 🏗️ Project Structure

```
AutoStringsCatalogsTranslator/
├── auto_strings_catalogs_translator.py  # Main script with beautiful interface
├── README.md                            # This documentation
├── requirements.txt                     # Python dependencies
├── LICENSE                              # MIT License
├── .gitignore                          # Git ignore rules
├── dictionaries/                       # Dictionary files
│   └── AppleWatchWorkoutTypes.csv      # Apple Watch workout types
├── examples/                           # Example files
│   ├── sample_input.xcstrings         # Sample xcstrings file
│   └── sample_input.json              # Sample JSON file
└── docs/                               # Additional documentation
    └── API_SETUP.md                    # API configuration guide
```

### 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 🙏 Acknowledgments

- Apple for the `.xcstrings` format specification
- Various translation service providers
- Open source community for inspiration and feedback

---

## 中文版本

### 🚀 功能特色

- **🎯 智能语言检测**: 自动检测输入文件中的目标语言
- **📚 词典优先翻译**: 使用CSV词典确保翻译的一致性和准确性
- **🎨 精美终端界面**: 渐变色标题和Claude Code风格展示
- **🌐 多种翻译服务**: 支持Google翻译、有道翻译、百度翻译、腾讯翻译君
- **🎯 智能翻译模式**: 可选择跳过已翻译内容或全量重新翻译
- **📱 iOS/macOS支持**: 原生支持 `.xcstrings` 和 `.json` 格式
- **🌍 双语界面**: 支持中英文界面切换
- **⚡ 可扩展词典系统**: 轻松添加自定义翻译词典
- **🔄 自动格式检测**: 智能处理输入输出格式
- **🛡️ 请求频率控制**: 内置频率限制，保护API配额

### 📋 系统要求

- Python 3.7+
- 网络连接（用于API翻译服务）
- API密钥（高级服务需要，可选）

### 🚀 快速开始

#### 安装方法

```bash
git clone https://github.com/KookyBread/AutoStringsCatalogsTranslator.git
cd AutoStringsCatalogsTranslator
pip install -r requirements.txt
```

#### 基本使用

```bash
# 交互式模式（推荐首次使用）
python3 auto_strings_catalogs_translator.py

# 命令行模式
python3 auto_strings_catalogs_translator.py input.xcstrings output.xcstrings dictionaries/AppleWatchWorkoutTypes.csv
```

#### v1.0 新特性

- **🎨 精美终端界面**: Claude Code风格的渐变标题和彩色输出
- **🎯 智能语言检测**: 自动从输入文件检测目标语言
- **🌈 增强用户体验**: 彩色编码的输出和进度指示器

#### 交互式模式功能

1. **语言选择**: 选择界面语言（中文/英文）
2. **文件格式验证**: 仅接受 `.xcstrings` 或 `.json` 文件
3. **输出格式选择**: 
   - 保持与输入文件相同格式
   - 强制输出为 `.xcstrings` 格式
   - 强制输出为 `.json` 格式
4. **翻译模式选择**:
   - 跳过已翻译的条目
   - 全量重新翻译所有符合条件的条目
5. **服务选择**: 选择主要翻译服务和备用服务
6. **词典管理**: 自动发现和添加自定义词典

### 🎯 翻译服务

| 服务 | 类型 | 需要配置 | 特点 |
|------|------|----------|------|
| **Google翻译** | 免费 | 无 | 无需API密钥，有频率限制 |
| **有道翻译** | 免费+付费 | `YOUDAO_APP_KEY`, `YOUDAO_APP_SECRET` | 有免费额度 |
| **百度翻译** | 免费+付费 | `BAIDU_APP_ID`, `BAIDU_APP_KEY` | 每月200万字符免费 |
| **腾讯翻译君** | 免费+付费 | `TENCENT_SECRET_ID`, `TENCENT_SECRET_KEY` | 每月500万字符免费 |

### 🔧 环境配置

设置API凭证为环境变量：

```bash
# 有道翻译
export YOUDAO_APP_KEY="你的APP密钥"
export YOUDAO_APP_SECRET="你的APP密钥"

# 百度翻译
export BAIDU_APP_ID="你的APP_ID"
export BAIDU_APP_KEY="你的APP密钥"

# 腾讯翻译君
export TENCENT_SECRET_ID="你的SECRET_ID"
export TENCENT_SECRET_KEY="你的SECRET_KEY"
```

将这些添加到你的shell配置文件（`.bashrc`, `.zshrc` 等）中以便持久化。

### 📚 词典系统

#### 创建自定义词典

创建符合以下格式的CSV文件：

```csv
English,简体中文,繁體中文,日本語,Italiano
Running,跑步,跑步,ランニング,Corsa
Walking,步行,步行,ウォーキング,Camminata
Swimming,游泳,游泳,スイミング,Nuoto
```

#### 词典功能

- **精确匹配**: 字符串精确匹配，确保翻译一致性
- **模糊匹配**: 处理空格、大小写、标点符号的变化
- **多词典支持**: 同时加载多个词典文件
- **优先级系统**: 按加载顺序搜索词典
- **易于扩展**: 简单添加新的CSV文件即可扩展词汇

#### 内置词典

- `AppleWatchWorkoutTypes.csv`: 90多种运动类型，支持4种语言

### 💡 使用示例

#### 示例1: 使用词典的基本翻译

```bash
python3 auto_strings_catalogs_translator.py Localizable.xcstrings Localizable_translated.xcstrings dictionaries/AppleWatchWorkoutTypes.csv
```

#### 示例2: 交互式模式自定义设置

```bash
python3 auto_strings_catalogs_translator.py
# 按照交互式提示进行：
# 1. 选择界面语言
# 2. 选择输入文件
# 3. 选择输出格式
# 4. 选择翻译模式
# 5. 选择翻译服务
# 6. 添加自定义词典
```

#### 示例3: 多个词典

```bash
python3 auto_strings_catalogs_translator.py input.json output.xcstrings dict1.csv dict2.csv dict3.csv
```

### 🏗️ 项目结构

```
AutoStringsCatalogsTranslator/
├── auto_strings_catalogs_translator.py    # 主脚本
├── README.md                     # 说明文档
├── requirements.txt              # Python依赖
├── LICENSE                       # MIT许可证
├── .gitignore                   # Git忽略规则
├── dictionaries/                # 词典文件目录
│   └── AppleWatchWorkoutTypes.csv
├── examples/                    # 示例文件
│   ├── sample_input.xcstrings
│   └── sample_input.json
└── docs/                        # 额外文档
    └── API_SETUP.md
```

### 🤝 贡献指南

1. Fork 这个仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 📝 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

### 🙏 致谢

- Apple提供的 `.xcstrings` 格式规范
- 各种翻译服务提供商
- 开源社区的灵感和反馈

---

## 📞 Support

If you encounter any issues or have questions, please:

1. Check the [documentation](docs/)
2. Search existing [issues](https://github.com/KookyBread/AutoStringsCatalogsTranslator/issues)
3. Create a new issue with detailed information

## 🔄 Version History

- **v1.0.0** - Major UI and UX improvements
  - **🎨 Beautiful Terminal Interface**: Claude Code-style gradient title and colors
  - **🎯 Automatic Language Detection**: Smart detection from input files
  - **🌈 Enhanced User Experience**: Color-coded output and progress indicators
  - **📊 Improved Progress Display**: Real-time translation progress with language names
  - **🔧 Better Error Handling**: Colorized error messages and warnings

- **v1.0.0** - Initial release with full feature set
  - Dictionary-first translation system
  - Multiple translation service support
  - Bilingual interface
  - Comprehensive error handling and validation
