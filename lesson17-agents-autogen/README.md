# Lesson 17 — AI Agents with AutoGen (Ollama)

This project implements **Lesson 17** of the *Generative AI for Beginners* course.

The assignment demonstrates a **multi-agent system** using **AutoGen**, where different departments of an education startup participate in a simulated business meeting.

The system runs **fully locally** using **Ollama** and the **phi3:mini** model.

---

## 🎯 Assignment Goal

Simulate a business meeting where:
- The user pitches a new product idea
- Multiple AI agents represent different departments
- Each department asks follow-up questions to refine the product idea

Departments:
- Product
- Engineering
- Marketing
- Finance

Each agent has:
- A distinct persona
- Clear priorities
- The same pitch as input
- Independent reasoning and output

---

## 🧠 Architecture Overview

- **Framework:** AutoGen (core + ext)
- **Model Runtime:** Ollama (local)
- **LLM:** `phi3:mini`
- **Communication:** Direct HTTP calls to Ollama API
- **UI:** Command-line (CLI)

No cloud APIs are used.

---

## 📁 Project Structure