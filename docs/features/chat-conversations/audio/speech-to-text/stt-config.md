---
sidebar_position: 1
title: "配置"
---

Open WebUI 同时支持本地、浏览器内置和远程语音转文本。

![STT 配置示意图](/images/tutorials/stt/image.png)

![STT 提供商示意图](/images/tutorials/stt/stt-providers.png)

## 云端 / 远程语音转文本提供商

当前支持以下语音转文本提供商：

| 服务 | 是否需要 API 密钥 | 指南 |
|---------|------------------|-------|
| Local Whisper（默认） | ❌ | 内置支持，参见 [环境变量](/features/chat-conversations/audio/speech-to-text/env-variables) |
| OpenAI（Whisper API） | ✅ | [OpenAI STT 指南](/features/chat-conversations/audio/speech-to-text/openai-stt-integration) |
| Mistral（Voxtral） | ✅ | [Mistral Voxtral 指南](/features/chat-conversations/audio/speech-to-text/mistral-voxtral-integration) |
| Deepgram | ✅ | — |
| Azure | ✅ | — |

**Web API** 则通过浏览器内置语音识别提供 STT（无需 API 密钥，在用户设置中配置）。

## 配置你的 STT 提供商

要配置语音转文本提供商：

- 进入管理面板
- 选择音频
- 填入 API 密钥，并从下拉框选择模型

![STT 配置页面截图](/images/tutorials/stt/stt-config.png)

## 用户级设置

除了在管理员面板中配置的实例级设置外，还有一些用户级设置可以提供额外功能。

- **STT 设置：** 包含与语音转文本相关的设置。
- **语音转文本引擎：** 决定使用哪种语音识别引擎（默认值或 Web API）。

![用户级音频设置截图](/images/tutorials/stt/user-settings.png)

## 使用 STT

语音转文本是一种高效“书写”提示词的方式；无论桌面端还是移动端，都有不错的使用体验。

要使用 STT，只需点击麦克风图标：

![点击麦克风开始 STT 的示意图](/images/tutorials/stt/stt-operation.png)

出现实时音频波形后，说明语音已被成功采集：

![正在进行中的 STT 录音波形截图](/images/tutorials/stt/stt-in-progress.png)

## STT 录音模式操作

开始录音后，你可以：

- 点击勾选图标保存录音（如果启用了完成后自动发送，就会自动发送；否则你也可以手动发送）
- 如果想中止录音（例如想重新开始），可以点击 `x` 图标退出录音界面

![结束 STT 录音的示意图](/images/tutorials/stt/endstt.png)

## 故障排查

### 常见问题

#### “int8 compute type not supported” 错误

如果你看到类似 `Error transcribing chunk: Requested int8 compute type, but the target device or backend do not support efficient int8 computation` 的报错，通常表示你的 GPU 不支持所请求的 `int8` 计算。

**解决方案：**
- **升级到最新版本** —— 近期更新已改进 compute type 的持久化配置，以解决已知 CUDA 兼容性问题。
- **改用标准 Docker 镜像** 而不是 `:cuda` 镜像 —— 较旧 GPU（Maxwell 架构，约 2014-2016 年）可能不受现代 CUDA 加速库支持。
- 使用 `WHISPER_COMPUTE_TYPE` 环境变量调整计算类型：
  ```yaml
  environment:
    - WHISPER_COMPUTE_TYPE=float16  # 或 float32
  ```

:::tip
对于 Whisper 这类较小模型，CPU 模式通常也能提供相近的体验，同时避免 GPU 兼容性问题。` :cuda ` 镜像主要加速的是 RAG embedding，对大多数用户的 STT 速度提升并不明显。
:::

#### 麦克风无法工作

1. **检查浏览器权限** —— 确保浏览器已获得麦克风权限
2. **使用 HTTPS** —— 某些浏览器要求安全连接才允许麦克风访问
3. **尝试其他浏览器** —— Chrome 通常对 Web Audio API 支持最好

#### 识别准确率较差

- 使用 `WHISPER_LANGUAGE=en` **显式设置语言**（使用 ISO 639-1 代码）
- **切换多语言支持** —— 如果需要支持英语以外的语言，可设置 `WHISPER_MULTILINGUAL=true`。关闭时（默认值）会使用仅英语版本模型，以获得更好的英文任务性能。
- **使用更大的 Whisper 模型** —— 可选：`tiny`、`base`、`small`、`medium`、`large`
- 模型越大通常越准确，但速度也越慢

更多排查信息请参阅 [音频故障排查指南](/troubleshooting/audio)。
