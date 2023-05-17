import wiki_api as w
# from wikipedia import summary
import wikipediaapi as ww

class WikiParsedData(): 
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
        self.flag_link: str = None
        self.coat_link: str = None
        self.leder_1_name: str = None
        self.leder_2_name: str = None 
        self.parlament_symbol: str = None 
        self._parse_home_page()

        self.wiki_wiki = ww.Wikipedia('en')

    def _info_box_finder(self, find_str: str, type: bool, raw_page) -> str:
        """
            type = 0: image_flag = Flag of India.svg
            type = 1: leader_name1 = [[Droupadi Murmu]]
        """
        tag_index = raw_page.find(find_str)
        
        if type:
            return raw_page[raw_page.find("[[", tag_index) + 2 : raw_page.find("]]", tag_index)]

        ckrange = raw_page[raw_page.find("=", tag_index) + 2 : raw_page.find("|", tag_index) - 1]

        if ckrange.find("<") != -1:
            return ckrange[:ckrange.find("<")]

        return ckrange

    def _parse_home_page(self) -> None: 
        self.raw_page = w.get_raw_page(self.symbol)
        self.flag_link = self._info_box_finder("image_flag", type=0, raw_page=self.raw_page)
        self.coat_link = self._info_box_finder("image_coat", type=0, raw_page=self.raw_page)
        self.leder_1_name = self._info_box_finder("leader_name1", type=1, raw_page=self.raw_page)
        self.leder_2_name = self._info_box_finder("leader_name2", type=1, raw_page=self.raw_page)
        self.parlament_symbol = self._info_box_finder("lower_house", type=1, raw_page=self.raw_page)
        if len(self.parlament_symbol) >= 1000:
            self.parlament_symbol = self._info_box_finder("legislature", type=1, raw_page=self.raw_page)

    def get_leader_bio(self, leader_name) -> str:
        page = self.wiki_wiki.page(leader_name)
        return page.summary

    def get_leader_1(self) -> list:
        name = self.leder_1_name
        row_page = w.get_raw_page(name)
        img = self._info_box_finder("image", type=0, raw_page=row_page) 
        bio = self.get_leader_bio(name)
        return {"img": img, "name": name, "txt": bio}

    def get_leader_2(self):
        name = self.leder_2_name
        row_page = w.get_raw_page(name)
        img = self._info_box_finder("image", type=0, raw_page=row_page) 
        bio = self.get_leader_bio(name)
        return {"img": img, "name": name, "txt": bio}

    def get_gov(self):
        name = self.parlament_symbol
        if name.find("|") != -1:
            name = name[0:name.find("|")]
        row_page = w.get_raw_page(name)
        img = self._info_box_finder("structure1", type=0, raw_page=row_page) 
        bio = self.get_leader_bio(name)
        return {"img": img, "name": name, "txt": bio}
    