import os

from common.pdf_extract import (
    extract_contents,
    extract_text,
    extract_metadata,
    mar_filter,
    sfr_filter,
    budget_filter,
    time_filter
)

from common.utils import parse_config, get_character, convert_to_html, inference, fetch_prompt


# Text Extraction

src_data = r"C:\Users\gukhwan\OneDrive - (주)스위트케이\바탕 화면\ChatRFP\data\20240417805-00_1712800396330_2._제안요청서_MICE시스템 3.pdf"
file_name = os.path.basename(src_data)
print(file_name)

a = extract_contents(src_data)
# print(a)
# print(len(a))
b = extract_text(a)
# print(b)
# print(len(b))

_, pdf_pages = extract_metadata(a)

print("\nBUDGET")
budget_points, budget_ids = budget_filter(b, pdf_pages)
print(budget_ids)
print(budget_points)

# prompt, _, _ = parse_config(character_name="budget_extractor", character_configs=get_character())
prompt = fetch_prompt("budget_extractor")
query = " ".join(budget_points)

budget_text = inference(
    gpt=True,
    system_msg=prompt,
    query=query,

)

print("\nTIME")
time_points, time_ids = time_filter(b, pdf_pages)
print(time_ids)
print(time_points)

# prompt, _, _ = parse_config(character_name="time_extractor", character_configs=get_character())
prompt = fetch_prompt("time_extractor")
query = " ".join(time_points)

time_text = inference(
    gpt=True,
    system_msg=prompt,
    query=query,

)

print("\nMAR")
mar_points, mar_ids = mar_filter(b, pdf_pages)
print(mar_ids)
print(mar_points)

# prompt, _, _ = parse_config(character_name="test-mar", character_configs=get_character())
prompt = fetch_prompt("mar_summary")
query = " ".join(mar_points)

mar_text = inference(
    gpt=True,
    system_msg=prompt,
    query=query,

)

# budget_text = "사업비: 1,053,412,000원"
# time_text = "사업기간: 계약체결일로부터 2025년 12월 31일까지"
# res = f"<h4>RFP Summary</h4><br>{budget_text}<br>{time_text}<h4>MAR Keypoints</h4>{mar_text}<br>"
# convert_to_html(res, filepath="./output/sample5.html")

print("\nSFR")
sfr_points, sfr_ids = sfr_filter(b, pdf_pages)
print(sfr_ids)
print(sfr_points)

# prompt, _, _ = parse_config(character_name="test-sfr", character_configs=get_character())
prompt = fetch_prompt("sfr_summary")
query = " ".join(sfr_points)

sfr_text = inference(
    gpt=True,
    system_msg=prompt,
    query=query,

)

convert_to_html(filepath=f"./output/{file_name}.html",
                file_name=file_name,
                budget_text=budget_text,
                time_text=time_text,
                mar_text=mar_text,
                sfr_text=sfr_text)



