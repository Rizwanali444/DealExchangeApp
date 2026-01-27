import flet as ft
import requests
import threading

DB_URL = "https://dealexchange-b7f4c-default-rtdb.firebaseio.com/posts.json"

def main(page: ft.Page):

    # ---------------- PAGE CONFIG ----------------
    page.title = "Deal Exchange Pro"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    # ---------------- UTILS ----------------
    def show_snack(msg, color):
        page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=color)
        page.snack_bar.open = True
        page.update()

    # ---------------- MAIN APP ----------------
    def start_app():
        page.clean()
        page.vertical_alignment = ft.MainAxisAlignment.START

        header = ft.Container(
            content=ft.Row(
                [
                    ft.Text("Deal Exchange 🤝", size=22, weight="bold"),
                    ft.Icon(ft.icons.NOTIFICATIONS_ACTIVE)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding=10,
            bgcolor="#121212"
        )

        name = ft.TextField(label="Your Name", border_radius=12)
        offer = ft.TextField(
            label="Your Offer",
            multiline=True,
            min_lines=3,
            max_lines=5,
            border_radius=12
        )

        post_list = ft.Column(scroll=ft.ScrollMode.AUTO)

        def load_posts():
            post_list.controls.clear()
            try:
                res = requests.get(DB_URL, timeout=10)
                if res.status_code == 200 and res.json():
                    for k, v in res.json().items():
                        post_list.controls.append(
                            ft.Container(
                                content=ft.Column([
                                    ft.Text(v.get("user", ""), weight="bold"),
                                    ft.Text(v.get("offer", "")),
                                ]),
                                padding=10,
                                margin=5,
                                bgcolor="#1e1e1e",
                                border_radius=10
                            )
                        )
            except:
                pass
            page.update()

        def send_post(e):
            if not name.value or not offer.value:
                show_snack("Fill all fields", "red")
                return

            try:
                requests.post(DB_URL, json={
                    "user": name.value,
                    "offer": offer.value
                }, timeout=10)

                name.value = ""
                offer.value = ""
                show_snack("Post Uploaded", "green")
                load_posts()
            except:
                show_snack("Network Error", "red")

        post_btn = ft.ElevatedButton(
            "POST",
            icon=ft.icons.SEND,
            on_click=send_post
        )

        refresh_btn = ft.IconButton(
            icon=ft.icons.REFRESH,
            on_click=lambda e: load_posts()
        )

        page.add(
            header,
            ft.Divider(),
            name,
            offer,
            post_btn,
            refresh_btn,
            ft.Text("Recent Deals", size=18),
            post_list
        )

        load_posts()

    # ---------------- SPLASH ----------------
    splash = ft.Column(
        [
            ft.Icon(ft.icons.HANDSHAKE, size=90, color="green"),
            ft.Text("Deal Exchange Pro", size=28, weight="bold"),
            ft.Text("Developed by Rizwan Ali", size=14),
            ft.ProgressRing()
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.add(splash)
    page.update()

    # NON-BLOCKING DELAY (APK SAFE)
    def delayed_start():
        import time
        time.sleep(2)
        page.clean()
        start_app()

    threading.Thread(target=delayed_start).start()


ft.app(target=main)
