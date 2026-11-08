#!/usr/bin/env python3
"""
md2pdf: Convert Markdown to high-quality PDF using Google Chrome Headless
Supports Mermaid diagrams, PlantUML diagrams, GitHub alerts, tables, code highlighting, and clean A4 typography.
"""

import sys
import os
import re
import zlib
import urllib.request
import urllib.parse
import subprocess
import tempfile
import shutil

CHROME_PATHS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium-browser",
]

def find_chrome():
    for path in CHROME_PATHS:
        if os.path.exists(path) and os.access(path, os.X_OK):
            return path
    which_chrome = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chrome")
    if which_chrome:
        return which_chrome
    return None

def _encode6bit(b):
    if b < 10: return chr(48 + b)
    b -= 10
    if b < 26: return chr(65 + b)
    b -= 26
    if b < 26: return chr(97 + b)
    b -= 26
    if b == 0: return '-'
    if b == 1: return '_'
    return '?'

def encode64(data):
    r = ''
    for i in range(0, len(data), 3):
        if i + 2 == len(data):
            r += _encode6bit(data[i] >> 2)
            r += _encode6bit(((data[i] & 0x3) << 4) | (data[i+1] >> 4))
            r += _encode6bit((data[i+1] & 0xF) << 2)
        elif i + 1 == len(data):
            r += _encode6bit(data[i] >> 2)
            r += _encode6bit(((data[i] & 0x3) << 4))
        else:
            r += _encode6bit(data[i] >> 2)
            r += _encode6bit(((data[i] & 0x3) << 4) | (data[i+1] >> 4))
            r += _encode6bit(((data[i+1] & 0xF) << 2) | (data[i+2] >> 6))
            r += _encode6bit(data[i+2] & 0x3F)
    return r

def plantuml_to_svg(text):
    zlibbed = zlib.compress(text.encode('utf-8'))[2:-4]
    code = encode64(zlibbed)
    url = 'https://www.plantuml.com/plantuml/svg/' + code
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as response:
            svg = response.read().decode('utf-8')
            return f'<div class="plantuml-diagram">{svg}</div>'
    except Exception:
        escaped = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        return f'<pre class="plantuml-fallback"><code>{escaped}</code></pre>'

def format_inline(text):
    text = re.sub(r'\[\!\[(.*?)\]\((.*?)\)\]\((.*?)\)', r'<a href="\3" class="badge-link"><img src="\2" alt="\1" class="badge-img"/></a> ', text)
    text = re.sub(r'\!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1" class="badge-img"/>', text)
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'___(.*?)___', r'<strong><em>\1</em></strong>', text)
    text = re.sub(r'__(.*?)__', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)', r'<em>\1</em>', text)
    text = re.sub(r'~~(.*?)~~', r'<del>\1</del>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    return text

def clean_heading_for_search(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'[*_`#~]', '', text)
    clean = re.sub(r'[^\w\s]', ' ', text, flags=re.UNICODE)
    words = clean.split()
    if not words:
        return text.strip()
    return ' '.join(words[:3])

def parse_markdown(md_content):
    lines = md_content.splitlines()
    html_parts = []
    headings = []
    i = 0
    n = len(lines)
    has_mermaid = False

    while i < n:
        line = lines[i].rstrip('\r\n')

        # Fenced code block
        if line.startswith('```'):
            lang = line[3:].strip().lower()
            block_lines = []
            i += 1
            while i < n and not lines[i].strip().startswith('```'):
                block_lines.append(lines[i].rstrip('\r\n'))
                i += 1
            i += 1  # Skip closing ```
            block_content = "\n".join(block_lines)

            if lang == 'mermaid':
                has_mermaid = True
                html_parts.append(f'<div class="diagram-wrapper"><pre class="mermaid">\n{block_content}\n</pre></div>')
            elif lang in ('plantuml', 'puml'):
                svg_html = plantuml_to_svg(block_content)
                html_parts.append(f'<div class="diagram-wrapper">{svg_html}</div>')
            else:
                escaped = block_content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                highlighted_lines = []
                for bline in escaped.split('\n'):
                    stripped = bline.strip()
                    if stripped.startswith('#') or stripped.startswith('//'):
                        highlighted_lines.append(f'<span class="code-comment">{bline}</span>')
                    elif lang in ('bash', 'sh', 'zsh', 'shell'):
                        if bline.startswith('netcfg') or bline.startswith('fs') or bline.startswith('kernel') or bline.startswith('git') or bline.startswith('npm') or bline.startswith('sudo'):
                            parts = bline.split(' ', 1)
                            cmd = f'<span class="code-keyword">{parts[0]}</span>'
                            rest = f' {parts[1]}' if len(parts) > 1 else ''
                            highlighted_lines.append(cmd + rest)
                        else:
                            highlighted_lines.append(bline)
                    else:
                        highlighted_lines.append(bline)
                code_html = "\n".join(highlighted_lines)
                html_parts.append(f'<div class="code-block"><div class="code-lang">{lang.upper() if lang else "CODE"}</div><pre><code>{code_html}</code></pre></div>')
            continue

        # GitHub Alerts / Blockquotes
        if line.startswith('>'):
            alert_type = None
            alert_lines = []
            while i < n and lines[i].startswith('>'):
                cur = lines[i].lstrip('>').strip()
                if cur.startswith('[!IMPORTANT]'):
                    alert_type = 'IMPORTANT'
                elif cur.startswith('[!TIP]'):
                    alert_type = 'TIP'
                elif cur.startswith('[!NOTE]'):
                    alert_type = 'NOTE'
                elif cur.startswith('[!WARNING]'):
                    alert_type = 'WARNING'
                elif cur.startswith('[!CAUTION]'):
                    alert_type = 'CAUTION'
                else:
                    alert_lines.append(cur)
                i += 1

            body = "<br>".join(alert_lines)
            body = format_inline(body)
            icon_map = {
                'TIP': '💡',
                'IMPORTANT': '⚠️',
                'NOTE': 'ℹ️',
                'WARNING': '⚡',
                'CAUTION': '🛑'
            }
            icon = icon_map.get(alert_type, '💬')
            title = alert_type.capitalize() if alert_type else "Note"
            css_class = alert_type.lower() if alert_type else "note"
            html_parts.append(f'''
            <div class="alert alert-{css_class}">
                <div class="alert-title">{icon} {title}</div>
                <div class="alert-content">{body}</div>
            </div>
            ''')
            continue

        # Tables
        if '|' in line and i + 1 < n and '|' in lines[i+1] and ('---' in lines[i+1] or ':---' in lines[i+1]):
            headers = [c.strip() for c in line.strip().strip('|').split('|')]
            i += 2  # skip separator
            rows = []
            while i < n and '|' in lines[i]:
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                rows.append(cells)
                i += 1

            th_html = "".join([f'<th>{format_inline(h)}</th>' for h in headers])
            tr_html = ""
            for row in rows:
                tds = "".join([f'<td>{format_inline(cell)}</td>' for cell in row])
                tr_html += f'<tr>{tds}</tr>\n'
            html_parts.append(f'''
            <div class="table-container">
                <table>
                    <thead><tr>{th_html}</tr></thead>
                    <tbody>{tr_html}</tbody>
                </table>
            </div>
            ''')
            continue

        # Headings
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            lvl = len(m.group(1))
            raw_title = m.group(2).strip()
            clean_title = re.sub(r'<[^>]+>', '', raw_title)
            clean_title = re.sub(r'[*_`#~]', '', clean_title).strip()
            search_query = clean_heading_for_search(raw_title)
            headings.append((lvl, clean_title, search_query))
            html_parts.append(f'<h{lvl}>{format_inline(raw_title)}</h{lvl}>')
            i += 1
            continue

        if line == '---' or line == '***':
            html_parts.append('<hr/>')
        elif line.strip().startswith('* ') or line.strip().startswith('- '):
            item = format_inline(line.strip()[2:])
            html_parts.append(f'<ul><li>{item}</li></ul>')
        elif re.match(r'^\d+\.\s', line.strip()):
            item = format_inline(re.sub(r'^\d+\.\s', '', line.strip()))
            html_parts.append(f'<ol><li>{item}</li></ol>')
        elif line.strip() != '':
            html_parts.append(f'<p>{format_inline(line.strip())}</p>')

        i += 1

    return "\n".join(html_parts), has_mermaid, headings

def build_full_html(body_html, has_mermaid, title="Document"):
    mermaid_script = """
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
      mermaid.initialize({
        startOnLoad: true,
        theme: 'default',
        flowchart: { useMaxWidth: true, htmlLabels: true, curve: 'basis' }
      });
    </script>
    """ if has_mermaid else ""

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<title>{title}</title>
{mermaid_script}
<style>
  @page {{
    size: A4;
    margin: 16mm 14mm 16mm 14mm;
  }}
  * {{
    box-sizing: border-box;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1f2328;
    background-color: #ffffff;
    line-height: 1.58;
    font-size: 13.5px;
    margin: 0;
    padding: 0;
  }}
  h1 {{
    font-size: 20px;
    font-weight: 700;
    color: #0969da;
    border-bottom: 2px solid #e1e4e8;
    padding-bottom: 8px;
    margin-top: 0;
    margin-bottom: 12px;
  }}
  h2 {{
    font-size: 16px;
    font-weight: 600;
    color: #24292f;
    border-bottom: 1px solid #d0d7de;
    padding-bottom: 5px;
    margin-top: 20px;
    margin-bottom: 12px;
    break-after: avoid;
  }}
  h3 {{
    font-size: 14.5px;
    font-weight: 600;
    color: #1f2328;
    margin-top: 14px;
    margin-bottom: 8px;
    break-after: avoid;
  }}
  h4 {{
    font-size: 13.5px;
    font-weight: 600;
    color: #57606a;
    margin-top: 10px;
    margin-bottom: 6px;
    break-after: avoid;
  }}
  p {{
    margin: 6px 0;
  }}
  hr {{
    height: 1px;
    background-color: #e1e4e8;
    border: none;
    margin: 14px 0;
  }}
  a.badge-link {{
    display: inline-block;
    vertical-align: middle;
    margin-right: 6px;
    margin-bottom: 6px;
    text-decoration: none;
    line-height: 0;
  }}
  .badge-img {{
    height: 24px;
    display: block;
    border: none;
  }}
  mark {{
    background-color: #fff8c5;
    padding: 0.15em 0.35em;
    border-radius: 4px;
    font-weight: 600;
  }}
  code {{
    font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
    font-size: 12px;
    background-color: #f6f8fa;
    border: 1px solid #d0d7de;
    padding: 2px 5px;
    border-radius: 4px;
    color: #cf222e;
  }}
  .code-block {{
    background-color: #1e1e2e;
    color: #cdd6f4;
    border-radius: 6px;
    margin: 8px 0;
    overflow: hidden;
    break-inside: avoid;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  }}
  .code-lang {{
    background-color: #181825;
    color: #a6adc8;
    font-size: 10px;
    font-weight: 700;
    padding: 3px 10px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-bottom: 1px solid #313244;
  }}
  .code-block pre {{
    margin: 0;
    padding: 10px 14px;
    overflow-x: auto;
  }}
  .code-block code {{
    background: transparent;
    border: none;
    padding: 0;
    color: #cdd6f4;
    font-size: 12px;
    line-height: 1.45;
  }}
  .code-comment {{
    color: #6c7086;
    font-style: italic;
  }}
  .code-keyword {{
    color: #89b4fa;
    font-weight: 600;
  }}
  .alert {{
    border-radius: 6px;
    padding: 8px 12px;
    margin: 10px 0;
    border-left: 4px solid;
    break-inside: avoid;
  }}
  .alert-important {{
    background-color: #fbf5fc;
    border-left-color: #8250df;
  }}
  .alert-important .alert-title {{
    color: #8250df;
    font-weight: 600;
    font-size: 12.5px;
    margin-bottom: 4px;
  }}
  .alert-tip {{
    background-color: #f0fdf4;
    border-left-color: #1a7f37;
  }}
  .alert-tip .alert-title {{
    color: #1a7f37;
    font-weight: 600;
    font-size: 12.5px;
    margin-bottom: 4px;
  }}
  .alert-note {{
    background-color: #f6f8fa;
    border-left-color: #0969da;
  }}
  .alert-note .alert-title {{
    color: #0969da;
    font-weight: 600;
    font-size: 12.5px;
    margin-bottom: 4px;
  }}
  .alert-content {{
    font-size: 12.5px;
    color: #24292f;
  }}
  .table-container {{
    margin: 12px 0;
    overflow-x: auto;
    break-inside: avoid;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 12.5px;
  }}
  th {{
    background-color: #f6f8fa;
    color: #24292f;
    font-weight: 600;
    text-align: left;
    padding: 7px 10px;
    border: 1px solid #d0d7de;
  }}
  td {{
    padding: 6px 10px;
    border: 1px solid #d0d7de;
    vertical-align: middle;
  }}
  tr:nth-child(even) {{
    background-color: #fcfcfc;
  }}
  .diagram-wrapper {{
    background: #fbfcfd;
    border: 1px solid #e1e4e8;
    border-radius: 6px;
    padding: 12px;
    margin: 10px 0;
    text-align: center;
    break-inside: avoid;
  }}
  .plantuml-diagram {{
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 6px;
  }}
  .plantuml-diagram svg {{
    max-height: 140px;
  }}
  ul, ol {{
    margin: 4px 0;
    padding-left: 20px;
  }}
  li {{
    margin-bottom: 3px;
  }}
  a {{
    color: #0969da;
    text-decoration: none;
  }}
</style>
</head>
<body>
{body_html}
</body>
</html>
"""

def add_bookmarks_to_pdf(pdf_path, headings):
    if not headings:
        return
    try:
        import fitz
    except ImportError:
        try:
            import pymupdf as fitz
        except ImportError:
            return

    try:
        doc = fitz.open(pdf_path)
        toc = []
        last_page = 1
        for lvl, title, query in headings:
            found_page = None
            found_y = 0.0
            # Search starting from last known page
            search_indices = list(range(last_page - 1, len(doc))) + list(range(0, last_page - 1))
            for p_idx in search_indices:
                page = doc[p_idx]
                rects = page.search_for(query)
                if not rects and len(query.split()) > 1:
                    shorter = ' '.join(query.split()[:2])
                    rects = page.search_for(shorter)
                if rects:
                    found_page = p_idx + 1
                    found_y = float(rects[0].y0)
                    break

            if found_page is None:
                found_page = last_page

            last_page = found_page
            toc.append([lvl, title, found_page, found_y])

        if toc:
            doc.set_toc(toc)
            tmp_out = pdf_path + ".tmp.pdf"
            doc.save(tmp_out)
            doc.close()
            os.replace(tmp_out, pdf_path)
    except Exception as e:
        print(f"Notice: Could not generate PDF bookmarks: {e}", file=sys.stderr)

def convert_md_to_pdf(input_md_path, output_pdf_path=None):
    if not os.path.exists(input_md_path):
        print(f"Error: File '{input_md_path}' does not exist.", file=sys.stderr)
        return False

    chrome_bin = find_chrome()
    if not chrome_bin:
        print("Error: Google Chrome / Chromium is not found on your system.", file=sys.stderr)
        return False

    if not output_pdf_path:
        base, _ = os.path.splitext(input_md_path)
        output_pdf_path = f"{base}.pdf"

    with open(input_md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    doc_title = os.path.basename(input_md_path)
    body_html, has_mermaid, headings = parse_markdown(md_text)
    full_html = build_full_html(body_html, has_mermaid, title=doc_title)

    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp:
        tmp.write(full_html)
        tmp_html_path = tmp.name

    try:
        cmd = [
            chrome_bin,
            "--headless=new",
            "--disable-gpu",
            "--run-all-compositor-stages-before-draw",
            f"--print-to-pdf={os.path.abspath(output_pdf_path)}",
            "--no-pdf-header-footer",
        ]
        if has_mermaid:
            cmd.append("--virtual-time-budget=5000")

        cmd.append(tmp_html_path)

        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        add_bookmarks_to_pdf(output_pdf_path, headings)
        print(f"✅ Exported successfully: {output_pdf_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running Chrome to print PDF: {e}", file=sys.stderr)
        return False
    finally:
        if os.path.exists(tmp_html_path):
            os.remove(tmp_html_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 md2pdf.py <path-to-markdown-file> [output-pdf-path]")
        sys.exit(1)

    input_file = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) > 2 else None
    success = convert_md_to_pdf(input_file, out_file)
    sys.exit(0 if success else 1)

