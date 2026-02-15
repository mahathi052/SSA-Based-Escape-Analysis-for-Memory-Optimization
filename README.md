# SSA-Based Escape Analysis for Memory Optimization

A compiler-style static analysis tool that determines whether objects
should be allocated on the **stack** or **heap** using SSA-based escape analysis.

---

## 📌 Overview

This project implements a simplified escape analysis system that analyzes
pseudo-Java code and classifies objects based on whether they escape
their defining scope.

Objects that do not escape can be stack-allocated, while escaping objects
must be heap-allocated.

The system also visualizes SSA transformation and allocation decisions
through an interactive interface.

---

## 🚀 Features

- Static Single Assignment (SSA) transformation
- Escape detection via:
  - Function calls
  - Return statements
  - Global storage
- Multiple analysis modes:
  - Conservative
  - Optimistic
  - Strict
- Before vs After allocation comparison
- Summary statistics
- SSA graph visualization
- Interactive frontend built with Streamlit

---

## 🧠 How It Works

1. Accept pseudo-Java input.
2. Convert program into SSA form.
3. Track object references and data flow.
4. Detect escape conditions.
5. Classify objects as STACK or HEAP.
6. Visualize allocation results.

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Graphviz

---




## ▶️ How to Run

```bash
pip install streamlit graphviz
python -m streamlit run app.py




