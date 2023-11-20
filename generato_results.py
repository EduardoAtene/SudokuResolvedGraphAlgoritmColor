import os
import pandas as pd

# Função para ler os arquivos de análise
def read_analysis_files(root_folder, num_folders):
    data = []

    for i in range(1, num_folders + 1):
        folder_name = f"Sudoku_{i}"
        analysis_file_path = os.path.join(root_folder, folder_name, f"analiz_sudoku_{i}.txt")

        if os.path.exists(analysis_file_path):
            with open(analysis_file_path, 'r') as file:
                lines = file.readlines()
                if len(lines) >= 5:
                    execution_time_code = float(lines[0].strip())
                    execution_time_create_sudoku = float(lines[1].strip())
                    execution_time_coloring = float(lines[2].strip())
                    num_recursive_calls = int(lines[3].strip())
                    num_colors_tested = int(lines[4].strip())

                    data.append({
                        'Pasta': folder_name,
                        'Tempo de execucao do codigo': execution_time_code,
                        'Tempo de execucao gerar Sudoku': execution_time_create_sudoku,
                        'Tempo de execucao do algoritmo de coloracao': execution_time_coloring,
                        'Numero de chamadas recursivas': num_recursive_calls,
                        'Numero de cores testadas': num_colors_tested
                    })
                else:
                    print(f"File {analysis_file_path} does not have enough data.")

        else:
            print(f"File {analysis_file_path} not found.")

    return data

# Função para calcular as medianas
def calculate_median_metrics(data):
    df = pd.DataFrame(data)
    df_numeric = df.drop(columns=['Pasta'])  # Remove a coluna 'Pasta'

    # Calcula as medianas apenas para as colunas numéricas
    median_values = df_numeric.median()
    return median_values

# Carregar dados e calcular as medianas
root_folder = "Output"
num_folders = 100

data = read_analysis_files(root_folder, num_folders)
median_metrics = calculate_median_metrics(data)

# Adicionando as medianas ao arquivo Excel
excel_file = 'results.xlsx'
with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    median_metrics.to_excel(writer, sheet_name='Medianas', startrow=1, startcol=1, header=True, index=True)
    workbook = writer.book
    worksheet = writer.sheets['Medianas']
    table = worksheet.tables.values()
    if table:
        table = list(table)[0]
        table.theme = "TableStyleMedium9"  # Definindo um estilo de tabela
    worksheet.cell(row=2, column=3).value = 'Mediana (' + str(num_folders) + ' sudoku)'  # Atualiza o cabeçalho da coluna B
    writer._save()

print("Medianas das métricas adicionadas ao arquivo Excel.")