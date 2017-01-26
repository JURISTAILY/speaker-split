#ifndef NEURALSPAN_H
#define NEURALSPAN_H

#include "kernel/cmatrix.h"
class CVector;

class NeuralSpan : public CMatrix
{
    mutable CVector potential;
public:
    NeuralSpan(int n, int l);

    static double norm(const CVector& synapse, const double* row);
    int nearest(const CVector& synapse) const;

    typedef std::pair<int, double> DistanceItem;
    typedef std::vector<DistanceItem> Distances;
    Distances distance(const CVector& sample);

    void clearPotential() const;
};

#endif // NEURALSPAN_H
