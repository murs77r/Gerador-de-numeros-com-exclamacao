import tkinter as tk
from tkinter import ttk, messagebox
from num2words import num2words
import pyautogui
import time
import threading
import queue
import keyboard
import pyperclip
import requests
from PIL import Image
from io import BytesIO
import os
import tempfile

comando_queue = queue.Queue()

script_interrompido = False
thread_insercao = None

def baixar_e_converter_icone(url, pasta_temp):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        imagem = Image.open(BytesIO(response.content))
        icone_path = os.path.join(pasta_temp, "script.ico")
        imagem.save(icone_path, format="ICO")
        return icone_path
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar a imagem: {e}")
        return None
    except Exception as e:
        print(f"Erro ao converter ou salvar a imagem: {e}")
        return None

def inserir_texto(numero_inicial, numero_final, tempo_espera):
    global script_interrompido, thread_insercao
    try:
        numero_inicial = int(numero_inicial)
        numero_final = int(numero_final)
        tempo_espera = float(tempo_espera)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira números válidos.")
        resetar_interface(iniciar=True)
        return

    if numero_inicial > numero_final:
        messagebox.showerror("Erro", "O número inicial deve ser menor que o número final.")
        resetar_interface(iniciar=True)
        return

    script_interrompido = False

    resposta = messagebox.askyesno("Aviso", "O script irá iniciar a inserção de números.\n\n"
                                      "Você pode interromper a qualquer momento pressionando CTRL + C (globalmente) ou clicando no botão PARAR que aparecerá na janela.\n\n"
                                      "Clique em 'Sim' para continuar ou 'Não' para cancelar.")
    if not resposta:
        resetar_interface(iniciar=True)
        return

    janela_contagem = tk.Toplevel(janela)
    janela_contagem.title("Contagem Regressiva")
    janela_contagem.configure(bg='black')
    janela_contagem.resizable(False, False)

    largura_janela_contagem = 300
    altura_janela_contagem = 150
    largura_tela = janela_contagem.winfo_screenwidth()
    altura_tela = janela_contagem.winfo_screenheight()
    x_c = (largura_tela / 2) - (largura_janela_contagem / 2)
    y_c = (altura_tela / 2) - (altura_janela_contagem / 2)
    janela_contagem.geometry(f"{largura_janela_contagem}x{altura_janela_contagem}+{int(x_c)}+{int(y_c)}")

    label_contagem = tk.Label(janela_contagem, text="", font=("Nunito", 48, "bold"), bg='black', fg='white')
    label_contagem.pack(expand=True)

    for i in range(10, 0, -1):
        label_contagem.config(text=f"{i}")
        janela_contagem.update()
        time.sleep(1)

    janela_contagem.destroy()

    def executar_insercao():
        global script_interrompido
        for numero in range(numero_inicial, numero_final + 1):
            if not comando_queue.empty():
                comando = comando_queue.get()
                if comando == "parar":
                    script_interrompido = True
                    break

            if script_interrompido:
                break

            numero_extenso = num2words(numero, lang="pt_BR").upper().replace(",", "")
            numero_extenso = numero_extenso.replace("TRS", "TRÊS")

            pyperclip.copy(numero_extenso)
            pyautogui.hotkey("ctrl", "v")
            pyautogui.press('enter')

            tempo_decorrido = 0
            while tempo_decorrido < tempo_espera:
                if not comando_queue.empty():
                    comando = comando_queue.get()
                    if comando == "parar":
                        script_interrompido = True
                        break
                time.sleep(0.05)
                tempo_decorrido += 0.05

            if script_interrompido:
                break

        if not script_interrompido:
            janela.after(0, messagebox.showinfo, "Sucesso", "Números inseridos com sucesso!")

        janela.after(0, resetar_interface)

    thread_insercao = threading.Thread(target=executar_insercao)
    thread_insercao.start()

    botao_gerar.config(state="disabled")
    botao_parar.grid(row=6, column=0, columnspan=2, pady=(0, 10))

def validar_entrada(texto):
    if texto == "":
        return True
    try:
        float(texto)
        return True
    except ValueError:
        return False

def interromper_script():
    comando_queue.put("parar")

def atalho_global():
    global script_interrompido
    if thread_insercao and thread_insercao.is_alive():
      script_interrompido = True
      comando_queue.put("parar")

def resetar_interface(iniciar=False):
    global script_interrompido, thread_insercao

    script_interrompido = False
    thread_insercao = None
    while not comando_queue.empty():
      comando_queue.get()

    botao_gerar.config(state="normal")
    botao_parar.grid_forget()

    if not iniciar:
        messagebox.showinfo("Interrompido", "Script interrompido pelo usuário.")

def criar_interface():
    global janela, botao_gerar, botao_parar

    pasta_temp = tempfile.gettempdir()
    icone_url = "https://i.ibb.co/rfKy802/script.png"
    icone_path = baixar_e_converter_icone(icone_url, pasta_temp)

    janela = tk.Tk()
    janela.title("Gerador de Números por Extenso")
    janela.configure(bg='white')
    janela.resizable(False, False)
    if icone_path:
        janela.wm_iconbitmap(icone_path)
    else:
        messagebox.showerror("Erro", "Falha ao baixar ou converter o ícone. O ícone padrão será usado.")

    keyboard.add_hotkey('ctrl+c', atalho_global)

    style = ttk.Style(janela)
    style.theme_use('clam')

    style.configure('.', font=('Nunito', 10), background='white', foreground='black')
    style.configure('TLabel', font=('Nunito', 10), background='white', foreground='black')

    style.configure('Rounded.TButton', font=('Nunito', 10), background='white', foreground='black', borderwidth=0, relief="flat", padding=5)
    style.map('Rounded.TButton',
        foreground=[('pressed', 'black'), ('active', 'black')],
        background=[('pressed', '#dbdbdb'), ('active', '#ebebeb')]
    )

    style.configure('Rounded.TEntry', font=('Nunito', 10), fieldbackground='white', foreground='black', borderwidth=0, relief="flat", padding=5)

    frame_principal = ttk.Frame(janela, padding="20")
    frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(frame_principal, text="Gerador de Números por Extenso", font=("Nunito", 14), background='white', foreground='black').grid(row=0, column=0, columnspan=2, pady=10)

    validacao = janela.register(validar_entrada)

    ttk.Label(frame_principal, text="Número Inicial:", background='white', foreground='black').grid(row=1, column=0, sticky=tk.W, pady=5, padx=(0, 10))
    entrada_inicial = ttk.Entry(frame_principal, validate="key", validatecommand=(validacao, '%P'), style="Rounded.TEntry")
    entrada_inicial.insert(0, "1")
    entrada_inicial.grid(row=1, column=1, pady=5, padx=(10, 0), sticky=tk.EW)

    ttk.Label(frame_principal, text="Número Final:", background='white', foreground='black').grid(row=2, column=0, sticky=tk.W, pady=5, padx=(0, 10))
    entrada_final = ttk.Entry(frame_principal, validate="key", validatecommand=(validacao, '%P'), style="Rounded.TEntry")
    entrada_final.insert(0, "100")
    entrada_final.grid(row=2, column=1, pady=5, padx=(10, 0), sticky=tk.EW)

    ttk.Label(frame_principal, text="Tempo entre envios (segundos):", background='white', foreground='black').grid(row=3, column=0, sticky=tk.W, pady=5, padx=(0, 10))
    entrada_tempo = ttk.Entry(frame_principal, validate="key", validatecommand=(validacao, '%P'), style="Rounded.TEntry")
    entrada_tempo.insert(0, "4")
    entrada_tempo.grid(row=3, column=1, pady=5, padx=(10, 0), sticky=tk.EW)

    botao_gerar = ttk.Button(frame_principal, text="INSERIR NÚMEROS", command=lambda: inserir_texto(entrada_inicial.get(), entrada_final.get(), entrada_tempo.get()), style="Rounded.TButton")
    botao_gerar.grid(row=4, column=0, columnspan=2, pady=20)

    botao_parar = ttk.Button(frame_principal, text="PARAR", command=interromper_script, style="Rounded.TButton")

    janela.columnconfigure(0, weight=1)
    janela.rowconfigure(0, weight=1)
    frame_principal.columnconfigure(1, weight=1)

    janela.mainloop()

    keyboard.remove_hotkey('ctrl+c')

if __name__ == "__main__":
    criar_interface()