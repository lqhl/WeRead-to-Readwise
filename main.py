import csv
import sys
import re
from datetime import datetime
import os


def parse_weread_notes(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 使用正则表达式提取书名
    title_match = re.match(r'《(.*)》', lines[0].strip())
    if title_match:
        title = title_match.group(1)
    else:
        title = lines[0].strip()

    author = lines[2].strip()

    highlights = []
    current_chapter = None
    current_note = None
    note = None

    for line in lines[4:]:
        line = line.strip()
        if line.startswith('◆'):
            if current_note:
                highlights.append((current_note, current_chapter, note))
                current_note = None
                note = None
            highlight = line.lstrip('◆').strip()
            highlights.append((highlight, current_chapter, None))
        elif '发表想法' in line:
            note_date = line.split('发表想法')[0].strip('◆').strip()
            note = line.split('发表想法')[1].strip()
            if current_note:
                highlights.append((current_note, current_chapter, note))
                current_note = None
                note = None
        elif '原文：' in line:
            current_note = line.lstrip('原文：').strip()
        elif line:
            current_chapter = line

    if current_note:
        highlights.append((current_note, current_chapter, note))

    return title, author, highlights


def write_highlights_to_csv(title, author, highlights, filename='highlights.csv'):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Highlight', 'Title', 'Author',
                        'URL', 'Note', 'Location', 'Date'])

        for i, (highlight, chapter, note) in enumerate(highlights, start=1):
            writer.writerow([highlight, title, author,
                            '', note, i, current_time])


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_weread_notes>")
        sys.exit(1)

    file_path = sys.argv[1]

    title, author, highlights = parse_weread_notes(file_path)

    csv_filename = os.path.splitext(file_path)[0] + '.csv'
    write_highlights_to_csv(title, author, highlights, filename=csv_filename)

    print(f"Highlights from '{title}' by {
          author} have been written to '{csv_filename}'")
