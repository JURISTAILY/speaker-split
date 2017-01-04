#include "sample.h"

#include <QJsonValue>
#include <QJsonObject>
#include <QJsonArray>
#include <QString>
#include <QDebug>

const QString Sample::SPEACH_KEY = QString("is_speech");
const QString Sample::TIMESTAP_KEY = QString("timestamp");
const QString Sample::FEATURES_KEY = QString("features");
const QString Sample::CLASS_KEY = QString("class");

Sample::Sample(const QJsonValue& data)
{
    if (!data.isObject()) {
        qFatal("unexpected input sample data (data must be an object)");
    }
    const QJsonObject obj(data.toObject());
    if (!obj.contains(SPEACH_KEY)) {
        qDebug() << "unexpected input sample data (data should have a speach sign)";
    }
    speech = obj.value(SPEACH_KEY).toBool();
    if (!obj.contains(TIMESTAP_KEY)) {
        qDebug() << "unexpected input sample data (data should have a time stap datum)";
    }
    timestamp = obj.value(TIMESTAP_KEY).toDouble();
    if (!obj.contains(SPEACH_KEY)) {
        qFatal("unexpected input sample data (data must have features data)");
    }
    const QJsonArray arr(obj.value(FEATURES_KEY).toArray());
    this->resize(arr.size());
    for (int i(0); i != static_cast<int>(size()); ++i) {
        if (!arr[i].isDouble()) {
            qDebug() << "unexpected input sample data (feature" << i << "isn't number)";
        }
        (*this)[i] = arr[i].toDouble();
    }
}

QJsonObject Sample::toJsonObject(const int classId) const
{
    return QJsonObject{
        { SPEACH_KEY, speech },
        { TIMESTAP_KEY, timestamp },
        { FEATURES_KEY, ([this]()->QJsonArray{ QJsonArray ret; for (const double& i : *this) { ret.insert(ret.size(), QJsonValue(i)); } return ret;})() },
        { CLASS_KEY, classId }
                    };

}
