import re
import json

def parse_md_file(md_path):
    with open(md_path, encoding='utf-8') as f:
        lines = f.readlines()

    questions = []
    question_num = None
    question_text_lines = []
    options = {}
    option_order = ['A', 'B', 'C', 'D']
    current_option_index = 0

    def save_question():
        if question_text_lines:
            question_text = ' '.join(question_text_lines).strip()
            questions.append({
                "question_text": question_text,
                "options": options.copy()
            })

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Kiểm tra dòng câu hỏi: số + dấu chấm + cách
        match_q = re.match(r'^(\d+)\.\s+(.*)', line)
        if match_q:
            # Lưu câu hỏi cũ trước khi sang câu mới
            save_question()

            question_num = match_q.group(1)
            question_text_lines = [match_q.group(2)]
            options = {}
            current_option_index = 0
            continue

        # Kiểm tra dòng đáp án: có thể dạng '> A. ...' hoặc 'A. ...' hoặc '**B. ...**'
        match_opt = re.match(r'^(>?\s*)?(\*\*)?([AaBbCcDd])\.\s*(.*?)(\*\*)?$', line)
        if match_opt:
            # Lấy key chữ A/B/C/D uppercase
            opt_key = match_opt.group(3).upper()
            opt_text = match_opt.group(4).strip()

            # Giữ nguyên dấu ** nếu có 2 group dấu ** bao ngoài
            prefix = '**' if match_opt.group(2) else ''
            suffix = '**' if match_opt.group(5) else ''

            if opt_text.startswith(f"{opt_key}."):
                opt_text = opt_text[len(opt_key)+1:].lstrip()  # bỏ "A." + khoảng trắng

            full_text = f"{prefix}{opt_key}. {opt_text}{suffix}"

            options[opt_key] = full_text
            continue

        # Nếu dòng không phải câu hỏi hay đáp án, thêm vào câu hỏi (câu hỏi dài nhiều dòng)
        question_text_lines.append(line)

    # Lưu câu cuối cùng
    save_question()
    return questions

if __name__ == "__main__":
    input_md = "input.md"
    output_json = "output.json"
    parsed = parse_md_file(input_md)
    with open(output_json, "w", encoding="utf-8") as f_out:
        json.dump(parsed, f_out, ensure_ascii=False, indent=2)
    print(f"Xong! Đã lưu {len(parsed)} câu hỏi vào {output_json}")
