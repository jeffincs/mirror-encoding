import streamlit as st
from PIL import Image
from matrix import encode_decode, text_encode_decode

st.set_page_config(page_title="Mirror Encoding", layout="wide")
st.title("Secret Document Mirror Encoding and Decoding")
st.header("1. Text Document")
input_mode=st.radio("Select Text Input Method:",["Type Text directly","Upload .txt File"],horizontal=True)
text_content=""
if input_mode=="Upload .txt File":
    uploaded_txt=st.file_uploader("Upload Text Document (.txt)", type=["txt"])
    if uploaded_txt is not None:
        text_content=uploaded_txt.read().decode("utf-8")
else:
    text_content=st.text_area("Type or paste secret document text here: ","Vinci Secret Research Document",height=150)
if text_content:
    enc_text,dec_text,is_lossless,rows,cols,A_slice,E_slice,D_slice=text_encode_decode(text_content)
    st.success(f"Text Document Processed! ASCII Matrix Dimensions: **{rows} rows x {cols} columns**")
    col1,col2,col3=st.columns(3)
    with col1:
        st.subheader("Original Text(A)")
        st.code(text_content,language="text")
    with col2:
        st.subheader("Encoded Text (E=AxJ)")
        st.code(enc_text,language="text")
    with col3:
        st.subheader("Decoded Text (D=ExJ)")
        st.code(dec_text,language="text")
    st.divider()
    with st.expander("Raw ASCII Matrix Values"):
        st.write("Displays character ASCII scalar values insider matrix $A$,$E$, and $D$")
        c1,c2,c3=st.columns(3)
        with c1:
            st.caption("**Matrix $A$ (Original ASCII)**")
            st.dataframe(A_slice)
        with c2:
            st.caption("**Matrix $E$ (Encoded ASCII)**")
            st.dataframe(E_slice)
        with c3:
            st.caption("**Matrix $D$ (Decoded ASCII)**")
            st.dataframe(D_slice)
    if is_lossless:
        st.info("Mathematical Verification Passed: Original Text == Decoded Text (A=D)")
    else:
        st.error("Verification Failed.")

st.divider()
st.header("2. Image Document")
uploaded_file=st.file_uploader("Document/Image file: ",type=["png","jpg","jpeg"])
if uploaded_file is not None:
    A_img,E_img,D_img,is_lossless,rows,cols,A_slice,E_slice,D_slice=encode_decode(uploaded_file)
    st.success(f"File Processed! Matrix Dimensions: **{rows} rows x {cols} columns**")
    col1,col2,col3=st.columns(3)
    with col1:
        st.subheader("Original Document (A)")
        st.image(A_img, use_container_width=True)
    with col2:
        st.subheader("Encoded Document (E=A x J)")
        st.image(E_img, use_container_width=True)
    with col3:
        st.subheader("Decoded Document (D=E x J)")
        st.image(D_img, use_container_width=True)
    st.divider()
    with st.expander("Raw Matrix Values"):
        st.write("This shows actual 8-bit grayscale values")
        c1,c2,c3=st.columns(3)
        with c1:
            st.caption("**Matrix $A$ (Original Pixel Values)**")
            st.dataframe(A_slice)
        with c2:
            st.caption("**Matrix $E$ (Encoded Pixel Values)**")
            st.dataframe(E_slice)
        with c3:
            st.caption("**Matrix $D$ (Decoded Pixel Values)**")
            st.dataframe(D_slice)

    if is_lossless:
        st.info("Mathematical Verification: (A=D)")
    else:
        st.error("Verification Failed.")