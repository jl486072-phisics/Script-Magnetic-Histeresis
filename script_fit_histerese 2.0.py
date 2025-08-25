import numpy as np
import matplotlib.pyplot as plt
import re
import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# Variáveis globais
campos, momentos, emu_g, emu_g2, reta, reta_centro, histerese = [], [], [], [], [], [], []
tipo, caminho_arquivo = False, ''

# Função para abrir e ler o arquivo
def ler_arquivo():
    global caminho_arquivo, campos, momentos
    caminho_arquivo = filedialog.askopenfilename(title="Selecione o arquivo de dados")
    if not caminho_arquivo:
        messagebox.showerror("Erro", "Nenhum arquivo selecionado.")
        return
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8-sig') as arquivo:
            conteudo = arquivo.read()
            em_dados = False
            for linha in conteudo.splitlines():
                linha = linha.strip()
                if linha.startswith('***DATA***'):
                    em_dados = True
                    continue
                if em_dados and re.match(r'^[\d\.\-]+[\s\t]+[\d\.\-]+$', linha):
                    partes = linha.split()
                    if len(partes) == 2:
                        campo = float(partes[0])
                        momento = float(partes[1])
                        campos.append(campo)
                        momentos.append(momento)
        messagebox.showinfo("Sucesso", "Arquivo lido com sucesso.")
    except FileNotFoundError:
        messagebox.showerror("Erro", f"O arquivo {caminho_arquivo} não foi encontrado.")
    except IOError:
        messagebox.showerror("Erro", f"Erro ao ler o arquivo {caminho_arquivo}.")

# Função para normalizar pela massa
def normalizar_massa():
    global tipo, emu_g
    resposta = messagebox.askyesno("Normalização", "Gostaria de normalizar a curva pela massa?")
    if resposta:
        gramas = simpledialog.askfloat("Entrada", "Informe o peso da amostra em gramas:")
        emu_g = [m / gramas for m in momentos]
        tipo = True
    else:
        emu_g = momentos
    centralizar_curva()

# Centraliza a curva na origem
def centralizar_curva():
    global emu_g2
    emu_g2 = [val - ((max(emu_g) + min(emu_g)) / 2) for val in emu_g]
    plotar_curva()

# Função para plotar a curva de histerese inicial
def plotar_curva():
    plt.plot(campos, emu_g2, '.')
    plt.axhline(0, color='black', linewidth=1)
    plt.axvline(0, color='black', linewidth=1)
    plt.show()
    ajuste_linear()

# Função para ajuste linear e cálculo da histerese
def ajuste_linear():
    global reta, reta_centro, histerese
    qpoint = simpledialog.askinteger("Ajuste Linear", "Escolha quantos pontos usar para o ajuste:")
    if not qpoint:
        return
    tipo_ponto = messagebox.askquestion("Seleção de Pontos", "Você quer pontos positivos?") == 'yes'
    x_primeiros = campos[:qpoint] if tipo_ponto else campos[-qpoint:]
    y_primeiros = emu_g2[:qpoint] if tipo_ponto else emu_g2[-qpoint:]
    
    coef_m, coef_b = np.polyfit(x_primeiros, y_primeiros, 1)
    reta = [coef_m * i + coef_b for i in campos]
    reta_centro = [n - ((max(reta) + min(reta)) / 2) for n in reta]
    histerese = [item1 - item2 for item1, item2 in zip(emu_g2, reta_centro)]
    plotar_ajustes()

# Função para plotar as três curvas
def plotar_ajustes():
    unit = ' (emu/g)' if tipo else ' (emu)'
    fig, ax = plt.subplots()
    ax.plot(campos, emu_g2, '.', color='r', label='Curva de Histerese')
    ax.plot(campos, reta_centro, '-', color='g', label='Antiferromagnetismo (Ajuste linear)')
    ax.plot(campos, histerese, '.', color='b', label='Contribuição Ferromagnética')
    ax.legend(fontsize=8, frameon=False)
    ax.set_xlabel('Campo (Oe)')
    ax.set_ylabel('Magnetização' + unit)
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    if messagebox.askyesno("Zoom Inset", "Gostaria de ampliar a origem do gráfico (zoom inset)?"):
        limitmax_x = simpledialog.askfloat("Zoom", "Informe o valor da largura do intervalo em x:")
        limitmax_y = simpledialog.askfloat("Zoom", "Informe o valor da largura do intervalo em y:")
        ax2 = ax.inset_axes([0.68, 0.08, 0.3, 0.3])
        ax2.plot(campos, histerese, '-', color='b', linewidth=2)
        ax2.set_xlim(-limitmax_x / 2, limitmax_x / 2)
        ax2.set_ylim(-limitmax_y / 2, limitmax_y / 2)
        ax2.axhline(0, color='black', linewidth=1)
        ax2.axvline(0, color='black', linewidth=1)
    plt.show()
    exportar_grafico(fig)

# Função para exportar o gráfico
def exportar_grafico(fig):
    if messagebox.askyesno("Exportar Gráfico", "Gostaria de exportar o gráfico das curvas?"):
        nome_grafico = simpledialog.askstring("Nome do Arquivo", "Insira o nome do gráfico a ser exportado:")
        if nome_grafico:
            caminho_exportacao = os.path.join(os.path.dirname(caminho_arquivo), nome_grafico + '.png')
            fig.savefig(caminho_exportacao, dpi=300, bbox_inches='tight')
            messagebox.showinfo("Exportação Completa", f"Gráfico exportado com sucesso para {caminho_exportacao}")
    exportar_dados()

# Função para exportar os dados
def exportar_dados():
    if messagebox.askyesno("Exportar Dados", "Gostaria de exportar os dados das curvas?"):
        nome_arquivo = simpledialog.askstring("Nome do Arquivo", "Insira o nome do arquivo a ser exportado:")
        if nome_arquivo:
            caminho_dados = os.path.join(os.path.dirname(caminho_arquivo), nome_arquivo + '.txt')
            os.makedirs(os.path.dirname(caminho_dados), exist_ok=True)
            with open(caminho_dados, 'w') as file:
                file.write("Magnetic Field\tHysteresis\tLinear Fit\tMagnetic Contribution\n")
                for i in range(len(campos)):
                    file.write(f"{campos[i]}\t{emu_g2[i]}\t{reta_centro[i]}\t{histerese[i]}\n")
            messagebox.showinfo("Exportação Completa", f"Dados exportados com sucesso para {caminho_dados}")

# Interface Tkinter
root = tk.Tk()
root.title("Análise de Curvas de Histerese")
root.geometry("300x200")

btn_ler_arquivo = tk.Button(root, text="Ler Arquivo", command=ler_arquivo)
btn_ler_arquivo.pack(pady=10)
btn_normalizar_massa = tk.Button(root, text="Iniciar Ajuste", command=normalizar_massa)
btn_normalizar_massa.pack(pady=10)
#btn_sair = tk.Button(root, text="Sair", command=root.quit)
#btn_sair.pack(pady=10)

root.mainloop()
