from os.path import split

def parse_gemini_response(raw_text):
    # Split by your custom delimiter
    sections = raw_text.split("!!!!!")

    # Section 0: Title + metadata
    header = sections[0].strip()
    print("header is:"+ header)

    # Extract fields using string slicing
    title = header.split("Type:")[0].split("Title:")[1]
    print("title is:" + title)

    type = header.split("Type:")[1].split("Method:")[0].strip()
    print("type is:" + type)
    method = header.split("Method:")[1].split("Cook Time:")[0].strip()
    print("method is:" + method)
    cook_time = header.split("Cook Time:")[1].split("Yield:")[0].strip()
    print("cook time is:" + cook_time)
    yield_block = header.split("Yield:")[1].strip()
    yield_elements=yield_block .split(" ")
    for yield_element in  yield_elements:
        if yield_element.isdigit():
            num_pieces=yield_element
            break
    for yield_element in yield_elements:
        if any(c.isalpha() for c in yield_element) and any(c.isdigit() for c in yield_element):
            serving_size=yield_element
            break


    # Section 1: Ingredients
    ingredients_text = sections[1].strip()

    # Section 2: Steps
    steps_text = sections[2].strip()

    # ✅ Print everything
    print("🍽️ Title:", title)
    print("📂 Type:", type)
    print("🔥 Method:", method)
    print("⏱️ Cook Time:", cook_time)
    print("🍴 Yield:", num_pieces)
    print("⚖️ Serving Size:", serving_size)
    print("\n🧂 Ingredients:\n", ingredients_text)
    print("\n👣 Steps:\n", steps_text)

    final_header = "🍽️ Title: " + title + "\n" + \
                   "📂 Type: " + type + "\n" + \
                   "🔥 Method: " + method + "\n" + \
                   "⏱️ Cook Time: " + cook_time + "\n"

    # ✅ Return values for cost calculation
    return title,final_header,ingredients_text,steps_text,num_pieces, serving_size



