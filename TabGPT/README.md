# ChatGPT Integration with Tableau

A complete guide for integrating OpenAI's ChatGPT with Tableau Desktop using TabPy. This enables you to use AI-powered text analysis and generation directly within your Tableau workbooks.

## 🎯 What This Does

This integration allows you to:
- Send text prompts from Tableau to ChatGPT
- Get AI-generated responses back into your visualizations
- Perform advanced text analysis using AI
- Create dynamic, AI-powered calculated fields

## 📋 Prerequisites

Before starting, ensure you have:
- **Tableau Desktop** (any recent version)
- **Windows or Mac computer** with admin rights
- **Internet connection** for API calls
- **OpenAI account** (free tier works for testing)

## 🚀 Part 1: Initial Setup (One-Time Only)

### Step 1: Install Python Components

**Why:** TabPy requires specific Python libraries to communicate between Tableau and external services.

1. **Open Command Prompt (Windows) or Terminal (Mac)**
   - Windows: Press `Win + R`, type `cmd`, press Enter
   - Mac: Press `Cmd + Space`, type `Terminal`, press Enter

2. **Install required packages:**
   ```bash
   pip install tabpy openai
   ```
   
3. **Wait for installation to complete** (usually 2-3 minutes)

### Step 2: Get Your OpenAI API Key

**Why:** This authenticates your requests to ChatGPT's servers.

1. **Visit** [platform.openai.com](https://platform.openai.com)
2. **Sign up** or log in to your account
3. **Click your profile icon** (top right) → "View API keys"
4. **Click** "Create new secret key"
5. **Name your key** and **select a project**
6. **Copy the key** and save it securely (you won't see it again!)

### Step 3: Configure Your API Key

**Why:** Your system needs to know your API key to make requests to OpenAI.

**For Windows:**
1. Press `Win + R`, type `sysdm.cpl`, press Enter
2. Click "Environment Variables" button
3. Click "New" under User variables
4. Variable name: `OPENAI_API_KEY`
5. Variable value: [paste your API key here]
6. Click OK, OK, OK
7. **Restart your computer** for changes to take effect

**For Mac:**
1. Open Terminal
2. Type: `echo 'export OPENAI_API_KEY="your_api_key_here"' >> ~/.zshrc`
3. Replace `your_api_key_here` with your actual API key
4. Type: `source ~/.zshrc`

## 🔧 Part 2: Deploy the ChatGPT Function

### Step 4: Start TabPy Server

**Why:** TabPy acts as a bridge between Tableau and Python functions.

1. **Open Command Prompt/Terminal**
2. **Navigate to your project folder:**
   ```bash
   cd /path/to/your/tabpy/folder
   ```
3. **Start the TabPy server:**
   ```bash
   tabpy
   ```
4. **Look for this message:** `Web service listening on port 9004`
5. **Keep this window open** - closing it stops the service

### Step 5: Deploy the ChatGPT Function

**Why:** This registers your custom ChatGPT function with TabPy so Tableau can use it.

1. **Open a NEW Command Prompt/Terminal window** (keep the first one running)
2. **Navigate to your project folder again:**
   ```bash
   cd /path/to/your/tabpy/folder
   ```
3. **Run the deployment script:**
   ```bash
   python deploy.py
   ```
4. **Look for success message:** Function successfully deployed

**If you see errors:**
- Check your API key is set correctly
- Ensure TabPy server is still running in the other window
- Verify you're in the correct folder

## 📊 Part 3: Connect Tableau to TabPy

### Step 6: Configure Tableau

**Why:** Tableau needs to know where to find your TabPy server.

1. **Open Tableau Desktop**
2. **Go to:** Help → Settings and Performance → Manage Analytics Extension Connection
3. **Select:** TabPy/External API
4. **Enter connection details:**
   - Server: `localhost`
   - Port: `9004`
5. **Click:** Test Connection
6. **You should see:** "Successfully connected"
7. **Click:** Save

### Step 7: Test the Integration

**Why:** Verify everything is working before building complex workbooks.

1. **Create a new Tableau workbook**
2. **Create a calculated field** with this formula:
   ```
   SCRIPT_STR("return tabpy.query('chat_gpt_query', _arg1)", "What is the capital of France?")
   ```
3. **Add the calculated field to your worksheet**
4. **You should see:** "Paris" (or similar response from ChatGPT)

## 💡 Using ChatGPT in Your Workbooks

### Basic Usage

Create calculated fields using this pattern:
```
SCRIPT_STR("return tabpy.query('chat_gpt_query', _arg1)", [Your Prompt])
```

### Practical Examples

**Sentiment Analysis:**
```
SCRIPT_STR("return tabpy.query('chat_gpt_query', _arg1)", 
"Analyze the sentiment of this review and respond with only 'Positive', 'Negative', or 'Neutral': " + [Review Text])
```

**Category Classification:**
```
SCRIPT_STR("return tabpy.query('chat_gpt_query', _arg1)", 
"Categorize this product description into one word: Electronics, Clothing, Books, or Other: " + [Product Description])
```

**Text Summarization:**
```
SCRIPT_STR("return tabpy.query('chat_gpt_query', _arg1)", 
"Summarize this text in 10 words or less: " + [Long Text Field])
```

## 🔧 Troubleshooting

### Common Issues and Solutions

**❌ "Connection failed" in Tableau:**
- Ensure TabPy server is running (`tabpy` command in terminal)
- Check server address is `localhost` and port is `9004`
- Try restarting TabPy server

**❌ "Function not found" error:**
- Re-run `python deploy.py`
- Check the deployment script completed successfully
- Verify you're using the correct function name

**❌ "API key not found" error:**
- Verify your OpenAI API key is set correctly
- Restart your computer (Windows) or terminal session (Mac)
- Check you have credits remaining in your OpenAI account

**❌ Slow responses:**
- This is normal - ChatGPT API calls take 2-10 seconds
- Consider caching results for repeated queries
- Use specific prompts to get shorter responses

### Getting Help

If you encounter issues:
1. Check the TabPy log files in your project folder
2. Verify your OpenAI account has available credits
3. Test with simple prompts first before complex ones

## 📁 Project Files Explained

- **`chat_gpt_query.py`** - The main function that communicates with ChatGPT
- **`deploy.py`** - Script that registers the function with TabPy
- **`tabpy_config.conf`** - Configuration settings for TabPy
- **`requirements.txt`** - List of required Python packages
- **Log files** - Troubleshooting information

## 🔒 Security Notes

- **Never share your OpenAI API key**
- **Monitor your OpenAI usage** to avoid unexpected charges
- **Use specific prompts** to prevent misuse
- **Consider rate limiting** for production use

## 💰 Cost Considerations

- OpenAI charges per API call
- GPT-4 costs more than GPT-3.5
- Monitor usage at [platform.openai.com](https://platform.openai.com)
- Consider using caching for repeated queries

## 🎉 You're Ready!

You now have ChatGPT integrated with Tableau! Start with simple prompts and gradually build more complex AI-powered visualizations.

