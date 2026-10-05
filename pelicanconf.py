AUTHOR = "aoi.mizma"
SITENAME = "path-works.net"
SITEURL = ""

PATH = "content"

TIMEZONE = "Asia/Tokyo"

DEFAULT_LANG = "ja"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = [
    ("GP2040-CE", "https://github.com/OpenStickCommunity/GP2040-CE"),
    ("ergoSHIFT", "https://github.com/mizma/ergoSHIFT"),
    ("slimDASH", "https://github.com/mizma/SlimDash"),
    ("mzm_kicad", "https://github.com/mizma/mzm_kicad"),
    ("ani2xcurtk", "https://github.com/mizma/ani2xcurtk"),
]
LINKS_WIDGET_NAME = "Links"

# Social widget
SOCIAL = [
    ("github", "https://github.com/mizma"),
    ("twitter", "https://x.com/mizma"),
    ("bluesky", "https://bsky.app/profile/mizma.bsky.social"),
    ("Pixiv", "https://www.pixiv.net/users/30348"),
]

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = "theme/notmyidea-cms/"

DEFAULT_CATEGORY = "その他"
GITHUB_URL = "https://github.com/mizma/path-works.net"

STATIC_PATHS = [
    "images",
]

ARTICLE_URL = "posts/{date:%Y}/{date:%b}/{date:%d}/{slug}/"
ARTICLE_SAVE_AS = "posts/{date:%Y}/{date:%b}/{date:%d}/{slug}/index.html"
PAGE_URL = "pages/{slug}/"
PAGE_SAVE_AS = "pages/{slug}/index.html"
YEAR_ARCHIVE_SAVE_AS = "posts/{date:%Y}/index.html"
YEAR_ARCHIVE_URL = "posts/{date:%Y}/"
MONTH_ARCHIVE_SAVE_AS = "posts/{date:%Y}/{date:%b}/index.html"
MONTH_ARCHIVE_URL = "posts/{date:%Y}/{date:%b}/"
DEFAULT_LANG = "ja"

LOCALE = [
    "ja_JP.UTF-8"
]

DATE_FORMATS = {
    "ja": ("ja_JP.UTF-8", "%Y年%m月%d日 (%a)"),
}

TWITTER_USERNAME = "mizma"
