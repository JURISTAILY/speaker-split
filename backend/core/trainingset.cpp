#include "trainingset.h"
#include <QJsonDocument>
#include <QFile>
#include <QJsonArray>
#include <QJsonParseError>
#include <QByteArray>

TrainingSet::TrainingSet(const QString& fName)
{
    QFile file(fName);
    if (!file.exists()) {
        qFatal((QString("File \"") + fName + QString("\" doesn't exist.")).toLocal8Bit().data());
    }
    if (!file.open(QFile::ReadOnly)) {
        qFatal((QString("Can't open file \"") + fName + QString("\"")).toLocal8Bit().data());
    }
    QJsonParseError errors;
    QJsonDocument doc(QJsonDocument::fromJson(file.readAll(), &errors));
    if (errors.error != QJsonParseError::NoError) {
        qFatal((errors.errorString() + " (" + errors.offset + " offset)").toLocal8Bit().data());
    }
    if (!doc.isArray()) {
        qFatal("unexpected input data (data must be an array)");
    }
    const QJsonArray arr(doc.array());
    this->reserve(arr.size());
    if (arr.isEmpty()) {
        qFatal("unexpected input data (data must not be empty)");
    }
    for (const QJsonValue& itm : arr) {
        this->emplace_back(itm);
    }
}
