import time
from rouge_score import rouge_scorer
from collections import Counter

class MetricsTracker:
    def __init__(self):
        self.scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)

    def calculate_latency(self, start_time):
        """Calculates execution time in ms"""
        return (time.time() - start_time) * 1000

    def calculate_basic_metrics(self, generated_answer, reference_context):
        """
        Calculates ROUGE scores against the retrieved context
        """
        scores = self.scorer.score(reference_context, generated_answer)
        
        # Simple F1 calculation based on token overlap
        gen_tokens = generated_answer.lower().split()
        ref_tokens = reference_context.lower().split()
        common = Counter(gen_tokens) & Counter(ref_tokens)
        num_same = sum(common.values())
        
        if len(gen_tokens) == 0 or len(ref_tokens) == 0:
            f1 = 0.0
        else:
            precision = num_same / len(gen_tokens)
            recall = num_same / len(ref_tokens)
            f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        return {
            "rouge1": round(scores['rouge1'].fmeasure, 3),
            "rougeL": round(scores['rougeL'].fmeasure, 3),
            "custom_f1": round(f1, 3)
        }
