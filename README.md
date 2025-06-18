# 🔓 Solucionador CAPTCHA OpenAI

Uma solução Python para resolver CAPTCHAs automaticamente usando a API GPT-4 Vision da OpenAI. Esta ferramenta utiliza inteligência artificial avançada para interpretar e resolver diferentes tipos de CAPTCHAs de forma eficiente.

## ✨ Características

- 🖼️ **Suporte a múltiplos formatos**: JPEG, PNG, GIF, WebP
- 🌐 **Flexibilidade de entrada**: Arquivos locais ou URLs de imagens
- 🔢 **Tipos de CAPTCHA suportados**:
  - Texto alfanumérico
  - Operações matemáticas
  - Identificação de objetos
- ⚙️ **Prompts otimizados** para cada tipo de CAPTCHA
- 🛡️ **Validação robusta** de arquivos e tipos MIME
- 📝 **Logs detalhados** para acompanhamento do processo

## 🚀 Instalação

### Pré-requisitos

- Python 3.7 ou superior
- Chave da API OpenAI

### Dependências

Instale as dependências necessárias:

```bash
pip install openai requests python-dotenv
```

## 🔑 Configuração

### 1. Obtenha uma chave da API OpenAI

Visite [OpenAI Platform](https://platform.openai.com/) e crie uma conta para obter sua chave da API.

### 2. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
OPENAI_API_KEY=sua_chave_openai_aqui
```

## 📖 Uso

### Uso Básico

```python
from solucionador_captcha_openai import SolucionadorCaptchaOpenAI
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Inicializa o solucionador
solucionador = SolucionadorCaptchaOpenAI(os.getenv('OPENAI_API_KEY'))

# Resolve um CAPTCHA de arquivo local
resultado = solucionador.resolver_captcha('captcha.png')
print(f'Resultado: {resultado}')
```

### Exemplos Avançados

#### 1. CAPTCHA de Texto (Padrão)

```python
# Resolve CAPTCHA alfanumérico
resultado = solucionador.resolver_captcha(
    'captcha_texto.png',
    tipo_captcha='texto'
)
```

#### 2. CAPTCHA Matemático

```python
# Resolve operações matemáticas
resultado = solucionador.resolver_captcha(
    'captcha_matematico.png',
    tipo_captcha='matematica'
)
```

#### 3. CAPTCHA de Identificação de Objetos

```python
# Identifica objetos específicos
resultado = solucionador.resolver_captcha(
    'captcha_objetos.png',
    tipo_captcha='objeto'
)
```

#### 4. CAPTCHA de URL

```python
# Resolve CAPTCHA diretamente de uma URL
resultado = solucionador.resolver_captcha(
    'https://exemplo.com/captcha.jpg'
)
```

#### 5. Prompt Personalizado

```python
# Usa um prompt customizado para casos específicos
prompt_customizado = """
Esta imagem contém um CAPTCHA especial.
Identifique apenas os números que aparecem em cor azul.
Retorne apenas os dígitos encontrados.
"""

resultado = solucionador.resolver_captcha(
    'captcha_especial.png',
    prompt_personalizado=prompt_customizado
)
```

## 🏗️ Estrutura da Classe

### `SolucionadorCaptchaOpenAI`

#### Métodos Principais

- **`__init__(chave_api_openai, modelo='gpt-4o')`**: Inicializa o solucionador
- **`resolver_captcha(entrada, tipo_captcha='texto', prompt_personalizado=None)`**: Método principal para resolver CAPTCHAs
- **`converter_imagem_base64(caminho_imagem)`**: Converte arquivo local para base64
- **`converter_url_base64(url_imagem)`**: Baixa e converte URL para base64

#### Parâmetros do `resolver_captcha`

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|---------|
| `entrada` | `str` | Caminho do arquivo ou URL da imagem | Obrigatório |
| `tipo_captcha` | `str` | Tipo do CAPTCHA: 'texto', 'matematica', 'objeto' | `'texto'` |
| `prompt_personalizado` | `str` | Prompt customizado para casos específicos | `None` |

## 📝 Tipos de CAPTCHA Suportados

### 1. Texto Alfanumérico
- Extrai códigos com letras e números
- Mantém formatação original (maiúsculas/minúsculas)
- Ignora ruídos e distorções

### 2. Matemática
- Resolve operações básicas (+, -, ×)
- Retorna apenas o resultado numérico
- Suporte a diferentes notações

### 3. Identificação de Objetos
- Identifica objetos específicos em imagens
- Responde perguntas sobre conteúdo visual
- Análise contextual avançada

## 🔧 Configurações Avançadas

### Modelos Suportados

```python
# Diferentes modelos GPT-4 Vision
solucionador = SolucionadorCaptchaOpenAI(
    chave_api_openai=sua_chave,
    modelo='gpt-4o'  # Padrão recomendado
)
```

### Parâmetros de Otimização

O código está otimizado com:
- **`max_tokens=50`**: Limite para respostas concisas
- **`temperature=0.1`**: Baixa criatividade para maior precisão
- **`detail='high'`**: Alta resolução para melhor análise

## ⚠️ Limitações e Considerações

### Limitações Técnicas
- Funciona apenas com CAPTCHAs visuais
- Requer conexão com internet para API da OpenAI
- Sujeito aos limites de rate da API OpenAI

### Considerações Éticas
- ⚖️ **Use responsavelmente**: Respeite os termos de serviço dos sites
- 🤖 **Automação**: Certifique-se de que o uso está em conformidade com as políticas
- 💰 **Custos**: Monitore o uso da API para controlar gastos

### Formatos Suportados
- ✅ JPEG/JPG
- ✅ PNG
- ✅ GIF
- ✅ WebP
- ❌ BMP, TIFF (não suportados)

## 🐛 Solução de Problemas

### Erros Comuns

#### 1. Arquivo não encontrado
```
❌ Arquivo não encontrado: captcha.png
```
**Solução**: Verifique se o caminho do arquivo está correto.

#### 2. Formato não suportado
```
❌ Formato não suportado: image/bmp
```
**Solução**: Converta a imagem para PNG, JPEG ou outro formato suportado.

#### 3. Erro de API
```
❌ Erro ao resolver CAPTCHA: API key inválida
```
**Solução**: Verifique se sua chave da OpenAI está correta e ativa.

### Debug

Para debug detalhado, observe as mensagens de log:
- 📥 Download de imagens
- 📤 Envio para API
- ✅ Resultados obtidos
- ❌ Erros encontrados

## 💡 Dicas de Uso

### Melhorando a Precisão
1. **Use imagens de alta qualidade**
2. **Escolha o tipo correto de CAPTCHA**
3. **Customize prompts para casos específicos**
4. **Teste diferentes abordagens**

### Otimização de Custos
- Cache resultados quando possível
- Use imagens com resolução adequada (não excessiva)
- Implemente retry logic com backoff

## 📊 Exemplo Completo

```python
#!/usr/bin/env python3
"""
Exemplo completo de uso do Solucionador CAPTCHA OpenAI
"""
import os
from dotenv import load_dotenv
from solucionador_captcha_openai import SolucionadorCaptchaOpenAI

def main():
    # Configuração
    load_dotenv()
    chave_api = os.getenv('OPENAI_API_KEY')

    if not chave_api:
        print("❌ Chave da API OpenAI não configurada!")
        return

    # Inicializa o solucionador
    solucionador = SolucionadorCaptchaOpenAI(chave_api)

    # Lista de CAPTCHAs para testar
    captchas = [
        {'arquivo': 'captcha_texto.png', 'tipo': 'texto'},
        {'arquivo': 'captcha_matematico.png', 'tipo': 'matematica'},
        {'arquivo': 'https://exemplo.com/captcha.jpg', 'tipo': 'objeto'}
    ]

    # Resolve cada CAPTCHA
    for captcha in captchas:
        print(f"\n🔍 Processando: {captcha['arquivo']}")
        resultado = solucionador.resolver_captcha(
            captcha['arquivo'],
            tipo_captcha=captcha['tipo']
        )

        if resultado:
            print(f"✅ Sucesso: {resultado}")
        else:
            print("❌ Falha na resolução")

if __name__ == '__main__':
    main()
```

## 📄 Licença

Este projeto é fornecido como está, para fins educacionais e de pesquisa. Use com responsabilidade e em conformidade com os termos de serviço aplicáveis.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir melhorias
- Enviar pull requests
- Compartilhar casos de uso interessantes
