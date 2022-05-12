import sqlite3
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
import sqlite3
from datetime import datetime

result_list = []
start = 0


class MonitorApp(MDApp):
    def enable_buttons(self):
        global screen
        screen.add_widget(self.next_button)
        screen.add_widget(self.back_button)

    def flip(self):
        screen = MDScreen()
        if self.state == 0:
            if len(result_list):
                self.state = 1
                self.input_fuel.hint_text = "Fuel"
                self.input_fuel.text = str(result_list[start]["added_fuel"])
                self.convert_button.opacity = 0
                self.convert_button.disabled = True
                self.converted.text = str(
                    result_list[start]["liters_per_1000km"])
                self.input_km.text = str(result_list[start]["km_driven"])
                self.input_price.text = str(result_list[start]["fuel_price"])
                self.label.text = "Consumtion per 100 km:"
                self.date_label.text = f'Date of fuel up: {result_list[start]["date"]}'
                self.total_label.text = f'Total spend: {result_list[start]["money_spend"]} lv'
                self.toolbar.right_action_items = []
                print(start)
            else:
                self.converted.text = "There is nothing to show. DB is empty"

    def convert(self, args):
        try:
            fuel = float(self.input_fuel.text)
            price = float(self.input_price.text)
            km = float(self.input_km.text)
            lpkm = round((fuel / km * 100), 2)
            self.converted.text = str(lpkm)
            self.label.text = "Consumtion per 100 km:"
            now = datetime.now()
            fuel_time = now.strftime("%d/%m/%Y")
            money = price * fuel

            conn = sqlite3.connect("fuel.db")
            c = conn.cursor()
            insert_with_params = ("INSERT INTO fillings(added_fuel, fuel_price, km_driven, liters_per_100km, money_spend, date) VALUES (?, ?, ?, ?, ?, ?)"
                                  )
            data_tuple = (fuel, price, km, lpkm, money, fuel_time)
            c.execute(insert_with_params, data_tuple)
            conn.commit()
            conn.close()

        except ValueError:
            self.label.text = "Please enter valid inputs"

    def show_table(self, args):
        screen = MDScreen()
        table = MDDataTable(
            column_data=[
                ("Consumption", dp(30)),
                ("Fuel", dp(30)),
                ("Kilometers", dp(30)),
                ("Fuel Price", dp(30)),
                ("Date", dp(30))
            ]
        )
        screen.add_widget(table)

    def backward(self, args):
        if len(result_list) > 0:
            try:
                global start
                start -= 1
                self.input_fuel.text = str(result_list[start]["added_fuel"])
                self.converted.text = str(
                    result_list[start]["liters_per_1000km"])
                self.input_km.text = str(result_list[start]["km_driven"])
                self.input_price.text = str(result_list[start]["fuel_price"])
                self.label.text = "Consumtion per 100 km:"
                self.date_label.text = f'Date of fuel up: {result_list[start]["date"]}'
                self.total_label.text = f'Total spend: {result_list[start]["money_spend"]} lv'
                print(start)

            except IndexError:
                start = 0
                self.input_fuel.text = str(result_list[start]["added_fuel"])
                self.converted.text = str(
                    result_list[start]["liters_per_1000km"])
                self.input_km.text = str(result_list[start]["km_driven"])
                self.input_price.text = str(result_list[start]["fuel_price"])
                self.label.text = "Consumtion per 100 km:"
                self.date_label.text = f'Date of fuel up: {result_list[start]["date"]}'
                self.total_label.text = f'Total spend: {result_list[start]["money_spend"]} lv'
        else:
            self.converted.text = "There are no entrys in database"

    def forward(self, args):
        if len(result_list) > 0:
            try:
                global start
                start += 1
                self.input_fuel.text = str(result_list[start]["added_fuel"])
                self.converted.text = str(
                    result_list[start]["liters_per_1000km"])
                self.input_km.text = str(result_list[start]["km_driven"])
                self.input_price.text = str(result_list[start]["fuel_price"])
                self.label.text = "Consumtion per 100 km:"
                self.date_label.text = f'Date of fuel up: {result_list[start]["date"]}'
                self.total_label.text = f'Total spend: {result_list[start]["money_spend"]} lv'
                print(start)
            except IndexError:
                start = 0
                self.input_fuel.text = str(result_list[start]["added_fuel"])
                self.converted.text = str(
                    result_list[start]["liters_per_1000km"])
                self.input_km.text = str(result_list[start]["km_driven"])
                self.input_price.text = str(result_list[start]["fuel_price"])
                self.label.text = "Consumtion per 100 km:"
                self.date_label.text = f'Date of fuel up: {result_list[start]["date"]}'
                self.total_label.text = f'Total spend: {result_list[start]["money_spend"]} lv'
        else:
            self.converted.text = "There are no entrys in database"

    def clear_table(self, args):
        conn = sqlite3.connect("fuel.db")
        c = conn.cursor()
        c.execute("""DELETE FROM fillings""")
        conn.commit()
        conn.close()
        result_list = []

    def build(self):
        global screen
        # Create Database or connecto to one

        conn = sqlite3.connect("fuel.db")
        c = conn.cursor()
        c.execute("""CREATE TABLE if not exists fillings(
            id integer PRIMARY KEY,
            added_fuel integer NOT NULL,
            km_driven integer,
            fuel_price integer,
            liters_per_100km integer NOT NULL,
            money_spend integer,
            date text
        ); """)
        conn.commit()
        # conn.close()
        # cursor = conn.cursor()
        mc = c.execute("""SELECT * FROM fillings ORDER BY id DESC""")
        result = mc.fetchall()

        for row in result:
            for i in range(len(result)):
                i = {"Id": row[0],
                     "added_fuel": row[1],
                     "km_driven": row[2],
                     "fuel_price": row[3],
                     "liters_per_1000km": row[4],
                     "money_spend": row[5],
                     "date": row[6]}
            result_list.append(i)

        c.close()

        self.state = 0
        self.theme_cls.primary_palette = "DeepOrange"
        screen = MDScreen()
        # UI Widgets goes here:

        self.toolbar = MDToolbar(title="Fuel Consumption monitor")
        self.toolbar.pos_hint = {"top": 1}
        self.toolbar.right_action_items = [
            ["page-next", lambda x: (self.enable_buttons(), self.flip())]]
        # self.toolbar.right_action_items = [
        #     ["page-next", lambda x: (self.flip())]]

        screen.add_widget(self.toolbar)

        # collect user input
        self.input_fuel = MDTextField(
            hint_text="Enter added fuel",
            halign="center",
            size_hint=(0.5, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.8},
            font_size=22,


        )
        screen.add_widget(self.input_fuel)

        self.input_km = MDTextField(
            hint_text="Enter driven kilometers",
            halign="center",
            size_hint=(0.5, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.7},
            font_size=22
        )
        screen.add_widget(self.input_km)

        self.input_price = MDTextField(
            hint_text="Enter gas price",
            halign="center",
            size_hint=(0.5, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            font_size=22
        )
        screen.add_widget(self.input_price)

        # BUTTONS
        self.convert_button = MDFillRoundFlatButton(
            text="CONVERT",
            font_size=17,
            pos_hint={"center_x": 0.5, "center_y": 0.2},
            on_press=self.convert
        )

        self.table_button = MDFillRoundFlatButton(
            text="TABLE",
            font_size=17,
            pos_hint={"center_x": 0.6, "center_y": 0.2},
            on_press=self.show_table
        )

        self.next_button = MDFillRoundFlatButton(
            text="NEXT",
            font_size=17,
            pos_hint={"center_x": 0.7, "center_y": 0.2},
            on_press=self.forward
        )

        self.back_button = MDFillRoundFlatButton(
            text="BACK",
            font_size=17,
            pos_hint={"center_x": 0.3, "center_y": 0.2},
            on_press=self.backward
        )
        screen.add_widget(self.convert_button)

        self.clear_db = MDFillRoundFlatButton(
            text="CLEAR DATA",
            font_size=17,
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            on_press=self.clear_table
        )

        screen.add_widget(self.clear_db)

        # secondary + primary labels
        self.label = MDLabel(
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.35},
            theme_text_color="Secondary"
        )

        self.date_label = MDLabel(
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            theme_text_color="Primary"
        )

        self.converted = MDLabel(
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.30},
            theme_text_color="Primary",
            font_style="H5"
        )

        self.total_label = MDLabel(
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            theme_text_color="Primary"
        )

        screen.add_widget(self.label)
        screen.add_widget(self.date_label)
        screen.add_widget(self.converted)
        screen.add_widget(self.total_label)

        return screen


if __name__ == '__main__':
    MonitorApp().run()
