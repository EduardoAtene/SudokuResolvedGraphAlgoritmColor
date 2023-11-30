import sys
import time
from random import shuffle, randint
import networkx as nx
import plotly.graph_objects as go
import matplotlib.cm as cm
import os

# Ideia resolver problema de grafos, utilziando algoritmo de coloração
# Nome: Eduardo Atene Silva e Igor 
# Pesquisa de Informação

class Sudoku:
	grid = [] # grade 9x9 do sudoku
	adj = [] # grafo por lista de adjacência
	index = [] # associa cada posição da matriz à um índice
	color = {} # cor do nó (cada cor representa o número)
	inv = {} # retorna as coordenadas na grade de acordo com o índice atribuído ao nó

  # inicializa a grade do sudoku vazia (preenchida com zeros)
	def __init__(self, grid=None):
		if grid is None:
			for _ in range(9):
				self.grid.append([0] * 9)
		else:
			self.grid = grid

		# inicializa o array de indices
		for _ in range(9):
			self.index.append([0] * 9)

		# inicializa lista de adjacência
		for _ in range(81):
			self.adj.append([])

  # imprime o sudoku no terminal
	def __str__(self):
		str_sudoku = ''

		for row in range(9):
			str_sudoku += ' '.join([str(number) for number in self.grid[row]]).replace('0', '_') + '\n'

		return str_sudoku
	
	# colore um nó de acordo com o índice na lista de adjacência
	def paint(self, node, color):
		self.color[node] = color
		self.grid[ self.inv[node][0] ][ self.inv[node][1] ] = color

	# gera o grafo por lista de adjacência baseado na grade do sudoku
	def build_graph(self):
		# gera os índices na lista de adjacência
		current_index = 0
		for i in range(9):
			for j in range(9):
				current_index += 1

				self.inv[current_index] = (i, j)
				self.index[i][j] = current_index
				self.color[current_index] = self.grid[i][j]

		# conecta os nós da mesma linha e mesma coluna
		for row in range(9):
			for column in range(9):
				# mesma linha
				for new_row in range(9):
					if row != new_row:
						self.adj[ self.index[row][column] ].append( self.index[new_row][column] )
				
				# mesma coluna
				for new_column in range(9):
					if column != new_column:
						self.adj[ self.index[row][column] ].append( self.index[row][new_column] )
		
		# conecta os nós do mesmo bloco 3x3
		for row in range(0, 9, 3):
			for column in range(0, 9, 3):
				# processa bloco que começa na posição [row][column]
				for old_row in range(row, row+3):
					for old_column in range(column, column+3):
						for new_row in range(row, row+3):
							for new_column in range(column, column+3):
								if not (old_row == new_row and old_column == new_column):
									# cria uma aresta entre u e v
									u = self.index[old_row][old_column]
									v = self.index[new_row][new_column]

									self.adj[u].append(v)

# gera um padrão aleatório de números de 1 à 9
def generate_random_pattern():
	random_pattern = [number for number in range(1, 10)]
	shuffle(random_pattern)
	
	return random_pattern

# verifica se o array number contém exatamente uma ocorrência dos elementos de 1 até 9
def has_distinct_numbers(numbers):
	# caso não exista exatamente uma ocorrência do número retorna falso
	for number in range(1, 10):
		if numbers[number] > 1:
			return False

	return True

# checa se a linha é válida
def check_row(sudoku, row):
	numbers = [0] * 10 # indica a quantidade de números iguais a i na posição i

	for column in range(9):
		numbers[ sudoku.grid[row][column] ] += 1

	return has_distinct_numbers(numbers)

# checa se a coluna é válida
def check_column(sudoku, column):
	numbers = [0] * 10 # indica a quantidade de números iguais a i na posição i

	for row in range(9):
		numbers[ sudoku.grid[row][column] ] += 1

	return has_distinct_numbers(numbers)

# checa se o bloco 3x3 é válido (começando em [row][column])
def check_block(sudoku, row, column):
	numbers = [0] * 10 # indica a quantidade de números iguais a i na posição i

	for row_it in range(row, row+3):
		for column_jt in range(column, column+3):
			numbers[ sudoku.grid[row_it][column_jt] ] += 1

	return has_distinct_numbers(numbers)

# checa se o sudoku é uma solução válida
def check(sudoku):
	# verifica as linhas
	for row in range(9):
		if not check_row(sudoku, row):
			return False

	# verifica as colunas
	for column in range(9):
		if not check_column(sudoku, column):
			return False

	# verifica os blocos 3x3
	for row in range(0, 9, 3):
		for column in range(0, 9, 3):
			if not check_block(sudoku, row, column):
				return False

	return True

# gera um tabuleiro de sudoku aleatório
def generate():
	sudoku = Sudoku()
	sudoku.build_graph() # cria grafo com lista de adjacência
 
	coloring(sudoku, generate_random_pattern(), 1, False, False) # colore o sudoku com um padrão aleatório

	# remove elementos do sudoku para gerar um jogo
	for node in range(1, 82):
		# 60% de chance de remover a célula (sudoku nível intermediário)
		if randint(0, 10) < 6:
			sudoku.paint(node, 0)

	return sudoku

def coloring(sudoku, pattern, node, show_steps=False, show_colors=False):
    global num_recursive_calls
    global num_colors_tested

    if show_steps:
        print(sudoku)
    
    # caso base é chegar no nó 9*9+1 (inexistente)
    if node == 82:
        return True

    # se o nó já está colorido, avança para o próximo nó
    if sudoku.color[node] != 0:
        return coloring(sudoku, pattern, node+1, show_steps, show_colors)

    found_color = False  # indica se encontrou uma cor válida para o nó atual
    for color in pattern:  # testa as cores de 1 à 9
        color_is_valid = True

        # verifica se há uma cor igual nos vizinhos
        for neighbor in sudoku.adj[node]:
            num_colors_tested += 1  # Conta o número de cores testadas para cada nó
            if sudoku.color[neighbor] == color:
                color_is_valid = False
                break

        if color_is_valid:
            sudoku.paint(node, color)
            found_color = coloring(sudoku, pattern, node+1, show_steps, show_colors)

            # se a cor escolhida não gerou uma solução válida, preenche novamente com zero
            if not found_color:
                sudoku.paint(node, 0)
            else:
                return True

    num_recursive_calls += 1  # Conta o número de chamadas recursivas da função
    return found_color

def print_sudoku(sudoku):
    str_sudoku = '|---------------------- |\n'
    for i in range(9):
        if i % 3 == 0 and i != 0:
            str_sudoku += '|---------------------- |\n'
        for j in range(9):
            if j % 3 == 0:
                str_sudoku += '| '
            str_sudoku += f'{sudoku.grid[i][j]} '
        str_sudoku += '|\n'
    str_sudoku += '|---------------------- |\n'
    return str_sudoku
    
def plot_interactive_graph(sudoku):
    G = nx.Graph()
    node_labels = {}  # Dicionário para armazenar os rótulos dos nós

    colors = cm.rainbow(range(9))  # Gerando uma paleta de cores para os números de 1 a 9

    # Criando o grafo
    for row in range(9):
        for column in range(9):
            node = sudoku.index[row][column]
            G.add_node(node)
            node_labels[node] = f'(X: {column}, Y: {row}, Value: {sudoku.grid[row][column]})'  # Definindo o texto para cada nó

    for node in range(1, 82):
        for neighbor in sudoku.adj[node]:
            G.add_edge(node, neighbor)

    pos = nx.spring_layout(G, dim=3)

    node_trace = go.Scatter3d(
        x=[pos[node][0] for node in G.nodes()],
        y=[pos[node][1] for node in G.nodes()],
        z=[pos[node][2] for node in G.nodes()],
        text=[node_labels[node] for node in G.nodes()],  # Adicionando os rótulos nos vértices
        mode='markers+text',  # Incluindo texto nos marcadores
        marker=dict(
            size=8,
            line=dict(color='black', width=1),
            color=[colors[sudoku.grid[row][column] - 1] for row, column in sudoku.inv.values()],  # Usando as cores para cada número do sudoku
            opacity=0.8
        ),
        textposition="bottom center",  # Posição do texto em relação ao marcador
        hoverinfo='text',
        textfont=dict(size=8)  # Tamanho do texto dos rótulos dos nós
    )

    edge_trace = go.Scatter3d(
        x=[pos[edge[0]][0] for edge in G.edges()],
        y=[pos[edge[0]][1] for edge in G.edges()],
        z=[pos[edge[0]][2] for edge in G.edges()],
        mode='lines',
        line=dict(color='gray', width=1),
        hoverinfo='none'
    )

    fig = go.Figure(data=[node_trace, edge_trace],
                    layout=go.Layout(
                        title='Grafo Sudoku Gerado Interativo',
                        showlegend=False,
                        scene=dict(
                            xaxis=dict(title='Column (X)'),
                            yaxis=dict(title='Row (Y)'),
                            zaxis=dict(title='Value (Z)')
                        )
                    ))

    fig.show()
   
def main(file_number):
    folder_name = f"Sudoku_{file_number}"
    output_folder = f"Output/{folder_name}"
    os.makedirs(output_folder, exist_ok=True)

    analizy_file = f"{output_folder}/analiz_sudoku_{file_number}.txt"  # Diretório resultado final
    output_file = f"{output_folder}/result_sudoku_{file_number}.txt"  # Diretório resultado final
    steps_output_file = f"{output_folder}/steps_sudoku_{file_number}.txt"  # Diretório salvar os passos gerados

    start_time_code = time.time()  # ínicio

    with open(output_file, 'w') as output:
        sudoku_Testt_1 = Sudoku([
    		[8, 0, 0, 1, 5, 0, 6, 0, 0],
			[0, 0, 0, 3, 0, 0, 0, 4, 1],
			[5, 0, 0, 0, 0, 0, 7, 0, 0],
			[0, 0, 0, 0, 0, 9, 0, 6, 2],
			[0, 0, 0, 0, 3, 0, 0, 0, 0],
			[1, 4, 0, 8, 0, 0, 0, 0, 0],
			[0, 0, 8, 0, 0, 0, 0, 0, 9],
			[2, 9, 0, 0, 0, 1, 0, 0, 0],
			[0, 0, 5, 0, 9, 7, 0, 0, 6],
        ])
        
        start_time_generator_sudoku = time.time()  # ínicio
        sudoku = generate()
        end_time_generator_sudoku = time.time()  # ínicio
        execution_time_algoritm_create_sudoku = end_time_generator_sudoku - start_time_generator_sudoku  # Calcula o tempo de execução do algoritmo de coloracao
        output.write(f'Sudoku gerado:\n{print_sudoku(sudoku)}\n')
            
        # plot_interactive_graph(sudoku) # Gera a visualização do grafo de maneira interantiva
            
        with open(steps_output_file, 'w') as steps_output:
            sys.stdout = steps_output  # Redirecionando a saída para o arquivo
            
            start_time_algoritm_colors_sudoku = time.time()  # ínicio
            coloring(sudoku, generate_random_pattern(), 1, True, True)
            end_time_algoritm_colors_sudoku = time.time()  # Marca o tempo de término
            execution_time_algoritm_colors = end_time_algoritm_colors_sudoku - start_time_algoritm_colors_sudoku  # Calcula o tempo de execução do algoritmo de coloracao
            
            sys.stdout = sys.__stdout__  # Restaurando a saída padrão
            
            print(f"Arquivo de passos gerado em: {steps_output_file}")

    end_time_code = time.time()  # ínicio
    execution_time_code = end_time_code - start_time_code  # Calcula o tempo de execução do algoritmo de coloracao

    # Escreve o tempo de execução no arquivo de saída
    with open(output_file, 'a') as output:
        output.write(f'Sudoku Solucionado:\n{print_sudoku(sudoku)}\n')
        output.write(f'O Sudoku e valido? {"Sim" if check(sudoku) else "Não"}\n\n')
        output.write(f'Tempo de execucao do codigo: {execution_time_code} segundos\n')
        output.write(f'Tempo de execucao gerar Sudoku: {execution_time_algoritm_create_sudoku} segundos\n')
        output.write(f'Tempo de execucao do algoritmo de coloracao: {execution_time_algoritm_colors} segundos\n')
        output.write(f'Numero de chamadas recursivas: {num_recursive_calls}\n')
        output.write(f'Numero de cores testadas: {num_colors_tested}\n')

    with open(analizy_file, 'a') as output:
        output.write(f'{execution_time_code}\n')
        output.write(f'{execution_time_algoritm_create_sudoku}\n')
        output.write(f'{execution_time_algoritm_colors}\n')
        output.write(f'{num_recursive_calls}\n')
        output.write(f'{num_colors_tested}\n')

    print(f'Todas as saídas foram inseridass no arquivo: {output_file}')


if __name__ == '__main__':
    num_files = 1000  # Altere conforme o número de GRAFOS que deseja gerar/testar

    for i in range(num_files):
        num_recursive_calls = 0
        num_colors_tested = 0
        main(i + 1)