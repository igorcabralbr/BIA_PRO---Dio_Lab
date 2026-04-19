# core/user_engine.py

from typing import Optional, Dict, Any


class UserEngine:
    """
    Engine responsável por gerenciar perfil do usuário
    e fornecer contexto personalizado para o Financial Brain.
    """

    def __init__(self):
        # perfil mock padrão (fallback seguro)
        # aqui serão puxados os dados dos usuarios, 
        self.user_profile = {
            "nome": "João Silva",
            "idade": 32,
            "profissao": "Analista de Sistemas",
            "renda_mensal": 5000.00,
            "perfil_investidor": "moderado",
            "objetivo_principal": "Construir reserva de emergência",
            "patrimonio_total": 15000.00,
            "reserva_emergencia_atual": 10000.00,
            "aceita_risco": False,
            "metas": [
                {
                    "meta": "Completar reserva de emergência",
                    "valor_necessario": 15000.00,
                    "prazo": "2026-06"
                },
                {
                    "meta": "Entrada do apartamento",
                    "valor_necessario": 50000.00,
                    "prazo": "2027-12"
                }
            ]
        }

    # ==============================
    # SETAR PERFIL DO USUÁRIO
    # ==============================
    def set_user_profile(self, profile: Dict[str, Any]):
        """
        Atualiza o perfil do usuário (vindo do frontend ou mock)
        """
        if not profile:
            return self.user_profile

        # merge seguro (não perde campos antigos)
        self.user_profile.update(profile)
        return self.user_profile

    # ==============================
    # OBTER PERFIL ATUAL
    # ==============================
    def get_user_profile(self) -> Dict[str, Any]:
        return self.user_profile

    # ==============================
    # GERAR INSIGHTS SIMPLES
    # ==============================
    def generate_insights(self) -> Dict[str, Any]:
        """
        Gera insights financeiros básicos baseados no perfil
        """

        profile = self.user_profile

        insights = {}

        #  taxa de reserva de emergência
        if profile.get("renda_mensal") and profile.get("reserva_emergencia_atual"):
            emergency_ratio = profile["reserva_emergencia_atual"] / (profile["renda_mensal"] * 6)

            insights["emergency_health"] = (
                "boa" if emergency_ratio >= 1 else "incompleta"
            )

        # perfil de risco
        if profile.get("perfil_investidor") == "conservador":
            insights["risk_advice"] = "Priorizar renda fixa e liquidez"
        elif profile.get("perfil_investidor") == "moderado":
            insights["risk_advice"] = "Balancear renda fixa e variável"
        elif profile.get("perfil_investidor") == "agressivo":
            insights["risk_advice"] = "Maior exposição a renda variável"

        #  progresso de metas
        metas = profile.get("metas", [])
        if metas:
            total_needed = sum(m["valor_necessario"] for m in metas)
            insights["goals_progress"] = {
                "total_meta": total_needed,
                "patrimonio": profile.get("patrimonio_total", 0)
            }

        return insights

    # ==============================
    # PERSONALIZAÇÃO DE RESPOSTA
    # ==============================
    def personalize_response(self, response: str) -> str:
        """
        Injeta contexto do usuário na resposta do sistema
        """

        profile = self.user_profile

        header = f"""
👤 Perfil: {profile.get('nome', 'Usuário')}
💼 Profissão: {profile.get('profissao', 'N/A')}
📊 Perfil: {profile.get('perfil_investidor', 'N/A')}
💰 Renda: R$ {profile.get('renda_mensal', 0):,.2f}

---

"""

        return header + response

    # ==============================
    # CONTEXTO PARA ORQUESTRADOR
    # ==============================
    def get_context(self) -> Dict[str, Any]:
        """
        Retorna tudo que o orchestrator pode usar
        """
        return {
            "profile": self.user_profile,
            "insights": self.generate_insights()
        }