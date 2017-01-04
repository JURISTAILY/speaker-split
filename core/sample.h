#ifndef SAMPLE_H
#define SAMPLE_H

#include "kernel/cvector.h"

class QJsonValue;

class Sample : public CVector
{
    bool speech;
    double timestamp;
    int classId;

    static const QString SPEACH_KEY;
    static const QString TIMESTAP_KEY;
    static const QString FEATURES_KEY;
    static const QString CLASS_KEY;

public:
    Sample(const QJsonValue&);

    QJsonObject toJsonObject(const int classId = -1) const;
    double timeBegin() const { return timestamp; }
};

#endif // SAMPLE_H
