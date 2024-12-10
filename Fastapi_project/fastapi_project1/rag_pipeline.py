import random
from typing import List, Optional

# Mock datastore for retrieval (this would usually be more complex)
mock_datastore = {
"dog": ["A dog is a domesticated mammal.", "Dogs are loyal companions.", "Dogs can be trained to perform various tasks."],
"car": ["A car is a vehicle with wheels.", "Cars run on various types of fuel.", "Cars have revolutionized transportation."],
"tree": ["A tree is a perennial plant with an elongated stem.", "Trees play a crucial role in the environment.", "Trees are essential for oxygen production."],
"elephant": ["An elephant is the largest land mammal.", "Elephants are known for their long trunks.", "Elephants have a strong social structure."],
"python": ["Python is a programming language.", "Python is a type of snake.", "Python is great for AI development."],
"banana": ["Bananas are a tropical fruit.", "Bananas are rich in potassium.", "Bananas grow on plants, not trees."],
"moon": ["The moon orbits the Earth.", "The moon has a significant impact on Earth's tides.", "The moon has been a source of fascination for humans."],
"book": ["A book is a collection of written or printed pages.", "Books are a source of knowledge.", "Books can be both fiction and non-fiction."],
"coffee": ["Coffee is a popular beverage.", "Coffee is made from roasted coffee beans.", "Coffee is often consumed to stay awake."],
"carrot": ["A carrot is a root vegetable.", "Carrots are known for their orange color.", "Carrots are rich in beta-carotene."],
}


def retrieve(query: str, top_k: int) -> List[str]:
    """Simulate the retrieval of relevant contexts from the datastore."""
    key = query.lower()  # For simplicity, use the query directly as the key
    contexts = mock_datastore.get(key, [])
    return contexts[:top_k]  # Limit to top_k contexts


def generate_response(query: str, contexts: List[str]) -> str:
    """Simulate response generation by combining the query and retrieved contexts."""
    if not contexts:
        return "No relevant information found."

    # Simple logic to generate a mock response
    context_summary = " ".join(contexts)
    return f"Query: {query}\nGenerated based on context: {context_summary}"
