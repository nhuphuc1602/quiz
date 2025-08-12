import re

def clean_md_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Xóa hết comment HTML <!-- ... -->
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

    # Xóa hết dấu '>' ở đầu dòng (thường là blockquote markdown)
    # Nếu bạn muốn xóa tất cả dấu '>' trong file, dùng pattern khác
    content = re.sub(r'^\s*>+\s?', '', content, flags=re.MULTILINE)

    # Nếu bạn muốn xóa tất cả dấu '>' trong file (không chỉ đầu dòng), dùng:
    # content = content.replace('>', '')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Ví dụ chạy:
clean_md_file('input.md', 'output.md')
