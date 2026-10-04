from fileinput import close

import numpy as np
from PIL import Image, ImageDraw, ImageFont

def identity_matrix(cols):
    J=np.zeros((cols,cols), dtype=np.int32)
    for i in range(cols):
        J[i,cols-1-i] = 1
    return J

def matrix_multiply(A, J):
    rows=len(A)
    cols=len(A[0])
    E=[[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            dot_sum=0
            for k in range(cols):
                dot_sum += A[i][k]*J[k][j]
            E[i][j] = dot_sum
    return E

def encode_decode(file_buffer):
    raw_image=Image.open(file_buffer)
    raw_image.thumbnail((400,400))
    img_gray=raw_image.convert('L')
    A=np.array(img_gray,dtype=np.int32)
    rows,cols=A.shape
    J=identity_matrix(cols)
    E=np.array(matrix_multiply(A,J))
    D=np.array(matrix_multiply(E,J))
    A_img=Image.fromarray(A.astype(np.uint8))
    E_image=Image.fromarray(E.astype(np.uint8))
    D_image=Image.fromarray(D.astype(np.uint8))
    is_lossless=bool(np.array_equal(A,D))
    mid_r, mid_c = rows // 2, cols // 2
    A_slice = A[mid_r: mid_r + 5, mid_c: mid_c + 5]
    E_slice = E[mid_r: mid_r + 5, mid_c: mid_c + 5]
    D_slice = D[mid_r: mid_r + 5, mid_c: mid_c + 5]
    return A_img,E_image,D_image,is_lossless,rows,cols,A_slice,E_slice,D_slice

def text_encode_decode(text_string):
    if not text_string:
        return "","",True,0,0,[],[],[]
    lines=text_string.splitlines()
    if not lines:
        lines=[""]
    cols=max(len(line) for line in lines)
    rows=len(lines)
    A=[]
    for line in lines:
        padded_line=line.ljust(cols)
        A.append([ord(char)for char in padded_line])

    J=identity_matrix(cols)
    E_matrix=matrix_multiply(A,J)
    D_matrix=matrix_multiply(E_matrix,J)
    encoded_lines=["".join([chr(val) for val in row]) for row in E_matrix]
    decoded_lines=["".join([chr(val) for val in row]) for row in D_matrix]
    encoded_text="\n".join(encoded_lines)
    decoded_text="\n".join(decoded_lines)
    is_lossless=bool(np.array_equal(A,D_matrix))

    A_np,E_np,D_np=np.array(A),np.array(E_matrix),np.array(D_matrix)
    r_sub,c_sub=min(5,rows),min(5,cols)
    A_slice=A_np[:r_sub,:c_sub]
    E_slice=E_np[:r_sub,:c_sub]
    D_slice=D_np[:r_sub,:c_sub]
    return encoded_text,decoded_text,is_lossless,rows,cols,A_slice,E_slice,D_slice



