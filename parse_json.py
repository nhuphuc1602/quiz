import json
import re

def remove_all_prefix_letters(text):
    # Xóa mọi 'A.', 'B.', 'C.', 'D.' (hoa hoặc thường) kèm dấu chấm và khoảng trắng ngay sau nó,
    # ở bất cứ vị trí nào trong chuỗi, nhưng vẫn giữ nguyên dấu ** và các phần khác
    # Lưu ý: chỉ xóa chữ cái + dấu chấm + khoảng trắng ngay sau đó, không xóa số hay ký tự khác
    return re.sub(r'(?i)([abcd])\.\s*', '', text)

def deduplicate_and_clean_options(data):
    for item in data:
        options = item.get("options", {})
        seen_texts = set()
        new_options = {}
        for key, value in options.items():
            cleaned = remove_all_prefix_letters(value).lower().strip()
            if cleaned not in seen_texts:
                seen_texts.add(cleaned)
                new_options[key] = remove_all_prefix_letters(value).strip()
        item["options"] = new_options
    return data

# Đọc file input.json, xử lý, ghi ra output.json
with open("output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

cleaned_data = deduplicate_and_clean_options(data)

with open("output__.json", "w", encoding="utf-8") as f:
    json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
