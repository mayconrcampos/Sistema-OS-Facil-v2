from tkinter import *
from tkinter import ttk
from datetime import date
from tkinter import messagebox
import sqlite3
import base64
import webbrowser
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image

root = Tk()

class Funcoes:
    def imagens64(self):
        self.imagem_nova_base64 = "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"

    def conecta_db_clientes(self):
        self.conn = sqlite3.connect("Clientes.db")
        self.cursor = self.conn.cursor()
    
    def conecta_db_produtos(self):
        self.db = sqlite3.connect("Produtos.db")
        self.cursor = self.db.cursor()
    
    def desconecta_db_clientes(self):
        self.conn.close()
    
    def desconecta_db_produtos(self):
        self.db.close()
    
    def criar_db_Clientes(self):
        self.conecta_db_clientes()
        # Criando a tabela ordens
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ordens (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                data TEXT,
                nome TEXT CHAR(40) NOT NULL,
                os TEXT NOT NULL,
                total REAL(6) NOT NULL,
                entrada REAL(6),
                status INTEGER NOT NULL
                    );
                """)
        self.conn.commit()
        self.desconecta_db_clientes()
    
    def criar_db_Produtos(self):
        self.conecta_db_produtos()
        # Criando a tabela Produtos
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                os TEXT,
                valor_uni REAL(6) NOT NULL,
                descricao TEXT NOT NULL,
                qtde INTEGER(6) NOT NULL,
                subtotal REAL(6),
                status INTEGER NOT NULL
                    );
                """)
        self.db.commit()
        self.desconecta_db_produtos()

    def variaveis_os_aba01(self):
        self.nome = self.entry_nome_aba01.get()
        self.os = self.entry_os_aba01.get()
        self.entrada = self.entry_entrada_vlr_aba01.get()
        if self.nome and self.os and self.entrada:
            self.nome = self.entry_nome_aba01.get()
            self.os = self.entry_os_aba01.get()
            self.entrada = float(self.entry_entrada_vlr_aba01.get())
        
    
    def variaveis_produtos(self):
        self.os = self.entry_os_aba02.get()
        self.vlr_uni = self.entry_preco_uni_aba02.get()
        self.descricao = self.entry_descricao_aba02.get()
        self.qtde = self.entry_qtde_aba02.get()
        if self.os and self.vlr_uni and self.descricao and self.qtde:
            self.os = self.entry_os_aba02.get()
            self.vlr_uni = float(self.entry_preco_uni_aba02.get())
            self.descricao = self.entry_descricao_aba02.get()
            self.qtde = int(self.entry_qtde_aba02.get())
            self.sub_total = float(self.soma_sub_total_aba02())
            self.status = 1

    def cria_OS_e_Add_Produtos(self):
        self.variaveis_produtos()
        if self.os and self.vlr_uni and self.descricao and self.qtde:
            self.conecta_db_produtos()
            self.cursor.execute("""INSERT INTO produtos 
                (os, valor_uni, descricao, qtde, subtotal, status)
                VALUES (?,?,?,?,?,?)""",(self.os, float(self.vlr_uni), self.descricao, int(self.qtde), float(self.sub_total), self.status))

            self.db.commit()
            self.desconecta_db_produtos()

            self.insere_Produtos_na_lista()
            self.insere_OS_no_db()
            self.limpar_casas_produtos()
        else:
            messagebox.showerror("Erro!", "Você precisa preencher todas as casas antes de Adicionar")

    def insere_OS_no_db(self):
        self.variaveis_produtos()
        self.conecta_db_produtos()
        lista = self.cursor.execute(""" SELECT os, valor_uni, descricao, qtde, subtotal, status FROM produtos
                    ORDER BY os ASC; """)

        total = 0
        for i in lista:
            if self.os == i[0]:
                total += i[4]
                self.status = i[5]

        self.desconecta_db_produtos()

        self.data = self.data_formatada()
        self.nome = self.entry_nome_aba02.get()
        self.os = self.entry_os_aba02.get()
        self.entrada = 0
        self.status = 1

        # Verificando a existência da OS na lista
        conta = 0
        self.conecta_db_clientes()
        lista = self.cursor.execute(""" SELECT id, data, nome, os, total, entrada FROM ordens
                    ORDER BY os ASC; """)
       
        for i in lista:
            #print(i)
            if i[3] == self.os:
                conta += 1
        
        #print(self.os)
        if conta == 0:
            self.conecta_db_clientes()
            self.cursor.execute("""INSERT INTO ordens 
                (data, nome, os, total, entrada, status)
                VALUES (?,?,?,?,?,?)""",(self.data, self.nome, self.os, total, self.entrada, self.status))
            self.conn.commit()

            self.limpar_casas_produtos()
            self.insere_Produtos_na_lista()
            self.insere_OS_na_lista()
            self.desconecta_db_clientes()
            self.totais_vlr_os()
        else:
            self.conecta_db_clientes()
            self.cursor.execute("""UPDATE ordens SET total=?
                            WHERE os=?""",(total, self.os))
            self.conn.commit()
            self.limpar_casas_produtos()
            self.insere_Produtos_na_lista()
            self.insere_OS_na_lista()
            self.desconecta_db_clientes()


    def insere_OS_na_lista(self):
        self.treeview_aba01.delete(*self.treeview_aba01.get_children())
        self.conecta_db_clientes()
        lista = self.cursor.execute(""" SELECT id, data, nome, os, total, entrada, status FROM ordens
                    ORDER BY os ASC; """)
        for i in lista:
            if i[6]:
                self.treeview_aba01.insert("", END, values=i)

        self.desconecta_db_clientes()
        self.totais_vlr_os()

    def insere_Produtos_na_lista(self):
        self.os = self.entry_os_aba02.get()
        self.treeview_aba02.delete(*self.treeview_aba02.get_children())
        self.conecta_db_produtos()
        lista = self.cursor.execute(""" SELECT id, os, valor_uni, descricao, qtde, subtotal, status FROM produtos
                    ORDER BY os ASC; """)
        for i in lista:
            if i[1] == self.os and i[6] == 1:
                self.treeview_aba02.insert("", END, values=i)
        self.desconecta_db_produtos()
        self.totais_vlr_os()
        self.totais_produtos()
        self.entry_nome_aba01.focus()
    
    def totais_vlr_os(self):
        self.conecta_db_clientes()
        lista = self.cursor.execute(""" SELECT id, data, nome, os, total, entrada, status FROM ordens
                    ORDER BY os ASC; """)
        entrada = 0
        total = 0
        for i in lista:
            if i[6] == 1:
                total += i[4]
                entrada += i[5]

        self.desconecta_db_clientes()
        aberto = total - entrada
        self.lb_pendentevlr_aba01["text"] = f"{aberto:6.2f}"
        self.lb_pagovlr_aba01["text"] = f"{entrada:6.2f}"
        self.lb_totvalor_aba01["text"] = f"{total:6.2f}"
        
    
    def totais_produtos(self):
        self.os = self.entry_os_aba02.get()

        self.conecta_db_clientes()
        lista = self.cursor.execute(""" SELECT id, data, nome, os, total, entrada, status FROM ordens
                    ORDER BY os ASC; """)
        entrada = 0
        for i in lista:
            if i[5] and i[3] == self.os and i[6] == 1:
                entrada += i[5]

        self.desconecta_db_clientes()

        self.conecta_db_produtos()
        lista = self.cursor.execute(""" SELECT id, os, valor_uni, descricao, qtde, subtotal, status FROM produtos
                    ORDER BY os ASC; """)
    
        total = 0
        pendente = 0
        for i in lista:
            if i[1] == self.os and i[6] == 1:
                total += i[5]
        
        pendente = total - entrada
        #print(pendente, total, entrada)
        self.lb_pagovlr_aba02["text"] = f"{entrada:6.2f}"
        self.lb_pendentevlr_aba02["text"] = f"{pendente:6.2f}"
        self.lb_totvalor_aba02["text"] = f"{total:6.2f}"
        self.desconecta_db_produtos()
    
    def clique_duplo_produtos(self, event):
        self.limpar_casas_produtos()
        self.treeview_aba02.selection()

        for n in self.treeview_aba02.selection():
            col1, col2, col3, col4, col5, col6, col7 = self.treeview_aba02.item(n, "values")
            self.entry_id_produto_aba02.insert(END, col1)
            self.entry_preco_uni_aba02.insert(END, col3)
            self.entry_descricao_aba02.insert(END, col4)
            self.entry_qtde_aba02 .insert(END, col5)
            

    
    def clique_duplo_OS(self, event):
        self.limpar_casas_OS()
        self.treeview_aba01.selection()

        for n in self.treeview_aba01.selection():
            col1, col2, col3, col4, col5, col6, col7 = self.treeview_aba01.item(n, "values")
            self.entry_nome_aba01.insert(END, col3)
            self.entry_os_aba01.insert(END, col4)
            self.entry_entrada_vlr_aba01.insert(END, col6)

    def data_formatada(self):
        dt = date.today()
        data_form = dt.strftime("%d/%m/%Y")
        return data_form
    
    def soma_sub_total_aba02(self):
        vlr_uni = self.entry_preco_uni_aba02.get()
        qtde = self.entry_qtde_aba02.get()
        if vlr_uni and qtde:
            vlr_uni = float(vlr_uni)
            qtde = int(qtde)
            return vlr_uni * qtde
        else:
            messagebox.showerror("ERRO!", "Preencher todas as casas.")
    
    def limpar_casas_produtos(self):
        self.entry_preco_uni_aba02.delete(0, END)
        self.entry_descricao_aba02.delete(0, END)
        self.entry_qtde_aba02.delete(0, END)
        self.entry_id_produto_aba02.delete(0, END)
    
    def botao_limpar(self):
        self.entry_preco_uni_aba02.delete(0, END)
        self.entry_descricao_aba02.delete(0, END)
        self.entry_qtde_aba02.delete(0, END)
        self.entry_id_produto_aba02.delete(0, END)
        self.entry_nome_aba02.delete(0, END)
        self.entry_os_aba02.delete(0, END)

    def limpar_casas_OS(self):
        self.entry_nome_aba01.delete(0, END)
        self.entry_os_aba01.delete(0, END)
        self.entry_entrada_vlr_aba01.delete(0, END)
    
    def define_entrada(self):
        self.variaveis_os_aba01()
        self.conecta_db_clientes()
        lista = self.cursor.execute(""" SELECT id, data, nome, os, total, entrada, status FROM ordens
                    ORDER BY os ASC; """)
        total = 0
        for i in lista:
            if i[5] and i[3] == self.os and i[6] == 1:
                total += i[4]
        print(total)
        self.desconecta_db_clientes()
        # Definir uma condicional pra extinguir OS caso
        # O valor seja de entrada seja igual ao valor da OS.
        self.conecta_db_clientes()
        self.cursor.execute("""UPDATE ordens SET entrada=?
                                WHERE os=?""",(self.entrada, self.os))
        self.conn.commit()
        self.desconecta_db_clientes()
            
        self.insere_OS_na_lista()
        self.insere_Produtos_na_lista()
        self.limpar_casas_OS()
        


    def visualizar_produtos(self):
        self.os = self.entry_os_aba01.get()
        if self.os:
            self.treeview_aba01.selection()

            self.entry_nome_aba02.delete(0, END)
            self.entry_os_aba02.delete(0, END)
            for n in self.treeview_aba01.selection():
                col1, col2, col3, col4, col5, col6, col7 = self.treeview_aba01.item(n, "values")
                self.entry_nome_aba02.insert(END, col3)
                self.entry_os_aba02.insert(END, col4)

            self.treeview_aba02.delete(*self.treeview_aba02.get_children())
            self.conecta_db_produtos()
            lista = self.cursor.execute(""" SELECT id, os, valor_uni, descricao, qtde, subtotal, status FROM produtos
                        ORDER BY os ASC; """)
            for i in lista:
                if i[1] == self.os and i[6] == 1:
                    self.treeview_aba02.insert("", END, values=i)
            self.desconecta_db_produtos()
            self.totais_produtos()
            self.entry_preco_uni_aba02.focus()
            
        else:
            messagebox.showerror("ERRO!", "Você precisa inserir a OS para ver os produtos!")
    
    def alterar_produto(self):
        self.variaveis_produtos()
        if self.entry_os_aba02.get() and self.vlr_uni and self.descricao and self.qtde:
            subtotal = self.soma_sub_total_aba02()
            ide = self.entry_id_produto_aba02.get()
            #print(ide)
            self.conecta_db_produtos()

            self.cursor.execute(""" UPDATE produtos SET valor_uni=?, descricao=?, qtde=?, subtotal=?
                            WHERE id=?""",(self.vlr_uni, self.descricao, self.qtde, subtotal, int(ide)))
            self.db.commit()
            self.desconecta_db_produtos()

            self.conecta_db_produtos()
            lista = self.cursor.execute(""" SELECT id, os, valor_uni, descricao, qtde, subtotal FROM produtos
                    ORDER BY os ASC; """)
    
            total = 0
            pendente = 0
            for i in lista:
                if i[1] == self.os:
                    total += i[5]
            self.desconecta_db_produtos()

            self.conecta_db_clientes()
            self.cursor.execute("""UPDATE ordens SET total=?
                            WHERE os=?""",(total, self.os))
            self.conn.commit()
            self.desconecta_db_clientes()

            self.insere_Produtos_na_lista()
            self.totais_produtos()
            self.totais_vlr_os()
            self.insere_OS_na_lista()
            self.limpar_casas_produtos()
        else:
            messagebox.showerror("ERRO!", "É necessário preencher todas as casas antes de alterar.")


    def deletar_produto(self):
        self.variaveis_produtos()
        if self.entry_os_aba02.get() and self.vlr_uni and self.descricao and self.qtde:
            ide = self.entry_id_produto_aba02.get()
            self.conecta_db_produtos()

            self.cursor.execute("""DELETE FROM produtos WHERE id = ? """, (ide,))
            self.db.commit()
            self.desconecta_db_produtos()

            # Aqui vai ter que abrir o banco de dados produtos, pegar total e passar para o total do db das OS.
            self.conecta_db_produtos()
            lista = self.cursor.execute(""" SELECT id, os, valor_uni, descricao, qtde, subtotal FROM produtos
                    ORDER BY os ASC; """)
    
            total = 0
            pendente = 0
            for i in lista:
                if i[1] == self.os:
                    total += i[5]
            self.desconecta_db_produtos()

            # Inserir total na no db OS
            self.conecta_db_clientes()
            self.cursor.execute("""UPDATE ordens SET total=?
                            WHERE os=?""",(total, self.os))
            self.conn.commit()

            # Atualizar listas com novos valores
            self.insere_Produtos_na_lista()
            self.totais_produtos()
            self.totais_vlr_os()
            self.insere_OS_na_lista()
            self.limpar_casas_produtos()
    
    def dar_baixa_os(self):
        resp = messagebox.askyesno("Confirmação?", "Deseja mesmo dar baixa?")
        if resp:
            self.variaveis_os_aba01()
            if self.os:
                self.status = 0
                # Update no valor status em produtos
                self.conecta_db_produtos()
                self.cursor.execute(""" UPDATE produtos SET status=?
                                WHERE os=?""",(self.status, self.os))
                self.db.commit()
                self.desconecta_db_produtos()

                # Pegar o valor total dessa OS para fazer a Quitação

                self.conecta_db_clientes()
                lista = self.cursor.execute(""" SELECT id, data, nome, os, total, entrada, status FROM ordens
                        ORDER BY os ASC; """)
                total = 0
                for i in lista:
                    if i[5] and i[3] == self.os and i[6] == 1:
                        total = i[4]

                self.desconecta_db_clientes()


                # Update no valor status em produtos
                self.entrada = total
                self.conecta_db_clientes()
                self.cursor.execute("""UPDATE ordens SET entrada=?, status=?
                                WHERE os=?""",(self.entrada, self.status, self.os))
                self.conn.commit()
                self.desconecta_db_clientes()
                self.insere_Produtos_na_lista()
                self.totais_produtos()
                self.totais_vlr_os()
                self.insere_OS_na_lista()
                self.historico_de_os()
                self.limpar_casas_produtos()
                self.limpar_casas_OS()
            else:
                messagebox.showerror("Erro!", "É necessário selecionar uma OS para dar baixa.")
    
    def historico_de_os(self):
        self.treeview_aba03.delete(*self.treeview_aba03.get_children())
        self.conecta_db_clientes()
        lista = self.cursor.execute(""" SELECT id, data, nome, os, total, entrada, status FROM ordens
                    ORDER BY os ASC; """)
        for i in lista:
            if i[6] == 0:
                self.treeview_aba03.insert("", END, values=i)

        self.desconecta_db_clientes()
        self.totais_vlr_os()

    
    def visualizar_produtos_historico(self):
        self.os = self.entry_os_aba03.get()
        self.nome = self.entry_nome_aba03.get()
        if self.os:
            self.treeview_aba033.delete(*self.treeview_aba033.get_children())
            self.conecta_db_produtos()
            lista = self.cursor.execute(""" SELECT id, os, valor_uni, descricao, qtde, subtotal, status FROM produtos
                        ORDER BY os ASC; """)
            for i in lista:
                if i[1] == self.os and i[6] == 0:
                    self.treeview_aba033.insert("", END, values=i)
            self.desconecta_db_produtos()
            self.totais_produtos_historico()
            self.entry_os_aba03.focus()
            
        else:
            messagebox.showerror("ERRO!", "Você precisa inserir a OS para ver os produtos!")
    
    def clique_duplo_histórico(self, event):
        self.limpar_casas_historico()
        self.treeview_aba03.selection()
        for n in self.treeview_aba03.selection():
            col1, col2, col3, col4, col5, col6, col7 = self.treeview_aba03.item(n, "values")
            self.entry_nome_aba03.insert(END, col3)
            self.entry_os_aba03.insert(END, col4)
    
    def limpar_casas_historico(self):
        self.entry_nome_aba03.delete(0, END)
        self.entry_os_aba03.delete(0, END)
    
    def totais_produtos_historico(self):
        self.os = self.entry_os_aba03.get()

        # Pegando valor da entrada
        self.conecta_db_clientes()
        lista = self.cursor.execute(""" SELECT id, data, nome, os, total, entrada, status FROM ordens
                    ORDER BY os ASC; """)
        entrada = 0
        for i in lista:
            if i[5] and i[3] == self.os and i[6] == 0:
                entrada += i[5]

        self.desconecta_db_clientes()

        # Pegando valor total
        self.conecta_db_produtos()
        lista = self.cursor.execute(""" SELECT id, os, valor_uni, descricao, qtde, subtotal, status FROM produtos
                    ORDER BY os ASC; """)
    
        total = 0
        pendente = 0
        for i in lista:
            if i[1] == self.os and i[6] == 0:
                total += i[5]
        
        pendente = total - entrada
        #print(pendente, total, entrada)
        self.lb_pagovlr_aba03["text"] = f"{entrada:6.2f}"
        self.lb_pendentevlr_aba03["text"] = f"{pendente:6.2f}"
        self.lb_totvalor_aba03["text"] = f"{total:6.2f}"
        self.desconecta_db_produtos()
    
    def salvar_em_PDF(self):
        self.variaveis_os_aba01()
        self.nome_pdf = f"OS_{self.os}.pdf"
        webbrowser.open(self.nome_pdf)
    
    def gerar_Ordem_de_servico(self):
        self.os = self.entry_os_aba02.get()
        self.nome = self.entry_nome_aba02.get()
        if self.os:
            # Capturar Data, nome e OS Nº
            self.conecta_db_clientes()
            lista = self.cursor.execute(""" SELECT id, data, nome, os, total, entrada, status FROM ordens
                        ORDER BY os ASC; """)
            entrada = 0
            data = ""
            for i in lista:
                if i[6] == 1 and i[3] == self.os:
                    data += i[1]
                    entrada = i[5]

            print(data, self.os, self.nome)
            self.desconecta_db_clientes()

            self.variaveis_os_aba01()
            self.nomepdf = f"OS_{self.os}.pdf"
            self.c = canvas.Canvas(self.nomepdf)

            self.c.setFont("Helvetica", 22)
            self.c.drawString(100, 800, "AM Sublimação - Ordem de Serviço")
            self.c.drawString(50, 785, "--------------------------------------------------------------")
            self.c.setFont("Helvetica", 14)
            self.c.drawString(50, 770, f"Data : {data} | Nome: {self.nome}                         | OS: {self.os}")
            self.c.setFont("Helvetica", 22)
            self.c.drawString(50, 755, "--------------------------------------------------------------")
            self.c.setFont("Helvetica", 11)
            self.c.drawString(20, 740, "Item Nº  | Preço Uni  | Qtde UNI | Subtotal    | Descrição do Produto")
            self.comprimento = 730
            self.c.drawString(20, self.comprimento, "-----------------------------------------------------------------------------------------------------------------------------------------------------")

            # Preenchendo PDF com lista de Itens
            self.conecta_db_produtos()
            lista = self.cursor.execute(""" SELECT id, os, valor_uni, descricao, qtde, subtotal, status FROM produtos
                        ORDER BY os ASC; """)
        
            total = 0
            pendente = 0
            conta_item = 0
            item = 1
            subtotal = 0
            for i in lista:
                if i[1] == self.os and i[6] == 1:
                    self.comprimento -= 13
                    subtotal += i[4] * i[2]
                    self.c.drawString(20, self.comprimento, f"Item: {item:0>2} | R$ {i[2]:0^6.2f} | Qtde: {i[4]:0>2}  | R$ {subtotal:0>7.2f} | {i[3]:<50}")
                    total += subtotal
                    subtotal = 0
                    conta_item += i[4]
                    item += 1

            
            pendente = total - self.entrada
            #print(pendente, total, entrada)

            self.comprimento -= 15
            self.c.drawString(20, self.comprimento, "---------------------------------------------------------------------------------------------------------------------------------------------------")
            self.comprimento -= 15
            self.c.drawString(20, self.comprimento, f"Total: {conta_item:0>3} Itens | Total Pedido (R$): {total:.2f} | Entrada (R$): {entrada:.2f} | Falta Pagar (R$): {pendente:.2f} ")
            self.comprimento -= 15
            self.c.drawString(20, self.comprimento, "---------------------------------------------------------------------------------------------------------------------------------------------------")
            
            self.c.showPage()
            self.c.save()

            self.salvar_em_PDF()
        else:
            messagebox.showerror("Erro!", "Você precisa selecionar uma OS.")

class Janela_Principal(Funcoes):
    def __init__(self):
        self.root = root
        self.imagens64()
        self.tela()
        self.frame_de_cima()
        self.frame_de_baixo()
        self.notebook_abas()
        self.aba_01_widgets()
        self.treeview_aba01()
        self.aba_02_widgets()
        self.treeview_aba02()
        self.aba_03_widgets()
        self.aba_04_widgets()
        # Funções externas - Criar banco de dados de OS e Produtos
        self.criar_db_Clientes()
        self.criar_db_Produtos()
        self.insere_Produtos_na_lista()
        self.insere_OS_na_lista()
        self.historico_de_os()
        
        root.mainloop()

    def tela(self):
        self.root.title("Gerenciamento de Ordens de Serviço v2.0")
        self.root.geometry("1000x600")
        self.root.configure(background="lightblue")
        self.root.minsize(width=900, height=500)
        self.root.maxsize(width=1200, height=800)
    
    def frame_de_cima(self):
        self.frame_cima = Frame(self.root, bd=7, bg="black", highlightbackground="white",
                                highlightthickness=3)
        self.frame_cima.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.20)

        self.canvas_lb = Canvas(self.frame_cima, bd=5, bg="lightgrey", highlightbackground="grey", highlightthickness=3)
        self.canvas_lb.place(relx=0.01, rely=0.05, relwidth=0.98, relheight=0.9)

        self.lb_cima = Label(self.frame_cima, text="AM Sublimação - Ordens de Serviço v2.0", bg="lightgrey", fg="black")
        self.lb_cima['font'] = "Arial", 24, "bold"
        self.lb_cima.place(relx=0.05, rely=0.3, relwidth=0.7, relheight=0.4)

        

        # Logo AM Sublimação
        imagem = PhotoImage(data=base64.b64decode(self.imagem_nova_base64))
        img = Label(self.frame_cima, image=imagem)
        imagem.zoom(12)
        imagem.subsample(12)
        img.imagem = imagem
        img.place(relx=0.80, rely=0.1, relwidth=0.09, relheight=0.8)
    
    def frame_de_baixo(self):
        self.frame_baixo = Frame(self.root, bd=7, bg="lightgrey", highlightbackground="black",
                                highlightthickness=3)
        self.frame_baixo.place(relx=0.01, rely=0.22, relwidth=0.98, relheight=0.765)
    
    def notebook_abas(self):
        self.note = ttk.Notebook(self.root)
        self.note.place(relx=0.014, rely=0.225, relwidth=0.974, relheight=0.756)

        # Aba Ordens de Serviço
        self.aba_01 = ttk.Frame(self.note)
        self.note.add(self.aba_01, text="Listar OS Cadastradas")

        # Aba Listar Produtos de OS
        self.aba_02 = ttk.Frame(self.note)
        self.note.add(self.aba_02, text="Visualizar/Cadastrar Produtos")

        # Histórico OS
        self.aba_03 = ttk.Frame(self.note)
        self.note.add(self.aba_03, text="Histórico")

        # Sobre este programa
        self.aba_04 = ttk.Frame(self.note)
        self.note.add(self.aba_04, text="Sobre")

    def aba_01_widgets(self):
        # Label e Entry nome cliente
        self.lb_nome_aba01 = Label(self.aba_01, text="Nome", bg="lightgrey", fg="black")
        self.lb_nome_aba01['font'] = "Arial", 14, "bold"
        self.lb_nome_aba01.place(relx=0.01, rely=0.03, relwidth=0.06, relheight=0.05)

        self.entry_nome_aba01 = Entry(self.aba_01, bg="lightblue", fg="black")
        self.entry_nome_aba01['font'] = "Arial", 14
        self.entry_nome_aba01.place(relx=0.08, rely=0.03, relwidth=0.52, relheight=0.07)

        # Label e Entry OS

        self.lb_OS_aba01 = Label(self.aba_01, text="OS", bg="lightgrey", fg="black")
        self.lb_OS_aba01['font'] = "Arial", 14, "bold"
        self.lb_OS_aba01.place(relx=0.613, rely=0.03, relwidth=0.03, relheight=0.05)

        self.entry_os_aba01 = Entry(self.aba_01, bg="lightblue", fg="black")
        self.entry_os_aba01['font'] = "Arial", 14
        self.entry_os_aba01.place(relx=0.65, rely=0.03, relwidth=0.1, relheight=0.07)

        # Botão Visualizar produtos de OS
        self.btn_visualizar_aba01 = Button(self.aba_01, text="Visualizar Produtos", bg="lightblue", fg="black", command=self.visualizar_produtos)
        self.btn_visualizar_aba01['font'] = "Arial", 14
        self.btn_visualizar_aba01.place(relx=0.78, rely=0.025, relwidth=0.205, relheight=0.08)

        # Label título
        self.lb_titulo_aba01 = Label(self.aba_01, text="Ordens de Serviços / Em Aberto", bg="lightgrey", fg="black")
        self.lb_titulo_aba01['font'] = "Arial", 12
        self.lb_titulo_aba01.place(relx=0.01, rely=0.13, relwidth=0.25, relheight=0.07)

        # Dar Baixa em OS
        self.btn_baixa_aba01 = Button(self.aba_01, text="Dar Baixa em OS", bg="lightblue", fg="black", command=self.dar_baixa_os)
        self.btn_baixa_aba01['font'] = "Arial", 14
        self.btn_baixa_aba01.place(relx=0.27, rely=0.122, relwidth=0.17, relheight=0.08)

        # Botão Limpa Casas
        self.btn_limpa_tela_aba01 = Button(self.aba_01, text="Limpar", bg="lightblue", fg="black", command=self.limpar_casas_OS)
        self.btn_limpa_tela_aba01['font'] = "Arial", 14, "bold"
        self.btn_limpa_tela_aba01.place(relx=0.45, rely=0.122, relwidth=0.075, relheight=0.08)


        # Label e Entry Entrada
        self.lb_entrada_aba01 = Label(self.aba_01, text="Entrada(R$)", bg="lightgrey", fg="black")
        self.lb_entrada_aba01['font'] = "Arial", 14, "bold"
        self.lb_entrada_aba01.place(relx=0.53, rely=0.14, relwidth=0.11, relheight=0.05)

        self.entry_entrada_vlr_aba01 = Entry(self.aba_01, bg="lightblue", fg="black")
        self.entry_entrada_vlr_aba01['font'] = "Arial", 14
        self.entry_entrada_vlr_aba01.place(relx=0.65, rely=0.13, relwidth=0.1, relheight=0.07)

        # Botão Definir Entrada

        self.btn_entrada_aba01 = Button(self.aba_01, text="Definir Entrada(R$)", bg="lightblue", fg="black", command=self.define_entrada)
        self.btn_entrada_aba01['font'] = "Arial", 14
        self.btn_entrada_aba01.place(relx=0.78, rely=0.122, relwidth=0.205, relheight=0.08)

        # Label rodapé Total
        self.lb_total_rodape_aba01 = Label(self.aba_01, text="Total(R$)", bg="lightgrey", fg="black")
        self.lb_total_rodape_aba01['font'] = "Arial", 16
        self.lb_total_rodape_aba01.place(relx=0.75, rely=0.925, relwidth=0.1, relheight=0.065)

        self.lb_totvalor_aba01 = Label(self.aba_01, text="", bg="white", fg="black", bd=4)
        self.lb_totvalor_aba01['font'] = "Arial", 16, "bold"
        self.lb_totvalor_aba01.place(relx=0.85, rely=0.925, relwidth=0.13, relheight=0.065)

        # Label Pago e valor pago.
        self.lb_pago_rodape_aba01 = Label(self.aba_01, text="Pago(R$)", bg="lightgrey", fg="black")
        self.lb_pago_rodape_aba01['font'] = "Arial", 16
        self.lb_pago_rodape_aba01.place(relx=0.35, rely=0.925, relwidth=0.11, relheight=0.065)

        self.lb_pagovlr_aba01 = Label(self.aba_01, text="", bg="white", fg="black", bd=4)
        self.lb_pagovlr_aba01['font'] = "Arial", 16, "bold"
        self.lb_pagovlr_aba01.place(relx=0.462, rely=0.925, relwidth=0.13, relheight=0.065)

        # Label pendente e pendente valor
        self.lb_pendente_aba01 = Label(self.aba_01, text="Pendente(R$)", bg="lightgrey", fg="black")
        self.lb_pendente_aba01['font'] = "Arial", 16
        self.lb_pendente_aba01.place(relx=0.01, rely=0.925, relwidth=0.15, relheight=0.065)

        self.lb_pendentevlr_aba01 = Label(self.aba_01, text="", bg="white", fg="black", bd=4)
        self.lb_pendentevlr_aba01['font'] = "Arial", 16, "bold"
        self.lb_pendentevlr_aba01.place(relx=0.1557, rely=0.925, relwidth=0.125, relheight=0.065)
    
    def treeview_aba01(self):
        self.treeview_aba01 = ttk.Treeview(self.aba_01, height=3, column=("col1", "col2", "col3", "col4", "col5", "col6"))
        # "ID", "Data", "nome", "OS Nº", "Valor"
        self.treeview_aba01.heading("#0", text="")
        self.treeview_aba01.heading("#1", text="ID")
        self.treeview_aba01.heading("#2", text="Data")
        self.treeview_aba01.heading("#3", text="Nome")
        self.treeview_aba01.heading("#4", text="OS Nº")
        self.treeview_aba01.heading("#5", text="Total (R$)")
        self.treeview_aba01.heading("#6", text="Entrada(R$)")

        # Definindo largura de cada coluna
        self.treeview_aba01.column("#0", width=1)
        self.treeview_aba01.column("#1", width=10)
        self.treeview_aba01.column("#2", width=15)
        self.treeview_aba01.column("#3", width=350)
        self.treeview_aba01.column("#4", width=20)
        self.treeview_aba01.column("#5", width=5)
        self.treeview_aba01.column("#6", width=5)
        self.treeview_aba01.place(relx=0.001, rely=0.22, relwidth=0.99, relheight=0.70)

        # Barra de rolagem_aba01 Treeview aba01
        self.rolagem_aba01 = Scrollbar(self.aba_01, orient="vertical", bg="lightgrey")
        self.treeview_aba01.configure(yscroll=self.rolagem_aba01.set)
        self.rolagem_aba01.place(relx=0.985, rely=0.22,relheight=0.7)

        # Binding evento duplo clique
        self.treeview_aba01.bind("<Double-1>", self.clique_duplo_OS)


    def aba_02_widgets(self):
        # Label entry OS
        self.lb_os_aba02 = Label(self.aba_02, text="OS Nº", bg="lightgrey", fg="black")
        self.lb_os_aba02['font'] = "Arial", 14, "bold"
        self.lb_os_aba02.place(relx=0.01, rely=0.03, relwidth=0.06, relheight=0.05)

        self.entry_os_aba02 = Entry(self.aba_02, bg="lightblue", fg="black")
        self.entry_os_aba02['font'] = "Arial", 14
        self.entry_os_aba02.place(relx=0.01, rely=0.08, relwidth=0.1, relheight=0.07)
        # Label entry nome
        self.lb_nome_aba02 = Label(self.aba_02, text="Nome / Cliente", bg="lightgrey", fg="black")
        self.lb_nome_aba02['font'] = "Arial", 14, "bold"
        self.lb_nome_aba02.place(relx=0.12, rely=0.03, relwidth=0.14, relheight=0.05)

        self.entry_nome_aba02 = Entry(self.aba_02, bg="lightblue", fg="black")
        self.entry_nome_aba02['font'] = "Arial", 14
        self.entry_nome_aba02.place(relx=0.12, rely=0.08, relwidth=0.7, relheight=0.07)
        # Label entry data
        self.lb_data_aba02 = Label(self.aba_02, text="Data", bg="lightgrey", fg="black")
        self.lb_data_aba02['font'] = "Arial", 14, "bold"
        self.lb_data_aba02.place(relx=0.825, rely=0.03, relwidth=0.05, relheight=0.05)

        self.entry_data_vlr_aba02 = Entry(self.aba_02, bg="lightblue", fg="black")
        self.entry_data_vlr_aba02['font'] = "Arial", 14
        self.entry_data_vlr_aba02.place(relx=0.825, rely=0.08, relwidth=0.15, relheight=0.07)
        data = self.data_formatada()
        self.entry_data_vlr_aba02.insert(0, f"{data}")
        # Label entry preco_uni
        self.lb_preco_uni_aba02 = Label(self.aba_02, text="Vlr UNI (R$)", bg="lightgrey", fg="black")
        self.lb_preco_uni_aba02['font'] = "Arial", 13, "bold"
        self.lb_preco_uni_aba02.place(relx=0.01, rely=0.16, relwidth=0.11, relheight=0.05)

        self.entry_preco_uni_aba02 = Entry(self.aba_02, bg="lightblue", fg="black")
        self.entry_preco_uni_aba02['font'] = "Arial", 14
        self.entry_preco_uni_aba02.place(relx=0.01, rely=0.215, relwidth=0.1, relheight=0.07)
        # Label entry descricao
        self.lb_descricao_aba02 = Label(self.aba_02, text="Descrição", bg="lightgrey", fg="black")
        self.lb_descricao_aba02['font'] = "Arial", 13, "bold"
        self.lb_descricao_aba02.place(relx=0.12, rely=0.16, relwidth=0.1, relheight=0.05)

        self.entry_descricao_aba02 = Entry(self.aba_02, bg="lightblue", fg="black")
        self.entry_descricao_aba02['font'] = "Arial", 14
        self.entry_descricao_aba02.place(relx=0.12, rely=0.215, relwidth=0.6, relheight=0.07)
        # Label entry qtde
        self.lb_qtde_aba02 = Label(self.aba_02, text="Qtd(UNI)", bg="lightgrey", fg="black")
        self.lb_qtde_aba02['font'] = "Arial", 13, "bold"
        self.lb_qtde_aba02.place(relx=0.71, rely=0.16, relwidth=0.105, relheight=0.05)

        self.entry_qtde_aba02 = Entry(self.aba_02, bg="lightblue", fg="black")
        self.entry_qtde_aba02['font'] = "Arial", 14
        self.entry_qtde_aba02.place(relx=0.726, rely=0.215, relwidth=0.093, relheight=0.07)

        self.lb_id_produto_aba02 = Label(self.aba_02, text="ID" ,bg="lightgrey", fg="black")
        self.lb_id_produto_aba02['font'] = "Arial", 13, "bold"
        self.lb_id_produto_aba02.place(relx=0.815, rely=0.16, relwidth=0.07, relheight=0.05)

        self.entry_id_produto_aba02 = Entry(self.aba_02, bg="lightblue", fg="black")
        self.entry_id_produto_aba02['font'] = "Arial", 14
        self.entry_id_produto_aba02.place(relx=0.84, rely=0.215, relwidth=0.06, relheight=0.07)

        # Botão gravar
        self.btn_Add_aba02 = Button(self.aba_02, text="Add/Produto", bg="white", fg="black", command=self.cria_OS_e_Add_Produtos)
        self.btn_Add_aba02['font'] = "Arial", 14, "bold"
        self.btn_Add_aba02.place(relx=0.23, rely=0.3, relwidth=0.13, relheight=0.07)
        # Botao Alterar
        self.btn_alterar_aba02 = Button(self.aba_02, text="Alterar", bg="lightblue", fg="black", command=self.alterar_produto)
        self.btn_alterar_aba02['font'] = "Arial", 14,
        self.btn_alterar_aba02.place(relx=0.361, rely=0.3, relwidth=0.1, relheight=0.07)

        # Botao Deletar
        self.btn_delete_aba02 = Button(self.aba_02, text="Delete Produto", bg="lightblue", fg="black", command=self.deletar_produto)
        self.btn_delete_aba02['font'] = "Arial", 14
        self.btn_delete_aba02.place(relx=0.462, rely=0.3, relwidth=0.15, relheight=0.07)

        # Salvar Arquivo
        self.btn_salvar_arquivo_aba02 = Button(self.aba_02, text="Salvar PDF", bg="lightblue", fg="black", command=self.gerar_Ordem_de_servico)
        self.btn_salvar_arquivo_aba02['font'] = "Arial", 14
        self.btn_salvar_arquivo_aba02.place(relx=0.784, rely=0.3, relwidth=0.12, relheight=0.07)
        # Limpa
        self.btn_limpa_tela_aba02 = Button(self.aba_02, text="Limpar", bg="lightgrey", fg="black", command=self.botao_limpar)
        self.btn_limpa_tela_aba02['font'] = "Arial", 14
        self.btn_limpa_tela_aba02.place(relx=0.9057, rely=0.3, relwidth=0.07, relheight=0.07)

        # Labels Total no rodapé
        self.lb_total_rodape_aba02 = Label(self.aba_02, text="Total(R$)", bg="lightgrey", fg="black")
        self.lb_total_rodape_aba02['font'] = "Arial", 16
        self.lb_total_rodape_aba02.place(relx=0.75, rely=0.925, relwidth=0.1, relheight=0.065)

        self.lb_totvalor_aba02 = Label(self.aba_02, text="", bg="white", fg="black", bd=4)
        self.lb_totvalor_aba02['font'] = "Arial", 16, "bold"
        self.lb_totvalor_aba02.place(relx=0.85, rely=0.925, relwidth=0.13, relheight=0.065) 

        # Label Pago e valor pago.
        self.lb_pago_rodape_aba02 = Label(self.aba_02, text="Pago(R$)", bg="lightgrey", fg="black")
        self.lb_pago_rodape_aba02['font'] = "Arial", 16
        self.lb_pago_rodape_aba02.place(relx=0.35, rely=0.925, relwidth=0.11, relheight=0.065)

        self.lb_pagovlr_aba02 = Label(self.aba_02, text="", bg="white", fg="black", bd=4)
        self.lb_pagovlr_aba02['font'] = "Arial", 16, "bold"
        self.lb_pagovlr_aba02.place(relx=0.462, rely=0.925, relwidth=0.13, relheight=0.065)

        # Label pendente e pendente valor
        self.lb_pendente_aba02 = Label(self.aba_02, text="Pendente(R$)", bg="lightgrey", fg="black")
        self.lb_pendente_aba02['font'] = "Arial", 16
        self.lb_pendente_aba02.place(relx=0.01, rely=0.925, relwidth=0.15, relheight=0.065)

        self.lb_pendentevlr_aba02 = Label(self.aba_02, text="", bg="white", fg="black", bd=4)
        self.lb_pendentevlr_aba02['font'] = "Arial", 16, "bold"
        self.lb_pendentevlr_aba02.place(relx=0.1557, rely=0.925, relwidth=0.125, relheight=0.065)

        #subtot = self.soma_sub_total_aba02()
        #while subtot:
        #    self.entry_sub_total_aba02.insert(0, subtot)
        #else:
        #    self.entry_sub_total_aba02.insert(0, 0.00)
        # Criar função que vai calcular unidade * preço unitário para preencher este entry automaticamente.
    
    def treeview_aba02(self):
        self.treeview_aba02 = ttk.Treeview(self.aba_02, height=3, column=("col1", "col2", "col3", "col4", "col5", "col6"))
        # "ID", "Data", "nome", "OS Nº", "Valor"
        self.treeview_aba02.heading("#0", text="")
        self.treeview_aba02.heading("#1", text="ID")
        self.treeview_aba02.heading("#2", text="OS")
        self.treeview_aba02.heading("#3", text="Valor UNI(R$)")
        self.treeview_aba02.heading("#4", text="Descrição Produto")
        self.treeview_aba02.heading("#5", text="QTDE (UNI)")
        self.treeview_aba02.heading("#6", text="Sub-Total(R$)")

        # Definindo largura de cada coluna
        self.treeview_aba02.column("#0", width=1)
        self.treeview_aba02.column("#1", width=5)
        self.treeview_aba02.column("#2", width=5)
        self.treeview_aba02.column("#3", width=25)
        self.treeview_aba02.column("#4", width=380)
        self.treeview_aba02.column("#5", width=15)
        self.treeview_aba02.column("#6", width=25)
        self.treeview_aba02.place(relx=0.001, rely=0.38, relwidth=0.99, relheight=0.541)

        # Barra de rolagem_aba01 Treeview aba01
        self.rolagem_aba02 = Scrollbar(self.aba_02, orient="vertical", bg="lightgrey")
        self.treeview_aba02.configure(yscroll=self.rolagem_aba02.set)
        self.rolagem_aba02.place(relx=0.985, rely=0.38, relwidth=0.02 ,relheight=0.541)

        # Bind clique duplo
        self.treeview_aba02.bind("<Double-1>", self.clique_duplo_produtos)

    
    def aba_03_widgets(self):
        # Treeview Ordens de Serviço - Histórico
        self.lb_frase_superior_aba03 = Label(self.aba_03, text="Ordens de Serviço Encerradas / Histórico", bg="lightgrey", fg="black")
        self.lb_frase_superior_aba03["font"] = "Arial", 12
        self.lb_frase_superior_aba03.place(relx=0.3, rely=0.01, relwidth=0.4, relheight=0.05)

        self.treeview_aba03 = ttk.Treeview(self.aba_03, height=3, column=("col1", "col2", "col3", "col4", "col5", "col6"))
        # "ID", "Data", "nome", "OS Nº", "Valor"
        self.treeview_aba03.heading("#0", text="")
        self.treeview_aba03.heading("#1", text="ID")
        self.treeview_aba03.heading("#2", text="Data")
        self.treeview_aba03.heading("#3", text="Nome")
        self.treeview_aba03.heading("#4", text="OS Nº")
        self.treeview_aba03.heading("#5", text="Total (R$)")
        self.treeview_aba03.heading("#6", text="Entrada(R$)")
        # Definindo largura de cada coluna
        self.treeview_aba03.column("#0", width=1)
        self.treeview_aba03.column("#1", width=10)
        self.treeview_aba03.column("#2", width=15)
        self.treeview_aba03.column("#3", width=350)
        self.treeview_aba03.column("#4", width=20)
        self.treeview_aba03.column("#5", width=5)
        self.treeview_aba03.column("#6", width=5)
        self.treeview_aba03.place(relx=0.001, rely=0.08, relwidth=0.99, relheight=0.2)
        # Barra de rolagem_aba01 Treeview aba01
        self.rolagem_aba03 = Scrollbar(self.aba_03, orient="vertical", bg="lightgrey")
        self.treeview_aba03.configure(yscroll=self.rolagem_aba03.set)
        self.rolagem_aba03.place(relx=0.985, rely=0.08,relheight=0.2)
        # Clique duplo 
        self.treeview_aba03.bind("<Double-1>", self.clique_duplo_histórico)


        # Label Frase - Clique sobre a OS

        self.lb_frase_aba03 = Label(self.aba_03, text="Clique Duplo sobre a OS para ver seus Produtos", bg="lightgrey", fg="black")
        self.lb_frase_aba03['font'] = "Arial", 12
        self.lb_frase_aba03.place(relx=0.35, rely=0.3)

        # Label Entry - OS e Nome
        self.lb_os_aba03 = Label(self.aba_03, text="OS", bg="lightgrey", fg="black")
        self.lb_os_aba03['font'] = "Arial", 14, "bold"
        self.lb_os_aba03.place(relx=0.1, rely=0.35, relwidth=0.06, relheight=0.05)

        self.entry_os_aba03 = Entry(self.aba_03, bg="lightblue", fg="black")
        self.entry_os_aba03['font'] = "Arial", 14
        self.entry_os_aba03.place(relx=0.1, rely=0.4, relwidth=0.06, relheight=0.07)

        # Botão Visualizar Produtos
        self.lb_nome_aba03 = Label(self.aba_03, text="Nome", bg="lightgrey", fg="black")
        self.lb_nome_aba03['font'] = "Arial", 14, "bold"
        self.lb_nome_aba03.place(relx=0.172, rely=0.35, relwidth=0.1, relheight=0.05)

        self.entry_nome_aba03 = Entry(self.aba_03, bg="lightblue", fg="black")
        self.entry_nome_aba03['font'] = "Arial", 14
        self.entry_nome_aba03.place(relx=0.172, rely=0.4, relwidth=0.4, relheight=0.07)

        # Botões Visualizar e Limpar
        self.btn_visualizar_aba03 = Button(self.aba_03, text="Visualizar Produtos", bg="lightblue", fg="black", command=self.visualizar_produtos_historico)
        self.btn_visualizar_aba03['font'] = "Arial", 14, "bold"
        self.btn_visualizar_aba03.place(relx=0.58, rely=0.4, relwidth=0.2, relheight=0.07)

        self.btn_limpa_tela_aba03 = Button(self.aba_03, text="Limpar", bg="Lightblue", fg="black", command=self.limpar_casas_historico)
        self.btn_limpa_tela_aba03['font'] = "Arial", 14, "bold"
        self.btn_limpa_tela_aba03.place(relx=0.786, rely=0.4, relwidth=0.1, relheight=0.07)
        # Treeview produtos - histórico
        self.treeview_aba033 = ttk.Treeview(self.aba_03, height=3, column=("col1", "col2", "col3", "col4", "col5", "col6"))
        # "ID", "Data", "nome", "OS Nº", "Valor"
        self.treeview_aba033.heading("#0", text="")
        self.treeview_aba033.heading("#1", text="ID")
        self.treeview_aba033.heading("#2", text="OS")
        self.treeview_aba033.heading("#3", text="Valor UNI(R$)")
        self.treeview_aba033.heading("#4", text="Descrição Produto")
        self.treeview_aba033.heading("#5", text="QTDE (UNI)")
        self.treeview_aba033.heading("#6", text="Sub-Total(R$)")

        # Definindo largura de cada coluna
        self.treeview_aba033.column("#0", width=1)
        self.treeview_aba033.column("#1", width=5)
        self.treeview_aba033.column("#2", width=5)
        self.treeview_aba033.column("#3", width=25)
        self.treeview_aba033.column("#4", width=380)
        self.treeview_aba033.column("#5", width=15)
        self.treeview_aba033.column("#6", width=25)
        self.treeview_aba033.place(relx=0.001, rely=0.5, relwidth=0.99, relheight=0.4)

        # Barra de rolagem_aba01 Treeview aba01
        self.rolagem_aba033 = Scrollbar(self.aba_03, orient="vertical", bg="lightgrey")
        self.treeview_aba033.configure(yscroll=self.rolagem_aba033.set)
        self.rolagem_aba033.place(relx=0.985, rely=0.5, relwidth=0.02 ,relheight=0.4)

        # Labels Total no rodapé
        self.lb_total_rodape_aba03 = Label(self.aba_03, text="Total(R$)", bg="lightgrey", fg="black")
        self.lb_total_rodape_aba03['font'] = "Arial", 16
        self.lb_total_rodape_aba03.place(relx=0.75, rely=0.925, relwidth=0.1, relheight=0.065)

        self.lb_totvalor_aba03 = Label(self.aba_03, text="", bg="white", fg="black", bd=4)
        self.lb_totvalor_aba03['font'] = "Arial", 16, "bold"
        self.lb_totvalor_aba03.place(relx=0.85, rely=0.925, relwidth=0.13, relheight=0.065) 

        # Label Pago e valor pago.
        self.lb_pago_rodape_aba03 = Label(self.aba_03, text="Pago(R$)", bg="lightgrey", fg="black")
        self.lb_pago_rodape_aba03['font'] = "Arial", 16
        self.lb_pago_rodape_aba03.place(relx=0.35, rely=0.925, relwidth=0.11, relheight=0.065)

        self.lb_pagovlr_aba03 = Label(self.aba_03, text="", bg="white", fg="black", bd=4)
        self.lb_pagovlr_aba03['font'] = "Arial", 16, "bold"
        self.lb_pagovlr_aba03.place(relx=0.462, rely=0.925, relwidth=0.13, relheight=0.065)

        # Label pendente e pendente valor
        self.lb_pendente_aba03 = Label(self.aba_03, text="Pendente(R$)", bg="lightgrey", fg="black")
        self.lb_pendente_aba03['font'] = "Arial", 16
        self.lb_pendente_aba03.place(relx=0.01, rely=0.925, relwidth=0.15, relheight=0.065)

        self.lb_pendentevlr_aba03 = Label(self.aba_03, text="", bg="white", fg="black", bd=4)
        self.lb_pendentevlr_aba03['font'] = "Arial", 16, "bold"
        self.lb_pendentevlr_aba03.place(relx=0.1557, rely=0.925, relwidth=0.125, relheight=0.065)
        
    
    def aba_04_widgets(self):
        self.lb_pro01 = Label(self.aba_04, text="OS Fácil v2.0", bg="lightgrey", fg="black")
        self.lb_pro01['font'] = "Arial", 24
        self.lb_pro01.place(relx=0.23, rely=0.2, relwidth=0.6, relheight=0.07)

        self.lb_pro02 = Label(self.aba_04, text="Empresa: Am Sublimação / Ary Dionel Foto Presentes", bg="lightgrey", fg="black")
        self.lb_pro02['font'] = "Arial", 18
        self.lb_pro02.place(relx=0.23, rely=0.3, relwidth=0.6, relheight=0.07)

        self.lb_pro03 = Label(self.aba_04, text="Autor: Maycon R. Campos", bg="lightgrey", fg="black")
        self.lb_pro03['font'] = "Arial", 18
        self.lb_pro03.place(relx=0.23, rely=0.4, relwidth=0.6, relheight=0.07)

        self.lb_pro04 = Label(self.aba_04, text="Escrito em Python 3.7.5 64-bit", bg="lightgrey", fg="black")
        self.lb_pro04['font'] = "Arial", 18
        self.lb_pro04.place(relx=0.23, rely=0.7, relwidth=0.6, relheight=0.07)

        self.lb_pro05 = Label(self.aba_04, text="Data Produção: Junho/2020", bg="lightgrey", fg="black")
        self.lb_pro05['font'] = "Arial", 12
        self.lb_pro05.place(relx=0.23, rely=0.8, relwidth=0.6, relheight=0.07)

Janela_Principal()
