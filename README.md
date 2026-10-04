# Mirror Encoding of Secret Documents

A Python and Streamlit web application demonstrating linear-algebraic document encoding inspired by Leonardo da Vinci’s historical mirror writing. 

The application transforms plain text documents and image files into horizontally reflected (mirrored) encodings through manual matrix multiplication with an **Exchange Matrix** ($J$). Re-applying the operator decodes the document back to its exact original state without loss.

---

## Key Features

* **Manual Matrix Multiplication Engine:** Built entirely from scratch using a custom 3-nested-loop algorithm to demonstrate first-principles linear algebra without reliance on high-level matrix shortcuts.
* **Dual Medium Support:**
  * **Text Documents:** Converts typed strings or `.txt` files into ASCII scalar integer matrices with automated space padding (`ASCII 32`) for rectangular grid normalization.
  * **Image Documents:** Converts uploaded images (`.png`, `.jpg`, `.jpeg`) into single-channel 8-bit grayscale pixel matrices.
* **Interactive 3-Column Display:** Displays Original ($A$), Encoded ($E$), and Decoded ($D$) documents side-by-side in real time.
* **Raw Matrix Inspector:** Includes expandable UI views showcasing $5 \times 5$ center slices of underlying numeric matrices.
* **Lossless Verification:** Automated integrity checks (`np.array_equal(A, D)`) confirming exact 100% bit-for-bit data recovery.

---

## Mathematical Foundations

### 1. The Exchange Matrix ($J$)
An Exchange Matrix (also known as an Anti-Identity Matrix) $J$ of dimensions $W \times W$ contains $1$s along its anti-diagonal and $0$s elsewhere:

$$J_{i, j} = \begin{cases} 1 & \text{if } j = W - 1 - i \\ 0 & \text{otherwise} \end{cases}$$

### 2. Mirror Encoding Operator ($E = A \cdot J$)
Right-multiplying a document matrix $A_{H \times W}$ by $J_{W \times W}$ performs a horizontal reflection on its column vectors, mapping column $c$ to column $W - 1 - c$.

### 3. Lossless Reversibility via Involutory Property ($J^2 = I$)
Because $J$ is an **involutory matrix** ($J^2 = I$), applying the transformation operator twice simplifies algebraically back to the Identity Matrix $I$:

$$D = E \cdot J = (A \cdot J) \cdot J = A \cdot (J \cdot J) = A \cdot I = A$$

This guarantees exact recovery without requiring matrix inversion routines ($A^{-1}$).

---

## Project Structure

```text
mirror-encoding/
├── app.py              # Streamlit frontend dashboard & layout
├── matrix.py           # Core backend linear algebra engine & matrix operations
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── docs/               # Architecture diagrams and mathematical documentation

How to Run
Setup Virtual Environment
python -m venv venv
venv\Scripts\activate

Install Dependencies
pip install -r requirements.txt

Run the Program
streamlit run app.py

Upload image, text file or input text directly to perform the transformation
