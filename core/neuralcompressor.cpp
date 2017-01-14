#include "neuralcompressor.h"

#include <cassert>
#include <cmath>

#include <QJsonArray>
#include <QJsonObject>

#include "trainingset.h"

#ifndef QT_NO_DEBUG
#include "timeline.h"
#include "application.h"
#endif

double NeuralCompressor::ETA = 0.5;

NeuralCompressor::NeuralCompressor(const TrainingSet& s, int l)
    : weights(s.front().size(), l)
{
    const double SIGMA(1);

    for (int CKOKA_PA3(1000); CKOKA_PA3--;) {
        //for each epoch
        for (const Sample& sample : s) if (sample.notSilence()) {
            //norm from this sample to each neuron
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
}

QJsonArray NeuralCompressor::classify(const TrainingSet& set) const
{
    QJsonArray result;

    for (const Sample& sample : set) {
        result.insert(result.size(), sample.toJsonObject(weights.nearest(sample)));
    }
#ifndef QT_NO_DEBUG
    Timeline widget;
    QMap<double, QPair<int, bool>> data;

    for (const Sample& sample : set) {
        data.insert(sample.timeBegin(), QPair<int, bool>(weights.nearest(sample), sample.notSilence()));
    }
    widget.setData(data);
    widget.show();
    qApp->exec();
#endif
    return result;
}
