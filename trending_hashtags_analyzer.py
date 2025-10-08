#!/usr/bin/env python3
"""
Trending Hashtags Analyzer - Discovers and analyzes top trending hashtags on Facebook
"""

import os
import sys
import json
import time
import random
from datetime import datetime
from collections import defaultdict, Counter
from typing import List, Dict, Tuple
from base import FacebookScraper

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    print("Installing colorama for colored output...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
    from colorama import init, Fore, Back, Style
    init(autoreset=True)

class TrendingHashtagsAnalyzer:
    """Analyzes trending hashtags with comprehensive metrics."""
    
    def __init__(self, headless: bool = False):
        self.scraper = FacebookScraper(headless=headless)
        self.hashtag_data = {}
        
        # Categories and keywords for hashtag discovery
        self.categories = {
            "technology": ["tech", "innovation", "gadgets", "software", "hardware"],
        
        }
        
        # Hashtag categories mapping
        self.hashtag_categories = {
            "technology": "🔧 Technology & Innovation",
            "AI": "🤖 Artificial Intelligence",
            "innovation": "💡 Innovation & R&D",
            "business": "💼 Business & Finance",
            "startup": "🚀 Startup & Entrepreneurship",
            "marketing": "📈 Marketing & Advertising",
            "social": "👥 Social Media & Community",
            "entertainment": "🎬 Entertainment & Media",
            "travel": "✈️ Travel & Tourism",
            "lifestyle": "🌟 Lifestyle & Personal"
        }
    
    def get_hashtag_category(self, hashtag: str) -> str:
        """Get the category for a hashtag."""
        return self.hashtag_categories.get(hashtag.lower(), "📊 General")
    
    def discover_hashtags_by_category(self) -> Dict[str, Dict[str, int]]:
        """Discover trending hashtags by category using real Facebook scraping."""
        trending_hashtags = {}
        
        for category, keywords in self.categories.items():
            print(f"\n{Fore.CYAN}{Style.BRIGHT}🔍 DISCOVERING HASHTAGS IN {category} CATEGORY{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Searching {len(keywords)} keywords...{Style.RESET_ALL}\n")
            
            category_hashtags = {}
            
            for keyword in keywords:
                print(f"{Fore.BLUE}[{keyword}] Scraping Facebook posts...{Style.RESET_ALL}")
                
                try:
                    # Scrape posts for this keyword to discover hashtags
                    posts = self.scraper.scrape_hashtag_posts(keyword, max_posts=20)
                    
                    if posts:
                        # Extract hashtags from post content
                        discovered = self.scraper.discover_hashtags_from_posts(posts)
                        
                        # Filter out the original keyword and very low frequency hashtags
                        filtered_hashtags = {
                            hashtag: data for hashtag, data in discovered.items()
                            if hashtag.lower() != keyword.lower() and data.get('frequency', 0) >= 2
                        }
                        
                        # Add to category hashtags with frequency as count
                        for hashtag, data in filtered_hashtags.items():
                            if hashtag in category_hashtags:
                                category_hashtags[hashtag] += data.get('frequency', 1)
                            else:
                                category_hashtags[hashtag] = data.get('frequency', 1)
                        
                        print(f"{Fore.GREEN}✓ Discovered {len(filtered_hashtags)} hashtags from {len(posts)} posts{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.YELLOW}⚠ No posts found for {keyword}{Style.RESET_ALL}")
                        
                except Exception as e:
                    print(f"{Fore.RED}❌ Error scraping {keyword}: {str(e)}{Style.RESET_ALL}")
                    continue
                
                # Small delay between keywords
                time.sleep(2)
            
            # Sort hashtags by frequency and store top ones
            if category_hashtags:
                sorted_hashtags = dict(sorted(category_hashtags.items(), key=lambda item: item[1], reverse=True))
                trending_hashtags[category] = dict(list(sorted_hashtags.items())[:20])  # Top 20 per category
                print(f"{Fore.CYAN}📊 Category {category}: {len(trending_hashtags[category])} trending hashtags{Style.RESET_ALL}")
            else:
                trending_hashtags[category] = {}
                print(f"{Fore.YELLOW}⚠ No hashtags discovered for {category} category{Style.RESET_ALL}")
        
        return trending_hashtags
    
    def analyze_specific_hashtags(self, max_posts_per_hashtag: int = 20) -> Dict[str, List[Dict]]:
        """Analyze specific hashtags directly."""
        print(f"{Fore.CYAN}{Style.BRIGHT}🔍 ANALYZING 10 TRENDING HASHTAGS{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Searching {len(self.categories)} categories with {max_posts_per_hashtag} posts each...{Style.RESET_ALL}\n")
        
        hashtag_posts = {}
        
        for category, hashtags in self.discover_hashtags_by_category().items():
            for i, hashtag in enumerate(hashtags, 1):
                print(f"{Fore.BLUE}[{i}/{len(hashtags)}] Analyzing #{hashtag}...{Style.RESET_ALL}")
                
                posts = self.scraper.scrape_hashtag_posts(hashtag, max_posts=max_posts_per_hashtag)
                
                if posts:
                    hashtag_posts[hashtag.lower()] = posts
                    print(f"{Fore.GREEN}✓ Found {len(posts)} posts for #{hashtag}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}✗ No posts found for #{hashtag}{Style.RESET_ALL}")
                
                time.sleep(random.uniform(1, 2))  # Rate limiting
        
        return hashtag_posts
    
    def analyze_hashtag_metrics(self, hashtag: str, posts: List[Dict]) -> Dict:
        """Analyze comprehensive metrics for a hashtag."""
        if not posts:
            return {}
        
        total_posts = len(posts)
        total_likes = sum(post.get('likes', 0) for post in posts)
        total_comments = sum(post.get('comments', 0) for post in posts)
        total_shares = sum(post.get('shares', 0) for post in posts)
        total_engagement = total_likes + total_comments + total_shares
        avg_engagement = total_engagement / total_posts if total_posts > 0 else 0
        
        # Engagement rating (1-10 scale)
        engagement_scores = [post.get('engagement_score', 0) for post in posts]
        avg_engagement_rating = sum(engagement_scores) / len(engagement_scores) if engagement_scores else 0
        
        # Sentiment analysis
        sentiments = [post.get('sentiment', 'neutral') for post in posts]
        sentiment_counts = Counter(sentiments)
        
        positive_count = sentiment_counts.get('positive', 0)
        negative_count = sentiment_counts.get('negative', 0)
        neutral_count = sentiment_counts.get('neutral', 0)
        
        # Overall sentiment
        if positive_count > negative_count and positive_count > neutral_count:
            overall_sentiment = 'positive'
        elif negative_count > positive_count and negative_count > neutral_count:
            overall_sentiment = 'negative'
        else:
            overall_sentiment = 'neutral'
        
        # Polarity and subjectivity
        polarities = [post.get('polarity', 0) for post in posts if post.get('polarity') is not None]
        subjectivities = [post.get('subjectivity', 0) for post in posts if post.get('subjectivity') is not None]
        
        avg_polarity = sum(polarities) / len(polarities) if polarities else 0
        avg_subjectivity = sum(subjectivities) / len(subjectivities) if subjectivities else 0
        
        # Top post
        top_post = max(posts, key=lambda p: p.get('engagement_score', 0)) if posts else {}
        
        # Hashtag URL
        hashtag_url = f"https://www.facebook.com/hashtag/{hashtag}"
        
        return {
            'hashtag': hashtag,
            'total_posts': total_posts,
            'total_likes': total_likes,
            'total_comments': total_comments,
            'total_shares': total_shares,
            'total_engagement': total_engagement,
            'avg_engagement': avg_engagement,
            'avg_engagement_rating': avg_engagement_rating,
            'overall_sentiment': overall_sentiment,
            'avg_polarity': avg_polarity,
            'avg_subjectivity': avg_subjectivity,
            'sentiment_distribution': {
                'positive': positive_count,
                'negative': negative_count,
                'neutral': neutral_count
            },
            'top_post': top_post,
            'hashtag_url': hashtag_url,
            'posts': posts
        }
    
    def get_trending_score(self, metrics: Dict) -> float:
        """Calculate trending score based on multiple factors."""
        engagement_factor = min(metrics.get('total_engagement', 0) / 1000, 10)  # Cap at 10
        posts_factor = min(metrics.get('total_posts', 0) / 10, 5)  # Cap at 5
        rating_factor = metrics.get('avg_engagement_rating', 0)
        
        # Sentiment bonus
        sentiment_bonus = 0
        if metrics.get('overall_sentiment') == 'positive':
            sentiment_bonus = 1
        elif metrics.get('overall_sentiment') == 'negative':
            sentiment_bonus = 0.5
        
        trending_score = engagement_factor + posts_factor + rating_factor + sentiment_bonus
        return round(trending_score, 2)
    
    def display_hashtag_analysis(self, metrics: Dict):
        """Display detailed analysis for a single hashtag in the requested format."""
        hashtag = metrics.get('hashtag', 'unknown').upper()
        category = self.get_hashtag_category(hashtag)
        
        print(f"\n{Fore.MAGENTA}{Style.BRIGHT}#{hashtag} ({category}){Style.RESET_ALL}")
        print(f"{Fore.BLUE}📝 Total Posts: {Style.BRIGHT}{metrics.get('total_posts', 0)}{Style.RESET_ALL}")
        print(f"{Fore.RED}💖 Total Engagement: {Style.BRIGHT}{metrics.get('total_engagement', 0):,}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}📊 Avg Engagement: {Style.BRIGHT}{metrics.get('avg_engagement', 0):.1f}{Style.RESET_ALL}")
        
        # Engagement rating with visual bar
        rating = metrics.get('avg_engagement_rating', 0)
        rating_bar = self.create_rating_bar(rating)
        print(f"{Fore.YELLOW}⭐ Average Engagement Rating: {Style.BRIGHT}{rating:.1f}/10{Style.RESET_ALL} {rating_bar}")
        
        # Overall sentiment with emoji
        sentiment = metrics.get('overall_sentiment', 'neutral')
        sentiment_emoji = {'positive': '😊', 'negative': '😞', 'neutral': '😐'}.get(sentiment, '❓')
        print(f"{Fore.CYAN}🎭 Overall Sentiment: {Style.BRIGHT}{sentiment.title()}{Style.RESET_ALL} {sentiment_emoji}")
        
        # Polarity and subjectivity
        polarity = metrics.get('avg_polarity', 0)
        subjectivity = metrics.get('avg_subjectivity', 0)
        print(f"{Fore.WHITE}📈 Polarity Score: {Style.BRIGHT}{polarity:.3f}{Style.RESET_ALL} (-1=very negative, +1=very positive)")
        print(f"{Fore.WHITE}📊 Subjectivity: {Style.BRIGHT}{subjectivity:.3f}{Style.RESET_ALL} (0=objective, 1=subjective)")
        
        # Posts analyzed
        print(f"{Fore.BLUE}📋 Posts Analyzed: {Style.BRIGHT}{metrics.get('total_posts', 0)}{Style.RESET_ALL}")
        
        # Top post info
        top_post = metrics.get('top_post', {})
        if top_post:
            top_engagement = top_post.get('engagement_score', 0)
            top_url = top_post.get('url', 'N/A')
            top_sentiment = top_post.get('sentiment', 'unknown')
            top_polarity = top_post.get('polarity', 0)
            
            print(f"{Fore.YELLOW}🔥 Top Post: {Style.BRIGHT}{top_engagement:.1f}{Style.RESET_ALL} engagement")
            print(f"   URL: {Fore.CYAN}{top_url}{Style.RESET_ALL}")
            print(f"   Sentiment: {sentiment} (polarity: {top_polarity:.3f})")
            
            # Engagement rating for top post
            top_rating = min(10, max(1, top_engagement))
            top_rating_bar = self.create_rating_bar(top_rating)
            print(f"   Engagement Rating: {top_rating:.1f}/10 {top_rating_bar}")
        
        # Sentiment distribution
        sentiment_dist = metrics.get('sentiment_distribution', {})
        print(f"{Fore.MAGENTA}📊 Sentiment Distribution:{Style.RESET_ALL}")
        print(f"   😊 Positive: {sentiment_dist.get('positive', 0)}/{metrics.get('total_posts', 0)} posts")
        print(f"   😞 Negative: {sentiment_dist.get('negative', 0)}/{metrics.get('total_posts', 0)} posts")
        print(f"   😐 Neutral: {sentiment_dist.get('neutral', 0)}/{metrics.get('total_posts', 0)} posts")
        
        # Hashtag URL
        hashtag_url = metrics.get('hashtag_url', '')
        print(f"{Fore.CYAN}🔗 Hashtag URL: {hashtag_url}{Style.RESET_ALL}")
    
    def create_rating_bar(self, rating: float, max_rating: float = 10) -> str:
        """Create a visual rating bar."""
        filled = int((rating / max_rating) * 10)
        bar = "█" * filled + "░" * (10 - filled)
        
        if rating >= 8:
            color = Fore.GREEN
        elif rating >= 6:
            color = Fore.YELLOW
        elif rating >= 4:
            color = Fore.BLUE
        else:
            color = Fore.RED
        
        return f"{color}{bar}{Style.RESET_ALL}"
    
    def analyze_trending_hashtags(self, top_n: int = 10) -> List[Dict]:
        """Main method to analyze trending hashtags."""
        print(f"{Fore.CYAN}{Style.BRIGHT}{'='*80}")
        print(f"🚀 FACEBOOK TOP 10 HASHTAGS ANALYZER")
        print(f"{'='*80}{Style.RESET_ALL}\n")
        
        # Setup scraper
        self.scraper.setup_driver()
        
        try:
            # Login
            print(f"{Fore.YELLOW}🔐 Logging into Facebook...{Style.RESET_ALL}")
            if not self.scraper.login():
                print(f"{Fore.RED}❌ Login failed! Please check your credentials.{Style.RESET_ALL}")
                return []
            
            print(f"{Fore.GREEN}✅ Login successful!{Style.RESET_ALL}\n")
            
            # Analyze specific hashtags
            hashtag_posts = self.analyze_specific_hashtags()
            
            if not hashtag_posts:
                print(f"{Fore.RED}❌ No hashtags data found!{Style.RESET_ALL}")
                return []
            
            print(f"\n{Fore.CYAN}{Style.BRIGHT}📊 CALCULATING HASHTAG METRICS{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Analyzing {len(hashtag_posts)} hashtags with detailed metrics...{Style.RESET_ALL}\n")
            
            # Analyze each hashtag
            hashtag_metrics = defaultdict(list)
            for hashtag, posts in hashtag_posts.items():
                if posts:  # Only analyze hashtags with data
                    metrics = self.analyze_hashtag_metrics(hashtag, posts)
                    if metrics:
                        trending_score = self.get_trending_score(metrics)
                        metrics['trending_score'] = trending_score
                        hashtag_metrics[self.get_hashtag_category(hashtag)].append(metrics)
            
            # Sort by trending score
            for category in hashtag_metrics:
                hashtag_metrics[category].sort(key=lambda x: x.get('trending_score', 0), reverse=True)
            
            # Display results for all found hashtags (up to 10)
            display_count = min(len(hashtag_metrics), 10)
            
            print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*80}")
            print(f"🏆 TOP {display_count} HASHTAGS ANALYSIS RESULTS")
            print(f"{'='*80}{Style.RESET_ALL}")
            
            for category, metrics in hashtag_metrics.items():
                print(f"\n{Fore.MAGENTA}{Style.BRIGHT}{category}{Style.RESET_ALL}")
                for i, metric in enumerate(metrics[:10], 1):
                    print(f"\n{Fore.WHITE}{Style.BRIGHT}[{i}] TRENDING SCORE: {metric.get('trending_score', 0):.2f}{Style.RESET_ALL}")
                    self.display_hashtag_analysis(metric)
                    print(f"{Fore.WHITE}{'─' * 80}{Style.RESET_ALL}")
            
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"./data/top_10_hashtags_{timestamp}.json"
            
            save_data = {
                'timestamp': datetime.now().isoformat(),
                'hashtags_searched': list(hashtag_posts.keys()),
                'hashtags_with_data': len(hashtag_metrics),
                'top_hashtags': {category: metrics[:10] for category, metrics in hashtag_metrics.items()}
            }
            
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            
            print(f"\n{Fore.GREEN}💾 Results saved to: {filename}{Style.RESET_ALL}")
            
            return [metric for metrics in hashtag_metrics.values() for metric in metrics[:10]]
            
        finally:
            self.scraper.cleanup()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, 'scraper'):
            self.scraper.cleanup()

def main():
    """Main execution function."""
    print(f"{Fore.CYAN}🎯 Starting Trending Hashtags Analysis...{Style.RESET_ALL}\n")
    
    try:
        with TrendingHashtagsAnalyzer(headless=False) as analyzer:
            trending_hashtags = analyzer.analyze_trending_hashtags(top_n=10)
            
            if trending_hashtags:
                print(f"\n{Fore.GREEN}{Style.BRIGHT}✅ Analysis Complete!{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Found {len(trending_hashtags)} trending hashtags with detailed metrics.{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}❌ No trending hashtags found.{Style.RESET_ALL}")
                
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️ Analysis interrupted by user.{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Error during analysis: {str(e)}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
