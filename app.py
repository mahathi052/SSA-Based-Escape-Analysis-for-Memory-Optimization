import streamlit as st
from backend import analyze_program
from ssa_graph import build_ssa_graph

# Page config
st.set_page_config(
    page_title="Escape Analysis Tool",
    layout="wide"
)

# Title
st.title("SSA-Based Escape Analysis")
st.caption("Memory Allocation Optimization Tool")

st.markdown("""
Analyze whether objects should be allocated on the **stack** or **heap**
using SSA-based escape analysis.
""")

# Sidebar
with st.sidebar:
    st.header("About")
    st.write("""
    This tool performs static escape analysis on pseudo-Java code.
    It determines whether objects can be safely stack-allocated
    or must be heap-allocated.
    """)

    st.markdown("### Escape Conditions")
    st.write("- Returned from method")
    st.write("- Passed to function")
    st.write("- Stored globally")

    st.markdown("### Modes")
    st.write("**Conservative:** Calls cause escape")
    st.write("**Optimistic:** Ignore calls")
    st.write("**Strict:** Everything escapes")

# Mode selector
mode = st.selectbox(
    "Select Escape Analysis Mode",
    ["conservative", "optimistic", "strict"]
)

# Example loader
if st.button("Load Example"):
    st.session_state.code_input = "a = new A\nb = a\ncall foo b"

# Code input
st.subheader("Enter Program (Pseudo Java)")

if "code_input" not in st.session_state:
    st.session_state.code_input = ""

code = st.text_area(
    "",
    height=200,
    key="code_input",
    placeholder="Example:\na = new A\nb = a\ncall foo b"
)

# Run analysis
if st.button("Run Escape Analysis"):

    if code.strip() == "":
        st.warning("Please enter some code.")
    else:
        ssa_code, allocation, heapified, reasons = analyze_program(code, mode)

        # BEFORE allocation (optimistic stack)
        before_allocation = {obj: "STACK" for obj in allocation.keys()}

        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(
            ["SSA Form", "Allocation (Before vs After)", "Summary", "Graph"]
        )

        # ---------------------------
        # TAB 1: SSA FORM
        # ---------------------------
        with tab1:
            st.subheader("SSA Representation")
            for stmt in ssa_code:
                st.code(str(stmt))

        # ---------------------------
        # TAB 2: ALLOCATION
        # ---------------------------
        with tab2:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### Before Escape Analysis")
                for obj in before_allocation:
                    st.success(f"{obj} → STACK")

            with col2:
                st.markdown("### After Escape Analysis")
                for obj, alloc in allocation.items():
                    if alloc == "HEAP":
                        reason = reasons.get(obj, "Escaped")
                        st.error(f"{obj} → HEAP | Reason: {reason}")
                    else:
                        st.success(f"{obj} → STACK")

        # ---------------------------
        # TAB 3: SUMMARY
        # ---------------------------
        with tab3:
            st.subheader("Analysis Summary")

            total_objects = len(allocation)
            stack_count = sum(1 for v in allocation.values() if v == "STACK")
            heap_count = sum(1 for v in allocation.values() if v == "HEAP")
            heapified_count = len(heapified)

            st.write(f"Total objects created: {total_objects}")
            st.write(f"Stack allocated: {stack_count}")
            st.write(f"Heap allocated: {heap_count}")
            st.write(f"Heapified after escape: {heapified_count}")

        # ---------------------------
        # TAB 4: GRAPH
        # ---------------------------
        with tab4:
            st.subheader("SSA Graph Visualization")
            graph = build_ssa_graph(ssa_code, allocation, heapified)
            st.graphviz_chart(graph)
