"""Connected read-only evaluation. Action and Learning explicitly complete the cycle."""
from .perception import perceive
from .attention import attend
from .reasoning import reason
from .decision import alternatives, decide, DEFAULT_WEIGHTS


def evaluate(raw: dict, memory, weights=None, top_k=5, matrix=None) -> dict:
    perception = perceive(raw)
    attention = attend(perception, top_k)
    context = memory.retrieve(attention)
    reasoning = reason(attention, context)
    decision = decide(alternatives(reasoning) if matrix is None else matrix,
                      DEFAULT_WEIGHTS if weights is None else weights)
    return {'perception': perception, 'attention': attention, 'memory': context,
            'reasoning': reasoning, 'decision': decision}
