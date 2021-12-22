# coding=utf-8
import bitarray as ba
import numpy as np
import itertools
class CyclicCodes:

    def __init__(self):
        self.k = int(7)
        self.n = int(15)
        self.g = ba.bitarray('100010111')
        self.t = int(2)

    def Encode(self, input):
            c = ba.bitarray('000000000000000')
            g1 = self.g
            for i in range(0, self.k):
                if input[i] == 1:
                    c[i:i + 9] ^= g1
            return c

    def Remainder(self, input):
            r = ba.bitarray()
            r.extend(input)
            for i in range(self.n - 1, self.n - self.k - 1, -1):
                if r[i] == 1:
                    r[i - (self.n - self.k): i + 1] ^= self.g

            return r

    def EncodySys(self, inp):
            new_in = ba.bitarray('0000000')
            new_in[self.n - self.k:] = inp
            rem = self.Remainder(new_in)
            new_in[:self.n - self.k] = rem[:self.n - self.k]
            return new_in
    def WH(self, a):  # расчёт веса Хэмминга
        wt = 0
        for i in range(int(len(a))):
            if (a[i]):
                wt += 1
        return wt

    @property
    def MakeTable(self):
        syndromes = {}
        n = [0, 1]
        l = 15
        r = list(itertools.product(n, repeat=l))
        for i in range(0, len(r)):
            rr = ba.bitarray(r[i])
            wt = 0
            for j in range(0, 15):
                if rr[j] == 1:
                    wt = wt + 1

            if wt <= self.t:
                ss = self.Remainder(rr)
                u = int(ss.to01(), 2)
                syndromes[u] = rr


        return syndromes

    def Read(self, name):  # чтение из файла
        path = "C:\\Users\\Маша\\PycharmProjects\\TK3-maybe\\" + name
        f = open(path, 'rb')
        v = ba.bitarray()
        v.fromfile(f)
        return v

    def Write(self, name, v):  # запись в файл
        path = "C:\\Users\\Маша\\PycharmProjects\\TK3-maybe\\" + name
        f = open(path, 'wb')
        v.tofile(f)

    def Code(self, a):
        cr = []
        for i in range(len(a) //7):
            a_p = np.array([a[i * 7], a[(i * 7) + 1], a[(i * 7) + 2], a[(i * 7) + 3], a[(i * 7) + 4], a[(i * 7) + 5], a[(i * 7) + 6]])
            a_2p = self.Encode(a_p)
            cr.extend(a_2p)
        bit = ba.bitarray()
        bit.extend(cr)
        return bit

    def Correct(self, a):
        synd = self.MakeTable
        k = list(synd.keys())
        cr2 = ba.bitarray()
        cr3 = ba.bitarray()
        zero = ba.bitarray('000000000000000')
        for i in range(len(a)//15):
            cr = np.array([a[i*15], a[(i*15)+1],  a[(i*15)+2],  a[(i*15)+3],  a[(i*15)+4],  a[(i*15)+5],  a[(i*15)+6], a[(i*15)+7], a[(i*15)+8],
                           a[(i*15)+9], a[(i*15)+10], a[(i*15)+11], a[(i*15)+12], a[(i*15)+13], a[(i*15)+14]])
            t = ba.bitarray()
            t.extend(cr)
            ad = self.Remainder(t)
            wt = self.WH(ad)
            if wt <= self.t:
                for j in range(len(k)):
                    z=k[j]
                    if (ad==synd[z]):
                        c1 = (t ^ ad)
                        cr2.extend(c1)
        bit = ba.bitarray()
        bit.extend(cr2)
        return bit

    def Err_imitation(self, a):
        a2= ba.bitarray()
        for i in range(len(a)//15):
            a[i*15] = not a[i]
        a2.extend(a)
        return a2

    def Decode(self, a):
        cr2 = ba.bitarray()
        cr3 = ba.bitarray()
        for i in range(len(a) // 15):
            cr = np.array([a[i*15], a[(i*15)+1],  a[(i*15)+2],  a[(i*15)+3],  a[(i*15)+4],  a[(i*15)+5],  a[(i*15)+6], a[(i*15)+7], a[(i*15)+8],
                           a[(i*15)+9], a[(i*15)+10], a[(i*15)+11], a[(i*15)+12], a[(i*15)+13], a[(i*15)+14]])
            t = ba.bitarray()
            t.extend(cr)
            ad = self.Encode(t)
            cr2.extend(ad)
        for i in range(len(cr2)//15):
            cr3.extend([cr2[i*15], cr2[(i*15)+1], cr2[(i*15)+2], cr2[(i*15)+3], cr2[(i*15)+4], cr2[(i*15)+5], cr2[(i*15)+6]])
        bit = ba.bitarray()
        bit.extend(cr3)
        return bit




CC = CyclicCodes()
inp1 = ba.bitarray('101110111')
res2 = CC.Encode(inp1)
print("№2 \nВходной сигнал: ", inp1, "\nВыходной сигнал:", res2)
inp2 = ba.bitarray('100010101101101')
res3 = CC.Remainder(inp2)
print("№3 \nВходной сигнал: ", inp2, "\nВыходной сигнал:", res3[:3])
res4 = CC.EncodySys(inp1)
print("№4 \nInput signal: Входной сигнал: ", inp1, "\nВыходной сигнал:", res4)
res5 = CC.MakeTable
print("№5", res5)

print("№6\nПример без ошибки")
a1 = CC.Read("code.txt")
b1 = CC.Code(a1)
c1 = CC.Decode(b1)
d1 = CC.Correct(b1)
e = CC.Decode(d1)
print("Считанный файл : ", a1, "\nЗакодированное: ", b1, "\nИсправленное  : ", d1, "\nДекодированное: \nДо проверки    :", c1, "\nПосле проверки :", e)
print("\nПример с ошибкой")
a2 = CC.Read("code.txt")
b2 = CC.Code(a2)
err = CC.Err_imitation(b1)
correct = CC.Correct(err)
c2 = CC.Decode(correct)
c3 = CC.Write("result.txt", e)

print("Считанный файл : ", a2, "\nЗакодированное: ", b2, "\nИмитир. ошибки: ", err, "\nИсправленное  : ", correct, "\nДекодированное: ", c2)

