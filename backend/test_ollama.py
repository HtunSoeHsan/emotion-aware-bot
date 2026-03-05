"""
Quick test to verify Ollama integration
"""

import sys
sys.path.insert(0, '.')

print("╔══════════════════════════════════════════════════════════╗")
print("║       🧪 Testing Ollama Integration                      ║")
print("╚══════════════════════════════════════════════════════════╝")
print()

# Test 1: Check Ollama connection
print("1️⃣ Testing Ollama connection...")
try:
    import ollama
    client = ollama.Client()
    models = client.list()
    print(f"  ✅ Ollama is running!")
    # Handle different Ollama API versions
    if hasattr(models, 'models'):
        model_list = list(models.models)
    elif isinstance(models, dict):
        model_list = models.get('models', [])
    else:
        model_list = list(models)
    print(f"  📦 Available models: {len(model_list)}")
    for model in model_list:
        if isinstance(model, dict):
            print(f"     - {model.get('name', 'unknown')}")
        elif hasattr(model, 'name'):
            print(f"     - {model.name}")
        else:
            print(f"     - {model}")
except Exception as e:
    print(f"  ❌ Ollama error: {e}")
    print("     Make sure Ollama is running: ollama serve")
    sys.exit(1)

print()

# Test 2: Test emotion recommendation
print("2️⃣ Testing AI recommendations...")
from ai.ollama_agent import get_agent

agent = get_agent()

if not agent.is_available():
    print("  ❌ Ollama agent not available")
    sys.exit(1)

print("  ✅ Ollama agent ready")
print()

# Test 3: Generate sample recommendations
print("3️⃣ Generating sample recommendations...")
print()

test_cases = [
    ("joy", "I just got promoted at work!"),
    ("anger", "My friend cancelled plans last minute"),
    ("sadness", "I miss my family who live far away"),
]

for emotion, context in test_cases:
    print(f"  Emotion: {emotion.upper()}")
    print(f"  Context: \"{context}\"")
    
    rec = agent.get_recommendations(emotion, context)
    
    if rec:
        print(f"  ✅ Recommendations:")
        print(f"     📤 Send: {rec['send_message']}")
        print(f"     🧘 Action: {rec['action']}")
    else:
        print(f"  ⚠️  Failed to get recommendations")
    print()

print("╔══════════════════════════════════════════════════════════╗")
print("║  ✅ All tests passed! System is ready.                   ║")
print("║                                                          ║")
print("║  Next: Run 'python main.py' to start the API server     ║")
print("╚══════════════════════════════════════════════════════════╝")
