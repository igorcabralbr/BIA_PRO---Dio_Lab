# Avaliação e Métricas

## Como Avaliar seu Agente

A avaliação do agente foi pensada considerando sua arquitetura baseada em um **orquestrador central com múltiplos motores especializados (RAG, Reasoning, Graph, Finance, etc.)**.

Dessa forma, utilizamos duas abordagens complementares:

1. **Testes estruturados:** Perguntas direcionadas para validar cada engine e o comportamento do orquestrador;
2. **Feedback real:** Usuários testam o agente e avaliam a qualidade da resposta, considerando clareza, utilidade e confiança.

---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste |
|---------|--------------|------------------|
| **Assertividade** | O agente respondeu corretamente usando o engine adequado | Pergunta financeira deve acionar o Finance Engine e retornar valor correto |
| **Segurança** | O agente evita alucinação e reconhece limites | Perguntar algo fora do domínio e o agente responder que não possui essa informação |
| **Coerência** | A resposta está alinhada com o contexto e perfil do usuário | Recomendação de investimento respeita perfil conservador/moderado/agressivo |

> [!TIP]
> Foram realizados testes com múltiplos usuários simulando diferentes perfis, garantindo maior confiabilidade nas avaliações.

---

## Exemplos de Cenários de Teste

Criação de testes focados no comportamento do orquestrador e integração entre os módulos.

---

### Teste 1: Consulta de gastos
- **Pergunta:** "Quanto gastei com alimentação?"
- **Comportamento esperado:**  
  - Orquestrador identifica intenção financeira  
  - Aciona o Finance Engine  
  - Retorna valor baseado nos dados disponíveis
- **Resposta esperada:** Valor correto calculado a partir das transações
- **Resultado:** [X] Correto  [ ] Incorreto

---

### Teste 2: Recomendação de investimento
- **Pergunta:** "Qual investimento você recomenda para mim?"
- **Comportamento esperado:**  
  - Orquestrador combina Reasoning + User Engine  
  - Considera perfil do usuário  
- **Resposta esperada:** Recomendação alinhada ao perfil (ex: conservador → renda fixa)
- **Resultado:** [X] Correto  [ ] Incorreto

---

### Teste 3: Pergunta fora do escopo
- **Pergunta:** "Qual a previsão do tempo?"
- **Comportamento esperado:**  
  - Orquestrador identifica fora do domínio  
  - Não aciona engines desnecessários  
- **Resposta esperada:**  
  "Não tenho informações sobre esse tema, posso te ajudar com finanças."
- **Resultado:** [X] Correto  [ ] Incorreto

---

### Teste 4: Informação inexistente
- **Pergunta:** "Quanto rende o produto XYZ?"
- **Comportamento esperado:**  
  - RAG Engine tenta buscar  
  - Não encontra dados  
  - Orquestrador retorna fallback seguro
- **Resposta esperada:**  
  "Não encontrei informações sobre esse produto."
- **Resultado:** [X] Correto  [ ] Incorreto

---

### Teste 5: Pergunta conceitual (RAG + Reasoning)
- **Pergunta:** "O que é inflação e como ela afeta meus investimentos?"
- **Comportamento esperado:**  
  - RAG busca conceito  
  - Reasoning adapta explicação  
- **Resposta esperada:** Explicação clara + impacto prático
- **Resultado:** [X] Correto  [ ] Incorreto

---

### Teste 6: Navegação de conceitos (Graph Engine)
- **Pergunta:** "Explique a relação entre juros, inflação e poder de compra"
- **Comportamento esperado:**  
  - Graph Engine conecta conceitos  
  - Reasoning organiza explicação  
- **Resposta esperada:** Explicação estruturada mostrando relação entre os três conceitos
- **Resultado:** [X] Correto  [ ] Incorreto

---

## Resultados

Após os testes realizados:

### ✅ O que funcionou bem:
- Orquestrador consegue identificar corretamente o tipo de pergunta;
- Boa separação de responsabilidades entre os engines;
- Respostas consistentes em perguntas financeiras e conceituais;
- Sistema evita alucinações em perguntas fora do escopo;
- Integração entre RAG + Reasoning gera respostas mais completas.

---

### ⚠️ O que pode melhorar:
- Falta de memória de contexto (conversa não é contínua);
- Orquestrador ainda pode evoluir na escolha de múltiplos engines simultaneamente;
- Ausência de score de confiança nas respostas;
- Personalização ainda básica (pode evoluir com mais dados do usuário);
- Necessidade de fallback mais sofisticado em respostas ambíguas.

---

## Métricas Avançadas (Opcional)

Considerando a arquitetura modular do sistema, as seguintes métricas técnicas podem ser aplicadas:

- **Latência por engine:** Tempo de resposta individual (RAG, Reasoning, etc.);
- **Tempo total de resposta:** Tempo do orquestrador até resposta final;
- **Uso de tokens (LLM):** Monitoramento de custo e eficiência;
- **Taxa de fallback:** Quantas vezes o sistema não encontrou resposta;
- **Taxa de acerto do orquestrador:** Se escolheu o engine correto;
- **Logs de decisão:** Registro das decisões do orquestrador para análise futura.

Ferramentas recomendadas:
- LangWatch
- LangFuse

Essas ferramentas permitem observar o comportamento do agente em produção, identificar gargalos e melhorar continuamente o sistema.

---

## Conclusão

O agente demonstra uma arquitetura robusta baseada em **orquestração inteligente de múltiplos módulos**, com boa capacidade de adaptação a diferentes tipos de perguntas.

Apesar disso, ainda há oportunidades claras de evolução, principalmente em:
- Memória de longo prazo
- Aprendizado contínuo
- Melhor orquestração multi-engine

O projeto já apresenta características de sistemas modernos de IA, estando bem posicionado para evoluir para um modelo mais próximo de **multi-agentes autônomos**.
