import flet as ft
from google import genai

def main(page: ft.Page):
    page.title = "J.A.R.V.I.S. v1.0"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0e1117"
    page.padding = 20

    # Campo para la API Key
    api_key_input = ft.TextField(
        label="API Key de Google Gemini (AIzaSy...)",
        password=True,
        can_reveal_password=True,
        border_color="#00ffcc",
        focused_border_color="#00ffcc",
        label_style=ft.TextStyle(color="#00ffcc")
    )

    # Lista donde irán apareciendo los mensajes del chat
    chat_list = ft.ListView(expand=True, spacing=10, auto_scroll=True)

    # Campo de texto para escribir la orden
    user_input = ft.TextField(
        hint_text="Escriba su orden, Señor...",
        border_color="#00ffcc",
        focused_border_color="#00ffcc",
        expand=True
    )

    def send_click(e):
        if not api_key_input.value:
            chat_list.controls.append(
                ft.Text("⚠️ Por favor, ingrese su API Key primero.", color="red")
            )
            page.update()
            return

        user_text = user_input.value.strip()
        if not user_text:
            return

        # Mostrar mensaje del usuario
        chat_list.controls.append(
            ft.Row([ft.Text(f"Señor: {user_text}", color="white")], alignment=ft.MainAxisAlignment.END)
        )
        user_input.value = ""
        page.update()

        try:
            # Conexión oficial con Google GenAI
            client = genai.Client(api_key=api_key_input.value)
            
            # Generar respuesta con JARVIS
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=f"Eres JARVIS, el asistente de Tony Stark. Responde de forma formal, eficiente y concisa, llamándome 'Señor'. Orden: {user_text}"
            )
            reply = response.text

            # Mostrar respuesta de JARVIS
            chat_list.controls.append(
                ft.Row([ft.Text(f"JARVIS: {reply}", color="#00ffcc")], alignment=ft.MainAxisAlignment.START)
            )
        except Exception as ex:
            chat_list.controls.append(
                ft.Row([ft.Text(f"Error de sistema: {ex}", color="red")], alignment=ft.MainAxisAlignment.START)
            )
        page.update()

    # Botón de enviar
    send_button = ft.IconButton(
        icon=ft.icons.SEND_ROUNDED,
        icon_color="#00ffcc",
        on_click=send_click
    )

    # Estructura visual de la app
    page.add(
        ft.Text("J.A.R.V.I.S. Sistemas en Línea", size=20, weight=ft.FontWeight.BOLD, color="#00ffcc"),
        api_key_input,
        ft.Divider(color="#00ffcc"),
        chat_list,
        ft.Row([user_input, send_button])
    )

ft.app(target=main)
          
