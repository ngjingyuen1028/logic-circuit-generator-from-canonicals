# Two-Level Boolean Logic Minimizer

A Python-based tool that converts canonical Boolean expressions (minterms or maxterms), together with don’t-care terms, into minimized **Sum of Products (SoP)** or **Product of Sums (PoS)** expressions.  
The tool also generates printable logic diagrams using `schemdraw` and `logicparse`.
---
## ⭐ Features
- Converts integer canonical terms into binary implicants  
- Handles don’t-care terms  
- Implements a Quine–McCluskey–style minimization algorithm  
- Identifies:
  - Prime implicants  
  - Essential prime implicants  
  - Minimum cover sets  
- Generates minimized 2-level Boolean expressions (SoP or PoS)  
- Produces logic circuit diagrams automatically  
- Fully interactive command-line interface  
---
## 🔧 Technologies Used
- Built-in libraries: `ast`, `itertools`
---
## 📦 Installation
Install the required dependency:
```bash
pip install schemdraw
---
## ▶️ How to Run
Run the script:
```bash
python Canonicals_to_SoP_PoS_Implementation.py

After running, follow the on-screen prompts:

1. **Choose the output form**  
   - Press **1** for Sum of Products (SoP)  
   - Press **2** for Product of Sums (PoS)  

2. **Enter the canonical terms**  
   - For SoP → enter **minterms**  
   - For PoS → enter **maxterms**  
   - Format: Python-style list  
     Example: `[1, 3, 7]`  

3. **Enter the don't-care terms**  
   - Format: Python-style list  
     Example: `[0, 2]`  

4. **Provide input variable names**  
   - Enter names from **MSB → LSB** (e.g., A, B, C)  
   - The program will automatically tell you how many inputs are needed  

5. **View the minimized Boolean expression**  
   - The program outputs the simplified SoP or PoS expression  

6. **Logic diagram generation**  
   - If the output is not a constant (0 or 1), a logic diagram will automatically be drawn using `schemdraw`
---




