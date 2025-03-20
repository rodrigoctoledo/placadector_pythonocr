# ui.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from api import login_api, create_occurrence
import config  # Importa o módulo config em vez de jwt_token e user_id diretamente

def login_window():
    root = tk.Tk()
    root.title("Login na API MyApp")

    tk.Label(root, text="Email:").grid(row=0, column=0)
    entry_email = tk.Entry(root)
    entry_email.grid(row=0, column=1)

    tk.Label(root, text="Senha:").grid(row=1, column=0)
    entry_senha = tk.Entry(root, show="*")  # Use "*" para ocultar a senha
    entry_senha.grid(row=1, column=1)

    def do_login():
        email = entry_email.get().strip()
        senha = entry_senha.get().strip()
        print("Tentando login com:", email, senha)

        # Chama a função login_api e recebe o token e o user_id se o login for bem-sucedido.
        token, user_id_val = login_api(email, senha)

        if token:
            # Atribui diretamente no módulo config
            config.jwt_token = token
            config.user_id = user_id_val

            # Se a API não retornou user_id, solicita manualmente
            if not config.user_id:
                user_id_str = simpledialog.askstring("User ID", "Digite seu ID de usuário:")
                try:
                    config.user_id = int(user_id_str)
                except Exception as e:
                    print("Erro ao converter User ID:", e)
                    config.user_id = 0

            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            root.destroy()
        else:
            messagebox.showerror("Erro",
                "Falha no login. Verifique suas credenciais.\n"
                "Confira o terminal para detalhes do erro.")

    tk.Button(root, text="Login", command=do_login).grid(row=2, column=0, columnspan=2)
    root.mainloop()


def manual_occurrence_registration():
    """Janela para cadastrar ocorrência manualmente."""
    win = tk.Toplevel()
    win.title("Cadastro Manual de Ocorrência")

    tk.Label(win, text="Placa:").grid(row=0, column=0)
    entry_plate = tk.Entry(win)
    entry_plate.grid(row=0, column=1)

    tk.Label(win, text="Descrição:").grid(row=1, column=0)
    entry_desc = tk.Entry(win)
    entry_desc.grid(row=1, column=1)

    def submit_occurrence():
        plate = entry_plate.get().strip()
        desc = entry_desc.get().strip()

        if not plate or not desc:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        occurrence_data = {
            "placa": plate,
            "descricao": desc,
            "usuarioId": config.user_id  # Pega o user_id direto de config
        }
        create_occurrence(occurrence_data)
        win.destroy()

    tk.Button(win, text="Cadastrar", command=submit_occurrence).grid(row=2, column=0, columnspan=2)


def main_menu():
    """Menu principal do sistema."""
    main_win = tk.Tk()
    main_win.title("Sistema de Cadastro de Ocorrências")

    tk.Button(main_win, text="Cadastrar Ocorrência Manual",
              command=manual_occurrence_registration).pack(pady=10)

    main_win.mainloop()
