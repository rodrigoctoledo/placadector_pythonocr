import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import datetime

# Configurações globais
API_BASE_URL = "https://localhost:44339/api"
jwt_token = ""
user_id = None


# ---------------------------
# Funções de Integração com a API
# ---------------------------

def login_api(email, senha):
    data = {"email": email, "senha": senha}
    try:
        response = requests.post(f"{API_BASE_URL}/Auth/login", json=data, verify=False)
        if response.status_code == 200:
            json_data = response.json()
            return json_data.get("token"), json_data.get("id")
        else:
            return None, None
    except Exception as e:
        messagebox.showerror("Erro", f"Exceção no login: {e}")
        return None, None


def register_api(nome, email, senha, niveisUsuario):
    data = {"nome": nome, "email": email, "senha": senha, "niveisUsuario": niveisUsuario}
    try:
        response = requests.post(f"{API_BASE_URL}/Auth/register", json=data, verify=False)
        return response.status_code in [200, 201]
    except Exception as e:
        messagebox.showerror("Erro", f"Exceção no registro: {e}")
        return False


def recover_password_api(email, novaSenha):
    data = {"email": email, "novaSenha": novaSenha}
    try:
        response = requests.post(f"{API_BASE_URL}/Auth/recover", json=data, verify=False)
        return response.status_code in [200, 201]
    except Exception as e:
        messagebox.showerror("Erro", f"Exceção na recuperação: {e}")
        return False


def create_occurrence_api(placa, descricao, usuarioId, token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {"placa": placa, "descricao": descricao, "usuarioId": usuarioId}
    try:
        response = requests.post(f"{API_BASE_URL}/Ocorrencias", json=data, headers=headers, verify=False)
        return response.status_code in [200, 201]
    except Exception as e:
        messagebox.showerror("Erro", f"Exceção ao cadastrar ocorrência: {e}")
        return False


def update_occurrence_api(occurrence_id, placa, descricao, usuarioId, token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {"id": occurrence_id, "placa": placa, "descricao": descricao, "usuarioId": usuarioId}
    try:
        response = requests.put(f"{API_BASE_URL}/Ocorrencias/{occurrence_id}", json=data, headers=headers, verify=False)
        return response.status_code in [200, 204]
    except Exception as e:
        messagebox.showerror("Erro", f"Exceção ao atualizar ocorrência: {e}")
        return False


def delete_occurrence_api(occurrence_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.delete(f"{API_BASE_URL}/Ocorrencias/{occurrence_id}", headers=headers, verify=False)
        return response.status_code in [200, 204]
    except Exception as e:
        messagebox.showerror("Erro", f"Exceção ao excluir ocorrência: {e}")
        return False


def update_plate_api(plate_id, placa, local, horario, usuarioId, token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {"id": plate_id, "placa": placa, "local": local, "horario": horario, "usuarioId": usuarioId}
    try:
        response = requests.put(f"{API_BASE_URL}/Plates/{plate_id}", json=data, headers=headers, verify=False)
        return response.status_code in [200, 204]
    except Exception as e:
        messagebox.showerror("Erro", f"Exceção ao atualizar plate: {e}")
        return False


def delete_plate_api(plate_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.delete(f"{API_BASE_URL}/Plates/{plate_id}", headers=headers, verify=False)
        return response.status_code in [200, 204]
    except Exception as e:
        messagebox.showerror("Erro", f"Exceção ao excluir plate: {e}")
        return False


# ---------------------------
# Interface com Tkinter
# ---------------------------

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MyApp - Janela Maximizada")
        self.state('zoomed')  # Maximiza a janela mantendo os botões do sistema
        self.configure(bg='white')

        # Variáveis para armazenar dados do usuário
        self.jwt_token = ""
        self.user_id = None

        # Container principal com fundo azul cobrindo toda a tela
        container = tk.Frame(self, bg='lightblue')
        container.place(relx=0, rely=0, relwidth=1, relheight=1)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (
        LoginFrame, RegisterFrame, RecoverFrame, DashboardFrame, OccurrenceFrame, OccurrenceEditFrame, PlateEditFrame):
            frame = F(parent=container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginFrame")

    def show_frame(self, frame_name):
        self.frames[frame_name].tkraise()


# Tela de Login
class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='lightblue')

        panel = tk.Frame(self, bg='white', padx=30, pady=30)
        panel.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(panel, text="Login", font=("Arial", 24), bg='white').grid(row=0, column=0, columnspan=2, pady=(0, 20))

        tk.Label(panel, text="Email:", bg='white').grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.email_entry = tk.Entry(panel, width=30)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(panel, text="Senha:", bg='white').grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.password_entry = tk.Entry(panel, width=30, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(panel, text="Entrar", command=self.do_login, width=15).grid(row=3, column=0, columnspan=2, pady=15)

        btn_frame = tk.Frame(panel, bg='white')
        btn_frame.grid(row=4, column=0, columnspan=2, pady=5)
        tk.Button(btn_frame, text="Registrar", command=lambda: controller.show_frame("RegisterFrame"), width=15) \
            .grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Recuperar Senha", command=lambda: controller.show_frame("RecoverFrame"), width=15) \
            .grid(row=0, column=1, padx=5, pady=5)

    def do_login(self):
        email = self.email_entry.get()
        senha = self.password_entry.get()
        token, uid = login_api(email, senha)
        if token:
            self.controller.jwt_token = token
            self.controller.user_id = uid
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            self.controller.show_frame("DashboardFrame")
        else:
            messagebox.showerror("Erro", "Falha no login. Verifique suas credenciais.")


# Tela de Registro
class RegisterFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='lightgreen')

        panel = tk.Frame(self, bg='white', padx=30, pady=30)
        panel.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(panel, text="Registrar", font=("Arial", 24), bg='white').grid(row=0, column=0, columnspan=2,
                                                                               pady=(0, 20))

        tk.Label(panel, text="Nome:", bg='white').grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.nome_entry = tk.Entry(panel, width=30)
        self.nome_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(panel, text="Email:", bg='white').grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.email_entry = tk.Entry(panel, width=30)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(panel, text="Senha:", bg='white').grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.senha_entry = tk.Entry(panel, width=30, show="*")
        self.senha_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(panel, text="Nível de Usuário:", bg='white').grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.nivel_var = tk.StringVar(value="User")
        nivel_box = ttk.Combobox(panel, textvariable=self.nivel_var, values=["Admin", "User"], state="readonly",
                                 width=28)
        nivel_box.grid(row=4, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(panel, bg='white')
        btn_frame.grid(row=5, column=0, columnspan=2, pady=15)
        tk.Button(btn_frame, text="Registrar", command=self.do_register, width=15) \
            .grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Voltar", command=lambda: controller.show_frame("LoginFrame"), width=15) \
            .grid(row=0, column=1, padx=5, pady=5)

    def do_register(self):
        nome = self.nome_entry.get()
        email = self.email_entry.get()
        senha = self.senha_entry.get()
        niveisUsuario = self.nivel_var.get()
        if register_api(nome, email, senha, niveisUsuario):
            messagebox.showinfo("Sucesso", "Registro realizado com sucesso!")
            self.controller.show_frame("LoginFrame")
        else:
            messagebox.showerror("Erro", "Falha no registro.")


# Tela de Recuperação de Senha
class RecoverFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='lightyellow')

        panel = tk.Frame(self, bg='white', padx=30, pady=30)
        panel.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(panel, text="Recuperar Senha", font=("Arial", 24), bg='white') \
            .grid(row=0, column=0, columnspan=2, pady=(0, 20))
        tk.Label(panel, text="Email:", bg='white').grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.email_entry = tk.Entry(panel, width=30)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(panel, text="Nova Senha:", bg='white').grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.new_password_entry = tk.Entry(panel, width=30, show="*")
        self.new_password_entry.grid(row=2, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(panel, bg='white')
        btn_frame.grid(row=3, column=0, columnspan=2, pady=15)
        tk.Button(btn_frame, text="Recuperar", command=self.do_recover, width=15) \
            .grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Voltar", command=lambda: controller.show_frame("LoginFrame"), width=15) \
            .grid(row=0, column=1, padx=5, pady=5)

    def do_recover(self):
        email = self.email_entry.get()
        novaSenha = self.new_password_entry.get()
        if recover_password_api(email, novaSenha):
            messagebox.showinfo("Sucesso", "Senha recuperada com sucesso!")
            self.controller.show_frame("LoginFrame")
        else:
            messagebox.showerror("Erro", "Falha na recuperação de senha.")


# Tela Dashboard
class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='white')

        tk.Label(self, text="Dashboard", font=("Arial", 24), bg='white') \
            .pack(pady=20)

        btn_frame = tk.Frame(self, bg='white')
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Plates", command=self.load_plates, width=18) \
            .grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Ocorrências", command=self.load_ocorrencias, width=18) \
            .grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Cadastrar Ocorrência", command=lambda: controller.show_frame("OccurrenceFrame"),
                  width=18) \
            .grid(row=0, column=2, padx=5, pady=5)
        tk.Button(btn_frame, text="Editar Ocorrência", command=lambda: controller.show_frame("OccurrenceEditFrame"),
                  width=18) \
            .grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Editar Plate", command=lambda: controller.show_frame("PlateEditFrame"), width=18) \
            .grid(row=1, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Logout", command=self.logout, width=18) \
            .grid(row=1, column=2, padx=5, pady=5)

        self.text_area = tk.Text(self, width=100, height=20)
        self.text_area.pack(pady=10)

    def load_plates(self):
        headers = {"Authorization": f"Bearer {self.controller.jwt_token}"}
        try:
            response = requests.get(f"{API_BASE_URL}/Plates", headers=headers, verify=False)
            if response.status_code == 200:
                plates = response.json()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, json.dumps(plates, indent=4))
            else:
                messagebox.showerror("Erro", f"Erro ao carregar Plates: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Erro", f"Exceção: {e}")

    def load_ocorrencias(self):
        headers = {"Authorization": f"Bearer {self.controller.jwt_token}"}
        try:
            response = requests.get(f"{API_BASE_URL}/Ocorrencias", headers=headers, verify=False)
            if response.status_code == 200:
                ocorrencias = response.json()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, json.dumps(ocorrencias, indent=4))
            else:
                messagebox.showerror("Erro", f"Erro ao carregar Ocorrências: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Erro", f"Exceção: {e}")

    def logout(self):
        self.controller.jwt_token = ""
        self.controller.user_id = None
        self.controller.show_frame("LoginFrame")


# Tela para Cadastrar Ocorrência
class OccurrenceFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='lightcyan')

        panel = tk.Frame(self, bg='white', padx=30, pady=30)
        panel.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(panel, text="Cadastrar Ocorrência", font=("Arial", 24), bg='white') \
            .grid(row=0, column=0, columnspan=2, pady=(0, 20))
        tk.Label(panel, text="Placa:", bg='white').grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.placa_entry = tk.Entry(panel, width=30)
        self.placa_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(panel, text="Descrição:", bg='white').grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.descricao_entry = tk.Entry(panel, width=30)
        self.descricao_entry.grid(row=2, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(panel, bg='white')
        btn_frame.grid(row=3, column=0, columnspan=2, pady=15)
        tk.Button(btn_frame, text="Cadastrar", command=self.do_create_occurrence, width=15) \
            .grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Voltar", command=lambda: controller.show_frame("DashboardFrame"), width=15) \
            .grid(row=0, column=1, padx=5, pady=5)

    def do_create_occurrence(self):
        placa = self.placa_entry.get()
        descricao = self.descricao_entry.get()
        usuarioId = self.controller.user_id
        token = self.controller.jwt_token
        if create_occurrence_api(placa, descricao, usuarioId, token):
            messagebox.showinfo("Sucesso", "Ocorrência cadastrada com sucesso!")
            self.controller.show_frame("DashboardFrame")
        else:
            messagebox.showerror("Erro", "Falha ao cadastrar ocorrência.")


# Tela para Alterar/Excluir Ocorrência
class OccurrenceEditFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='lightcyan')

        panel = tk.Frame(self, bg='white', padx=30, pady=30)
        panel.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(panel, text="Alterar/Excluir Ocorrência", font=("Arial", 24), bg='white') \
            .grid(row=0, column=0, columnspan=2, pady=(0, 20))
        tk.Label(panel, text="ID:", bg='white').grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.id_entry = tk.Entry(panel, width=30)
        self.id_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(panel, text="Placa:", bg='white').grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.placa_entry = tk.Entry(panel, width=30)
        self.placa_entry.grid(row=2, column=1, padx=5, pady=5)
        tk.Label(panel, text="Descrição:", bg='white').grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.descricao_entry = tk.Entry(panel, width=30)
        self.descricao_entry.grid(row=3, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(panel, bg='white')
        btn_frame.grid(row=4, column=0, columnspan=2, pady=15)
        tk.Button(btn_frame, text="Atualizar", command=self.do_update_occurrence, width=15) \
            .grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Excluir", command=self.do_delete_occurrence, width=15) \
            .grid(row=0, column=1, padx=5, pady=5)
        tk.Button(panel, text="Voltar", command=lambda: controller.show_frame("DashboardFrame"), width=15) \
            .grid(row=5, column=0, columnspan=2, pady=5)

    def do_update_occurrence(self):
        try:
            occurrence_id = int(self.id_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "ID deve ser numérico")
            return
        placa = self.placa_entry.get()
        descricao = self.descricao_entry.get()
        usuarioId = self.controller.user_id
        token = self.controller.jwt_token
        if update_occurrence_api(occurrence_id, placa, descricao, usuarioId, token):
            messagebox.showinfo("Sucesso", "Ocorrência atualizada com sucesso!")
            self.controller.show_frame("DashboardFrame")
        else:
            messagebox.showerror("Erro", "Falha ao atualizar ocorrência.")

    def do_delete_occurrence(self):
        try:
            occurrence_id = int(self.id_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "ID deve ser numérico")
            return
        token = self.controller.jwt_token
        if delete_occurrence_api(occurrence_id, token):
            messagebox.showinfo("Sucesso", "Ocorrência excluída com sucesso!")
            self.controller.show_frame("DashboardFrame")
        else:
            messagebox.showerror("Erro", "Falha ao excluir ocorrência.")


# Tela para Alterar/Excluir Plate
class PlateEditFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='lightgrey')

        panel = tk.Frame(self, bg='white', padx=30, pady=30)
        panel.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(panel, text="Alterar/Excluir Plate", font=("Arial", 24), bg='white') \
            .grid(row=0, column=0, columnspan=2, pady=(0, 20))
        tk.Label(panel, text="ID:", bg='white').grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.id_entry = tk.Entry(panel, width=30)
        self.id_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(panel, text="Placa:", bg='white').grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.placa_entry = tk.Entry(panel, width=30)
        self.placa_entry.grid(row=2, column=1, padx=5, pady=5)
        tk.Label(panel, text="Local:", bg='white').grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.local_entry = tk.Entry(panel, width=30)
        self.local_entry.grid(row=3, column=1, padx=5, pady=5)
        tk.Label(panel, text="Horário (ISO):", bg='white').grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.horario_entry = tk.Entry(panel, width=30)
        self.horario_entry.grid(row=4, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(panel, bg='white')
        btn_frame.grid(row=5, column=0, columnspan=2, pady=15)
        tk.Button(btn_frame, text="Atualizar", command=self.do_update_plate, width=15) \
            .grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Excluir", command=self.do_delete_plate, width=15) \
            .grid(row=0, column=1, padx=5, pady=5)
        tk.Button(panel, text="Voltar", command=lambda: controller.show_frame("DashboardFrame"), width=15) \
            .grid(row=6, column=0, columnspan=2, pady=5)

    def do_update_plate(self):
        try:
            plate_id = int(self.id_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "ID deve ser numérico")
            return
        placa = self.placa_entry.get()
        local = self.local_entry.get()
        horario = self.horario_entry.get()
        usuarioId = self.controller.user_id
        token = self.controller.jwt_token
        if update_plate_api(plate_id, placa, local, horario, usuarioId, token):
            messagebox.showinfo("Sucesso", "Plate atualizada com sucesso!")
            self.controller.show_frame("DashboardFrame")
        else:
            messagebox.showerror("Erro", "Falha ao atualizar plate.")

    def do_delete_plate(self):
        try:
            plate_id = int(self.id_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "ID deve ser numérico")
            return
        token = self.controller.jwt_token
        if delete_plate_api(plate_id, token):
            messagebox.showinfo("Sucesso", "Plate excluída com sucesso!")
            self.controller.show_frame("DashboardFrame")
        else:
            messagebox.showerror("Erro", "Falha ao excluir plate.")


# Execução da aplicação
if __name__ == "__main__":
    app = App()
    app.mainloop()
