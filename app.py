from cgitb import text
import sqlite3
from turtle import title
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivymd.uix.button import MDFillRoundFlatIconButton, MDFillRoundFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDToolbar
import sqlite3


class MonitorApp(MDApp):
    def flip(self):
        pass

    def convert(self, args):
        try:
            fuel = float(self.input_fuel.text)
            price = float(self.input_fuel.text)
            km = float(self.input_km.text)
            lpkm = fuel / km * 100
            self.converted.text = str(lpkm)
            self.label.text = "Consumtion per 100 km:"

        except ValueError:
            self.label.text = "Please enter valid inputs"

    def build(self):
        # Create Database or connecto to one

        conn = sqlite3.connect("fuel.db")
        c = conn.cursor()
        c.execute("""CREATE TABLE if not exists fillings(
            id integer PRIMARY KEY,
            added_fuel integer NOT NULL,
            fuel_price integer,
            liters_per_100km integer NOT NULL
        ); """)

        self.state = 0
        self.theme_cls.primary_palette = "DeepOrange"
        screen = MDScreen()
        # UI Widgets goes here:

        self.toolbar = MDToolbar(title="Fuel Consumption monitor")
        self.toolbar.pos_hint = {"top": 1}
        self.toolbar.right_action_items = [
            ["rotate-3d-variant", lambda x: self.flip()]]
        screen.add_widget(self.toolbar)

        # collect user input
        self.input_fuel = MDTextField(
            text="enter fuel added",
            halign="center",
            size_hint=(0.5, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.8},
            font_size=22
        )
        screen.add_widget(self.input_fuel)

        self.input_km = MDTextField(
            text="enter km driven",
            halign="center",
            size_hint=(0.5, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.7},
            font_size=22
        )
        screen.add_widget(self.input_km)

        self.input_price = MDTextField(
            text="enter gas price",
            halign="center",
            size_hint=(0.5, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            font_size=22
        )
        screen.add_widget(self.input_price)

        # "CONVERT" button
        screen.add_widget(MDFillRoundFlatButton(
            text="CONVERT",
            font_size=17,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            on_press=self.convert
        ))

        # secondary + primary labels
        self.label = MDLabel(
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.35},
            theme_text_color="Secondary"
        )

        self.converted = MDLabel(
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.30},
            theme_text_color="Primary",
            font_style="H5"
        )

        screen.add_widget(self.label)
        screen.add_widget(self.converted)

        return screen


if __name__ == '__main__':
    MonitorApp().run()
