import numpy as np

class Hierarchy(object):
    def __init__(self):
        self.finalPriorities = list()

        self.crtMatr = list()
        self.crtVector = list()
        self.crtCoherence = list()

        self.altMatrs = list()
        self.altVectors = list()
        self.altCoherences = list()

        self.minimalval = 0.000001

    def getComparisonMatrix(self, values, valueReflectionMin = 1.0, valueReflectionMax = 9.0):
        result = np.identity(len(values))
        minv = 1.0
        maxv = values.max()/max([values.min(), self.minimalval])
        dminv = valueReflectionMin
        dmaxv = valueReflectionMax - valueReflectionMin
        for i in range(0, len(values)):
            for j in range(i+1, len(values)):
                (p1, p2) = (i, j) if (values[i] > values[j]) else (j, i)
                value = round(  (values[p1] / max([values[p2], self.minimalval]) - minv)
                                    * dmaxv/maxv + dminv  )
                result[p1][p2] = value
                result[p2][p1] = 1.0/value
        return result

    def getSelfVector(self, m):
        vec = [pow(np.prod(row), 1.0/len(row)) for row in m]
        return [item/sum(vec) for item in vec]

    def getCoherenceVector(self, m, v):
        return [sum(m.T[i])*v[i] for i in range(len(m))]
    def getCoherenceValue(self, m, v):
        return sum(self.getCoherenceVector(m, v))
        
    def getPriorities(self, crtPriorities, altPriorities):
        self.crtMatr = np.array(self.getComparisonMatrix(crtPriorities))
        self.crtVector = np.array(self.getSelfVector(self.crtMatr))
        self.crtCoherence = self.getCoherenceValue(self.crtMatr, self.crtVector)
        #print('Compare criteria matrixes:\n',self.crtMatr)
        #print('Self criteria vectors:', self.crtVector)
        #print('Criteria coherence:', self.crtCoherence)
        self.altMatrs = list()
        self.altVectors = list()
        self.altCoherences = list()
        for criteria in altPriorities.T:
            m = self.getComparisonMatrix(criteria)
            v = self.getSelfVector(m)
            c = self.getCoherenceValue(m, v)
            self.altMatrs.append(m)
            self.altVectors.append(v)
            self.altCoherences.append(c)
            #print(m)
            #print(v)
        #print('Compare matrixes:');
        #for m in self.altMatrs: print(m);
        #print('Self vectors:');
        #for v in self.altVectors: print(v);
        #print('Coherence:',self.altCoherences)
        self.altVectors = np.array(self.altVectors).transpose()
        self.finalPriorities = list()
        for i in range(len(self.altVectors)):
            s = 0.0
            for j in range(len(self.crtVector)):
                s+=self.crtVector[j]*self.altVectors[i][j]
            self.finalPriorities.append(s)
        return self.finalPriorities

crtPriorities = np.array([9, 7, 4])

altPriorities = np.array([[3,3,6],
                          [1,5,2],
                          [2,4,5],
                          [3,1,3]])

def main():
    print(Hierarchy().getPriorities(crtPriorities, altPriorities))

if __name__ == "__main__":
    main()


