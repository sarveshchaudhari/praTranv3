import re
import csv

def sanskrit_to_arabic(sans):
    # Mapping for Sanskrit digits
    mapping = {'०':'0','१':'1','२':'2','३':'3','४':'4','५':'5','६':'6','७':'7','८':'8','९':'9'}
    arab = "".join(mapping.get(ch, '') for ch in sans if ch in mapping)
    try:
        return int(arab)
    except:
        return None

def extract_shlokas(text):
    # This regex will split the text at every occurrence of a delimiter of the form:
    # || some_label ||
    # The pattern captures the label inside.
    # re.split returns a list where even indices are the content and odd indices are the captured labels.
    parts = re.split(r'\|\|\s*([^\|]+?)\s*\|\|', text, flags=re.DOTALL)
    
    shlokas = []
    # Starting from index 1, each odd index is a label and the preceding text is the shloka content.
    for i in range(1, len(parts), 2):
        label = parts[i].strip()
        content = parts[i-1].strip()
        # Skip if label contains any Latin letters (like A, B, C, etc.)
        if re.search(r'[A-Za-z]', label):
            continue
        # Only add if we can convert the label to a number
        num = sanskrit_to_arabic(label)
        if num is not None:
            shlokas.append((num, content))
    return shlokas

def build_shloka_dict(shlokas):
    # In case some shlokas might be missing or out of order,
    # we create a dictionary mapping the shloka number to its content.
    shloka_dict = {}
    for num, content in shlokas:
        shloka_dict[num] = content
    return shloka_dict

def write_csv(shloka_dict, output_csv):
    if not shloka_dict:
        print("No shlokas found.")
        return

    max_row = max(shloka_dict.keys())
    # Create rows for each shloka number 1...max_row
    rows = []
    for i in range(1, max_row + 1):
        # If a shloka is missing, write an empty string.
        rows.append([i, shloka_dict.get(i, "")])
        
    with open(output_csv, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Shloka Number", "Text"])
        writer.writerows(rows)
    print(f"CSV file '{output_csv}' created with preprocessed shlokas.")

if __name__ == "__main__":
    input_file = "mahaPrakText_cleaned.txt"  # This is the cleaned text from previous preprocessing
    output_csv = "shlokas.csv"
    
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading {input_file}: {e}")
        exit(1)
    
    # Extract shlokas based on the delimiter pattern.
    shlokas = extract_shlokas(text)
    shloka_dict = build_shloka_dict(shlokas)
    
    # Write the shlokas to a CSV file.
    write_csv(shloka_dict, output_csv)
