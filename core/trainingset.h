#ifndef TRAININGSET_H
#define TRAININGSET_H

#include <vector>
#include "sample.h"

class QString;

class TrainingSet : public std::vector<Sample>
{
public:
    TrainingSet(const QString& fName);
};

#endif // TRAININGSET_H
