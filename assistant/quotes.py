"""
quotes.py — Curated collection of motivational quotes.
"""

import hashlib
import random
from datetime import date


_QUOTES = [
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
    ("It does not matter how slowly you go as long as you do not stop.", "Confucius"),
    ("Everything you've ever wanted is on the other side of fear.", "George Addair"),
    ("Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"),
    ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
    ("In the middle of every difficulty lies opportunity.", "Albert Einstein"),
    ("What you get by achieving your goals is not as important as what you become by achieving your goals.", "Zig Ziglar"),
    ("Don't watch the clock; do what it does. Keep going.", "Sam Levenson"),
    ("You are never too old to set another goal or to dream a new dream.", "C.S. Lewis"),
    ("Act as if what you do makes a difference. It does.", "William James"),
    ("The secret of getting ahead is getting started.", "Mark Twain"),
    ("Your limitation — it's only your imagination.", "Unknown"),
    ("Push yourself, because no one else is going to do it for you.", "Unknown"),
    ("Great things never come from comfort zones.", "Unknown"),
    ("Dream it. Wish it. Do it.", "Unknown"),
    ("Success doesn't just find you. You have to go out and get it.", "Unknown"),
    ("The harder you work for something, the greater you'll feel when you achieve it.", "Unknown"),
    ("Dream bigger. Do bigger.", "Unknown"),
    ("Don't stop when you're tired. Stop when you're done.", "Unknown"),
    ("Wake up with determination. Go to bed with satisfaction.", "Unknown"),
    ("Do something today that your future self will thank you for.", "Sean Patrick Flanery"),
    ("Little things make big days.", "Unknown"),
    ("It's going to be hard, but hard does not mean impossible.", "Unknown"),
    ("Don't wait for opportunity. Create it.", "Unknown"),
    ("The only impossible journey is the one you never begin.", "Tony Robbins"),
    ("Happiness is not something ready-made. It comes from your own actions.", "Dalai Lama"),
    ("If you want to lift yourself up, lift up someone else.", "Booker T. Washington"),
    ("We generate fears while we sit. We overcome them by action.", "Dr. Henry Link"),
    ("Whether you think you can or think you can't, you're right.", "Henry Ford"),
    ("Security is mostly a superstition. Life is either a daring adventure or nothing.", "Helen Keller"),
    ("The man who has confidence in himself gains the confidence of others.", "Hasidic Proverb"),
    ("The only limit to our realization of tomorrow will be our doubts of today.", "Franklin D. Roosevelt"),
    ("Creativity is intelligence having fun.", "Albert Einstein"),
    ("What you do today can improve all your tomorrows.", "Ralph Marston"),
    ("It always seems impossible until it is done.", "Nelson Mandela"),
    ("Quality is not an act, it is a habit.", "Aristotle"),
    ("With the new day comes new strength and new thoughts.", "Eleanor Roosevelt"),
    ("Setting goals is the first step in turning the invisible into the visible.", "Tony Robbins"),
    ("A champion is defined not by their wins but by how they can recover when they fall.", "Serena Williams"),
    ("Start where you are. Use what you have. Do what you can.", "Arthur Ashe"),
    ("I find that the harder I work, the more luck I seem to have.", "Thomas Jefferson"),
    ("Everything has beauty, but not everyone sees it.", "Confucius"),
    ("Tough times never last but tough people do.", "Robert H. Schuller"),
    ("Keep your face always toward the sunshine and shadows will fall behind you.", "Walt Whitman"),
    ("Believe in yourself! Have faith in your abilities!", "Norman Vincent Peale"),
    ("You don't have to be great to start, but you have to start to be great.", "Zig Ziglar"),
    ("The best time to plant a tree was 20 years ago. The second best time is now.", "Chinese Proverb"),
    ("Be not afraid of life. Believe that life is worth living, and your belief will help create the fact.", "William James"),
    ("What lies behind us and what lies before us are tiny matters compared to what lies within us.", "Ralph Waldo Emerson"),
]


def get_random_quote() -> tuple[str, str]:
    """Return a random (quote_text, author) tuple."""
    return random.choice(_QUOTES)


def get_daily_quote() -> tuple[str, str]:
    """
    Return a deterministic quote for today.
    The same quote is returned throughout the day, changing each day.
    """
    today = date.today().isoformat()
    index_hash = int(hashlib.md5(today.encode()).hexdigest(), 16)
    index = index_hash % len(_QUOTES)
    return _QUOTES[index]


def get_all_quotes() -> list[tuple[str, str]]:
    """Return the full list of quotes."""
    return list(_QUOTES)
