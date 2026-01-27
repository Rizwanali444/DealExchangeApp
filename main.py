import flet as ft
import requests

DB_URL = "https://dealexchange-b7f4c-default-rtdb.firebaseio.com/posts.json"

def main(page: ft.Page):

    # ---------------- PAGE CONFIG ----------------
    page.title = "Deal Exchange Pro"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # ---------------- SNACK ----------------
    def show_snack(msg, color):
        page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=color)
        page.snack_bar.open = True
        page.update()

    # ---------------- MAIN APP ----------------
    def start_app(e=None):
        page.clean()
        page.vertical_alignment = ft.MainAxisAlignment.START

        header = ft.Container(
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

        name = ft.TextField(label="Your Name")
        offer = ft.TextField(label="Your Offer", multiline=True, min_lines=3)

        post_list = ft.Column()

        def load_posts(e=None):
            post_list.controls.clear()
            try:
                res = requests.get(DB_URL, timeout=5)
                if res.ok and res.json():
                    for v in res.json().values():
                        post_list.controls.append(
                            ft.Container(
                                ft.Column([
                                    ft.Text(v.get("user", ""), weight="bold"),
                                    ft.Text(v.get("offer", ""))
                                ]),
                                padding=10,
                                margin=5,
                                bgcolor="#1e1e1e",
                                border_radius=10
                            )
                        )
            except:
                show_snack("Failed to load posts", "red")

            page.update()

        def send_post(e):
            if not name.value or not offer.value:
                show_snack("Fill all fields", "red")
                return

            try:
                requests.post(
                    DB_URL,
                    json={"user": name.value, "offer": offer.value},
                    timeout=5
                )
                name.value = ""
                offer.value = ""
                show_snack("Post Uploaded", "green")
                load_posts()
            except:
                show_snack("Network Error", "red")

        page.add(
            header,
            name,
            offer,
            ft.ElevatedButton("POST", on_click=send_post),
            ft.IconButton(ft.icons.REFRESH, on_click=load_posts),
            ft.Text("Recent Deals", size=18),
            post_list
        )

        load_posts()

    # ---------------- SPLASH (NO THREAD, NO SLEEP) ----------------
    splash = ft.Column(
        [
            ft.Icon(ft.icons.HANDSHAKE, size=90, color="green"),
            ft.Text("Deal Exchange Pro", size=28, weight="bold"),
            ft.Text("Developed by Rizwan Ali"),
            ft.ElevatedButton("START", on_click=start_app)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.add(splash)


ft.app(target=main)
