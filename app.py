import streamlit as st
import sympy as sp

# Define variables
x, y, z = sp.symbols('x y z')

# Function to calculate divergence and curl
def calculate_divergence_and_curl(Fx, Fy, Fz):
    F = sp.Matrix([Fx, Fy, Fz])
    vars = (x, y, z)

    # Divergence
    divergence = sum(sp.diff(F[i], vars[i]) for i in range(3))

    # Curl
    curl = sp.Matrix([
        sp.diff(F[2], y) - sp.diff(F[1], z),
        sp.diff(F[0], z) - sp.diff(F[2], x),
        sp.diff(F[1], x) - sp.diff(F[0], y)
    ])

    return divergence, curl, F

# --- Custom CSS for Dark Theme ---
st.markdown("""
    <style>
        .stApp {
            background-color: #0E1117;
            color: white;
            font-family: 'Courier New', monospace;
        }
        .stTextInput > div > div > input {
            background-color: #262730;
            color: white;
        }
        .stButton>button {
            background-color: #08F7FE;
            color: black;
            font-weight: bold;
            border-radius: 10px;
            height: 3em;
            width: 10em;
        }
        .custom-box {
            background-color: #1A1C23;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #08F7FE;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Title and Description ---
st.title("🌌 Vector Field Calculator")
st.caption("Analyze a **vector function** \\( \\vec{F}(x, y, z) \\): Compute **Divergence** and **Curl** 🧮")

# --- Input Section with Border Only ---
st.markdown('<div class="custom-box">', unsafe_allow_html=True)
st.markdown("### 📥 Enter Vector Function Components")
Fx_input = st.text_input("Fₓ(x, y, z)", "y*z")
Fy_input = st.text_input("Fᵧ(x, y, z)", "x*z")
Fz_input = st.text_input("F𝓏(x, y, z)", "x*y")
st.markdown('</div>', unsafe_allow_html=True)

# --- Compute and Display ---
if st.button("Calculate"):
    try:
        # Convert inputs to SymPy expressions
        Fx = sp.sympify(Fx_input)
        Fy = sp.sympify(Fy_input)
        Fz = sp.sympify(Fz_input)

        # Calculate
        divergence, curl, F = calculate_divergence_and_curl(Fx, Fy, Fz)

        # Display vector function and results
        st.markdown("### 📌 Vector Function")
        st.latex(r"\vec{F}(x, y, z) = " + 
                 r"\begin{bmatrix}" +
                 sp.latex(F[0]) + r"\\" +
                 sp.latex(F[1]) + r"\\" +
                 sp.latex(F[2]) + r"\end{bmatrix}")

        st.markdown("### 🧮 Results")
        st.latex(r"\text{Divergence } (\nabla \cdot \vec{F}) = " + sp.latex(sp.simplify(divergence)))
        st.latex(r"\text{Curl } (\nabla \times \vec{F}) = " +
                 r"\begin{bmatrix}" + r"\\".join([sp.latex(sp.simplify(c)) for c in curl]) + r"\end{bmatrix}")

        # Interpretation
        if all(sp.simplify(c) == 0 for c in curl):
            st.success("✅ The vector field is **Irrotational** (Curl = 0)")
        else:
            st.error("❌ The vector field is **NOT Irrotational**")

        if sp.simplify(divergence) == 0:
            st.success("✅ The vector field is **Solenoidal** (Divergence = 0)")
        else:
            st.error("❌ The vector field is **NOT Solenoidal**")

    except Exception as e:
        st.error(f"⚠️ Error in input: {e}")
