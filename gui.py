import customtkinter
import wiki_api as w

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")

class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="ns")
        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.button_list = []

    def add_item(self, item, compound, image=None):
        button = customtkinter.CTkButton(self, text=item.symbol, image=image, 
                                         compound=compound, fg_color="#F5F5F5", 
                                         hover_color="#D9D9D9", text_color="#000",
                                         font=customtkinter.CTkFont("Inte", 28))
        if self.command is not None:
            button.configure(command=lambda: self.command(item))
        button.grid(row=len(self.button_list), column=0, pady=14, sticky="e")
        self.button_list.append(button)

    def remove_item(self, item):
        for label, button in zip(self.label_list, self.button_list):
            if item == label.cget("text"):
                button.destroy()
                self.button_list.remove(button)
                return

class CountryInfoFrame():
    def __init__(self, master: any, country_example: object, **kwargs):
        self.master = master
        self.cuntry_symbol = country_example
        self.choice_country_frame = customtkinter.CTkFrame(self.master, corner_radius=0, fg_color="#fff",
                                                           width = 960, height = 540)
        
        self.def_links = [self.leder_1, self.leder_2, self.gov, self.symb]
        for index, item in enumerate(["President", "Prime Minister", "Government", "Symbol"]):
            customtkinter.CTkButton(self.choice_country_frame, text=item, 
                                    image=customtkinter.CTkImage(w.get_image_old([item, "png"]), 
                                    size=(324, 60)), compound="bottom", width=324, height=62,
                                    command=self.def_links[index], fg_color="#F5F5F5", 
                                    hover_color="#D9D9D9", text_color="#000",
                                    font=customtkinter.CTkFont("Inte", 28)
                                    ).grid(row=index, column=0, pady=9, padx=318)
        customtkinter.CTkButton(self.choice_country_frame, text="home", command=self.to_home_page).grid(row=7, column=0, padx=0)
    
    def display_on(self):
        # self.choice_country_frame.grid(row=0, column=0, sticky="nsew", padx=100)
        self.choice_country_frame.grid(row=0, column=0, pady=0, sticky="ns")
        self.choice_country_frame.grid_columnconfigure(0, weight=1)

    def display_off(self):
        self.choice_country_frame.grid_forget()

    def to_home_page(self):
        self.display_off()
        self.master.home_page()

    def leder_open(self, info, it_is = "l"):
        if it_is != "s":
            img = info["img"]
            name = info["name"]
            if name.find("|") != -1:
                name = name[0:name.find("|")]
            txt_link = info["txt"]
        else: 
            img = info[0]
            img_link = info[1]
            name = ""

        if it_is == "l":
            pag = 0
            img_width = 324
            img_height = 400
            txt_row = 1
            column_alig = 2

        if it_is == "g" or it_is == "s":
            pag = 40
            img_width = 400
            img_height = 200
            column_alig = 1
            txt_row = 2

        self.display_off()
        self.frame = customtkinter.CTkFrame(self.master, corner_radius=0, fg_color="#fff",
                                            width = 960, height = 540)
        
        customtkinter.CTkLabel(self.frame, text=name,
                                image=customtkinter.CTkImage(w.get_image(img), 
                                size=(img_width, img_height)), compound="top",
                                font=customtkinter.CTkFont("Inte", 28)
                                ).grid(row=1, column=1, pady=20, padx=pag, sticky="e")
        if it_is != "s":
            self.textbox = customtkinter.CTkTextbox(self.frame, width=500, height=img_height)
            self.textbox.grid(row=txt_row, column=column_alig, padx=pag, sticky="e")
            self.textbox.insert("0.0", info["txt"])
            self.textbox.configure(state="disabled")
        else:
            img_width = img_height
            customtkinter.CTkLabel(self.frame, text=name,
                                image=customtkinter.CTkImage(w.get_image(img_link), 
                                size=(img_width, img_height)), compound="top"
                                ).grid(row=2, column=1, padx=pag)
        customtkinter.CTkButton(self.frame, text="<-- back", command=self.leder_close).grid(row=0, column=0, pady=10)
        self.frame.grid(row=0, column=0, pady=10, padx=pag, sticky="wns")

    def leder_close(self):
        self.frame.grid_forget()
        self.display_on()

    def leder_1(self):
        self.leder_open(self.cuntry_symbol.get_leader_1())
        pass

    def leder_2(self):
        self.leder_open(self.cuntry_symbol.get_leader_2())
        pass

    def gov(self):
        self.leder_open(self.cuntry_symbol.get_gov(), "g")
        pass

    def symb(self):
        self.leder_open([self.cuntry_symbol.flag_link, self.cuntry_symbol.coat_link], "s")
        pass



class App(customtkinter.CTk):

    width = 960
    height = 540
    def __init__(self, page_symbols: list):
        super().__init__()

        self.page_symbols = page_symbols
        self.title("leaderboard")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)
        self.configure(fg_color="#fff")

        self.bg_image = customtkinter.CTkImage(w.get_image_old(["bg", "png"]),
                                               size=(self.width, self.height))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        self.start_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="#fff")
        self.start_frame.grid(row=0, column=0, sticky="ns")

        customtkinter.CTkLabel(self.start_frame, text="", width=self.width, height=self.height)
        self.login_label = customtkinter.CTkLabel(self.start_frame, text="Leaderboard",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=30, pady=20)

        self.start_image = customtkinter.CTkImage(w.get_image_old(["world", "png"]),
                                               size=(360, 360))
        self.start_image_label = customtkinter.CTkLabel(self.start_frame, image=self.start_image, text="")
        self.start_image_label.grid(row=1, column=0)

        self.login_button = customtkinter.CTkButton(self.start_frame, text="Start", command=self.home_page, width=200)
        self.login_button.grid(row=2, column=0, padx=30, pady=(15, 15))

        self.scrollable_label_button_frame = ScrollableLabelButtonFrame(master=self, width=400, 
                                                                        height=self.height, command=self.choice_country, 
                                                                        corner_radius=0, fg_color="#fff",
                                                                        scrollbar_button_hover_color="#fff",
                                                                        scrollbar_button_color="#fff")
        for i in self.page_symbols:
            self.image = customtkinter.CTkImage(w.get_image(i.flag_link), size=(114, 73))
            self.scrollable_label_button_frame.add_item(i, image=self.image, compound="right")
        
        self.scrollable_label_button_frame.grid_forget()

    def choice_country(self, cuntry_symbol):
        self.scrollable_label_button_frame.grid_forget()
        CountryInfoFrame(master=self, country_example=cuntry_symbol).display_on()

    def home_page(self):
        self.start_frame.grid_forget()
        self.scrollable_label_button_frame.grid(row=0, column=0, padx=0, pady=0, sticky="ns")