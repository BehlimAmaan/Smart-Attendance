class LivenessEngine:
    def __init__(self):
        self.blink_weight = 0.3
        self.head_weight = 0.3
        self.spoof_weight = 0.4

        self.threshold = 0.7

    def calculate_score(self, blink_ok, head_ok, spoof_ok):
        score = 0.0

        if blink_ok:
            score += self.blink_weight

        if head_ok:
            score += self.head_weight

        if spoof_ok:
            score += self.spoof_weight

        return score

    def verify_liveness(self, blink_ok, head_ok, spoof_ok):
        score = self.calculate_score(blink_ok, head_ok, spoof_ok)
        return score >= self.threshold, score

    def verify_liveness(self, blink_ok, head_ok, spoof_ok):
        score = 0

        if blink_ok:
            score += 0.4
        if head_ok:
            score += 0.3
        if spoof_ok:
            score += 0.3

        return score >= 0.7, score

