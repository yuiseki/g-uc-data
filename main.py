import requests
from bs4 import BeautifulSoup
import datasets


urls = [
    "https://gobuzaki.ehoh.net/unicorn/ep1.html",
    "https://gobuzaki.ehoh.net/unicorn/ep2.html",
    "https://gobuzaki.ehoh.net/unicorn/ep3.html",
    "https://gobuzaki.ehoh.net/unicorn/ep4.html",
    "https://gobuzaki.ehoh.net/unicorn/ep5.html",
    "https://gobuzaki.ehoh.net/unicorn/ep6.html",
    "https://gobuzaki.ehoh.net/unicorn/ep7.html",
]

# List
# place: str
# person: str
# text: str
text_list = []

for url in urls:
    print(url)
    # Download html
    res = requests.get(url)
    # Check text encoding
    res.encoding = "Shift_JIS"
    soup = BeautifulSoup(res.text, "html.parser")

    # Get all tr tags
    trs = soup.find_all("tr")
    episode = ""
    subtitle = ""
    place = ""
    person = ""
    for tr in trs:
        tds = tr.find_all("td")
        # Skip if tds[0] contain "サブタイトル"
        if "サブタイトル" in tds[0].text:
            continue
        # Skip if tds[0] contain "エンドロール"
        if "エンドロール" in tds[0].text:
            continue
        count = len(tds)
        if count == 1:
            # skip if colspan is not 2
            if "colspan" not in tds[0].attrs:
                if place == "":
                    text = tds[0].text
                    print(text)
                    # Check if text contain "episode"
                    if "episode" in text:
                        # split episode1「ユニコーンの日」 to episode and subtitle
                        episode = text.split("「")[0]
                        subtitle = text.split("「")[1].replace("」", "")
                    continue
                text = tds[0].text
                # Replace \u3000 to space of text
                text = text.replace("\u3000", " ")
                row = {
                    "episode": episode,
                    "subtitle": subtitle,
                    "place": place,
                    "person": person,
                    "text": text
                }
                print(row)
                text_list.append(row)
                continue
            # Place
            place = tds[0].text
            # Remove \u3000
            place = place.replace("\u3000", "")
            continue
        elif count == 2:
            # Person and text
            person = tds[0].text
            text = tds[1].text
            # Replace \u3000 to space of text
            text = text.replace("\u3000", " ")
        if place == "":
            continue
        if person is None or text is None:
            continue
        if person == "" or text == "":
            continue

        text_original = text
        # "「"と"」"を除去する
        text = text.replace("「", "")
        text = text.replace("」", "")
        text = text.replace("「", "")
        text = text.replace("」", "")
        text = text.replace("「", "")
        text = text.replace("」", "")

        if text == "……":
            continue
        if text == "……！":
            continue
        if text == "……？":
            continue
        if text == "…………":
            continue

        row = {
            "episode": episode,
            "subtitle": subtitle,
            "place": place,
            "person": person,
            "text": text,
            "text_original": text_original
        }
        print(row)
        text_list.append(row)

print("text_list", len(text_list))

my_dataset = datasets.Dataset.from_list(text_list)

print(my_dataset)

my_dataset.push_to_hub("yuiseki/g-uc")
