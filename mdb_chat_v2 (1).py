"""
================================================================================
MDB CHAT - Conversational interface powered by MDB AI
================================================================================
Usage:
  python mdb_chat_v2.py                        # Chat (uses trained model)
  python mdb_chat_v2.py --demo                 # Quick demo (no training needed)
  python mdb_chat_v2.py --lm  path/to/lm.json  # Specify LM file
  python mdb_chat_v2.py --kb  path/to/kb.json  # Specify KB file
================================================================================
"""

import sys
import os
import random

try:
    from mdb_brain import MDBBrain
    from mdb_lm import MDBLanguageModel
except ImportError as e:
    print(f"Error: {e}")
    print("Make sure mdb_core.py, mdb_lm.py, and mdb_brain.py are in this folder.")
    sys.exit(1)

DEFAULT_LM = "mdb_model.json"
DEFAULT_KB = "mdb_knowledge.json"


# =============================================================================
# BUILT-IN KNOWLEDGE (works with zero training for demo purposes)
# =============================================================================

BUILTIN_FACTS = [
    # Science
    ("Gravity", "Gravity is a fundamental force that attracts objects with mass toward each other. On Earth, it gives weight to physical objects and causes them to fall toward the ground."),
    ("Light", "Light is electromagnetic radiation visible to the human eye. It travels at approximately 299,792 kilometers per second in a vacuum, making it the fastest thing in the universe."),
    ("DNA", "DNA, or deoxyribonucleic acid, is the molecule that carries genetic instructions for the development, functioning, growth, and reproduction of all known living organisms."),
    ("Evolution", "Evolution is the process of change in all forms of life over generations. Charles Darwin proposed the theory of natural selection as the primary mechanism driving evolution."),
    ("Atom", "An atom is the smallest unit of ordinary matter. It consists of a nucleus containing protons and neutrons, surrounded by electrons. The number of protons determines the element."),
    ("Black hole", "A black hole is a region of spacetime where gravity is so strong that nothing, not even light or other electromagnetic waves, can escape from it."),
    ("Photosynthesis", "Photosynthesis is the process by which plants convert sunlight, water, and carbon dioxide into oxygen and energy in the form of sugar."),
    ("Quantum mechanics", "Quantum mechanics is a fundamental theory in physics describing the behavior of matter and energy at the smallest scales. It reveals that particles can exist in multiple states simultaneously until observed."),
    ("Climate change", "Climate change refers to long-term shifts in global temperatures and weather patterns. Since the 1800s, human activities have been the main driver, primarily due to the burning of fossil fuels."),
    ("Relativity", "Einstein's theory of relativity fundamentally changed our understanding of space, time, and gravity. It established that space and time are intertwined as spacetime, and that gravity is the curvature of spacetime."),
    # Technology
    ("Artificial intelligence", "Artificial intelligence (AI) is intelligence demonstrated by machines. AI systems can perform tasks that typically require human intelligence, such as recognizing speech, making decisions, and translating languages."),
    ("Internet", "The Internet is a global system of interconnected computer networks that use standardized communication protocols to link devices worldwide. It allows billions of people to share information and communicate."),
    ("Algorithm", "An algorithm is a set of step-by-step instructions for solving a problem or accomplishing a task. Algorithms are fundamental to computing and are used in everything from search engines to navigation apps."),
    ("Computer", "A computer is an electronic device that processes data according to instructions stored in its memory. Modern computers can perform billions of calculations per second."),
    ("Machine learning", "Machine learning is a branch of AI where systems learn from data to improve their performance over time. It powers applications like image recognition, language translation, and recommendation systems."),
    # History
    ("World War II", "World War II was a global conflict from 1939 to 1945 involving most of the world's nations. It was the deadliest conflict in history, with an estimated 70 to 85 million fatalities."),
    ("Industrial Revolution", "The Industrial Revolution was a period of major industrialization from the 18th to early 19th century. It transformed manufacturing, transport, and society, beginning in Britain and spreading worldwide."),
    ("Ancient Egypt", "Ancient Egypt was a civilization that flourished along the Nile River for over 3,000 years. It is renowned for its monumental architecture, including the pyramids and the Sphinx."),
    ("Roman Empire", "The Roman Empire was one of the largest empires in ancient history. At its height, it spanned from Britain to Mesopotamia and profoundly influenced Western civilization, law, language, and culture."),
    # People
    ("Albert Einstein", "Albert Einstein was a German-born theoretical physicist who developed the theory of relativity. He is widely regarded as one of the greatest scientists of all time and won the Nobel Prize in Physics in 1921."),
    ("Isaac Newton", "Isaac Newton was an English mathematician and physicist who formulated the laws of motion and universal gravitation. His work laid the foundation for classical mechanics and calculus."),
    ("Marie Curie", "Marie Curie was a Polish-French physicist and chemist who conducted pioneering research on radioactivity. She was the first woman to win a Nobel Prize and the only person to win Nobel Prizes in two different sciences."),
    ("Charles Darwin", "Charles Darwin was an English naturalist who established the theory of evolution by natural selection. His book 'On the Origin of Species' fundamentally transformed biology."),
    ("Alan Turing", "Alan Turing was a British mathematician and computer scientist who is considered the father of theoretical computer science and artificial intelligence."),
    # Nature
    ("Ocean", "The ocean covers more than 70% of Earth's surface and contains about 97% of all water. It regulates climate, produces oxygen, and supports an enormous diversity of life."),
    ("Amazon rainforest", "The Amazon rainforest is the world's largest tropical rainforest, covering most of the Amazon basin in South America. It is home to an estimated 10% of all species on Earth."),
    ("Volcano", "A volcano is an opening in the Earth's crust through which molten rock, ash, and gases can escape. Volcanoes can form mountains and islands and have shaped much of Earth's surface."),
    ("Human brain", "The human brain is the most complex organ in the body, containing approximately 86 billion neurons. It controls all bodily functions, processes sensory information, generates thoughts, and enables consciousness."),
    # Philosophy & Culture
    ("Philosophy", "Philosophy is the study of fundamental questions about existence, knowledge, values, reason, and language. Major branches include metaphysics, epistemology, ethics, and logic."),
    ("Democracy", "Democracy is a system of government in which citizens exercise power by voting. It is characterized by free and fair elections, civil liberties, and the rule of law."),
    ("Mathematics", "Mathematics is the study of numbers, quantities, shapes, and their relationships. It underlies all sciences and technology, and provides tools for logical reasoning and problem-solving."),
    ("Music", "Music is an art form that uses organized sound to express ideas and emotions. It is universal to all human cultures and encompasses an enormous variety of styles, instruments, and traditions."),
    ("Language", "Language is a structured system of communication unique to humans. There are approximately 7,000 languages spoken worldwide, each with its own grammar, vocabulary, and sound system."),
]


# =============================================================================
# CHAT SESSION
# =============================================================================

def load_brain(lm_path: str, kb_path: str, verbose: bool = True) -> MDBBrain:
    """Load a trained brain from files."""
    brain = MDBBrain(name="MDB")

    # Load knowledge base
    if os.path.exists(kb_path):
        if verbose:
            print(f"Loading knowledge base from {kb_path}...")
        brain.load_knowledge(kb_path)
    else:
        if verbose:
            print("No knowledge base found. Using built-in facts.")

    # Always add built-in facts as a foundation
    for topic, content in BUILTIN_FACTS:
        if brain.knowledge.get(topic) is None:
            brain.teach(topic, content)

    # Load language model
    if os.path.exists(lm_path):
        if verbose:
            print(f"Loading language model from {lm_path}...")
        lm = MDBLanguageModel.load(lm_path)
        brain.set_lm(lm)
    else:
        if verbose:
            print("No language model found. (Run mdb_train.py to train one)")

    return brain


def demo_brain() -> MDBBrain:
    """Create a brain with built-in knowledge only, for instant demo."""
    brain = MDBBrain(name="MDB")
    for topic, content in BUILTIN_FACTS:
        brain.teach(topic, content)
    print(f"[DEMO] Loaded {brain.knowledge.count} built-in facts. No LM.")
    return brain


def print_banner(brain: MDBBrain):
    stats = brain.stats()
    print()
    print("╔══════════════════════════════════════════════════╗")
    print("║             MDB AI - Conversational              ║")
    print("╠══════════════════════════════════════════════════╣")
    print(f"║  Knowledge base: {stats['knowledge_facts']:>6} facts                  ║")
    lm_info = "yes" if stats['lm_attached'] else "no (run mdb_train.py)"
    print(f"║  Language model: {lm_info:<30} ║")
    print("╠══════════════════════════════════════════════════╣")
    print("║  Type anything to chat.                          ║")
    print("║  Commands: /stats  /clear  /quit                 ║")
    print("╚══════════════════════════════════════════════════╝")
    print()


def chat_loop(brain: MDBBrain):
    """Main interactive chat loop."""
    print_banner(brain)

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\nMDB: See you.")
            break

        if not user_input:
            continue

        # Handle commands
        if user_input.startswith('/'):
            cmd = user_input.lower()
            if cmd in ['/quit', '/exit', '/q']:
                print("MDB: Bye.")
                break
            elif cmd == '/stats':
                stats = brain.stats()
                print(f"\n--- MDB Stats ---")
                print(f"  Facts in KB:   {stats['knowledge_facts']}")
                print(f"  Conv. turns:   {stats['conversation_turns']}")
                if stats['lm_stats']:
                    lm = stats['lm_stats']
                    print(f"  LM vocab:      {lm['vocab_size']:,} words")
                    print(f"  LM contexts:   {lm['total_contexts']:,} SuperBits")
                print()
            elif cmd == '/clear':
                brain.memory.clear()
                print("MDB: Memory cleared.\n")
            else:
                print(f"MDB: Unknown command. Try /stats, /clear, /quit\n")
            continue

        # Generate response
        response = brain.respond(user_input)
        print(f"\nMDB: {response}\n")


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    args = sys.argv[1:]

    lm_path = DEFAULT_LM
    kb_path = DEFAULT_KB
    demo_mode = '--demo' in args

    # Parse --lm and --kb flags
    for i, arg in enumerate(args):
        if arg == '--lm' and i + 1 < len(args):
            lm_path = args[i + 1]
        if arg == '--kb' and i + 1 < len(args):
            kb_path = args[i + 1]

    if demo_mode:
        brain = demo_brain()
    else:
        brain = load_brain(lm_path, kb_path)

    chat_loop(brain)
