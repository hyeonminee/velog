import feedparser
import os
import re

# Velog RSS 주소
RSS_URL = "https://api.velog.io/rss/@hyeonminee"

# 글이 저장될 디렉터리
POSTS_DIR = "velog-posts"


def sanitize_filename(title):
    """
    GitHub 파일명으로 사용하기 어려운 문자를 제거/변환
    """
    filename = re.sub(r'[\\/:*?"<>|]', "-", title)
    filename = re.sub(r"\s+", " ", filename).strip()

    return filename + ".md"


def make_post_content(entry):
    """
    RSS 정보를 Markdown 파일 형태로 구성
    """

    title = entry.get("title", "Untitled")
    link = entry.get("link", "")
    published = entry.get("published", "")
    description = entry.get("description", "")

    return f"""# {title}

> Velog 원문: {link}

- 작성일: {published}

---

{description}
"""


def main():
    os.makedirs(POSTS_DIR, exist_ok=True)

    print(f"Fetching Velog RSS: {RSS_URL}")

    feed = feedparser.parse(RSS_URL)

    if feed.bozo:
        print(f"RSS parsing warning: {feed.bozo_exception}")

    if not feed.entries:
        print("No Velog posts found.")
        return

    print(f"Found {len(feed.entries)} posts.")

    created = 0
    updated = 0
    unchanged = 0

    for entry in feed.entries:
        title = entry.get("title", "Untitled")

        filename = sanitize_filename(title)
        filepath = os.path.join(POSTS_DIR, filename)

        new_content = make_post_content(entry)

        # 기존 글이 존재하는 경우 내용 비교
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as file:
                old_content = file.read()

            # Velog에서 글이 수정된 경우 GitHub 파일도 갱신
            if old_content != new_content:
                with open(filepath, "w", encoding="utf-8") as file:
                    file.write(new_content)

                print(f"Updated: {title}")
                updated += 1

            else:
                print(f"Unchanged: {title}")
                unchanged += 1

        # 새로운 글
        else:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(new_content)

            print(f"Created: {title}")
            created += 1

    print()
    print("===== Result =====")
    print(f"Created   : {created}")
    print(f"Updated   : {updated}")
    print(f"Unchanged : {unchanged}")


if __name__ == "__main__":
    main()
