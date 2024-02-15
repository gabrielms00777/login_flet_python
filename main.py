import flet as ft
import httpx

BASE_URL = 'LINK_API'
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

def main(page: ft.Page):
    page.window_height = 500
    page.window_width = 500

    title = ft.Text('Faça seu login')
    email = ft.TextField(hint_text='Email', value='admin@admin')
    password = ft.TextField(hint_text='Senha', password=True, value='admin')

    def submit(e):
        button.disabled = True
        try:
            data = {
                "email": email.value,
                "password": password.value,
            }
            res = httpx.post(f'{BASE_URL}/login', headers=headers, json=data)
            res = res.json()
            if 'token' in res:
                page.client_storage.set('token', res['token'])
                
                page.go('/home')
            else:
                ft.AlertDialog(
                    title=ft.Text("Credenciais invaldas, tente novamente!"), on_dismiss=lambda e: print("Dialog dismissed!")
                )  
                page.update() 
                print(f'Erro no login. Mensagem do servidor: {res.get("message")}')
        except:
            print('error')
            ft.AlertDialog(
                title=ft.Text("Erro no serivdor, tente novamente!"), on_dismiss=lambda e: print("Dialog dismissed!"),
                open=True
            )   

    def logout(e):
        page.client_storage.remove("token")
        page.go("/")

    button = ft.FilledButton('Entrar', on_click=submit)

    login_page = ft.View('/', 
                         vertical_alignment=ft.MainAxisAlignment.CENTER,
                         horizontal_alignment=ft.MainAxisAlignment.CENTER,
                         controls=[ft.Container(
                            content=ft.Column([title, email, password, button]),
                        )]) 

    def route_change(e):
        page.views.clear()
        page.views.append(
            login_page
        )   
        if page.route == '/home':
            page.views.append(
                ft.View(
                "/home",
                [
                    ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ft.ElevatedButton("Logout", on_click=logout),
                ]
                )
            )
        page.update()
    
    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    if page.client_storage.get('token'):
        try:
            headers['Authorization'] = f"Bearer {page.client_storage.get('token')}"
            res = httpx.get(f'{BASE_URL}/user', headers=headers, )
            res = res.json()
            if 'name' in res:
                page.go('/home')
            else:
                page.go('/')
        except:
            page.go('/')
    else:
        page.go('/')


ft.app(target=main)
