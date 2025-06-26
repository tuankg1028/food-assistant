# 🍔 Food Shopping Assistant

A Vietnamese food shopping assistant that helps you find and compare products across major Vietnamese grocery retailers using AI-powered search and analysis.

## Features

- **Multi-retailer Search**: Search across multiple Vietnamese grocery websites simultaneously
- **Real-time Product Information**: Get current prices, discounts, and availability
- **Intelligent Query Processing**: AI-optimized search queries for better results
- **Chat Interface**: Natural conversation interface powered by Streamlit
- **Price Comparison**: Compare products across different retailers
- **Discount Highlighting**: Automatic detection and highlighting of sales and promotions

## Supported Retailers

- **Kingfoodmart** (kingfoodmart.com)
- **Bách Hóa Xanh** (bachhoaxanh.com)
- **Winmart** (winmart.vn)

## Tech Stack

- **Frontend**: Streamlit
- **AI/LLM**: OpenAI GPT-4o
- **Web Search**: Tavily API
- **Web Scraping**: Jina AI
- **Language Support**: Vietnamese and English

## Prerequisites

- Python 3.8+
- OpenAI API key
- Tavily API key
- Jina AI API key

## Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd food
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your API keys:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   JINA_API_KEY=your_jina_api_key_here
   ```

## API Keys Setup

### OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com)
2. Create an account or sign in
3. Navigate to API Keys section
4. Create a new API key

### Tavily API Key

1. Visit [Tavily](https://app.tavily.com)
2. Sign up for an account
3. Get your API key from the dashboard

### Jina AI API Key

1. Visit [Jina AI](https://jina.ai)
2. Create an account
3. Get your API key from the platform

## Usage

1. **Start the application**

   ```bash
   streamlit run main.py
   ```

2. **Open your browser**
   Navigate to `http://localhost:8501`

3. **Start searching**
   - Type your food product questions in Vietnamese or English
   - Examples:
     - "Tìm sữa tươi giá rẻ nhất"
     - "Find the cheapest fresh milk"
     - "So sánh giá gạo ST25"
     - "Compare rice prices"

## Project Structure

```
food/
├── main.py                 # Main Streamlit application
├── config.py              # Configuration settings and prompts
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in git)
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── README.md             # Project documentation
└── utils/                # Utility modules
    ├── api_clients.py    # API client initialization
    ├── search.py         # Web search functionality
    └── response.py       # GPT response processing
```

## Configuration

The `config.py` file contains important settings:

- **ALLOWED_DOMAINS**: List of supported retailer domains
- **QUERY_OPTIMIZER_PROMPT**: Prompt for optimizing search queries
- **GPT_RESPONSE_PROMPT**: Prompt for generating responses

## Features in Detail

### Intelligent Search

- Automatically optimizes your search queries for better results
- Searches across multiple retailers simultaneously
- Extracts key product information and specifications

### Multi-language Support

- Supports both Vietnamese and English queries
- Automatically detects query language and responds accordingly
- Translates product information appropriately

### Real-time Data

- Scrapes current product information from retailer websites
- Shows live prices, discounts, and availability
- Highlights special offers and promotions

### Chat Interface

- Maintains conversation history
- Streaming responses for better user experience
- Easy-to-use interface with source citations

## Troubleshooting

### Common Issues

1. **API Key Errors**

   - Ensure all API keys are correctly set in `.env`
   - Check that API keys have sufficient credits/quota
   - Verify API key format and validity

2. **No Search Results**

   - Check internet connection
   - Verify that target websites are accessible
   - Try different search terms or keywords

3. **Slow Responses**
   - Large queries may take time to process
   - Web scraping depends on website response times
   - Consider using more specific search terms

### Getting Help

If you encounter issues:

1. Check the console logs for error messages
2. Verify all dependencies are installed correctly
3. Ensure API keys are valid and have quota remaining

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational and personal use. Please respect the terms of service of the retailer websites being accessed.
