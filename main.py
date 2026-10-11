import tkinter as tk
from tkinter import messagebox
from scrapers.inspired_taste import get_recipe_from_inspired_taste
from scrapers.bread_dad import get_recipe_from_bread_dad


def get_recipe(url):
    if url.find("inspiredtaste") >= 0:
        recipe = get_recipe_from_inspired_taste(url)
        return recipe
    if url.find("breaddad") >= 0:
        recipe = get_recipe_from_bread_dad(url)
        return recipe
    return None

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("help me")
        self.geometry("500x500")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.pages ={}

        for Page in (URLPage,ResultPage):
            page = Page(container,self)
            self.pages[Page] = page
            page.grid(row=0,column=0,sticky="nsew")

        self.show_page(URLPage)

    def show_page(self, page):
        self.pages[page].tkraise()

class URLPage(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)

        tk.Label(self,text="Enter URL:",font=("Helvetica",12)).pack(pady=30)

        self.url_entry = tk.Entry(self,text = "hello", width=50)
        self.url_entry.insert(tk.END,"https://breaddad.com/easy-banana-bread-recipe")
        self.url_entry.pack(pady=10)
        self.updating = False

        tk.Button(
            self,
            text="Submit",
            command=self.submit_url
        ).pack(pady=20)

        self.controller = controller

    def submit_url(self):
        url = self.url_entry.get()

        if not url:
            messagebox.showerror("URL Error","Please enter a valid URL")
            return

        else:
            reciperesult = get_recipe(url)
            if reciperesult:
                print(reciperesult)
                self.controller.pages[ResultPage].show_list(reciperesult)

                self.controller.show_page(ResultPage)
            else:
                messagebox.showerror("URL Error","URL Not Supported")

        # except Exception as e:
        #     messagebox.showerror("URL Error",e)

class ResultPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        scroll_container = tk.Frame(self)
        scroll_container.pack(fill="both", expand=True)

        canvas = tk.Canvas(scroll_container)

        vertical_scrollbar = tk.Scrollbar(
            scroll_container,
            orient="vertical",
            command=canvas.yview
        )

        horizontal_scrollbar = tk.Scrollbar(
            scroll_container,
            orient="horizontal",
            command=canvas.xview
        )

        canvas.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        vertical_scrollbar.pack(side="right", fill="y")
        horizontal_scrollbar.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)

        self.results_frame = tk.Frame(canvas)

        canvas_window = canvas.create_window(
            (0, 0),
            window=self.results_frame,
            anchor="nw"
        )

        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfig(
                canvas_window,
                width=event.width
            )
        )
        self.results_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.bind_all(
            "<MouseWheel>",
            lambda event: canvas.yview_scroll(
                -1 if event.delta >0 else 1,
                "units"
            )
        )

        self.number_vars = []
        self.original_values = []
        self.updating = False

        tk.Button(
            self,
            text="Back",
            command=lambda: self.controller.show_page(URLPage)
        ).pack()

    def show_list(self,result):
        print(result)
        title = tk.Label(
            self.results_frame,
            text=result.name,
            font=("Arial", 14, "bold")
        )
        title.pack(anchor="w", pady=(0, 10))

        self.controller.title(result.name)
        print(result.ingredients)
        self.show_ingredients(result.ingredients)
        self.show_directions(result.directions)
        if result.tips:
            self.show_tips(result.tips)

    def show_tips(self,tips):
        print(tips)
        title = tk.Label(
            self.results_frame,
            text="Tips:",
            font=("Arial", 14, "bold")

        )
        title.pack(anchor="w", pady=(0, 10))
        index = 0
        for tip in tips.tips:
            row = tk.Frame(self.results_frame)
            row.pack(fill="x", padx=20, pady=5)
            if tip.title:
                tk.Label(
                    row,
                    text=tip.title,
                    font=("Arial", 14, "bold")
                ).pack(side="left", padx=10)
            label = tk.Label(
                row,
                text=tip.tip,
                wraplength=400,
                justify="left",
                anchor="w"
            )
            label.pack(side="left", padx=10, expand=True)
            row.bind(
                "<Configure>",
                lambda event, lbl=label: lbl.config(wraplength=event.width)
            )




    def show_directions(self,directions):
        print(directions)
        index =0
        for direction in directions:
            print(direction)
            direction.print()
            title = tk.Label(
                self.results_frame,
                text= str(index) + "." +direction.title,
            )
            index+=1
            title.pack(anchor="w", pady=(0, 10))
            for listitem in direction.instructions:
                row = tk.Frame(self.results_frame)
                row.pack(fill="x", padx=20, pady=5)
                label = tk.Label(
                    row,
                    text=listitem,
                    wraplength=400,
                    justify="left",
                    anchor="w"
                )
                label.pack(side="left", fill="x", expand=True)
                row.bind(
                    "<Configure>",
                    lambda event,lbl = label: lbl.config(wraplength=event.width)
                )
        return


    def show_ingredients(self,ingredients):
        index = 0
        for ingredient in ingredients:
            print("1")
            ingredient.print()
            # tk.Label(self.results_frame,ingredient.title).pack(side="left",padx=10)
            print(ingredient.title)
            row_frame = tk.Frame(self.results_frame)
            row_frame.pack(fill='x', padx=10, pady=10)
            title = tk.Label(
                row_frame,
                text="Ingredients",#ingredient.title,
                font=("Arial", 14, "bold")
            )
            title.pack(side="left", padx =5)
            tk.Button(
                row_frame,
                text="Reset",
                command=lambda: self.reset_all_values()
            ).pack(side="left", padx =5)

            for recipeitem in ingredient.ingredients:
                row = tk.Frame(self.results_frame)
                row.pack(fill="x", padx=20, pady=5)
                # Number input

                var = tk.StringVar(value=str(recipeitem.quantity))
                self.original_values.append(float(recipeitem.quantity))
                number_entry = tk.Entry(row, width=5, textvariable=var)
                number_entry.pack(side="left")
                self.number_vars.append(var)

                number_entry.bind(
                    "<FocusOut>",
                    lambda event, saved_index=index: self.update_all_numbers(saved_index)
                )
                # Item name
                tk.Label(
                    row,
                    text=recipeitem.unit
                ).pack(side="left", padx=10)
                index += 1
#if secondary unit
                if recipeitem.secondary_unit:
                    var3 = tk.StringVar(value=recipeitem.secondary_quantity)

                    entry3 = tk.Entry(row, width=5, textvariable=var3)
                    self.original_values.append(float(recipeitem.secondary_quantity))
                    entry3.pack(side="left")
                    tk.Label(
                        row,
                        text=recipeitem.secondary_unit
                    ).pack(side="left", padx=10)
                    entry3.bind(
                        "<FocusOut>",
                        lambda event, saved_index=index: self.update_all_numbers(saved_index)
                    )
                    index += 1
#item name
                    self.number_vars.append(var3)
                tk.Label(
                    row,
                    text=recipeitem.name
                ).pack(side="left", padx=10)

#if item weight is there
                if recipeitem.weight:

                    var2 = tk.StringVar(value=recipeitem.weight)

                    entry2 = tk.Entry(row, width=5, textvariable=var2)
                    self.original_values.append(float(recipeitem.weight))
                    entry2.pack(side="left")
                    tk.Label(
                        row,
                        text=recipeitem.weightUnit
                    ).pack(side="left", padx=10)
                    entry2.bind(
                        "<FocusOut>",
                        lambda event, saved_index=index: self.update_all_numbers(saved_index)
                    )

                    index += 1
                    self.number_vars.append(var2)
                # row.bind(
                #     "<Configure>",
                #     lambda event: label.config(
                #         wraplength=max(100, event.width - 150)
                #     )
                # )

                # Save the Entry so we can get its value later

                # self.number_entries.append(recipeitem.name,number_entry)

        # for item in self.number_entries:
        #     print(item)

    def reset_all_values(self):
        if self.updating:
            return
        # new_value = self.number_vars[changed_index].get()
        # print("new valye:",new_value,"old value",self.original_values[changed_index])
        # try:
        #     new_value = float(new_value)
        # except ValueError:
        #     return
        #
        # if new_value == 0:
        #     return
        #
        # self.updating = True
        #
        # try:
        #     ratio = new_value/self.original_values[changed_index]

        self.updating = True
        for i in range(0, len(self.number_vars)):
            new_number = round(self.original_values[i],2)
            self.number_vars[i].set(str(new_number))
        self.updating = False
        return

    def update_all_numbers(self,changed_index):
        if self.updating:
            return
        new_value = self.number_vars[changed_index].get()
        print("new value:",new_value,"old value",self.original_values[changed_index])
        try:
            new_value = float(new_value)
        except ValueError:
            return

        if new_value == 0:
            return

        self.updating = True

        try:
            ratio = new_value/self.original_values[changed_index]
            for i in range(0, len(self.number_vars)):
                new_number = round(ratio * self.original_values[i],2)
                if new_number.is_integer():
                    new_number = int(new_number)
                self.number_vars[i].set(str(new_number))

        finally:
            self.updating = False
        return

    def make_reset_call(self):
        def rescallbkac(*args):
            self.reset_all_values()
    def make_callback(self,index):
        def callback(*args):
            self.update_all_numbers(index)

        return callback
app = App()
app.mainloop()




