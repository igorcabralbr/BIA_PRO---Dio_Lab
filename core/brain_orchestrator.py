# core/brain_orchestrator.py

class BrainOrchestrator:
    def __init__(
        self,
        graph_engine,
        reasoning_engine,
        rag_engine,
        quiz_engine,
        finance_engine,
        user_engine,
        accessibility_engine,
        llm_engine=None,
    ):
        self.graph_engine = graph_engine
        self.reasoning_engine = reasoning_engine
        self.rag_engine = rag_engine
        self.quiz_engine = quiz_engine
        self.finance_engine = finance_engine
        self.user_engine = user_engine
        self.accessibility_engine = accessibility_engine

        self.llm_engine = llm_engine

    # =========================
    # MAIN ENTRY
    # =========================
    def process_query(self, query: str, user_id: str = None, user_profile: dict = None):

        try:
            user_context = {}
            resolved_profile = {}

            #  PRIORIDADE 1: profile vindo do frontend
            if user_profile:
                try:
                    self.user_engine.set_user_profile(user_profile)
                except Exception:
                    pass

            #  PRIORIDADE 2: fallback por user_id
            if user_id:
                try:
                    user_context = self.user_engine.get_context(user_id) or {}
                    resolved_profile = user_context.get("profile", {}) or {}
                except Exception:
                    pass

            #  PRIORIDADE 3: pegar do engine
            try:
                if not resolved_profile:
                    resolved_profile = self.user_engine.get_user_profile()
            except Exception:
                resolved_profile = {}

            user_context_final = {
                "profile": resolved_profile,
                "insights": self.user_engine.generate_insights()
            }

            # =========================
            # INTENT
            # =========================
            intent = self._detect_intent(query)

            # =========================
            # ROUTE
            # =========================
            try:
                raw_response = self._route(query, intent, resolved_profile)
            except Exception as e:
                raw_response = {
                    "type": "error",
                    "message": f"Erro no roteamento: {str(e)}"
                }

            # =========================
            # ACCESSIBILITY (SMART)
            # =========================
            try:
                #  NÃO quebrar quiz
                if isinstance(raw_response, dict) and raw_response.get("type") == "quiz":
                    final_response = raw_response
                else:
                    final_response = self.accessibility_engine.adapt(
                        content=raw_response,
                        user_profile=resolved_profile
                    )
            except Exception:
                final_response = raw_response

            return {
                "intent": intent,
                "response": final_response,
                "user_profile": user_context_final["profile"],
                "insights": user_context_final["insights"]
            }

        except Exception as e:
            return {
                "intent": "error",
                "response": f"Erro geral: {str(e)}",
                "user_profile": {},
                "insights": {}
            }

    # =========================
    # ROUTER
    # =========================
    def _route(self, query: str, intent: str, user_profile: dict):

        if intent == "concept":
            return self._handle_concept(query)

        if intent == "calculation":
            return self._handle_calculation(query, user_profile)

        if intent == "quiz":
            return self._handle_quiz(query, user_profile)

        if intent == "explanation":
            return self._handle_explanation(query, user_profile)

        return self._handle_general(query, user_profile)

    # =========================
    # CONCEPT
    # =========================
    def _handle_concept(self, query: str):

        try:
            concept = self.graph_engine.find_concept(query)
        except Exception:
            concept = {}

        concept_id = concept.get("id") if concept else None

        try:
            relations = self.graph_engine.get_related(concept_id) if concept_id else []
        except Exception:
            relations = []

        relations_limited = relations[:3] if relations else []

        llm_context = {
            "concept": concept,
            "relations": relations_limited
        }

        try:
            explanation = self.llm_engine.generate(
                prompt=query,
                context=llm_context,
                system_prompt="Explique de forma simples, didática e clara."
            ) if self.llm_engine else str(concept)
        except Exception:
            explanation = str(concept)

        return {
            "type": "concept",
            "concept": concept,
            "relations": relations,
            "content": explanation
        }

    # =========================
    # CALCULATION
    # =========================
    def _handle_calculation(self, query: str, user_profile: dict):

        try:
            computation = self.finance_engine.compute(query, user_context=user_profile)
        except Exception as e:
            return {"error": f"Erro no cálculo: {str(e)}"}

        try:
            explanation = self.finance_engine.explain_with_llm(
                query=query,
                computation=computation,
                user_context=user_profile or {}
            )
        except Exception:
            explanation = str(computation)

        return {
            "type": "calculation",
            "computation": computation,
            "explanation": explanation
        }

    # =========================
    # QUIZ (REFATORADO FINAL)
    # =========================
    def _handle_quiz(self, query: str, user_profile: dict):

        try:
            quiz = self.quiz_engine.generate(query, user_context=user_profile)
        except Exception as e:
            return {"error": f"Erro no quiz: {str(e)}"}

        try:
            if isinstance(quiz, dict):

                question = quiz.get("question") or quiz.get("pergunta") or "Pergunta não definida"
                options = quiz.get("options") or quiz.get("alternativas") or []
                correct = quiz.get("correct") or quiz.get("correta")

                # 🔥 GARANTE RESPOSTA CORRETA
                if not correct and options:
                    correct = options[1] if len(options) > 1 else options[0]

                return {
                    "type": "quiz",
                    "question": question,
                    "options": options,
                    "correct": correct
                }

            return {
                "type": "quiz",
                "question": "Erro ao gerar quiz",
                "options": [],
                "correct": None
            }

        except Exception:
            return {
                "type": "quiz",
                "question": "Erro inesperado no quiz",
                "options": [],
                "correct": None
            }

    # =========================
    # EXPLANATION
    # =========================
    def _handle_explanation(self, query: str, user_profile: dict):

        try:
            context = self.rag_engine.retrieve(query)
        except Exception:
            context = []

        if not context:
            return {
                "type": "fallback",
                "content": "Não encontrei dados suficientes."
            }

        try:
            reasoning = self.reasoning_engine.process(
                query=query,
                context=context,
                user_profile=user_profile
            )
        except Exception:
            reasoning = {}

        try:
            llm_context = self.reasoning_engine.prepare_for_llm(reasoning)
        except Exception:
            llm_context = reasoning

        try:
            explanation = self.llm_engine.explain_from_reasoning(
                query=query,
                reasoning_data=llm_context,
                user_profile=user_profile or {}
            ) if self.llm_engine else str(reasoning)
        except Exception:
            explanation = str(reasoning)

        return {
            "type": "explanation",
            "content": explanation
        }

    # =========================
    # GENERAL
    # =========================
    def _handle_general(self, query: str, user_profile: dict):

        try:
            context = self.rag_engine.retrieve(query)
        except Exception:
            context = []

        try:
            reasoning = self.reasoning_engine.process(
                query=query,
                context=context,
                user_profile=user_profile
            )
        except Exception:
            reasoning = {}

        try:
            llm_context = self.reasoning_engine.prepare_for_llm(reasoning)
        except Exception:
            llm_context = reasoning

        try:
            response = self.llm_engine.explain_from_reasoning(
                query=query,
                reasoning_data=llm_context,
                user_profile=user_profile or {}
            ) if self.llm_engine else str(reasoning)
        except Exception:
            response = str(reasoning)

        return {
            "type": "general",
            "content": response
        }

    # =========================
    # INTENT
    # =========================
    def _detect_intent(self, query: str) -> str:

        q = query.lower()

        #  PRIORIDADE MÁXIMA
        if "quiz" in q:
            return "quiz"

        if any(x in q for x in ["o que é", "definição"]):
            return "concept"

        if any(x in q for x in ["quanto", "calcular", "juros"]):
            return "calculation"

        if any(x in q for x in ["por que", "explique", "como funciona"]):
            return "explanation"

        return "general"