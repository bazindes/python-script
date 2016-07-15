#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__=''

import sys

print('please input the row scale of matrix A')
matrixA_Rscale = int(input())
print('please input the col scale of matrix A')
matrixA_Cscale = int(input())
matrixA = []
for i in range(matrixA_Rscale):
    matrixAj = []
    for j in range(matrixA_Cscale):
        print('please input the element in position (%d,%d) of matrix A' % (i,j))
        matrixAij = int(input())
        matrixAj.append(matrixAij)
    matrixA.append(matrixAj)

print('row scale of matrix B is %d,%d' % (matrixA_Cscale,matrixA_Rscale))
matrixB_Rscale = matrixA_Cscale
matrixB_Cscale = matrixA_Rscale
matrixB = []
for i in range(matrixB_Rscale):
    matrixBj = []
    for j in range(matrixB_Cscale):
        print('please input the element in position (%d,%d) of matrix B' % (i,j))
        matrixBij = int(input())
        matrixBj.append(matrixBij)
    matrixB.append(matrixBj)

matrixC = []
for i in range(matrixA_Rscale):
    matrixCi = []
    for j in range(matrixA_Rscale):
        matrixCij = 0
        for k in range(matrixA_Cscale):
            matrixCij += matrixA[i][k] * matrixB[k][j]
        matrixCi.append(matrixCij)
    matrixC.append(matrixCi)

print('matrix A:')
for i in range(matrixA_Rscale):
    for j in range(matrixA_Cscale):
        sys.stdout.write(str(matrixA[i][j]) + ' ')
        sys.stdout.flush()
    print('')

print('matrix B:')
for i in range(matrixB_Rscale):
    for j in range(matrixB_Cscale):
        sys.stdout.write(str(matrixB[i][j]) + ' ')
        sys.stdout.flush()
    print('')

print('A * B:')
for i in range(len(matrixC)):
    for j in range(len(matrixC[i])):
        sys.stdout.write(str(matrixC[i][j]) + ' ')
        sys.stdout.flush()
    print('')