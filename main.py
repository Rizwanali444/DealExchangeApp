import flet as ft
import requests
import time

# Aapka Database URL
DB_URL = "https://dealexchange-b7f4c-default-rtdb.firebaseio.com/posts.json?print=pretty"

def main(page: ft.Page):
    # Page Settings
    page.title = "Deal Exchange Pro"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Function to start the real app after permissions
    def start_real_app(e=None):
        page.clean()
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.horizontal_alignment = ft.CrossAxisAlignment.START
        
        # Header
        header = ft.Container(
            content=ft.Row([
                ft.Text("Deal Exchange 🤝", size=24, weight="bold", color="green"),
                ft.Icon(ft.icons.NOTIFICATIONS, color="white")
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=10,
            bgcolor="#1e1e1e"
        )

        # Inputs
        user_name = ft.TextField(label="Your Name", border_color="green", border_radius=10)
        user_offer = ft.TextField(label="What are you offering?", multiline=True, min_lines=3, border_color="green")

        def send_data(e):
            if not user_name.value or not user_offer.value:
                page.snack_bar = ft.SnackBar(ft.Text("Please fill all fields!"), bgcolor="red")
                page.snack_bar.open = True
                page.update()
                return
            
            # Firebase Post
            try:
                requests.post(DB_URL, json={"user": user_name.value, "offer": user_offer.value})
                page.snack_bar = ft.SnackBar(ft.Text("Post Uploaded Successfully!"), bgcolor="green")
                user_name.value = ""
                user_offer.value = ""
            except:
                page.snack_bar = ft.SnackBar(ft.Text("Network Error!"), bgcolor="red")
            
            page.snack_bar.open = True
            page.update()

        post_btn = ft.ElevatedButton(
            "POST NOW", 
            on_click=send_data, 
            bgcolor="green", 
            color="white", 
            width=400,
            height=50
        )

        page.add(header, ft.Divider(), user_name, user_offer, post_btn)
        page.update()

    # Permission Dialog
    def show_perm_dialog():
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Permissions Required"),
            content=ft.Text("This app needs Camera and Storage permissions to work properly."),
            actions=[ft.TextButton("ALLOW", on_click=lambda _: (setattr(page.dialog, 'open', False), start_real_app(), page.update()))]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    # Splash Screen UI
    splash = ft.Column([
        ft.Icon(ft.icons.HANDSHAKE_ROUNDED, size=100, color="green"),
        ft.Text("DEAL EXCHANGE", size=32, weight="bold", color="blue"),
        ft.Text("Developed by Rizwan Ali", size=16, italic=True, color="gold"),
        ft.Container(height=20),
        ft.ProgressBar(width=200, color="green")
    ], horizontal_alignment="center")

    page.add(splash)
    page.update()
    
    time.sleep(3) # Wait for splash
    page.clean()
    show_perm_dialog()

if __name__ == "__main__":
    ft.app(target=main)
