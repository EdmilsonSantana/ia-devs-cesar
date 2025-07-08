#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import json
from datetime import datetime
import openai
from fpdf import FPDF
from rich.console import Console
from rich.markdown import Markdown
from dotenv import load_dotenv

# Configuração inicial
console = Console()
load_dotenv()

class DocumentGenerator:
    def __init__(self, model="gpt-4o"):
        if os.environ.get("OPENAI_API_KEY"):
            openai.api_key = os.environ.get("OPENAI_API_KEY")
        else:
            raise ValueError("API key não encontrada. Defina OPENAI_API_KEY no arquivo .env")
        
        self.model = model
        
        # Carrega os prompts
        with open("prompt_gerar_docs.md", "r", encoding="utf-8") as f:
            self.prompt_gerar = f.read()
        with open("prompt_validar_docs.md", "r", encoding="utf-8") as f:
            self.prompt_validar = f.read()
    
    def executar_prompt(self, prompt_content, user_input, response_format=None):
        console.print("[bold blue]Enviando requisição para a API...[/bold blue]")
        
        client = openai.OpenAI()
        params = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": prompt_content},
                {"role": "user", "content": user_input}
            ],
            "temperature": 0.7,
        }
        
        if response_format:
            params["response_format"] = response_format
            
        response = client.chat.completions.create(**params)
        return response.choices[0].message.content
    
    def gerar_documentacao(self, titulo, conceito, publico_alvo, foco_requisitos):
        user_input = f"""
# Cenário

* **Título:** {titulo}
* **Conceito da Aplicação:** {conceito}
* **Público-Alvo Principal:** {publico_alvo}
* **Foco dos Requisitos:** {foco_requisitos}
"""

        console.print("[bold green]Gerando documentação inicial...[/bold green]")
        resultado = self.executar_prompt(self.prompt_gerar, user_input, {"type": "json_object"})
        return json.loads(resultado)
    
    def validar_documentacao(self, doc_gerada):
        resumo = doc_gerada.get('resumoExecutivo', '')
        user_stories = doc_gerada.get('userStories', [])
        
        # Encontra a user story selecionada
        historia_usuario = None
        for story in user_stories:
            if story.get('selecionadaParaAC', False):
                historia_usuario = story.get('texto', '')
                break
        
        if not historia_usuario and user_stories:
            historia_usuario = user_stories[0].get('texto', '')
        
        criterios = doc_gerada.get('criteriosAceitacao', {})
        criterios_funcionais = criterios.get('criteriosFuncionais', [])
        criterios_nao_funcionais = criterios.get('criteriosNaoFuncionais', [])
        cenarios_erro = criterios.get('cenariosErro', [])
        
        user_input = f"""
- **Resumo Executivo:** {resumo}
- **Estória de Usuário:** {historia_usuario}
- **Critérios Funcionais:** {json.dumps(criterios_funcionais, ensure_ascii=False)}
- **Critérios Não-Funcionais:** {json.dumps(criterios_nao_funcionais, ensure_ascii=False)}
- **Cenários de Erro/Borda:** {json.dumps(cenarios_erro, ensure_ascii=False)}
"""

        resultado = self.executar_prompt(self.prompt_validar, user_input, {"type": "json_object"})
        return json.loads(resultado)
    
    def verificar_criterios_inaceitaveis(self, validacao):
        """Verifica se existem critérios com avaliação 'Inaceitável'"""
        criterios = validacao.get('analiseCriterios', [])
        inaceitaveis = [c for c in criterios if c.get('avaliacao') == 'Inaceitável']
        return len(inaceitaveis) > 0, inaceitaveis
    
    def verificar_necessidade_refinamento(self, validacao):
        """Verifica se há necessidade de refinamento (critérios inaceitáveis OU novos critérios sugeridos)"""
        criterios = validacao.get('analiseCriterios', [])
        inaceitaveis = [c for c in criterios if c.get('avaliacao') == 'Inaceitável']
        novos_criterios = validacao.get('novosCriterios', [])
        
        tem_inaceitaveis = len(inaceitaveis) > 0
        tem_novos_criterios = len(novos_criterios) > 0
        
        return tem_inaceitaveis or tem_novos_criterios, inaceitaveis, novos_criterios
    
    def refinar_documentacao(self, doc_gerada, validacao):
        """Refina a documentação baseado na validação"""
        console.print("[bold yellow]Refinando documentação baseado na validação...[/bold yellow]")
        
        # Extrai problemas identificados
        criterios_inaceitaveis = [c for c in validacao.get('analiseCriterios', []) if c.get('avaliacao') == 'Inaceitável']
        novos_criterios = validacao.get('novosCriterios', [])
        
        # Cria prompt de refinamento
        prompt_refinamento = f"""
Baseado na validação anterior, refine os critérios de aceitação:

PROBLEMAS IDENTIFICADOS:
{json.dumps([{'criterio': c['criterio'], 'justificativa': c['justificativa']} for c in criterios_inaceitaveis], ensure_ascii=False, indent=2)}

NOVOS CRITÉRIOS SUGERIDOS:
{json.dumps([{'criterio': c['criterio'], 'justificativa': c['justificativa']} for c in novos_criterios], ensure_ascii=False, indent=2)}

DOCUMENTAÇÃO ATUAL:
{json.dumps(doc_gerada, ensure_ascii=False, indent=2)}

Refine a documentação corrigindo os problemas e incorporando os novos critérios. Mantenha o mesmo formato JSON.
"""
        
        resultado = self.executar_prompt(self.prompt_gerar, prompt_refinamento, {"type": "json_object"})
        return json.loads(resultado)
    
    def processar_com_iteracao(self, titulo, conceito, publico_alvo, foco_requisitos, max_iteracoes=5):
        """Processa a documentação iterando até não haver critérios inaceitáveis"""
        console.print(f"[bold blue]Iniciando processo iterativo (máximo {max_iteracoes} iterações)[/bold blue]")
        
        # Gera documentação inicial
        doc_gerada = self.gerar_documentacao(titulo, conceito, publico_alvo, foco_requisitos)
        validacao = None
        
        for iteracao in range(max_iteracoes):
            console.print(f"[bold cyan]Iteração {iteracao + 1}/{max_iteracoes}[/bold cyan]")
            
            # Valida a documentação atual
            validacao = self.validar_documentacao(doc_gerada)
            
            # Verifica se há necessidade de refinamento
            precisa_refinar, criterios_inaceitaveis, novos_criterios = self.verificar_necessidade_refinamento(validacao)
            
            if not precisa_refinar:
                console.print("[bold green]✓ Documentação completa e adequada! Processo concluído.[/bold green]")
                return doc_gerada, validacao
            
            # Exibe informações sobre o que precisa ser refinado
            if criterios_inaceitaveis:
                console.print(f"[bold yellow]⚠ Encontrados {len(criterios_inaceitaveis)} critérios inaceitáveis[/bold yellow]")
                for c in criterios_inaceitaveis:
                    console.print(f"  - {c['criterio']}: {c['justificativa']}")
            
            if novos_criterios:
                console.print(f"[bold blue]💡 Encontrados {len(novos_criterios)} novos critérios sugeridos[/bold blue]")
                for c in novos_criterios:
                    console.print(f"  - {c['criterio']}: {c['justificativa']}")
            
            # Se não é a última iteração, refina a documentação
            if iteracao < max_iteracoes - 1:
                doc_gerada = self.refinar_documentacao(doc_gerada, validacao)
            else:
                console.print("[bold red]⚠ Máximo de iterações atingido. Usando última versão.[/bold red]")
        
        return doc_gerada, validacao
    
    def gerar_pdf_simples(self, titulo, doc_final):
        """Gera um PDF simples apenas com o documento final"""
        console.print("[bold blue]Gerando PDF final...[/bold blue]")
        
        data_atual = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"requisitos_final_{data_atual}.pdf"
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, titulo, 0, 1, "C")
        pdf.ln(10)
        
        # Extrai o conteúdo do documento
        doc_content = doc_final.get('documentoCompleto', '')
        
        pdf.set_font("Arial", "", 12)
        for linha in doc_content.split('\n'):
            if linha.strip():
                linha_limpa = linha.encode('latin-1', 'ignore').decode('latin-1')
                try:
                    if linha.startswith('#'):
                        pdf.set_font("Arial", "B", 14)
                        pdf.cell(0, 8, linha_limpa.replace('#', '').strip(), 0, 1)
                        pdf.set_font("Arial", "", 12)
                    else:
                        pdf.multi_cell(0, 6, linha_limpa)
                    pdf.ln(2)
                except:
                    pass
        
        pdf.output(nome_arquivo)
        console.print(f"[bold green]PDF gerado: {nome_arquivo}[/bold green]")
        return nome_arquivo

def main():
    parser = argparse.ArgumentParser(
        description="Gerador e validador de documentos de requisitos usando IA"
    )
    
    parser.add_argument(
        "--titulo", 
        type=str, 
        required=True, 
        help="Título da aplicação"
    )
    
    parser.add_argument(
        "--conceito", 
        type=str, 
        required=True, 
        help="Conceito detalhado da aplicação"
    )
    
    parser.add_argument(
        "--publico", 
        type=str, 
        required=True, 
        help="Descrição do público-alvo principal"
    )
    
    parser.add_argument(
        "--foco", 
        type=str, 
        required=True, 
        help="Foco dos requisitos (ex: engajamento, monetização, eficiência)"
    )
    
    parser.add_argument(
        "--modelo", 
        type=str, 
        default="gpt-4o", 
        help="Modelo de IA a ser utilizado (padrão: gpt-4o)"
    )
    
    args = parser.parse_args()
    
    try:
        # Inicia o gerador
        gerador = DocumentGenerator(model=args.modelo)
        
        # Processa com iteração até não haver critérios inaceitáveis
        doc_final, validacao_final = gerador.processar_com_iteracao(
            args.titulo,
            args.conceito,
            args.publico,
            args.foco
        )
        
        # Gera o PDF simples apenas com o documento final
        pdf_path = gerador.gerar_pdf_simples(args.titulo, doc_final)
        
        console.print(f"\n[bold blue]Processo concluído![/bold blue] O arquivo PDF foi salvo como [green]{pdf_path}[/green]")
        
    except Exception as e:
        console.print(f"[bold red]Erro durante a execução: {str(e)}[/bold red]")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
