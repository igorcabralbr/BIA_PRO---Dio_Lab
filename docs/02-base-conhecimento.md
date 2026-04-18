# Base de Conhecimento

## Dados Utilizados

O projeto utiliza uma base de conhecimento estruturada em arquivos JSON para simular um ambiente de aprendizado financeiro inteligente, com suporte a raciocínio, navegação conceitual e personalização.

| Arquivo                        | Formato | Utilização no Agente                                                                                                 |
| ------------------------------ | ------- | -------------------------------------------------------------------------------------------------------------------- |
| `concepts.json`                | JSON    | Armazena conceitos financeiros (ex: juros compostos, inflação) utilizados pelo Graph Engine para navegação semântica |
| `relations.json`               | JSON    | Define relações entre conceitos (grafo), permitindo explicações encadeadas e aprendizado progressivo                 |
| `quizzes.json`                 | JSON    | Contém perguntas e respostas para o Quiz Engine, permitindo validação de conhecimento do usuário                     |
| `user_profile.json`            | JSON    | Armazena preferências e nível do usuário para personalização das respostas                                           |
| (futuro) `financial_data.json` | JSON    | Simula dados financeiros para cálculos e análises no Finance Engine                                                  |

> [!TIP]
> **Quer um dataset mais robusto?** O projeto pode ser facilmente expandido para utilizar datasets reais do Hugging Face ou APIs financeiras, integrando-os ao RAG Engine para respostas mais precisas.

---

## Adaptações nos Dados

Os dados mockados foram estruturados para simular um **grafo de conhecimento financeiro**, permitindo:

* Navegação entre conceitos relacionados (ex: juros → inflação → poder de compra)
* Explicações progressivas (nível iniciante até avançado)
* Base para raciocínio híbrido (Graph + Reasoning Engine)

Além disso:

* Os conceitos foram simplificados para facilitar explicações didáticas
* As relações foram organizadas para suportar traversal (busca em profundidade/largura)
* Os quizzes foram pensados como extensão do aprendizado (modo mentor)

---

## Estratégia de Integração

### Como os dados são carregados?

Os arquivos JSON são carregados no início da execução do sistema pelos respectivos engines:

* `graph_engine.py` → carrega `concepts.json` e `relations.json`
* `quiz_engine.py` → carrega `quizzes.json`
* `rag_engine.py` → pode carregar documentos ou embeddings (simulado atualmente)

O carregamento ocorre em memória, permitindo acesso rápido durante a execução do orquestrador.

---

### Como os dados são usados no prompt?

Os dados **não são inseridos diretamente no system prompt de forma estática**.

Em vez disso, o sistema utiliza uma abordagem dinâmica:

1. O **Brain Orchestrator** interpreta a intenção do usuário
2. Seleciona o(s) engine(s) adequado(s)
3. Cada engine consulta os dados relevantes
4. O resultado é retornado e **injetado no contexto da resposta**

Exemplos:

* Graph Engine → retorna explicações baseadas no grafo
* RAG Engine → recupera contexto relevante
* Quiz Engine → gera perguntas baseadas no progresso

👉 Isso evita prompts grandes e melhora eficiência e precisão

---

## Exemplo de Contexto Montado

Abaixo um exemplo de como o contexto pode ser estruturado internamente antes de gerar a resposta final:

```
Contexto de Conhecimento:

Conceito atual: Juros Compostos
Descrição: Juros sobre juros acumulados ao longo do tempo

Relações:
- Relacionado a: Inflação
- Impacta: Poder de compra
- Usado em: Investimentos

Nível do usuário: Iniciante

Modo ativo: Mentor Inteligente

Resposta esperada:
- Explicação simples
- Exemplo prático
- Possível pergunta para reforço
```

---

Esse formato permite que o sistema funcione como um **mentor adaptativo**, combinando:

* Recuperação de conhecimento (RAG)
* Navegação em grafo (Graph Engine)
* Raciocínio (Reasoning Engine)
* Personalização (User Engine)
* Ensino ativo (Quiz Engine)
