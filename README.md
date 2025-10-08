# Create README.md
@"
# Facebook Category Scraper

Automated Facebook hashtag trending analyzer that discovers and analyzes the top 10 trending hashtags across 8 different categories using real engagement metrics.

## 🌟 Features

- **8 Categories Supported**: Technology, Business, Health, Food, Travel, Fashion, Entertainment, Sports
- **Real Engagement Metrics**: Extracts likes, comments, and shares from actual Facebook posts
- **Sentiment Analysis**: Analyzes post sentiment using TextBlob
- **Smart Trending Algorithm**: Calculates trending scores based on engagement, post count, sentiment, and time factors
- **Dual Mode Operation**:
  - **Interactive Mode**: Manual category selection with detailed results
  - **Automated Mode**: GitHub Actions support for scheduled runs
- **Database Integration**: Automatic data storage in Supabase
- **Intelligent Fallback**: Uses predefined hashtags if scraping fails

## 📋 Categories

| Category | Keywords | Sample Hashtags |
|----------|----------|-----------------|
| Technology | tech, innovation, AI, software | #technology, #AI, #machinelearning |
| Business | entrepreneur, startup, marketing | #business, #entrepreneur, #startup |
| Health | fitness, wellness, nutrition | #health, #fitness, #wellness |
| Food | cooking, recipe, chef | #food, #foodie, #cooking |
| Travel | tourism, vacation, adventure | #travel, #wanderlust, #vacation |
| Fashion | style, beauty, makeup | #fashion, #style, #ootd |
| Entertainment | movies, music, gaming | #entertainment, #movies, #music |
| Sports | football, basketball, athlete | #sports, #fitness, #athlete |

## 🚀 Setup

### Prerequisites

- Python 3.8+
- Firefox browser (for Playwright)
- Facebook account
- Supabase account (for database storage)

### Installation

1. **Clone the repository**
``````bash
git clone https://github.com/Aditya0611/Facebook_hashing.git
cd Facebook_hashing

Install dependencies

bashpip install -r requirements.txt

Install Playwright browsers

bashplaywright install firefox
playwright install-deps firefox

Download TextBlob corpora

bashpython -m textblob.download_corpora
Configuration
Create a .env file in the project root:
env# Facebook Credentials
FACEBOOK_EMAIL=your_email@example.com
FACEBOOK_PASSWORD=your_password

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key

# Optional: For automated runs
SCRAPE_CATEGORY=technology
⚠️ IMPORTANT: Never commit your .env file to Git!
💻 Usage
Local Interactive Mode
Run the script to manually select categories:
bashpython facebook_category_scraper.py
Follow the prompts:

Enter category number (1-8) or name
Wait 2-4 minutes for scraping
View detailed results
Optionally scrape another category

Automated Mode (GitHub Actions)
Set the SCRAPE_CATEGORY environment variable:
bashexport SCRAPE_CATEGORY=technology
python facebook_category_scraper.py
🤖 GitHub Actions Setup
1. Add Repository Secrets
Go to: Settings → Secrets and variables → Actions
Add these 4 secrets:

FACEBOOK_EMAIL
FACEBOOK_PASSWORD
SUPABASE_URL
SUPABASE_ANON_KEY

2. Workflow Configuration
The workflow (.github/workflows/facebook-scraper.yml) runs:

Automatically: Every 12 hours
Manually: Via workflow dispatch with category selection

3. Manual Workflow Run

Go to Actions tab
Select "Facebook Category Scraper"
Click "Run workflow"
Choose category (default: technology)
Click "Run workflow"

📊 Database Schema
Supabase Table: facebook
sqlCREATE TABLE facebook (
  id BIGSERIAL PRIMARY KEY,
  platform TEXT NOT NULL DEFAULT 'Facebook',
  "topic/hashtag" TEXT NOT NULL,
  engagement_score DOUBLE PRECISION,
  sentiment_polarity DOUBLE PRECISION,
  sentiment_label TEXT,
  posts BIGINT,
  views BIGINT,
  metadata JSONB,
  scraped_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  version_id UUID NOT NULL
);

CREATE INDEX idx_facebook_scraped_at ON facebook(scraped_at);
CREATE INDEX idx_facebook_version_id ON facebook(version_id);
CREATE INDEX idx_facebook_hashtag ON facebook("topic/hashtag");
Metadata Structure
json{
  "category": "technology",
  "trending_score": 85.5,
  "avg_engagement": 2500,
  "likes": 1500,
  "comments": 800,
  "shares": 200,
  "avg_likes": 150.0,
  "avg_comments": 80.0,
  "avg_shares": 20.0,
  "hashtag_url": "https://www.facebook.com/hashtag/technology",
  "is_estimated": false
}
📈 Output
Console Output

Real-time scraping progress
Top 10 trending hashtags with scores
Summary statistics
Top performers analysis

JSON File
facebook_top10_{category}_{timestamp}.json
Supabase Database
All results automatically saved with version tracking
🔧 Key Features Explained
Engagement Score (1-10)
Weighted calculation:

Likes × 1
Comments × 4
Shares × 8

Logarithmic scaling for fairness across different post sizes.
Trending Score (0-100)
Factors:

Engagement score (25%)
Post count (20%)
Total engagement (15%)
Average engagement (15%)
Sentiment (10%)
Time factor (15%)
Consistency (5%)

Smart Estimation
If engagement data is partially missing, the scraper intelligently estimates based on available metrics and content quality.
🛠️ Troubleshooting
Login Issues

Verify Facebook credentials in .env
Check for 2FA (not supported)
Ensure account is not locked

Scraping Failures

Facebook may block automated access temporarily
Wait 15-30 minutes and retry
Use fallback data if needed

Supabase Connection

Verify URL and key in .env
Check table exists with correct schema
Review Supabase logs for errors

📝 Requirements
playwright==1.40.0
supabase==2.3.0
textblob==0.17.1
python-dotenv==1.0.0
🔒 Security

Never commit .env file
Use GitHub Secrets for automation
Rotate credentials if exposed
Keep dependencies updated

📄 License
MIT License - Feel free to use and modify
🤝 Contributing

Fork the repository
Create feature branch
Commit changes
Push to branch
Open pull request

📧 Support
For issues or questions:

Open an issue on GitHub
Check existing issues for solutions


Made with ❤️ for trend analysis
"@ | Out-File -FilePath "README.md" -Encoding UTF8
Write-Host "✅ README.md created successfully!" -ForegroundColor Green

This README is comprehensive and matches your exact code structure, including:
- All 8 categories with their keywords
- Both interactive and automated modes
- Complete database schema
- GitHub Actions setup
- Security warnings
- Troubleshooting section

Save this and push it to your repository!
