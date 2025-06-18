import base64
import os
import requests
from openai import OpenAI
from typing import Optional, Union
import mimetypes

class SolucionadorCaptchaOpenAI:
    """
    Classe para resolver CAPTCHAs de imagem usando GPT-4 Vision da OpenAI
    """

    def __init__(self, chave_api_openai: str, modelo: str = 'gpt-4o'):
        """
        Inicializa o solucionador com a chave da API OpenAI

        Args:
            chave_api_openai (str): Chave da API da OpenAI
            modelo (str): Modelo a ser usado (padrão: gpt-4o para visão)
        """
        self.cliente_openai = OpenAI(api_key=chave_api_openai)
        self.modelo = modelo
        self.chave_api = chave_api_openai

    def _validar_arquivo_imagem(self, caminho_imagem) -> bool:
        """
        Valida se o arquivo de imagem existe e é um formato suportado

        Args:
            caminho_imagem (str): Caminho para o arquivo de imagem

        Returns:
            bool: True se válido, False caso contrário
        """
        if not os.path.exists(caminho_imagem):
            print(f'❌ Arquivo não encontrado: {caminho_imagem}')
            return False

        # Verifica tipos MIME suportados
        tipo_mime, _ = mimetypes.guess_type(caminho_imagem)
        tipos_suportados = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']

        if tipo_mime not in tipos_suportados:
            print(f'❌ Formato não suportado: {tipo_mime}')
            return False

        return True

    def converter_url_base64(self, url_imagem: str) -> Optional[str]:
        """
        Baixa uma imagem de URL e converte para base64

        Args:
            url_imagem (str): URL da imagem

        Returns:
            str: String base64 da imagem ou None se houver erro
        """
        try:
            print(f'📥 Baixando imagem de: {url_imagem}')

            # Baixa a imagem
            resposta = requests.get(url_imagem, timeout=10)
            resposta.raise_for_status()

            # Converte para base64
            base64_imagem = base64.b64encode(resposta.content).decode('utf-8')

            # Tenta determinar o tipo MIME do cabeçalho
            tipo_mime = resposta.headers.get('content-type', 'image/png')

            return f'data:{tipo_mime};base64,{base64_imagem}'

        except Exception as erro:
            print(f'❌ Erro ao baixar e converter URL para base64: {erro}')
            return None

    def converter_imagem_base64(self, caminho_imagem: str) -> Optional[str]:
        """
        Converte uma imagem para base64

        Args:
            caminho_imagem (str): Caminho para o arquivo de imagem

        Returns:
            str: String base64 da imagem ou None se houver erro
        """
        try:
            # Valida o arquivo
            if not self._validar_arquivo_imagem(caminho_imagem):
                return None

            # Lê e converte para base64
            with open(caminho_imagem, 'rb') as arquivo_imagem:
                conteudo_imagem = arquivo_imagem.read()
                base64_imagem = base64.b64encode(conteudo_imagem).decode('utf-8')

            # Determina o tipo MIME
            tipo_mime, _ = mimetypes.guess_type(caminho_imagem)

            # Retorna no formato data URL
            return f'data:{tipo_mime};base64,{base64_imagem}'

        except Exception as erro:
            print('❌ Erro ao converter imagem para base64: {erro}')
            return None

    def _criar_prompt_captcha(self, tipo_captcha: str = 'texto') -> str:
        """
        Cria o prompt apropriado para resolução do CAPTCHA

        Args:
            tipo_captcha (str): Tipo do CAPTCHA ("texto", "matematica", "objeto")

        Returns:
            str: Prompt otimizado para o tipo de CAPTCHA
        """
        prompts = {
            "texto": """
                Analise esta imagem de CAPTCHA e extraia APENAS o texto/código que está visível.

                Instruções:
                - Retorne APENAS os caracteres alfanuméricos visíveis
                - Ignore qualquer ruído, distorção ou elementos de fundo
                - NÃO inclua explicações, pontuação ou texto adicional
                - Se houver letras maiúsculas e minúsculas, mantenha o formato original
                - Se não conseguir ler claramente, faça sua melhor estimativa

                Resposta esperada: apenas o código/texto
            """,

            "matematica": """
                Esta imagem contém uma operação matemática simples (CAPTCHA).

                Instruções:
                - Resolva a operação matemática mostrada
                - Retorne APENAS o resultado numérico
                - Operações típicas: soma (+), subtração (-), multiplicação (×, *)

                Resposta esperada: apenas o número resultado
            """,

            "objeto": """
                Esta imagem é um CAPTCHA que pede para identificar objetos específicos.

                Instruções:
                - Identifique os objetos solicitados na imagem
                - Retorne apenas a resposta ao que está sendo perguntado
                - Seja específico e conciso

                Resposta esperada: apenas a resposta direta
            """
        }

        return prompts.get(tipo_captcha, prompts['texto'])

    def resolver_captcha(self, entrada: str,
                         tipo_captcha: str = 'texto',
                         prompt_personalizado: Optional[str] = None) -> Optional[str]:
        """
        Resolve um CAPTCHA usando GPT-4 Vision

        Args:
            entrada (str): Caminho da imagem local ou URL da imagem
            tipo_captcha (str): Tipo do CAPTCHA ("texto", "matematica", "objeto")
            prompt_personalizado (str, optional): Prompt customizado para casos específicos

        Returns:
            str: Texto extraído do CAPTCHA ou None se houver erro
        """
        try:
            # Determina se é arquivo local ou URL
            if entrada.startswith(('http://', 'https://')):
                base64_imagem = ''
            else:
                base64_imagem = self.converter_imagem_base64(entrada)

            if not base64_imagem:
                print('❌ Não foi possível processar a imagem')
                return None

            # Usa prompt personalizado ou padrão
            prompt = prompt_personalizado or self._criar_prompt_captcha(tipo_captcha)

            print(f'📤 Enviando para GPT-4 Vision...')

            # Faz a chamada para a API OpenAI
            resposta = self.cliente_openai.chat.completions.create(
                model=self.modelo,
                messages=[
                    {
                        'role': 'user',
                        'content': [
                            {
                                'type': 'text',
                                'text': prompt
                            },
                            {
                                'type': 'image_url',
                                'image_url': {
                                    'url': base64_imagem,
                                    'detail': 'high' # Alta resolução para melhor precisão
                                }
                            }
                        ]
                    }
                ],
                max_tokens=50, # CAPTCHAs são geralmente curtos
                temperature=0.1 # Baixa criatividade para maior precisão
            )

            # Extrai a resposta
            texto_captcha = resposta.choices[0].message.content.strip()

            print(f'✅ CAPTCHA resolvido: {texto_captcha}')
            return texto_captcha

        except Exception as erro:
            print(f'❌ Erro ao resolver CAPTCHA: {erro}')
            return None

# Exemplo de uso
if __name__ == '__main__':
    # Exemplo de como usar a classe
    print('=== Exemplo de Uso do Solucionador CAPTCHA OpenAI ===')

    from dotenv import load_dotenv

    # Carrega variáveis do arquivo .env
    load_dotenv()

    # Substitua pela sua chave real da OpenAI
    # CHAVE_OPENAI = 'sua_chave_openai_aqui'
    CHAVE_OPENAI = os.getenv('OPENAI_API_KEY')

    if CHAVE_OPENAI == 'sua_chave_openai_aqui':
        print('⚠️  Configure sua chave da OpenAI antes de usar!')
    else:
        # Inicializa o solucionador
        solucionador = SolucionadorCaptchaOpenAI(CHAVE_OPENAI)

        # Exemplo 1: Resolver CAPTCHA de arquivo local
        resultado = solucionador.resolver_captcha('captcha.png')
        print(f'Resultado: {resultado}')

        # Exemplo 2: Resolver CAPTCHA de URL
        # resultado = solucionador.resolver_captcha('https://exemplo.com/captcha.jpg')
        # print(f'Resultado: {resultado}')

        # Exemplo 3: CAPTCHA matemático
        # resultado = solucionador.resolver_captcha('captcha_matematico.png', tipo_captcha='matematico')
        # print(f'Resultado: {resultado}')
