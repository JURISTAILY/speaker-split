#include "neuralcompressor.h"

#include <cassert>
#include <cmath>

#include <QJsonArray>
#include <QJsonObject>

#include "trainingset.h"

double NeuralCompressor::ETA = 0.5;

NeuralCompressor::NeuralCompressor(const TrainingSet& s, int l)
    : weights(s.front().size(), l)
{
    const double SIGMA(1);

    for (int CKOKA_PA3(10); CKOKA_PA3--;) {
        //for each epoch
        for (const Sample& sample : s) {
            NeuralSpan::Distances g(weights.distance(sample));
            std::sort(g.begin(), g.end(), [](const NeuralSpan::DistanceItem& a, const NeuralSpan::DistanceItem& b) { return a.second < b.second; });

            for (int i(0); i != g.size(); ++i) {
                double* datum(weights[g[i].first]);
                const double dK(exp(-static_cast<double>(i) / SIGMA));
                for (int j(0); j != sample.size(); ++j) {
                    datum[j] += ETA * dK * (sample[j] - datum[j]);
                }
            }
        }
        weights.clearPotential();
    }

    for (TrainingSet::const_iterator it(s.begin());  it != s.end(); ++it) {
        conformity.insert(ConformityItem(weights.nearest(*it), it - s.begin()));
    }
}

QJsonArray NeuralCompressor::classify(const TrainingSet& set) const
{
    QJsonArray result;

    for (const Sample& sample : set) {
        result.insert(result.size(), sample.toJsonObject(weights.nearest(sample)));
    }
    return result;
}
