# API Setup Guide

This guide will help you set up API credentials for various translation services supported by Localization Translator.

## 🌐 Google Translate

Google Translate is available without API setup, but has rate limiting.

- **Cost**: Free
- **Setup**: No API key required
- **Limitations**: Rate limited, may block frequent requests
- **Recommendation**: Good for testing and small projects

## 🔵 Youdao Translate (有道翻译)

### Getting API Credentials

1. Visit [Youdao AI Open Platform](https://ai.youdao.com/)
2. Register an account and verify your identity
3. Create a new application
4. Get your APP_KEY and APP_SECRET

### Environment Setup

```bash
export YOUDAO_APP_KEY="your_app_key_here"
export YOUDAO_APP_SECRET="your_app_secret_here"
```

### Features
- **Cost**: Free tier available (limited requests)
- **Quality**: Good for Chinese translations
- **Languages**: Supports major languages including Chinese, Japanese, Italian

## 🔴 Baidu Translate (百度翻译)

### Getting API Credentials

1. Visit [Baidu Translate Open Platform](http://api.fanyi.baidu.com/)
2. Register and create a developer account
3. Create a new application
4. Get your APP_ID and APP_KEY

### Environment Setup

```bash
export BAIDU_APP_ID="your_app_id_here"
export BAIDU_APP_KEY="your_app_key_here"
```

### Features
- **Cost**: 2 million characters free per month
- **Quality**: Excellent for Chinese translations
- **Speed**: Fast response times

## 🟢 Tencent Cloud Translation (腾讯翻译君)

### Getting API Credentials

1. Visit [Tencent Cloud Console](https://console.cloud.tencent.com/)
2. Create an account and verify your identity
3. Navigate to "Translation" service
4. Create API credentials (SecretId and SecretKey)

### Environment Setup

```bash
export TENCENT_SECRET_ID="your_secret_id_here"
export TENCENT_SECRET_KEY="your_secret_key_here"
```

### Features
- **Cost**: 5 million characters free per month
- **Quality**: High-quality translations
- **Languages**: Comprehensive language support

## 🔧 Setting Up Environment Variables

### Temporary Setup (Current Session Only)

```bash
export YOUDAO_APP_KEY="your_key"
export YOUDAO_APP_SECRET="your_secret"
# ... other variables
```

### Permanent Setup

#### For Bash (.bashrc)

```bash
echo 'export YOUDAO_APP_KEY="your_key"' >> ~/.bashrc
echo 'export YOUDAO_APP_SECRET="your_secret"' >> ~/.bashrc
source ~/.bashrc
```

#### For Zsh (.zshrc)

```bash
echo 'export YOUDAO_APP_KEY="your_key"' >> ~/.zshrc
echo 'export YOUDAO_APP_SECRET="your_secret"' >> ~/.zshrc
source ~/.zshrc
```

#### For Fish (.config/fish/config.fish)

```fish
set -Ux YOUDAO_APP_KEY "your_key"
set -Ux YOUDAO_APP_SECRET "your_secret"
```

### Using .env File (Alternative)

Create a `.env` file in your project directory:

```bash
# .env file
YOUDAO_APP_KEY=your_app_key_here
YOUDAO_APP_SECRET=your_app_secret_here
BAIDU_APP_ID=your_app_id_here
BAIDU_APP_KEY=your_app_key_here
TENCENT_SECRET_ID=your_secret_id_here
TENCENT_SECRET_KEY=your_secret_key_here
```

Then load it before running the script:

```bash
export $(grep -v '^#' .env | xargs)
python3 localization_translator.py
```

## ✅ Verifying Setup

The Localization Translator will automatically detect which services are properly configured:

```bash
python3 localization_translator.py
```

You'll see output like:

```
🌐 Available translation services:
1. Google Translate - 🆓 Free to use
2. Youdao Translate - 🔑 Requires API key
   ✅ Environment variables configured
3. Baidu Translate - 🔑 Requires API key
   ⚠️ Missing environment variables: BAIDU_APP_ID, BAIDU_APP_KEY
```

## 🚨 Security Best Practices

1. **Never commit API keys to version control**
2. **Use environment variables** instead of hardcoding credentials
3. **Regularly rotate your API keys**
4. **Monitor your API usage** to detect unusual activity
5. **Use least privilege principle** - only grant necessary permissions

## 🏷️ Cost Optimization Tips

1. **Use dictionary-first approach** - The tool checks dictionaries before making API calls
2. **Choose appropriate fallback services** - Configure cheaper services as fallbacks
3. **Monitor your usage** - Most services provide usage dashboards
4. **Batch translations** - Process multiple files in one session to reduce overhead

## 🆘 Troubleshooting

### Common Issues

1. **"Missing environment variables" error**
   - Verify variables are exported: `echo $YOUDAO_APP_KEY`
   - Check spelling and format
   - Restart terminal after setting variables

2. **API authentication errors**
   - Verify credentials are correct
   - Check if API service is enabled in your account
   - Ensure billing is set up (for paid services)

3. **Rate limiting errors**
   - Switch to a different service
   - Add delays between requests
   - Consider upgrading to paid tier

### Getting Help

If you encounter issues:

1. Check service status pages
2. Review API documentation for each service
3. Verify your account status and quotas
4. Contact service support if needed

## 📊 Service Comparison

| Service | Free Tier | Languages | Quality | Speed | Setup Difficulty |
|---------|-----------|-----------|---------|-------|-----------------|
| Google | Limited | 100+ | Good | Fast | Easy |
| Youdao | Yes | 100+ | Excellent (Chinese) | Fast | Medium |
| Baidu | 2M chars/month | 200+ | Excellent (Chinese) | Very Fast | Medium |
| Tencent | 5M chars/month | 15+ | High | Fast | Medium |

Choose the services that best fit your needs, language requirements, and budget.