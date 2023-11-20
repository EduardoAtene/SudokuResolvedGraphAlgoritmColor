import shutil
import os

def delete_output_folders(root_folder):
    output_folder = os.path.abspath(root_folder)

    for folder_name in os.listdir(output_folder):
        folder_path = os.path.join(output_folder, folder_name)
        
        # Verifica se é um diretório
        if os.path.isdir(folder_path):
            # Remove a pasta e todo o seu conteúdo
            shutil.rmtree(folder_path)
            print(f"Deleted folder: {folder_name}")

# Exemplo de utilização:
root_folder = "Output"  # Diretório raiz onde estão as pastas Sudoku_X

delete_output_folders(root_folder)