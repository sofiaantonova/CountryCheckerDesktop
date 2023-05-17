from gui import App
from wiki_parser import WikiParsedData

page_symbols = [
    "Russia", 
    "United States",
    "United Kingdom",
    "India",
    "China",
    "Germany",
    "France",
    "Spain",
    "Japan",
    "Hungary",
    "Denmark",
    "Poland",
    "Canada",
    "Austria",
    "Australia",
    "Finland",
    "Israel",
    "Republic of Ireland",
    "Mexico",
    "New Zealand"
]

# page_symbols = [
#     "Russia", 
#     "United States",
#     "United Kingdom",
#     "India",
#     "China",
#     "Germany"
# ]

if __name__ == "__main__":
    wiki_parser_class = []
    for i in page_symbols:
        wiki_parser_class.append(WikiParsedData(i))
    app = App(wiki_parser_class)
    app.mainloop()