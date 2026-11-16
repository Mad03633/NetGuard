"""T4: transparent rules combining attended evidence and learned context."""


def reason(attention: dict, memory: dict) -> dict:
    base = attention['signal_risk']
    # Evidence strength increases smoothly and is bounded, limiting feedback poisoning.
    strength = min(.65, memory['confirmed'] / (memory['confirmed'] + 2))
    risk = (1 - strength) * base + strength * memory['posterior']
    risk = min(.99, max(.01, risk))
    level = 'HIGH' if risk >= .70 else 'MEDIUM' if risk >= .35 else 'LOW'
    steps = [f'R1: risk = 0.08 + 0.87 × selected weighted signals = {base:.4f}',
             f'R2: verified {memory["attacks"]} attack / {memory["benign"]} benign; Beta({memory["alpha"]}, {memory["beta"]}) mean = {memory["posterior"]:.4f}',
             f'R3: feedback strength = min(0.65, n/(n+2)) = {strength:.4f}; combined risk = {risk:.4f}',
             f'R4: LOW < 0.35; MEDIUM < 0.70; otherwise HIGH. Result: {level}']
    return {'risk': risk, 'base_risk': base, 'level': level, 'steps': steps,
            'learned_strength': strength, 'pattern': attention['pattern']}
