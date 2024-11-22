from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from data_operations import get_items, add_order

LOGO_PATH = 'online-shop-logo-design-vector-illustrtaion-mobile-online-shopping-logo-vector-template-2C195PA.jpg'
BANNER_PATH = 'banner.jpg'
BUTTON_LABELS = ["Home", "Snacks", "Drinks", "Stationery"]
PAYMENT_METHODS = ['Cash Transaction', 'M-PESA', 'Airtel Money']

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.add_widget(self.layout)

        self.layout.add_widget(Label(text='Welcome to Maelezo Tuckshop!', font_size='24sp', bold=True))
        self.layout.add_widget(Label(text='Please log in to continue', font_size='18sp'))

        self.username_input = TextInput(hint_text='Username', multiline=False, size_hint=(0.8, None), height=40)
        self.password_input = TextInput(hint_text='Password', password=True, multiline=False, size_hint=(0.8, None), height=40)
        self.layout.add_widget(self.username_input)
        self.layout.add_widget(self.password_input)

        self.login_button = Button(text='Login', size_hint=(0.5, None), height=50)
        self.login_button.bind(on_press=self.verify_credentials)
        self.layout.add_widget(self.login_button)

    def verify_credentials(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        if username == "user" and password == "user123":
            self.manager.current = 'main'
        else:
            popup = Popup(title='Login Failed', content=Label(text='Invalid username or password'),
                          size_hint=(0.5, 0.5))
            popup.open()

class MainScreen(Screen):
    search_query = StringProperty("")

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=15)
        self.add_widget(self.layout)
        self.layout.add_widget(self.create_header())
        self.layout.add_widget(self.create_menu())
        self.layout.add_widget(self.create_banner())
        self.layout.add_widget(self.create_scrollable_content())
        
        # Adding the logout button to the layout
        self.layout.add_widget(self.create_logout_button())

    def create_header(self):
        header = BoxLayout(size_hint_y=None, height=80, padding=10, spacing=10)
        logo = Image(source=LOGO_PATH, size_hint_x=None, width=50, height=50)
        header.add_widget(logo)
        header.add_widget(Label(text='Maelezo Tuckshop', font_size='28sp', bold=True, color=[0.2, 0.5, 0.8, 1]))

        search_bar = TextInput(hint_text='Search for items', size_hint=(0.5, None), height=40)
        search_bar.bind(text=self.update_search_query)
        header.add_widget(search_bar)
        return header

    def create_logout_button(self):
        logout_btn = Button(text='Logout', size_hint_y=None, height=50)
        logout_btn.bind(on_press=self.logout)
        return logout_btn
    
    def logout(self, instance):
        self.manager.current = 'login'

    def create_menu(self):
        menu = BoxLayout(size_hint_y=None, height=50, spacing=10)
        for item in BUTTON_LABELS:
            btn = Button(text=item)
            btn.bind(on_press=self.filter_items)
            menu.add_widget(btn)
        return menu

    def create_banner(self):
        return Image(source=BANNER_PATH, size_hint_y=None, height=80)

    def create_scrollable_content(self):
        scroll = ScrollView()
        self.content = GridLayout(cols=1, spacing=20, size_hint_y=None, padding=[20, 20, 20, 20])
        self.content.bind(minimum_height=self.content.setter('height'))
        self.populate_items()
        scroll.add_widget(self.content)
        return scroll

    def update_search_query(self, instance, value):
        self.search_query = value
        self.populate_items()

    def populate_items(self, category=None):
        items = get_items()
        self.content.clear_widgets()

        filtered_items = self.filter_items_by_category(items, category)
        filtered_items = self.filter_items_by_search_query(filtered_items)

        for item in filtered_items:
            self.add_item_to_content(item)

    def filter_items_by_category(self, items, category):
        if category and category != "Home":
            return [item for item in items if item['category'] == category]
        return items

    def filter_items_by_search_query(self, items):
        if self.search_query:
            return [item for item in items if self.search_query.lower() in item['name'].lower()]
        return items

    def add_item_to_content(self, item):
        item_layout = BoxLayout(orientation='vertical', padding=20, spacing=20, size_hint_y=None, height=350)

        item_image = Image(source=item.get('image', 'Hand-drawn-various-food-and-drink-doodle-Graphics-34078553-1-1-580x386.png'), size_hint_y=None, height=120)
        item_layout.add_widget(item_image)

        item_layout.add_widget(Label(text=item['name'], size_hint_y=None, height=30, font_size='18sp', bold=True))
        item_layout.add_widget(Label(text=f"Price: Ksh {item['price']}", size_hint_y=None, height=30, font_size='16sp'))
        offer_text = item.get('offer', 'No offer')
        item_layout.add_widget(Label(text=f"Offer: {offer_text}", size_hint_y=None, height=30, font_size='16sp'))

        button_container = BoxLayout(size_hint_y=None, height=60, padding=[10, 10, 10, 10])
        order_button = Button(text='Order', size_hint=(1, None), height=40)
        order_button.bind(on_press=lambda btn, i=item: self.show_order_popup(i))
        button_container.add_widget(order_button)
        item_layout.add_widget(button_container)

        card = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_y=None, height=350)
        card.add_widget(item_layout)

        self.content.add_widget(card)
        self.content.add_widget(Widget())

    def filter_items(self, instance):
        self.populate_items(instance.text)

    def show_order_popup(self, item):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=f"Order {item['name']}", font_size='18sp', bold=True))
        qty_input = TextInput(hint_text='Quantity', multiline=False, input_filter='int')
        content.add_widget(qty_input)

        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        submit_btn = Button(text='Submit', on_press=lambda x: self.show_payment_popup(item, qty_input.text))
        cancel_btn = Button(text='Cancel', on_press=lambda x: popup.dismiss())
        btn_layout.add_widget(submit_btn)
        btn_layout.add_widget(cancel_btn)
        content.add_widget(btn_layout)

        popup = Popup(title='Place Order', content=content, size_hint=(0.75, 0.5))
        popup.open()

    def show_payment_popup(self, item, quantity):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=f"Pay for {quantity} of {item['name']}", font_size='18sp', bold=True))

        try:
            quantity = int(quantity)
            total_amount = quantity * float(item['price'])
        except ValueError:
            total_amount = 'Invalid quantity'

        content.add_widget(Label(text=f"Total Amount: {total_amount}", font_size='16sp', bold=True))

        for method in PAYMENT_METHODS:
            btn = Button(text=method, size_hint_y=None, height=50)
            btn.bind(on_press=lambda x, m=method: self.complete_payment(item, quantity, m))
            content.add_widget(btn)

        popup = Popup(title='Select Payment Method', content=content, size_hint=(0.75, 0.5))
        popup.open()

    def complete_payment(self, item, quantity, payment_method):
        try:
            user_id = "current_user_id"  # Replace with actual user ID from your authentication
            items = {item['name']: quantity}
            total_amount = quantity * float(item['price'])
            add_order(user_id, items, total_amount)
            print(f"Processing payment for {quantity} of {item['name']} using {payment_method}")
            self.show_confirmation_popup(item, quantity, payment_method)
        except Exception as e:
            print(f"Error storing order: {e}")

    def show_confirmation_popup(self, item, quantity, payment_method):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text='Payment successful!', font_size='18sp', bold=True))
        content.add_widget(Label(text=f"Ordered {quantity} of {item['name']} with {payment_method}", font_size='16sp', bold=True))

        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        close_btn = Button(text='Close', on_press=lambda x: (popup.dismiss(), self.populate_items()))
        btn_layout.add_widget(close_btn)
        content.add_widget(btn_layout)

        popup = Popup(title='Order Confirmation', content=content, size_hint=(0.75, 0.5))
        popup.open()

class TuckshopApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    TuckshopApp().run()
