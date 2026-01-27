import flet as ft
import requests

DB_URL = "https://dealexchange-b7f4c-default-rtdb.firebaseio.com/posts.json"


# ---------------- UTILITY FUNCTIONS ----------------
def show_snack(page, message, color):
    page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor=color)
    page.snack_bar.open = True
    page.update()


def fetch_posts():
    try:
        res = requests.get(DB_URL, timeout=5)
        if res.ok and res.json():
            return res.json().values()
    except:
        pass
    return []


def upload_post(name, offer):
    try:
        requests.post(
            DB_URL,
            json={"user": name, "offer": offer},
            timeout=5
        )
        return True
    except:
        return False


# ---------------- UI COMPONENTS ----------------
def header_ui():
    return ft.Container(
        ft.Row(
            [
                ft.Text("Deal Exchange 🤝", size=22, weight="bold"),
                ft.Icon(ft.icons.NOTIFICATIONS)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        padding=10,
        bgcolor="#121212"
    )


def post_card(user, offer):
    return ft.Container(
        ft.Column([
            ft.Text(user, weight="bold"),
            ft.Text(offer)
        ]),
        padding=10,
        margin=5,
        bgcolor="#1e1e1e",
        border_radius=10
    )


# ---------------- MAIN APP ----------------
def start_app(page: ft.Page):
    page.clean()
    page.vertical_alignment = ft.MainAxisAlignment.START

    name_field = ft.TextField(label="Your Name")
    offer_field = ft.TextField(label="Your Offer", multiline=True, min_lines=3)
    post_list = ft.Column()

    def load_posts(e=None):
        post_list.controls.clear()
        for post in fetch_posts():
            post_list.controls.append(
                post_card(
                    post.get("user", ""),
                    post.get("offer", "")
                )
            )
        page.update()

    def send_post(e):
        if not name_field.value or not offer_field.value:
            show_snack(page, "Fill all fields", "red")
            return

        success = upload_post(name_field.value, offer_field.value)
        if success:
            name_field.value = ""
            offer_field.value = ""
            show_snack(page, "Post Uploaded", "green")
            load_posts()
        else:
            show_snack(page, "Network Error", "red")

    page.add(
        header_ui(),
        name_field,
        offer_field,
        ft.ElevatedButton("POST", on_click=send_post),
        ft.IconButton(ft.icons.REFRESH, on_click=load_posts),
        ft.Text("Recent Deals", size=18),
        post_list
    )

    load_posts()


# ---------------- SPLASH SCREEN ----------------
def splash_screen(page: ft.Page):
    page.clean()
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(
        ft.Column(
            [
                ft.Icon(ft.icons.HANDSHAKE, size=90, color="green"),
                ft.Text("Deal Exchange Pro", size=28, weight="bold"),
                ft.Text("Developed by Rizwan Ali"),
                ft.ElevatedButton(
                    "START",
                    on_click=lambda e: start_app(page)
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )


# ---------------- ENTRY POINT ----------------
def main(page: ft.Page):
    page.title = "Deal Exchange Pro"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO

    splash_screen(page)


ft.app(target=main)
