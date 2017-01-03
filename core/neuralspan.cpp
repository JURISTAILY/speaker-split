#include "neuralspan.h"
#include <cstdlib>
#include <cassert>
#include <ctime>
#include <cmath>

namespace {
double sqr(const double& x) {
    return x * x;
}
}

NeuralSpan::NeuralSpan(int n, int l)
    : CMatrix(n, l)
{
    srand(time(0));
    NeuralSpan& m(*this);
    for (double* it(m[0]), *end(m[m.height() - 1] + m.width()); it != end; ++it) {
        *it = (rand() << 8) / RAND_MAX;
    }
    potential.fill(1.0, this->height());
}

double NeuralSpan::norm(const CVector& synapse, const double* row)
{
    CVector::const_iterator i(synapse.begin());
    const CVector::const_iterator end(synapse.end());

    double delta(0.0);
    while (i != end) {
        delta += sqr(*i - *row);
        ++row;
        ++i;
    }
    return sqrt(delta);
}

int NeuralSpan::nearest(const CVector& synapse) const
{
    assert(synapse.size() == this->width());
    int minRow(-1);
    const double piMin(0.75);
    double minVal(std::numeric_limits<double>::infinity());
    for (int i(0); i != this->height(); ++i) {
        //if (potential[i] > piMin) {
            const double dest(norm(synapse, (*this)[i]));
            if (dest < minVal) {
                minRow = i;
                minVal = dest;
            }
        //}
    }
    potential += 1.0 / this->height();
    potential[minRow] -= piMin;
    assert(minRow >= 0);
    return minRow;
}

void NeuralSpan::clearPotential() const
{
    potential.fill(1.0);
}

NeuralSpan::Distances NeuralSpan::distance(const CVector &sample)
{
    Distances r(this->height());
    for (int i(0); i != this->height(); ++i) {
        r[i].first = i;
        r[i].second = norm(sample, (*this)[i]);
    }
    return r;
}
