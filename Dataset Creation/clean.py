import re

def preprocess_text(input_file, output_file):
    try:
        # Read the entire file
        with open(input_file, encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading {input_file}: {e}")
        return

    # 1. Remove page headers like "===== Page 118 ====="
    text = re.sub(r'^===== Page \d+ =====\s*\n', '', text, flags=re.MULTILINE)

    # 2. Remove footnote blocks
    # Footnote blocks: They start with a line that begins with one or more numbers and a period,
    # and then somewhere later contain the three footer lines:
    # "Jain Education International", "For Private & Personal Use Only", "www.jainelibrary.org"
    # We use a non-greedy match (.*?) and DOTALL to catch newlines.
    footnote_block_pattern = (
        r'\d+\..*?'                             # starts with number and period and any text
        r'Jain Education International\s*\n'     # first footer line
        r'For Private & Personal Use Only\s*\n'   # second footer line
        r'www\.jainelibrary\.org'                # third footer line (dot escaped)
    )
    text = re.sub(footnote_block_pattern, '', text, flags=re.DOTALL)

    # 3. Remove any stray footnote markers that are on their own lines.
    # (This removes lines that start with a number and period.)
    text = re.sub(r'^\d+\..*$', '', text, flags=re.MULTILINE)

    # 4. Remove any leftover footer lines (in case they occur outside a block)
    footer_pattern = r'Jain Education International\s*\nFor Private & Personal Use Only\s*\nwww\.jainelibrary\.org'
    text = re.sub(footer_pattern, '', text, flags=re.DOTALL)

    # 5. Remove extra blank lines and trim spaces
    lines = text.splitlines()
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    cleaned_text = '\n'.join(cleaned_lines)

    try:
        # Write the cleaned text to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        print(f"Preprocessing complete. Cleaned text saved as {output_file}")
    except Exception as e:
        print(f"Error writing {output_file}: {e}")

if __name__ == "__main__":
    input_file = "mahaPrakText.txt"
    output_file = "mahaPrakText_cleaned.txt"
    preprocess_text(input_file, output_file)
