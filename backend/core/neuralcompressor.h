#ifndef NEURALCOMPRESSOR_H
#define NEURALCOMPRESSOR_H
class TrainingSet;
#include "neuralspan.h"
#include <map>
#include "kernel/csize.h"

class QJsonArray;

class NeuralCompressor
{
public:
    NeuralCompressor(const TrainingSet&, const int l);

    static double ETA;

    QJsonArray classify(const TrainingSet&) const;
private:
    NeuralSpan weights;
};

#endif // NEURALCOMPRESSOR_H
