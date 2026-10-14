#!/usr/bin/env python
"""
Test baseline untuk intent detection - membandingkan dua implementasi yang ada.
Menjalankan detect_intent (app.py) dan intent_butuh_spreadsheet (answer.py)
pada dataset yang sama untuk mengidentifikasi inkonsistensi.
"""
import json
import sys
from pathlib import Path
from collections import defaultdict, Counter

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src" / "api"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "generation"))

# Import kedua fungsi intent detection
from app import detect_intent  # noqa: E402
from answer import intent_butuh_spreadsheet  # noqa: E402


def load_dataset():
    """Load dataset intent_cases.json"""
    dataset_path = PROJECT_ROOT / "tests" / "intent_cases.json"
    with open(dataset_path, encoding="utf-8") as f:
        data = json.load(f)
    return data["cases"]


def map_app_intent_to_expected(app_intent: str, expected: str) -> bool:
    """
    Map intent dari app.py ke expected label dataset.
    app.py hanya return: "definisi", "formula", "data"
    dataset punya: data, definisi, formula, hybrid, general
    """
    if expected == "data":
        return app_intent == "data"
    elif expected == "definisi":
        return app_intent == "definisi"
    elif expected == "formula":
        return app_intent == "formula"
    elif expected == "hybrid":
        # Hybrid idealnya perlu deteksi khusus, tapi app.py tidak punya
        # Untuk baseline, kita anggap salah kalau tidak detect "data"
        # (karena hybrid pasti butuh data)
        return app_intent == "data"
    elif expected == "general":
        # General idealnya dijawab langsung tanpa RAG
        # app.py akan fallback ke "definisi" untuk yang tidak match
        return app_intent == "definisi"  # toleransi untuk baseline
    return False


def map_answer_intent_to_expected(answer_intent: bool, expected: str) -> bool:
    """
    Map intent dari answer.py (True/False) ke expected label.
    answer.py hanya detect: butuh_spreadsheet (True/False)
    """
    if expected in ["data", "hybrid"]:
        return answer_intent is True
    elif expected in ["definisi", "formula", "general"]:
        return answer_intent is False
    return False


def test_both_implementations():
    """Test kedua implementasi dan bandingkan hasilnya."""
    cases = load_dataset()
    
    # Statistik per kategori
    stats_app = defaultdict(lambda: {"total": 0, "correct": 0})
    stats_answer = defaultdict(lambda: {"total": 0, "correct": 0})
    
    # Confusion matrix
    confusion_app = Counter()
    confusion_answer = Counter()
    
    # Kasus di mana keduanya berbeda
    different_decisions = []
    
    # Detail per kasus
    results = []
    
    for case in cases:
        question = case["question"]
        expected = case["expected_intent"]
        case_id = case["id"]
        
        # Test app.py detect_intent
        try:
            app_result = detect_intent(question)
            app_correct = map_app_intent_to_expected(app_result, expected)
        except Exception as e:
            app_result = f"ERROR: {e}"
            app_correct = False
        
        # Test answer.py intent_butuh_spreadsheet
        try:
            answer_result = intent_butuh_spreadsheet(question)
            answer_correct = map_answer_intent_to_expected(answer_result, expected)
        except Exception as e:
            answer_result = f"ERROR: {e}"
            answer_correct = False
        
        # Update statistik
        stats_app[expected]["total"] += 1
        stats_answer[expected]["total"] += 1
        if app_correct:
            stats_app[expected]["correct"] += 1
        if answer_correct:
            stats_answer[expected]["correct"] += 1
        
        # Confusion matrix (app.py)
        if isinstance(app_result, str) and not app_result.startswith("ERROR"):
            confusion_app[(expected, app_result)] += 1
        
        # Confusion matrix (answer.py) - map boolean ke label
        if isinstance(answer_result, bool):
            answer_label = "butuh_spreadsheet" if answer_result else "tidak_butuh_spreadsheet"
            confusion_answer[(expected, answer_label)] += 1
        
        # Deteksi perbedaan keputusan
        # Kasus kritis: app.py skip RAG (intent=data), tapi answer.py tidak butuh spreadsheet
        # atau sebaliknya
        if isinstance(app_result, str) and isinstance(answer_result, bool):
            app_skip_rag = (app_result == "data")
            answer_needs_data = answer_result
            
            if app_skip_rag != answer_needs_data:
                different_decisions.append({
                    "case_id": case_id,
                    "question": question,
                    "expected": expected,
                    "app_intent": app_result,
                    "app_skip_rag": app_skip_rag,
                    "answer_needs_spreadsheet": answer_needs_data,
                    "impact": "KONFLIK: app.py skip RAG tapi answer.py tidak butuh data" 
                              if app_skip_rag and not answer_needs_data
                              else "KONFLIK: app.py panggil RAG+answer.py tapi tidak butuh data"
                })
        
        # Simpan detail
        results.append({
            "case_id": case_id,
            "question": question,
            "expected": expected,
            "app_result": app_result,
            "app_correct": app_correct,
            "answer_result": answer_result,
            "answer_correct": answer_correct,
        })
    
    return {
        "stats_app": dict(stats_app),
        "stats_answer": dict(stats_answer),
        "confusion_app": dict(confusion_app),
        "confusion_answer": dict(confusion_answer),
        "different_decisions": different_decisions,
        "results": results,
    }


def print_report(data):
    """Print laporan hasil test."""
    print("=" * 80)
    print("BASELINE INTENT DETECTION TEST")
    print("=" * 80)
    print()
    
    # Akurasi app.py (detect_intent)
    print("1. AKURASI app.py (detect_intent)")
    print("-" * 80)
    total_app = sum(s["total"] for s in data["stats_app"].values())
    correct_app = sum(s["correct"] for s in data["stats_app"].values())
    print(f"Overall: {correct_app}/{total_app} = {correct_app/total_app*100:.1f}%")
    print()
    print("Per kategori:")
    for cat, stats in sorted(data["stats_app"].items()):
        acc = stats["correct"] / stats["total"] * 100 if stats["total"] > 0 else 0
        print(f"  {cat:10s}: {stats['correct']:2d}/{stats['total']:2d} = {acc:5.1f}%")
    print()
    
    # Akurasi answer.py (intent_butuh_spreadsheet)
    print("2. AKURASI answer.py (intent_butuh_spreadsheet)")
    print("-" * 80)
    total_answer = sum(s["total"] for s in data["stats_answer"].values())
    correct_answer = sum(s["correct"] for s in data["stats_answer"].values())
    print(f"Overall: {correct_answer}/{total_answer} = {correct_answer/total_answer*100:.1f}%")
    print()
    print("Per kategori:")
    for cat, stats in sorted(data["stats_answer"].items()):
        acc = stats["correct"] / stats["total"] * 100 if stats["total"] > 0 else 0
        print(f"  {cat:10s}: {stats['correct']:2d}/{stats['total']:2d} = {acc:5.1f}%")
    print()
    
    # Confusion matrix app.py
    print("3. CONFUSION MATRIX app.py")
    print("-" * 80)
    print(f"{'Expected':<12} | {'Predicted':<20} | Count")
    print("-" * 80)
    for (expected, predicted), count in sorted(data["confusion_app"].items()):
        print(f"{expected:<12} | {predicted:<20} | {count}")
    print()
    
    # Confusion matrix answer.py
    print("4. CONFUSION MATRIX answer.py")
    print("-" * 80)
    print(f"{'Expected':<12} | {'Predicted':<25} | Count")
    print("-" * 80)
    for (expected, predicted), count in sorted(data["confusion_answer"].items()):
        print(f"{expected:<12} | {predicted:<25} | {count}")
    print()
    
    # Kasus konflik
    print("5. KASUS KONFLIK (app.py vs answer.py)")
    print("-" * 80)
    if not data["different_decisions"]:
        print("Tidak ada konflik ditemukan.")
    else:
        print(f"Total konflik: {len(data['different_decisions'])} kasus")
        print()
        for diff in data["different_decisions"]:
            print(f"[{diff['case_id']}] {diff['question']}")
            print(f"  Expected: {diff['expected']}")
            print(f"  app.py intent: {diff['app_intent']} (skip RAG: {diff['app_skip_rag']})")
            print(f"  answer.py butuh spreadsheet: {diff['answer_needs_spreadsheet']}")
            print(f"  DAMPAK: {diff['impact']}")
            print()
    
    # Kasus salah klasifikasi menarik
    print("6. KASUS EDGE YANG SALAH KLASIFIKASI")
    print("-" * 80)
    edge_cases = [r for r in data["results"] if r["case_id"].startswith("EDGE-")]
    edge_wrong = [r for r in edge_cases if not r["app_correct"] or not r["answer_correct"]]
    if not edge_wrong:
        print("Semua edge case berhasil diklasifikasi dengan benar.")
    else:
        for case in edge_wrong:
            print(f"[{case['case_id']}] {case['question']}")
            print(f"  Expected: {case['expected']}")
            print(f"  app.py: {case['app_result']} ({'✓' if case['app_correct'] else '✗'})")
            print(f"  answer.py: {case['answer_result']} ({'✓' if case['answer_correct'] else '✗'})")
            print()


def save_report(data, output_path):
    """Simpan hasil test sebagai JSON."""
    # Convert tuple keys to string for JSON serialization
    data_json = {
        "stats_app": data["stats_app"],
        "stats_answer": data["stats_answer"],
        "confusion_app": {f"{k[0]}->{k[1]}": v for k, v in data["confusion_app"].items()},
        "confusion_answer": {f"{k[0]}->{k[1]}": v for k, v in data["confusion_answer"].items()},
        "different_decisions": data["different_decisions"],
        "results": data["results"],
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data_json, f, indent=2, ensure_ascii=False)
    print(f"Hasil test disimpan ke: {output_path}")


if __name__ == "__main__":
    print("Menjalankan baseline test untuk intent detection...")
    print()
    
    data = test_both_implementations()
    print_report(data)
    
    # Simpan hasil
    output_path = PROJECT_ROOT / "reports" / "intent_baseline_test.json"
    output_path.parent.mkdir(exist_ok=True)
    save_report(data, output_path)
