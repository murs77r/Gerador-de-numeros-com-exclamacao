# 🔢 Gerador de Números por Extenso com Inserção Automatizada (Tkinter) 🤖

Este script Python cria uma interface gráfica (GUI) usando a biblioteca Tkinter que permite gerar números por extenso (usando `num2words`) e inseri-los automaticamente em qualquer campo de texto ativo (usando `pyautogui`, `pyperclip`, e `keyboard`), com um intervalo de tempo configurável.

## ✨ Funcionalidades

*   **Interface Gráfica Intuitiva:**
    *   Campos para inserir o número inicial e final do intervalo.
    *   Campo para definir o tempo de espera (em segundos) entre as inserções.
    *   Botão "INSERIR NÚMEROS" para iniciar o processo.
    *   Botão "PARAR" (aparece durante a execução) para interromper a inserção.
    *   Validação de entrada: garante que apenas números sejam inseridos nos campos.
    *   Mensagens de erro claras para o usuário.
    * Contagem regressiva.
    * Ícone customizado.

*   **Geração de Números por Extenso:**
    *   Utiliza a biblioteca `num2words` para converter números em sua representação por extenso em português (ex: 1 -> "UM").
    *   Converte o resultado para letras maiúsculas.

*   **Inserção Automatizada:**
    *   Usa `pyperclip` para copiar o número por extenso para a área de transferência.
    *   Usa `pyautogui` para simular as teclas "Ctrl+V" (colar) e "Enter" no campo de texto ativo (onde o cursor estiver).
    *   Aguarda o tempo especificado antes de inserir o próximo número.

*   **Interrupção:**
    *   O usuário pode interromper a inserção a qualquer momento:
        *   Clicando no botão "PARAR".
        *   Pressionando a combinação de teclas "Ctrl+C" (globalmente).
    *   Usa uma `queue` (fila) para comunicação entre a thread principal e a thread de inserção, permitindo uma interrupção limpa.

*   **Multithreading:**
    *   A inserção dos números é executada em uma thread separada (`threading.Thread`), para evitar que a interface gráfica congele durante o processo.

* **Tratamento de Erros**:
    * Caso o valor inserido não seja um número.
    * Caso o número inicial seja maior que o final.
    * Caso o ícone não possa ser carregado.
    * Caso o usuário não clique em confirmar para rodar o script.

* **Design**:
    * Uso do tema 'clam'.
    * Uso do estilo 'Rounded.TButton' e 'Rounded.TEntry'.
    * Uso da fonte "Nunito".

## 🛠️ Tecnologias Utilizadas

*   **Python:** Linguagem de programação.
*   **Tkinter:** Biblioteca padrão do Python para criação de interfaces gráficas.
*   **ttk (Themed Tkinter):**  Extensão do Tkinter que oferece widgets com visual mais moderno.
*   **num2words:**  Biblioteca para converter números em palavras (em vários idiomas).
*   **pyautogui:**  Biblioteca para automação de GUI (simular teclado e mouse).
*   **pyperclip:** Biblioteca para copiar e colar texto na área de transferência.
*   **threading:**  Módulo do Python para criar e gerenciar threads.
*   **queue:** Módulo do Python para criar filas (usado para comunicação entre threads).
*   **time:** Módulo do Python para lidar com tempo (pausas).
*   **keyboard:** Biblioteca para monitorar e manipular eventos de teclado (atalho global).
* **requests**: Biblioteca para fazer requisições HTTP e baixar arquivos.
* **PIL (Pillow):** Para manipulação de imagens, como carregar, converter (para ícone) e salvar.
* **io (BytesIO)** Para lidar com dados binários na memória.
* **os**: Acessar arquivos.
* **tempfile**: Gerar pasta temporária para salvar o ícone.
